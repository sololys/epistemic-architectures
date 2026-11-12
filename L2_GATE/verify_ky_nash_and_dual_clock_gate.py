#!/usr/bin/env python3
"""
Deterministic L1 Verifier: KY-Nash Admissibility & Dual-Clock Consequence Gate
==============================================================================
Surface          : L2_GATE/verify_ky_nash_and_dual_clock_gate.py
Companion Notes  : L3_NOTES/KY_NASH_ADMISSIBLE_GAMES.md
                   L3_NOTES/THE_UNIFIED_FIELD_NASH_DUALITY.md
                   L3_NOTES/NASH_MATHEMATICAL_INVARIANTS_AND_STRUCTURES.md
Dependencies     : Python Standard Library ONLY (dataclasses, fractions, hashlib, json, sys, typing, unittest)
Arithmetic       : Exact rational arithmetic over Q (fractions.Fraction); zero floating-point operations
Epistemic Tier   : L1 Deterministic Software Verifier (PHYSICAL_AUTHORITY = NONE)
Epistemic Bound  : INSPIRED_BY != IMPLEMENTS != PROVES
Legal Boundary   : MATHEMATICS != LEGAL_MANDATE (0% algorithmic legal capacity)
Ledger Disclaimer: In-memory append-only SHA-256 hash chain; not physical WORM hardware
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import sys
from typing import Callable, Dict, List, Sequence, Tuple
import unittest


GENESIS_HASH = "0" * 64
ActionProfile = Tuple[str, str]
GateRule = Callable[[int, ActionProfile, str], str]


def canonical_sha256(payload: Dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ==============================================================================
# PART I: DUAL-CLOCK CONSEQUENCE GATE (INVARIANTS 1, 2, 3)
# ==============================================================================


@dataclass(frozen=True)
class TransitionProposal:
    case_id: str
    evidence_id: str
    missing_items: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ClockWitnessRecord:
    seq: int
    case_id: str
    jurisdiction: str
    verdict: str
    tau_q: str
    detail: str
    prev_hash: str
    record_hash: str


class DualClockConsequenceGate:
    """
    Fail-closed consequence gate enforcing the Dual-Clock Law over Q:
      1. Time passing never mutates HOLD -> OPEN without valid evidence.
      2. Entering HOLD requires a non-empty deficiency manifest (delta_k != empty).
      3. Exceeding tau_max in HOLD forfeits internal gatekeeper jurisdiction
         (P_int -> P_ext) and logs the stall without opening the gate.
    """

    def __init__(self, tau_max: Fraction) -> None:
        if not isinstance(tau_max, Fraction) or tau_max <= Fraction(0, 1):
            raise ValueError("tau_max must be a strictly positive Fraction")
        self.tau_max = tau_max
        self.authorized_open_count = 0
        self.ledger: List[ClockWitnessRecord] = []
        self._held_cases: Dict[str, Tuple[TransitionProposal, Fraction, Fraction, str]] = {}

    def _append_witness(
        self,
        case_id: str,
        jurisdiction: str,
        verdict: str,
        tau_now: Fraction,
        detail: str,
    ) -> ClockWitnessRecord:
        prev = self.ledger[-1].record_hash if self.ledger else GENESIS_HASH
        seq = len(self.ledger) + 1
        body = {
            "case_id": case_id,
            "detail": detail,
            "jurisdiction": jurisdiction,
            "prev_hash": prev,
            "seq": seq,
            "tau_q": str(tau_now),
            "verdict": verdict,
        }
        digest = canonical_sha256(body)
        rec = ClockWitnessRecord(
            seq=seq,
            case_id=case_id,
            jurisdiction=jurisdiction,
            verdict=verdict,
            tau_q=str(tau_now),
            detail=detail,
            prev_hash=prev,
            record_hash=digest,
        )
        self.ledger.append(rec)
        return rec

    def verify_witness_chain(self) -> bool:
        expected_prev = GENESIS_HASH
        for idx, rec in enumerate(self.ledger, start=1):
            if rec.seq != idx or rec.prev_hash != expected_prev:
                return False
            recomputed = canonical_sha256(
                {
                    "case_id": rec.case_id,
                    "detail": rec.detail,
                    "jurisdiction": rec.jurisdiction,
                    "prev_hash": rec.prev_hash,
                    "seq": rec.seq,
                    "tau_q": rec.tau_q,
                    "verdict": rec.verdict,
                }
            )
            if recomputed != rec.record_hash:
                return False
            expected_prev = rec.record_hash
        return True

    def evaluate_proposal(
        self,
        proposal: TransitionProposal,
        tau_now: Fraction = Fraction(0, 1),
    ) -> str:
        if not isinstance(tau_now, Fraction) or tau_now < Fraction(0, 1):
            raise ValueError("tau_now must be a non-negative Fraction")

        cleaned_evidence = proposal.evidence_id.strip()
        cleaned_missing = tuple(item.strip() for item in proposal.missing_items if item.strip())

        if not cleaned_evidence or cleaned_missing:
            # Invariant 2: Free silence is forbidden; HOLD requires explicit delta_k != empty
            if not cleaned_missing:
                self._append_witness(
                    proposal.case_id,
                    "P_ext",
                    "REJECTED_SILENT_HOLD_FORBIDDEN",
                    tau_now,
                    "delta_k=EMPTY",
                )
                return "REJECTED_SILENT_HOLD"

            self._held_cases[proposal.case_id] = (proposal, tau_now, tau_now, "P_int")
            self._append_witness(
                proposal.case_id,
                "P_int",
                "HOLD",
                tau_now,
                "delta_k=" + ",".join(cleaned_missing),
            )
            return "HOLD"

        # Single-lane occupancy window: at most one active OPEN authorization
        if self.authorized_open_count >= 1:
            self._held_cases[proposal.case_id] = (proposal, tau_now, tau_now, "P_int")
            self._append_witness(
                proposal.case_id,
                "P_int",
                "HOLD",
                tau_now,
                "delta_k=OCCUPANCY_WINDOW_ACTIVE",
            )
            return "HOLD"

        self.authorized_open_count += 1
        self._held_cases.pop(proposal.case_id, None)
        self._append_witness(
            proposal.case_id,
            "P_int",
            "OPEN",
            tau_now,
            f"evidence_id={cleaned_evidence}",
        )
        return "OPEN"

    def advance_clock(self, case_id: str, tau_now: Fraction) -> str:
        if case_id not in self._held_cases:
            raise KeyError(f"Unknown held case_id: {case_id!r}")
        if not isinstance(tau_now, Fraction):
            raise ValueError("tau_now must be a Fraction")

        proposal, tau_entered, tau_last, owner = self._held_cases[case_id]
        if tau_now < tau_last:
            raise ValueError("Non-monotone clock rollback is forbidden")
        elapsed = tau_now - tau_entered

        # Invariant 1 & 3: Exceeding tau_max forfeits P_int -> P_ext without opening gate
        if owner == "P_int" and elapsed > self.tau_max:
            self._held_cases[case_id] = (proposal, tau_entered, tau_now, "P_ext")
            self._append_witness(
                case_id,
                "P_ext",
                "JURISDICTION_FORFEITED_TO_EXT",
                tau_now,
                f"elapsed={elapsed}>tau_max={self.tau_max};open_authorized=false",
            )
            return "ESCALATED_EXT"

        self._held_cases[case_id] = (proposal, tau_entered, tau_now, owner)
        return "HOLD"


def verify_anti_exhaustion_bound(
    challenger_budget: Fraction,
    bleed_rate_per_unit: Fraction,
    honest_kill_cost: Fraction,
    stall_forfeit_penalty: Fraction,
    tau_max: Fraction,
) -> Dict[str, object]:
    tau_exhaust = challenger_budget / bleed_rate_per_unit
    uncapped_stall_cost = Fraction(0, 1)
    capped_stall_cost = (
        stall_forfeit_penalty if tau_max < tau_exhaust else Fraction(0, 1)
    )
    return {
        "tau_exhaust_q": str(tau_exhaust),
        "tau_max_q": str(tau_max),
        "exhaustion_ghost_win_without_cap": uncapped_stall_cost < honest_kill_cost,
        "exhaustion_blocked_with_dual_clock": capped_stall_cost > honest_kill_cost,
    }


# ==============================================================================
# PART II: KY-NASH ADMISSIBILITY, SAFE_BUT_WEAK, REACH_OPEN & GATE CAPTURE
#          (INVARIANTS 4 & 5)
# ==============================================================================


@dataclass(frozen=True)
class IntegrityPayoff:
    u_raw: Fraction
    c_struct: Fraction = Fraction(0, 1)
    s_irr: Fraction = Fraction(0, 1)
    r_wit: Fraction = Fraction(0, 1)

    @property
    def u_net(self) -> Fraction:
        return self.u_raw - self.c_struct - self.s_irr - self.r_wit


def evaluate_admissibility_gate(
    score_a: Fraction,
    tau_a: Fraction,
    eps_belt: Fraction,
) -> str:
    """
    Exhaustive gate verdict Omega(tilde_a) over Q:
      - OPEN : score_a >= tau_a + eps_belt
      - HOLD : tau_a - eps_belt <= score_a < tau_a + eps_belt
      - KILL : score_a < tau_a - eps_belt
    """
    if eps_belt < Fraction(0, 1):
        raise ValueError("eps_belt must be non-negative")
    if score_a >= tau_a + eps_belt:
        return "OPEN"
    if score_a >= tau_a - eps_belt:
        return "HOLD"
    return "KILL"


def classify_transition_vector(
    delta_u_raw: Fraction,
    delta_u_net: Fraction,
    score_a: Fraction,
    tau_a: Fraction,
    eps_belt: Fraction,
) -> Tuple[str, str, bool]:
    """
    Separates gate legality (Omega) orthogonally from actor payoff (Delta U_i).
    Returns (gate_verdict, strategic_zone, is_improving_open_deviation).
    """
    verdict = evaluate_admissibility_gate(score_a, tau_a, eps_belt)
    if verdict == "HOLD":
        return verdict, "HOLD_BELT", False

    if verdict == "KILL":
        zone = "GHOST_WIN" if delta_u_raw > Fraction(0, 1) else "DEAD_NOISE"
        return verdict, zone, False

    # verdict == "OPEN": structurally lawful transition
    if delta_u_raw > Fraction(0, 1):
        if delta_u_net > Fraction(0, 1):
            return verdict, "TRUE_STRATEGY", True
        return verdict, "GHOST_WIN_NET_LOSS", False

    # Invariant 4: Lawful transition with non-positive payoff is OPEN (SAFE_BUT_WEAK), never HOLD
    return verdict, "SAFE_BUT_WEAK", False


class ExactKYNashGame:
    """
    Exact rational 2-player game enforcing:
      s* in E_KY_Nash iff
        1. Gate neutrality holds across players (Omega_0 == Omega_neutral == Omega_1),
        2. s* in Reach_OPEN(s_0), and
        3. No player i has a deviation a_i' with Omega_i(s*, a_i') == OPEN
           and U_i(s*_-i, a_i') > U_i(s*).
    """

    def __init__(
        self,
        actions_p0: Sequence[str],
        actions_p1: Sequence[str],
        payoffs: Dict[ActionProfile, Tuple[IntegrityPayoff, IntegrityPayoff]],
        transition_scores: Dict[Tuple[int, ActionProfile, str], Fraction],
        tau_a: Fraction = Fraction(1, 2),
        eps_belt: Fraction = Fraction(1, 10),
    ) -> None:
        self.actions = (tuple(actions_p0), tuple(actions_p1))
        self.payoffs = dict(payoffs)
        self.transition_scores = dict(transition_scores)
        self.tau_a = tau_a
        self.eps_belt = eps_belt

    def profiles(self) -> List[ActionProfile]:
        return [(a0, a1) for a0 in self.actions[0] for a1 in self.actions[1]]

    def neutral_gate(
        self, player: int, current: ActionProfile, next_action: str
    ) -> str:
        score = self.transition_scores[(player, current, next_action)]
        return evaluate_admissibility_gate(score, self.tau_a, self.eps_belt)

    def classical_raw_nash(self) -> List[ActionProfile]:
        equilibria: List[ActionProfile] = []
        for s in self.profiles():
            p0_cur, p1_cur = self.payoffs[s]
            dev_p0 = any(
                self.payoffs[(a0, s[1])][0].u_raw > p0_cur.u_raw
                for a0 in self.actions[0]
                if a0 != s[0]
            )
            dev_p1 = any(
                self.payoffs[(s[0], a1)][1].u_raw > p1_cur.u_raw
                for a1 in self.actions[1]
                if a1 != s[1]
            )
            if not dev_p0 and not dev_p1:
                equilibria.append(s)
        return equilibria

    def reach_open(
        self,
        initial_state: ActionProfile,
        gate_override: GateRule | None = None,
    ) -> List[ActionProfile]:
        gate = gate_override or self.neutral_gate
        visited = {initial_state}
        queue = [initial_state]
        while queue:
            cur = queue.pop(0)
            for alt0 in self.actions[0]:
                nxt0 = (alt0, cur[1])
                if alt0 != cur[0] and nxt0 not in visited and gate(0, cur, alt0) == "OPEN":
                    visited.add(nxt0)
                    queue.append(nxt0)
            for alt1 in self.actions[1]:
                nxt1 = (cur[0], alt1)
                if alt1 != cur[1] and nxt1 not in visited and gate(1, cur, alt1) == "OPEN":
                    visited.add(nxt1)
                    queue.append(nxt1)
        return [s for s in self.profiles() if s in visited]

    def audit_gate_neutrality(
        self, candidate_gate: GateRule
    ) -> List[Tuple[ActionProfile, int, str, str, str]]:
        anomalies: List[Tuple[ActionProfile, int, str, str, str]] = []
        for s in self.profiles():
            for player in (0, 1):
                for alt in self.actions[player]:
                    if alt == s[player]:
                        continue
                    expected = self.neutral_gate(player, s, alt)
                    actual = candidate_gate(player, s, alt)
                    if expected != actual:
                        anomalies.append((s, player, alt, expected, actual))
        return anomalies

    def local_unfiltered_fixed_points(
        self, gate_override: GateRule | None = None
    ) -> List[ActionProfile]:
        """Diagnostic helper: local stability check WITHOUT Reach_OPEN or gate-capture audit."""
        gate = gate_override or self.neutral_gate
        pts: List[ActionProfile] = []
        for s in self.profiles():
            u0 = self.payoffs[s][0].u_net
            u1 = self.payoffs[s][1].u_net
            imp0 = any(
                gate(0, s, a0) == "OPEN" and self.payoffs[(a0, s[1])][0].u_net > u0
                for a0 in self.actions[0]
                if a0 != s[0]
            )
            imp1 = any(
                gate(1, s, a1) == "OPEN" and self.payoffs[(s[0], a1)][1].u_net > u1
                for a1 in self.actions[1]
                if a1 != s[1]
            )
            if not imp0 and not imp1:
                pts.append(s)
        return pts

    def ky_nash_equilibria(
        self,
        initial_state: ActionProfile,
        gate_override: GateRule | None = None,
    ) -> Tuple[str, List[ActionProfile]]:
        """
        Full KY-Nash admissibility resolver:
          - Rejects captured / non-neutral gates fail-closed (KILL_GATE_CAPTURE).
          - Restricts candidate equilibria to Reach_OPEN(initial_state).
        """
        gate = gate_override or self.neutral_gate
        if self.audit_gate_neutrality(gate):
            return "KILL_GATE_CAPTURE", []

        reachable = set(self.reach_open(initial_state, gate_override=gate))
        local_pts = self.local_unfiltered_fixed_points(gate_override=gate)
        admissible = [s for s in local_pts if s in reachable]
        return "VALID_NEUTRAL_GATE", admissible


def build_canonical_governance_game(
    c_struct_extraction: Fraction = Fraction(2, 1),
    s_irr_extraction: Fraction = Fraction(3, 1),
    r_wit_extraction: Fraction = Fraction(3, 1),
) -> ExactKYNashGame:
    """
    3x3 exact rational game with actions:
      - STEWARDSHIP (S): sustainable baseline s_0 = (S, S)
      - EXTRACTION  (E): short-term temptation (classical Prisoner's Dilemma trap)
      - LOCKED_VAULT(L): isolated state unreachable via OPEN from s_0
    """
    s, e, l = "STEWARDSHIP", "EXTRACTION", "LOCKED_VAULT"
    actions = (s, e, l)
    payoffs: Dict[ActionProfile, Tuple[IntegrityPayoff, IntegrityPayoff]] = {}
    scores: Dict[Tuple[int, ActionProfile, str], Fraction] = {}

    base_raw: Dict[ActionProfile, Tuple[int, int]] = {
        (s, s): (6, 6),
        (e, s): (10, 1),
        (s, e): (1, 10),
        (e, e): (3, 3),
        (l, s): (2, 2),
        (s, l): (2, 2),
        (l, e): (1, 2),
        (e, l): (2, 1),
        (l, l): (5, 5),
    }

    for prof, (u0, u1) in base_raw.items():
        p0 = (
            IntegrityPayoff(
                Fraction(u0),
                c_struct=c_struct_extraction,
                s_irr=s_irr_extraction,
                r_wit=r_wit_extraction,
            )
            if prof[0] == e
            else IntegrityPayoff(Fraction(u0))
        )
        p1 = (
            IntegrityPayoff(
                Fraction(u1),
                c_struct=c_struct_extraction,
                s_irr=s_irr_extraction,
                r_wit=r_wit_extraction,
            )
            if prof[1] == e
            else IntegrityPayoff(Fraction(u1))
        )
        payoffs[prof] = (p0, p1)

    for prof in payoffs:
        for player in (0, 1):
            for nxt in actions:
                if nxt == prof[player]:
                    continue
                if nxt == e:
                    # Extraction violates structural bearing capacity -> KILL
                    scores[(player, prof, nxt)] = Fraction(1, 5)
                elif nxt == l or prof == (l, l):
                    # Entering or leaving LOCKED_VAULT is blocked -> KILL
                    scores[(player, prof, nxt)] = Fraction(1, 5)
                else:
                    # Returning to STEWARDSHIP from ordinary states -> OPEN
                    scores[(player, prof, nxt)] = Fraction(9, 10)

    return ExactKYNashGame(actions, actions, payoffs, scores)


# ==============================================================================
# PART III: DETERMINISTIC VERIFICATION SUITE (5 INVARIANTS)
# ==============================================================================


class TestKYNashAndDualClockGate(unittest.TestCase):
    def test_invariant_1_first_clock_law_time_never_opens_hold(self) -> None:
        gate = DualClockConsequenceGate(tau_max=Fraction(14, 1))
        prop = TransitionProposal(
            case_id="CASE-01",
            evidence_id="",
            missing_items=("structural_load_proof",),
        )
        self.assertEqual(gate.evaluate_proposal(prop, Fraction(0, 1)), "HOLD")
        self.assertEqual(gate.advance_clock("CASE-01", Fraction(7, 1)), "HOLD")
        self.assertEqual(gate.advance_clock("CASE-01", Fraction(14, 1)), "HOLD")
        self.assertEqual(gate.advance_clock("CASE-01", Fraction(100, 1)), "ESCALATED_EXT")
        self.assertEqual(gate.authorized_open_count, 0)
        with self.assertRaises(ValueError):
            gate.advance_clock("CASE-01", Fraction(5, 1))

    def test_invariant_2_free_silence_forbidden_on_hold(self) -> None:
        gate = DualClockConsequenceGate(tau_max=Fraction(14, 1))
        silent = TransitionProposal(
            case_id="CASE-SILENT",
            evidence_id="",
            missing_items=(),
        )
        whitespace_only = TransitionProposal(
            case_id="CASE-BLANK",
            evidence_id="   ",
            missing_items=("   ",),
        )
        self.assertEqual(gate.evaluate_proposal(silent, Fraction(1, 1)), "REJECTED_SILENT_HOLD")
        self.assertEqual(gate.evaluate_proposal(whitespace_only, Fraction(2, 1)), "REJECTED_SILENT_HOLD")
        self.assertEqual(gate.authorized_open_count, 0)
        self.assertEqual(gate.ledger[-1].jurisdiction, "P_ext")
        self.assertEqual(gate.ledger[-1].detail, "delta_k=EMPTY")

    def test_invariant_3_second_clock_law_forfeits_stalling_keeper_and_chains_sha256(self) -> None:
        gate = DualClockConsequenceGate(tau_max=Fraction(14, 1))
        prop = TransitionProposal(
            case_id="CASE-STALL",
            evidence_id="",
            missing_items=("ultrasonic_weld_attestation",),
        )
        self.assertEqual(gate.evaluate_proposal(prop, Fraction(0, 1)), "HOLD")
        self.assertEqual(gate.advance_clock("CASE-STALL", Fraction(29, 2)), "ESCALATED_EXT")
        # Subsequent ticks do not duplicate forfeiture or open the gate
        self.assertEqual(gate.advance_clock("CASE-STALL", Fraction(30, 1)), "HOLD")
        self.assertEqual(gate.authorized_open_count, 0)
        self.assertTrue(gate.verify_witness_chain())
        self.assertEqual(gate.ledger[-1].verdict, "JURISDICTION_FORFEITED_TO_EXT")
        self.assertEqual(gate.ledger[-1].jurisdiction, "P_ext")

        bound = verify_anti_exhaustion_bound(
            challenger_budget=Fraction(30, 1),
            bleed_rate_per_unit=Fraction(1, 1),
            honest_kill_cost=Fraction(5, 1),
            stall_forfeit_penalty=Fraction(12, 1),
            tau_max=Fraction(14, 1),
        )
        self.assertTrue(bound["exhaustion_ghost_win_without_cap"])
        self.assertTrue(bound["exhaustion_blocked_with_dual_clock"])

    def test_invariant_4_safe_but_weak_is_open_never_hold(self) -> None:
        verdict, zone, improving = classify_transition_vector(
            delta_u_raw=Fraction(-3, 1),
            delta_u_net=Fraction(-3, 1),
            score_a=Fraction(4, 5),
            tau_a=Fraction(1, 2),
            eps_belt=Fraction(1, 10),
        )
        self.assertEqual(verdict, "OPEN")
        self.assertNotEqual(verdict, "HOLD")
        self.assertEqual(zone, "SAFE_BUT_WEAK")
        self.assertFalse(improving)

        hold_v, hold_z, hold_imp = classify_transition_vector(
            delta_u_raw=Fraction(5, 1),
            delta_u_net=Fraction(4, 1),
            score_a=Fraction(11, 20),
            tau_a=Fraction(1, 2),
            eps_belt=Fraction(1, 10),
        )
        self.assertEqual((hold_v, hold_z, hold_imp), ("HOLD", "HOLD_BELT", False))

        ghost_v, ghost_z, ghost_imp = classify_transition_vector(
            delta_u_raw=Fraction(8, 1),
            delta_u_net=Fraction(-2, 1),
            score_a=Fraction(1, 5),
            tau_a=Fraction(1, 2),
            eps_belt=Fraction(1, 10),
        )
        self.assertEqual((ghost_v, ghost_z, ghost_imp), ("KILL", "GHOST_WIN", False))

    def test_invariant_5_reach_open_and_captured_gate_rejection(self) -> None:
        game = build_canonical_governance_game()
        s0 = ("STEWARDSHIP", "STEWARDSHIP")
        collapsed = ("EXTRACTION", "EXTRACTION")
        unreachable_vault = ("LOCKED_VAULT", "LOCKED_VAULT")

        # Classical raw Nash admits both mutual extraction and the isolated vault
        self.assertEqual(game.classical_raw_nash(), [collapsed, unreachable_vault])

        # Unfiltered local check admits the unreachable vault state
        local_only = game.local_unfiltered_fixed_points()
        self.assertIn(unreachable_vault, local_only)

        # Reach_OPEN(s_0) excludes both collapsed extraction and the isolated vault
        reachable = game.reach_open(s0)
        self.assertEqual(reachable, [s0])
        status_neutral, admissible_eq = game.ky_nash_equilibria(initial_state=s0)
        self.assertEqual(status_neutral, "VALID_NEUTRAL_GATE")
        self.assertEqual(admissible_eq, [s0])
        self.assertNotIn(unreachable_vault, admissible_eq)
        self.assertNotIn(collapsed, admissible_eq)

        # Closed room without public witness (r_wit = 0) and asymmetric captured gate
        # (Omega_0 != Omega_1): Player 0 grants self OPEN on EXTRACTION while locking Player 1 in HOLD
        closed_room_game = build_canonical_governance_game(
            c_struct_extraction=Fraction(1, 1),
            s_irr_extraction=Fraction(0, 1),
            r_wit_extraction=Fraction(0, 1),
        )
        self.assertEqual(
            closed_room_game.ky_nash_equilibria(initial_state=s0),
            ("VALID_NEUTRAL_GATE", [s0]),
        )

        def captured_gate(player: int, current: ActionProfile, nxt: str) -> str:
            if player == 0 and nxt == "EXTRACTION":
                return "OPEN"
            if player == 1:
                return "HOLD"
            return closed_room_game.neutral_gate(player, current, nxt)

        # Under naive local evaluation without neutrality audit, Player 0's capture looks like an equilibrium
        self.assertEqual(
            [
                prof
                for prof in closed_room_game.local_unfiltered_fixed_points(
                    gate_override=captured_gate
                )
                if prof in closed_room_game.reach_open(s0, gate_override=captured_gate)
            ],
            [("EXTRACTION", "STEWARDSHIP")],
        )

        # Full KY-Nash gate audits Omega_0 != Omega_1 and rejects captured equilibrium fail-closed
        anomalies = closed_room_game.audit_gate_neutrality(captured_gate)
        self.assertIn((s0, 0, "EXTRACTION", "KILL", "OPEN"), anomalies)
        self.assertIn((("EXTRACTION", "STEWARDSHIP"), 1, "EXTRACTION", "KILL", "HOLD"), anomalies)
        status_captured, rejected_eq = closed_room_game.ky_nash_equilibria(
            initial_state=s0, gate_override=captured_gate
        )
        self.assertEqual(status_captured, "KILL_GATE_CAPTURE")
        self.assertEqual(rejected_eq, [])


def build_gate_summary() -> Dict[str, object]:
    gate = DualClockConsequenceGate(tau_max=Fraction(14, 1))
    gate.evaluate_proposal(
        TransitionProposal("SUMMARY-01", "", ("load_proof",)),
        Fraction(0, 1),
    )
    gate.advance_clock("SUMMARY-01", Fraction(15, 1))
    game = build_canonical_governance_game()
    status, eq = game.ky_nash_equilibria(("STEWARDSHIP", "STEWARDSHIP"))

    summary: Dict[str, object] = {
        "admissible_ky_nash": [list(item) for item in eq],
        "arithmetic_domain": "EXACT_RATIONAL_Q",
        "classical_raw_nash": [list(item) for item in game.classical_raw_nash()],
        "dual_clock_ledger_tip": gate.ledger[-1].record_hash,
        "epistemic_boundary": "INSPIRED_BY != IMPLEMENTS != PROVES",
        "float_operations": 0,
        "gate_neutrality_status": status,
        "invariants_verified": 5,
        "legal_authority": "NONE_HUMAN_L01_REQUIRED",
        "modeled_voltage": "0.00 V",
        "verdict": "HOLD_READY_FOR_W2",
    }
    summary["gate_sha256"] = canonical_sha256(summary)
    return summary


def main() -> int:
    if sys.version_info < (3, 8):
        raise RuntimeError("FAIL_CLOSED_ENV_ERROR: Python >= 3.8 required.")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestKYNashAndDualClockGate)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    summary = build_gate_summary()
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
