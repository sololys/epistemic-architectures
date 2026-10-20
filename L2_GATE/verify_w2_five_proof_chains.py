#!/usr/bin/env python3
"""
Deterministic L1 Verifier: Five Mathematical Proof Chains for W^2 Authorization
===============================================================================
Surface       : /demonstrators/verify_w2_five_proof_chains.py
Specification : /specifications/W2_FIVE_PROOF_CHAINS_SPEC.md
Dependencies  : Python Standard Library ONLY (fractions, hashlib, json, math, sys, unittest)
Epistemic Tier: L1 Deterministic Software Demonstrator (PHYSICAL_AUTHORITY = NONE)
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
import sys
import unittest
from typing import Any, Dict, Optional, Sequence, Tuple

C_VACUUM_M_PER_S = 299_792_458.0


def canonical_sha256(payload: Dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ---------------------------------------------------------------------------
# Chain 1: Involutive Reversibility & Envelope Gate (Door 25 Digital Twin)
# ---------------------------------------------------------------------------
def verify_chain_1_involutive_twin(
    s0: Tuple[float, float],
    delta_cmd: Tuple[float, float],
    leakage: Tuple[float, float] = (0.0, 0.0),
    envelope_max: float = 10.0,
    eps_iso: float = 1e-9,
) -> Dict[str, Any]:
    sf = (s0[0] + delta_cmd[0] + leakage[0], s0[1] + delta_cmd[1] + leakage[1])
    sr = (sf[0] - delta_cmd[0], sf[1] - delta_cmd[1])
    residual = math.hypot(s0[0] - sr[0], s0[1] - sr[1])
    within_env = max(abs(sf[0]), abs(sf[1])) <= envelope_max

    if residual > eps_iso:
        return {"chain": 1, "verdict": "KILL", "reason": "TWIN_ASYMMETRY_DETECTED", "residual": round(residual, 12), "voltage_v": 0.0}
    if not within_env:
        return {"chain": 1, "verdict": "HOLD", "reason": "TWIN_ENVELOPE_BREACH", "residual": round(residual, 12), "voltage_v": 0.0}
    return {"chain": 1, "verdict": "OPEN", "reason": "TWIN_INVOLUTIVE_PASS", "residual": round(residual, 12), "voltage_v": 5.0}


# ---------------------------------------------------------------------------
# Chain 2: Relational Gram Invariance (Monolith 4 Kernel Drift)
# ---------------------------------------------------------------------------
def _gram_2x2(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    g11 = v1[0] * v1[0] + v1[1] * v1[1]
    g12 = v1[0] * v2[0] + v1[1] * v2[1]
    g22 = v2[0] * v2[0] + v2[1] * v2[1]
    return ((g11, g12), (g12, g22))


def verify_chain_2_relational_gram(
    ref_vectors: Optional[Tuple[Tuple[float, float], Tuple[float, float]]],
    cur_vectors: Tuple[Tuple[float, float], Tuple[float, float]],
    tau_g: float = 1e-9,
) -> Dict[str, Any]:
    if ref_vectors is None:
        return {"chain": 2, "verdict": "HOLD", "reason": "MISSING_REFERENCE_GRAM", "delta_g": None, "voltage_v": 0.0}

    g0 = _gram_2x2(ref_vectors[0], ref_vectors[1])
    gt = _gram_2x2(cur_vectors[0], cur_vectors[1])
    diff_sq = (
        (gt[0][0] - g0[0][0]) ** 2
        + 2.0 * (gt[0][1] - g0[0][1]) ** 2
        + (gt[1][1] - g0[1][1]) ** 2
    )
    delta_g = math.sqrt(diff_sq)
    det_gt = gt[0][0] * gt[1][1] - gt[0][1] * gt[1][0]

    if delta_g > tau_g or det_gt < -1e-12:
        return {"chain": 2, "verdict": "KILL", "reason": "RELATIONAL_GRAM_SHEAR_KILL", "delta_g": round(delta_g, 12), "voltage_v": 0.0}
    return {"chain": 2, "verdict": "OPEN", "reason": "RELATIONAL_GRAM_INVARIANT_PASS", "delta_g": round(delta_g, 12), "voltage_v": 5.0}


# ---------------------------------------------------------------------------
# Chain 3: Exact Rational Conservation & Operator Completeness (Q)
# ---------------------------------------------------------------------------
def verify_chain_3_rational_conservation(
    inputs_q: Sequence[Fraction],
    outputs_q: Sequence[Fraction],
    povm_weights_q: Sequence[Fraction],
    window_sealed: bool = True,
) -> Dict[str, Any]:
    if not window_sealed:
        return {"chain": 3, "verdict": "HOLD", "reason": "RATIONAL_WINDOW_PENDING", "delta_r": None, "voltage_v": 0.0}

    delta_r = sum(inputs_q, Fraction(0, 1)) - sum(outputs_q, Fraction(0, 1))
    povm_sum = sum(povm_weights_q, Fraction(0, 1))

    if delta_r != Fraction(0, 1) or povm_sum != Fraction(1, 1):
        return {
            "chain": 3,
            "verdict": "KILL",
            "reason": "RATIONAL_CONSERVATION_BREACH",
            "delta_r": str(delta_r),
            "povm_sum": str(povm_sum),
            "voltage_v": 0.0,
        }
    return {
        "chain": 3,
        "verdict": "OPEN",
        "reason": "EXACT_RATIONAL_BALANCE_PASS",
        "delta_r": "0",
        "povm_sum": "1",
        "voltage_v": 5.0,
    }


# ---------------------------------------------------------------------------
# Chain 4: Relativistic Light-Cone & Euclidean Phase-Cone
# ---------------------------------------------------------------------------
def verify_chain_4_causal_phase_cone(
    delta_t_ns: float,
    d_claimed_m: float,
    delta_phi_rad: float,
    d_max_m: float = 20.0,
    tau_spoof_m: float = 1.5,
) -> Dict[str, Any]:
    s_obs = delta_phi_rad / math.pi
    d_tof_m = C_VACUUM_M_PER_S * (delta_t_ns * 1e-9) / 2.0
    divergence_m = abs(d_claimed_m - d_tof_m)

    if abs(s_obs) > 1.0:
        return {"chain": 4, "verdict": "KILL", "reason": "UNPHYSICAL_PHASE_CONE_KILL", "s_obs": round(s_obs, 6), "voltage_v": 0.0}
    if d_tof_m > d_max_m or divergence_m > tau_spoof_m:
        return {"chain": 4, "verdict": "HOLD", "reason": "CAUSAL_LIGHTCONE_HOLD", "d_tof_m": round(d_tof_m, 6), "voltage_v": 0.0}
    return {"chain": 4, "verdict": "OPEN", "reason": "CAUSAL_PHASE_CONE_PASS", "d_tof_m": round(d_tof_m, 6), "voltage_v": 5.0}


# ---------------------------------------------------------------------------
# Chain 5: Cook-Levin Ancestor Hash, Monotone Fuse & Conjunctive W^2
# ---------------------------------------------------------------------------
def verify_chain_5_cook_levin_w2(
    expected_ancestor: str,
    provided_ancestor: str,
    fuse_prev: int,
    fuse_next: int,
    w_machine_id: str,
    w_human_id: str,
    zone_occupied: bool = False,
) -> Dict[str, Any]:
    fuse_monotone = (fuse_prev & fuse_next) == fuse_prev
    ancestor_ok = (expected_ancestor == provided_ancestor) and len(expected_ancestor) == 64

    if not fuse_monotone or not ancestor_ok:
        return {"chain": 5, "verdict": "KILL", "reason": "COOK_LEVIN_FUSE_OR_HASH_KILL", "voltage_v": 0.0}
    if not w_machine_id.strip() or not w_human_id.strip() or zone_occupied:
        return {"chain": 5, "verdict": "HOLD", "reason": "W2_ATTESTATION_OR_ZONE_HOLD", "voltage_v": 0.0}
    return {"chain": 5, "verdict": "OPEN", "reason": "COOK_LEVIN_W2_SEALED_PASS", "voltage_v": 5.0}


# ---------------------------------------------------------------------------
# Master Conjunctive Gate Evaluator (Chains 1..5 -> Omega_CI/CD)
# ---------------------------------------------------------------------------
def evaluate_w2_conjunctive_gate(chain_results: Sequence[Dict[str, Any]], ancestor_hash: str) -> Dict[str, Any]:
    verdicts = [c["verdict"] for c in chain_results]
    if "KILL" in verdicts:
        overall = "KILL"
        voltage_v = 0.00
    elif "HOLD" in verdicts or len(chain_results) != 5:
        overall = "HOLD"
        voltage_v = 0.00
    else:
        overall = "OPEN"
        voltage_v = 5.00

    envelope = {
        "ancestor": ancestor_hash,
        "chains": list(chain_results),
        "overall_verdict": overall,
        "voltage_v": voltage_v,
    }
    envelope["witness_sha256"] = canonical_sha256(envelope)
    return envelope


class TestW2FiveProofChains(unittest.TestCase):
    def test_chain_1_open_hold_kill(self) -> None:
        self.assertEqual(verify_chain_1_involutive_twin((1.0, 2.0), (0.5, -0.5))["verdict"], "OPEN")
        self.assertEqual(verify_chain_1_involutive_twin((9.0, 2.0), (2.5, 0.0))["verdict"], "HOLD")
        self.assertEqual(verify_chain_1_involutive_twin((1.0, 2.0), (0.5, -0.5), leakage=(0.01, 0.0))["verdict"], "KILL")

    def test_chain_2_open_hold_kill(self) -> None:
        ref = ((1.0, 0.0), (0.0, 1.0))
        theta = math.pi / 4.0
        rot = ((math.cos(theta), math.sin(theta)), (-math.sin(theta), math.cos(theta)))
        shear = ((1.0, 0.2), (0.0, 1.0))
        self.assertEqual(verify_chain_2_relational_gram(ref, rot)["verdict"], "OPEN")
        self.assertEqual(verify_chain_2_relational_gram(None, rot)["verdict"], "HOLD")
        self.assertEqual(verify_chain_2_relational_gram(ref, shear)["verdict"], "KILL")

    def test_chain_3_open_hold_kill(self) -> None:
        ins = [Fraction(100, 3), Fraction(200, 3)]
        outs = [Fraction(50, 1), Fraction(50, 1)]
        povm = [Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)]
        self.assertEqual(verify_chain_3_rational_conservation(ins, outs, povm)["verdict"], "OPEN")
        self.assertEqual(verify_chain_3_rational_conservation(ins, outs, povm, window_sealed=False)["verdict"], "HOLD")
        self.assertEqual(verify_chain_3_rational_conservation(ins, [Fraction(99, 1)], povm)["verdict"], "KILL")

    def test_chain_4_open_hold_kill(self) -> None:
        self.assertEqual(verify_chain_4_causal_phase_cone(100.0, 15.0, math.pi / 3.0)["verdict"], "OPEN")
        self.assertEqual(verify_chain_4_causal_phase_cone(100.0, 30.0, math.pi / 3.0)["verdict"], "HOLD")
        self.assertEqual(verify_chain_4_causal_phase_cone(100.0, 15.0, 1.3 * math.pi)["verdict"], "KILL")

    def test_chain_5_and_master_gate(self) -> None:
        h0 = "0" * 64
        self.assertEqual(verify_chain_5_cook_levin_w2(h0, h0, 0b0011, 0b0111, "WM-01", "WH-L01")["verdict"], "OPEN")
        self.assertEqual(verify_chain_5_cook_levin_w2(h0, h0, 0b0011, 0b0111, "WM-01", "")["verdict"], "HOLD")
        self.assertEqual(verify_chain_5_cook_levin_w2(h0, h0, 0b0111, 0b0011, "WM-01", "WH-L01")["verdict"], "KILL")

        all_open = [
            verify_chain_1_involutive_twin((1.0, 2.0), (0.5, -0.5)),
            verify_chain_2_relational_gram(((1.0, 0.0), (0.0, 1.0)), ((0.0, 1.0), (-1.0, 0.0))),
            verify_chain_3_rational_conservation([Fraction(10, 1)], [Fraction(10, 1)], [Fraction(1, 2), Fraction(1, 2)]),
            verify_chain_4_causal_phase_cone(100.0, 15.0, 0.5),
            verify_chain_5_cook_levin_w2(h0, h0, 0b0001, 0b0011, "WM-01", "WH-L01"),
        ]
        res = evaluate_w2_conjunctive_gate(all_open, h0)
        self.assertEqual(res["overall_verdict"], "OPEN")
        self.assertEqual(res["voltage_v"], 5.00)


if __name__ == "__main__":
    if sys.version_info < (3, 8):
        raise RuntimeError("FAIL_CLOSED_ENV_ERROR: Python >= 3.8 required.")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestW2FiveProofChains)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
