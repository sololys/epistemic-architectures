#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic L1 Verifier: OMNI-KY / SUSY^2 / Sosionomos XOR-ROX Consequence Gate
==================================================================================
Surface          : L2_GATE/verify_sosionomos_xor_rox_gate.py
Specification    : L1_LAW/OMNI_KY_SUSY2_SOSIONOMOS_BRIDGE_SPEC_v1.0.md
Dependencies     : Python Standard Library ONLY (ast, dataclasses, enum, fractions, hashlib, json, pathlib, unittest)
Arithmetic       : Exact integer, bit-exact 64-bit, and rational arithmetic (fractions.Fraction); ZERO float
Epistemic Tier   : L1 Deterministic Software Verifier (PHYSICAL_AUTHORITY = NONE)
Epistemic Bound  : INSPIRED_BY != IMPLEMENTS != PROVES
Ledger Disclaimer: Append-only SHA-256 hash chain in software; not physical WORM hardware
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest


PHYSICAL_AUTHORITY = "NONE"
OPERATIONAL_AUTHORITY = "NONE"
MASK_64 = (1 << 64) - 1

STATE_INVALID_ZERO = 0x00
STATE_CANDIDATE = 0x01
STATE_REALIZED = 0x02
STATE_INVALID_BOTH = 0x03

# Exact integer LUT for Amygdala delay ticks by excitation bucket (0..1000) -> delay ticks
AMYGDALA_DELAY_LUT: tuple[tuple[int, int], ...] = (
    (100, 0),    # calm signal -> immediate eligibility
    (300, 5),    # mild excitation -> 5 ticks
    (600, 20),   # elevated excitation -> 20 ticks
    (899, 60),   # high excitation -> 60 ticks
)
EXCITATION_MAX_KILL = 900  # >= 900 => KILL

# Exact rational backpressure thresholds
RHO_SOFT = Fraction(1, 2)
RHO_HARD = Fraction(3, 4)
RHO_KILL = Fraction(9, 10)


class Decision(Enum):
    OPEN = "OPEN"
    HOLD = "HOLD"
    KILL = "KILL"
    TRAP = "TRAP"


class NodeTemp(Enum):
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"
    REVOKED = "REVOKED"
    INVALID = "INVALID"


def xor64(x: int, k: int) -> int:
    """Reversible pre-gate involution: xor64(xor64(x, k), k) == x."""
    return (x ^ k) & MASK_64


def rox64(x: int, k: int, rot: int = 13) -> int:
    """Non-involutive directional gate seal: ROTL_64(x ^ k, rot)."""
    if not (1 <= rot <= 63):
        raise ValueError("ROTATION_OUT_OF_RANGE")
    mixed = (x ^ k) & MASK_64
    return ((mixed << rot) | (mixed >> (64 - rot))) & MASK_64


def verify_state_xor_invariant(state_byte: int) -> bool:
    """Ontological XOR guard: exactly one of bit 0 (0x01) or bit 1 (0x02) must be set."""
    if state_byte not in (STATE_INVALID_ZERO, STATE_CANDIDATE, STATE_REALIZED, STATE_INVALID_BOTH):
        return False
    bit0 = state_byte & 1
    bit1 = (state_byte >> 1) & 1
    return (bit0 ^ bit1) == 1


def double_pulse_xor_check(word: int, mask_out: int, mask_back: int) -> bool:
    """OMNI-KY 4.1 double-pulse identity: forward + backward XOR must return exact origin."""
    forward = xor64(word, mask_out)
    returned = xor64(forward, mask_back)
    return returned == (word & MASK_64)


def amygdala_delay_ticks(excitation: int) -> int | None:
    """Exact integer LUT delay (0 float). Returns None if excitation >= EXCITATION_MAX_KILL."""
    if excitation < 0:
        raise ValueError("NEGATIVE_EXCITATION")
    if excitation >= EXCITATION_MAX_KILL:
        return None
    for upper, ticks in AMYGDALA_DELAY_LUT:
        if excitation <= upper:
            return ticks
    return None


def sha256_hex(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass
class ActorState:
    actor_id: str
    seq_last: int = 0
    prev_actor_hash: str = "0" * 64
    arena_capacity: int = 100
    used_in: int = 0
    used_hold: int = 0
    used_shadow: int = 0
    trapped: bool = False
    kill_count: int = 0

    def pressure(self) -> Fraction:
        return Fraction(self.used_in + self.used_hold + self.used_shadow, self.arena_capacity)

    def read_permit(self) -> int:
        if self.trapped or self.pressure() >= RHO_HARD:
            return 0
        return 1


@dataclass
class Candidate:
    actor_id: str
    payload: str
    parent_hash: str
    sequence: int
    excitation: int
    reach_n: int
    created_tick: int
    state_byte: int = STATE_CANDIDATE
    phase_word: int = 0x13579BDF2468ACE0
    phase_mask_out: int = 0x55AA55AA55AA55AA
    phase_mask_back: int = 0x55AA55AA55AA55AA

    def candidate_hash(self, prev_actor_hash: str) -> str:
        return sha256_hex({
            "actor_id": self.actor_id,
            "parent_hash": self.parent_hash,
            "payload": self.payload,
            "prev_actor_hash": prev_actor_hash,
            "reach_n": self.reach_n,
            "sequence": self.sequence,
        })


class SosionomosGate:
    """Minimal 0-float reference implementation of the OMNI-KY / Sosionomos XOR-ROX gate."""

    def __init__(self) -> None:
        self.genesis_hash = sha256_hex({"genesis": "SOSIONOMOS_v1.0"})
        self.anchor_index: dict[str, NodeTemp] = {self.genesis_hash: NodeTemp.HOT}
        self.public_dag: dict[str, dict] = {
            self.genesis_hash: {"state_byte": STATE_REALIZED, "payload": "GENESIS", "rox_seal": 0}
        }
        self.shadow_dag: dict[str, list[dict]] = {}
        self.actors: dict[str, ActorState] = {}
        self.hold_buffer: dict[str, Candidate] = {}
        self.witness_chain: list[dict] = []

    def bootstrap_actor(self, actor_id: str, arena_capacity: int = 100) -> ActorState:
        st = ActorState(actor_id=actor_id, arena_capacity=arena_capacity)
        self.actors[actor_id] = st
        return st

    def _append_witness(self, actor_id: str, cand_hash: str, decision: Decision, tick: int, rox_seal: int) -> str:
        prev = self.witness_chain[-1]["witness_hash"] if self.witness_chain else "0" * 64
        record = {
            "actor_id": actor_id,
            "candidate_hash": cand_hash,
            "decision": decision.value,
            "prev_witness_hash": prev,
            "rox_seal": rox_seal,
            "tick": tick,
        }
        wh = sha256_hex(record)
        record["witness_hash"] = wh
        self.witness_chain.append(record)
        return wh

    def verify_witness_chain(self) -> bool:
        expected_prev = "0" * 64
        for rec in self.witness_chain:
            if rec["prev_witness_hash"] != expected_prev:
                return False
            check = {k: v for k, v in rec.items() if k != "witness_hash"}
            if sha256_hex(check) != rec["witness_hash"]:
                return False
            expected_prev = rec["witness_hash"]
        return True

    def cool_node(self, node_hash: str, target_temp: NodeTemp) -> None:
        if node_hash not in self.anchor_index:
            raise KeyError("UNKNOWN_NODE")
        if target_temp not in (NodeTemp.HOT, NodeTemp.WARM, NodeTemp.COLD):
            raise ValueError("INVALID_COOLING_TARGET")
        self.anchor_index[node_hash] = target_temp
        if target_temp is NodeTemp.COLD:
            # Payload cools; hash and anchor survive intact.
            self.public_dag[node_hash]["payload"] = None

    def admit(self, c: Candidate, current_tick: int) -> tuple[Decision, dict]:
        actor = self.actors[c.actor_id]
        chash = c.candidate_hash(actor.prev_actor_hash)

        # 0. Backpressure saturation check
        if actor.pressure() >= RHO_KILL:
            actor.trapped = True
            self.shadow_dag.setdefault(c.actor_id, []).append({"hash": chash, "tick": current_tick})
            self._append_witness(c.actor_id, chash, Decision.TRAP, current_tick, 0)
            return Decision.TRAP, {"ack_shadow": True, "public": False}

        # 1. Trapped actor: silent shadow routing (no oracle differentiation)
        if actor.trapped:
            shadow_seal = rox64(c.phase_word, int(chash[:16], 16), rot=17)
            self.shadow_dag.setdefault(c.actor_id, []).append(
                {"hash": chash, "tick": current_tick, "shadow_seal": shadow_seal}
            )
            self._append_witness(c.actor_id, chash, Decision.TRAP, current_tick, shadow_seal)
            return Decision.TRAP, {"ack_shadow": True, "public": False}

        # 2. Ontological XOR state invariant & double-pulse check
        if not verify_state_xor_invariant(c.state_byte) or c.state_byte != STATE_CANDIDATE:
            actor.kill_count += 1
            self._append_witness(c.actor_id, chash, Decision.KILL, current_tick, 0)
            return Decision.KILL, {"reason": "INVALID_STATE_SUPERPOSITION"}

        if not double_pulse_xor_check(c.phase_word, c.phase_mask_out, c.phase_mask_back):
            actor.kill_count += 1
            self._append_witness(c.actor_id, chash, Decision.KILL, current_tick, 0)
            return Decision.KILL, {"reason": "MASK_MUTATED"}

        # 3. O(1) AnchorIndex & monotonic sequence check
        parent_temp = self.anchor_index.get(c.parent_hash)
        if parent_temp not in (NodeTemp.HOT, NodeTemp.WARM, NodeTemp.COLD):
            actor.kill_count += 1
            self._append_witness(c.actor_id, chash, Decision.KILL, current_tick, 0)
            return Decision.KILL, {"reason": "ANCHOR_INVALID"}

        if c.sequence != actor.seq_last + 1:
            actor.kill_count += 1
            self._append_witness(c.actor_id, chash, Decision.KILL, current_tick, 0)
            return Decision.KILL, {"reason": "SEQUENCE_INVALID"}

        # 4. Amygdala brake (0 float LUT)
        delay = amygdala_delay_ticks(c.excitation)
        if delay is None:
            actor.kill_count += 1
            self._append_witness(c.actor_id, chash, Decision.KILL, current_tick, 0)
            return Decision.KILL, {"reason": "EXCITATION_OVER_MAX"}

        elapsed = current_tick - c.created_tick
        if elapsed < delay:
            self.hold_buffer[c.actor_id] = c
            actor.used_hold = len([x for x in self.hold_buffer if x == c.actor_id])
            self._append_witness(c.actor_id, chash, Decision.HOLD, current_tick, 0)
            return Decision.HOLD, {
                "remaining_ticks": delay - elapsed,
                "options": ("wait", "revise", "narrow"),
            }

        # 5. OPEN: non-involutive ROX directional seal & state transition 0x01 -> 0x02
        rox_key = int(chash[:16], 16)
        rox_seal = rox64(c.phase_word, rox_key, rot=13)
        actor.seq_last = c.sequence
        actor.prev_actor_hash = chash
        if c.actor_id in self.hold_buffer:
            del self.hold_buffer[c.actor_id]
            actor.used_hold = 0
        self.anchor_index[chash] = NodeTemp.HOT
        self.public_dag[chash] = {
            "state_byte": STATE_REALIZED,
            "parent_hash": c.parent_hash,
            "payload": c.payload,
            "rox_seal": rox_seal,
        }
        wh = self._append_witness(c.actor_id, chash, Decision.OPEN, current_tick, rox_seal)
        return Decision.OPEN, {"node_hash": chash, "rox_seal": rox_seal, "witness_hash": wh}


class TestSosionomosXorRoxGate(unittest.TestCase):
    def test_01_xor_involution_and_rox_asymmetry(self) -> None:
        w = 0x123456789ABCDEF0
        k = 0x0F0F0F0F0F0F0F0F
        self.assertEqual(xor64(xor64(w, k), k), w)
        self.assertNotEqual(rox64(rox64(w, k), k), w)
        self.assertTrue(verify_state_xor_invariant(STATE_CANDIDATE))
        self.assertTrue(verify_state_xor_invariant(STATE_REALIZED))
        self.assertFalse(verify_state_xor_invariant(STATE_INVALID_ZERO))
        self.assertFalse(verify_state_xor_invariant(STATE_INVALID_BOTH))

    def test_02_double_pulse_mutation_triggers_kill(self) -> None:
        gate = SosionomosGate()
        gate.bootstrap_actor("alice")
        c = Candidate(
            actor_id="alice",
            payload="tampered",
            parent_hash=gate.genesis_hash,
            sequence=1,
            excitation=50,
            reach_n=10,
            created_tick=0,
            phase_mask_out=0xAAAA,
            phase_mask_back=0xAAAB,
        )
        decision, info = gate.admit(c, current_tick=0)
        self.assertEqual(decision, Decision.KILL)
        self.assertEqual(info["reason"], "MASK_MUTATED")

    def test_03_hold_revise_preserves_sequence_and_opens(self) -> None:
        gate = SosionomosGate()
        gate.bootstrap_actor("alice")
        hot_cand = Candidate(
            actor_id="alice",
            payload="urgent shout",
            parent_hash=gate.genesis_hash,
            sequence=1,
            excitation=700,  # requires 60 ticks
            reach_n=50,
            created_tick=10,
        )
        d1, info1 = gate.admit(hot_cand, current_tick=15)
        self.assertEqual(d1, Decision.HOLD)
        self.assertEqual(info1["remaining_ticks"], 55)
        self.assertEqual(gate.actors["alice"].seq_last, 0)

        # Revise lowers excitation without locking sequence=1
        revised = Candidate(
            actor_id="alice",
            payload="calm reflection",
            parent_hash=gate.genesis_hash,
            sequence=1,
            excitation=80,  # 0 ticks delay
            reach_n=12,
            created_tick=16,
        )
        d2, info2 = gate.admit(revised, current_tick=16)
        self.assertEqual(d2, Decision.OPEN)
        self.assertEqual(gate.actors["alice"].seq_last, 1)
        self.assertIn(info2["node_hash"], gate.public_dag)

    def test_04_backpressure_and_shadow_trap_isolation(self) -> None:
        gate = SosionomosGate()
        bot = gate.bootstrap_actor("bot_1", arena_capacity=10)
        bot.used_in = 8  # 8/10 >= 3/4 (RHO_HARD)
        self.assertEqual(bot.read_permit(), 0)
        bot.used_in = 9  # 9/10 >= 9/10 (RHO_KILL)
        c = Candidate(
            actor_id="bot_1",
            payload="spam burst",
            parent_hash=gate.genesis_hash,
            sequence=1,
            excitation=10,
            reach_n=5,
            created_tick=0,
        )
        d, info = gate.admit(c, current_tick=0)
        self.assertEqual(d, Decision.TRAP)
        self.assertTrue(info["ack_shadow"])
        self.assertFalse(info["public"])
        self.assertEqual(len(gate.public_dag), 1)  # only genesis

    def test_05_cold_anchor_survives_cooling_and_witness_chain_valid(self) -> None:
        gate = SosionomosGate()
        gate.bootstrap_actor("alice")
        c1 = Candidate("alice", "first", gate.genesis_hash, 1, 20, 5, 0)
        d1, info1 = gate.admit(c1, 0)
        self.assertEqual(d1, Decision.OPEN)
        h1 = info1["node_hash"]

        gate.cool_node(h1, NodeTemp.COLD)
        self.assertIsNone(gate.public_dag[h1]["payload"])
        self.assertEqual(gate.anchor_index[h1], NodeTemp.COLD)

        # Child anchored to COLD node still succeeds in O(1)
        c2 = Candidate("alice", "reply to archive", h1, 2, 20, 5, 1)
        d2, _ = gate.admit(c2, 1)
        self.assertEqual(d2, Decision.OPEN)
        self.assertTrue(gate.verify_witness_chain())

    def test_06_zero_float_ast_gate(self) -> None:
        src = Path(__file__).read_text(encoding="utf-8")
        tree = ast.parse(src)
        float_nodes = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, float)
        ]
        self.assertEqual(float_nodes, [])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSosionomosXorRoxGate)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
