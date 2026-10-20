#!/usr/bin/env python3
"""
Deterministic L1 Verification Suite: IT-OT Consequence Gate & Digital Twin (SFI NORCICS Brief)
==============================================================================================
Specification : IT_OT_CONSEQUENCE_GATE_NORCICS_BRIEF.md (Domains I-IV)
Dependencies  : Python Standard Library ONLY (hashlib, json, math, sys, unittest)
Epistemic Tier: L1 Deterministic Software Demonstrator (INSPIRED_BY != IMPLEMENTS != PROVES)
Actuation Lock: KILL (0.00 V DC) > HOLD (0.00 V DC) > OPEN (5.00 V DC)
"""

import hashlib
import json
import math
import sys
import unittest
from typing import Dict, Any, Tuple

C_VACUUM_M_PER_S = 299_792_458.0


def canonical_sha256(payload: Dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ---------------------------------------------------------------------------
# Domain I: Digital Twin Involutive Collision & Envelope Gate (Door 25)
# ---------------------------------------------------------------------------
def evaluate_domain_i_digital_twin(
    s0: Tuple[float, float],
    delta_cmd: Tuple[float, float],
    non_reversible_leakage: Tuple[float, float],
    envelope_limit: float = 10.0,
    eps_iso: float = 1e-9,
    ancestor_hash: str = "0" * 64,
) -> Dict[str, Any]:
    """
    Simulates S0 --(a)--> Sf --(a^-1)--> Sr inside the isolated Digital Twin W_twin.
    """
    sf = (s0[0] + delta_cmd[0] + non_reversible_leakage[0], s0[1] + delta_cmd[1] + non_reversible_leakage[1])
    sr = (sf[0] - delta_cmd[0], sf[1] - delta_cmd[1])

    residual_iso = math.hypot(s0[0] - sr[0], s0[1] - sr[1])
    within_envelope = (abs(sf[0]) <= envelope_limit) and (abs(sf[1]) <= envelope_limit)

    if residual_iso > eps_iso:
        verdict = "KILL"
        reason = "TWIN_ASYMMETRY_DETECTED"
        voltage_v = 0.00
    elif not within_envelope:
        verdict = "HOLD"
        reason = "TWIN_ENVELOPE_BREACH"
        voltage_v = 0.00
    else:
        verdict = "OPEN"
        reason = "TWIN_INVOLUTIVE_PASS"
        voltage_v = 5.00

    record = {
        "domain": "I_DIGITAL_TWIN_DOOR25",
        "s0": [round(s0[0], 6), round(s0[1], 6)],
        "sf": [round(sf[0], 6), round(sf[1], 6)],
        "sr": [round(sr[0], 6), round(sr[1], 6)],
        "residual_iso": round(residual_iso, 12),
        "within_envelope": within_envelope,
        "verdict": verdict,
        "reason": reason,
        "voltage_v": voltage_v,
        "ancestor": ancestor_hash,
    }
    record["witness_sha256"] = canonical_sha256(record)
    return record


# ---------------------------------------------------------------------------
# Domain II: Constrained Local LLM / HMI Nagumo Control Barrier Gate
# ---------------------------------------------------------------------------
def evaluate_domain_ii_llm_hmi_barrier(
    h_val: float,
    grad_h_dot_f: float,
    alpha_gain: float = 1.0,
    eps_margin: float = 0.10,
    w_machine: bool = True,
    w_human: bool = True,
    ancestor_hash: str = "0" * 64,
) -> Dict[str, Any]:
    """
    Evaluates Nagumo tangency <grad h(x), f(x, u_cand)> + alpha * h(x) >= 0 and W^2 pre-commit.
    """
    nagumo_lhs = grad_h_dot_f + alpha_gain * h_val
    w2_valid = bool(w_machine and w_human)

    if h_val < 0.0 or nagumo_lhs < 0.0 or not w2_valid:
        verdict = "KILL"
        reason = "RC-BARRIER-BREACH-KILL"
        voltage_v = 0.00
    elif h_val <= eps_margin:
        verdict = "HOLD"
        reason = "RC-BOUNDARY-MARGIN-HOLD"
        voltage_v = 0.00
    else:
        verdict = "OPEN"
        reason = "RC-NAGUMO-W2-PASS"
        voltage_v = 5.00

    record = {
        "domain": "II_CONSTRAINED_LLM_HMI",
        "h_val": round(h_val, 6),
        "nagumo_lhs": round(nagumo_lhs, 6),
        "w2_valid": w2_valid,
        "verdict": verdict,
        "reason": reason,
        "voltage_v": voltage_v,
        "ancestor": ancestor_hash,
    }
    record["witness_sha256"] = canonical_sha256(record)
    return record


# ---------------------------------------------------------------------------
# Domain III: Maritime GNSS Denial & UWB Time-of-Flight Light-Cone Gate
# ---------------------------------------------------------------------------
def evaluate_domain_iii_maritime_uwb(
    delta_t_net_ns: float,
    d_gnss_m: float,
    s_obs_aoa: float,
    d_max_m: float = 20.0,
    tau_spoof_m: float = 1.5,
    ancestor_hash: str = "0" * 64,
) -> Dict[str, Any]:
    """
    Evaluates relativistic UWB ToF distance bound d_ToF = c * dt / 2 and AoA |s_obs| <= 1.0.
    """
    d_tof_m = C_VACUUM_M_PER_S * (delta_t_net_ns * 1e-9) / 2.0
    gnss_divergence_m = abs(d_gnss_m - d_tof_m)

    if abs(s_obs_aoa) > 1.0:
        verdict = "KILL"
        reason = "JAMMING_KILL_UNPHYSICAL_AOA"
        voltage_v = 0.00
    elif d_tof_m > d_max_m or gnss_divergence_m > tau_spoof_m:
        verdict = "HOLD"
        reason = "RC-CAUSAL-LIGHTCONE-VIOLATION"
        voltage_v = 0.00
    else:
        verdict = "OPEN"
        reason = "CAUSAL_LIGHTCONE_PASS"
        voltage_v = 5.00

    record = {
        "domain": "III_MARITIME_UWB_LIGHTCONE",
        "d_tof_m": round(d_tof_m, 6),
        "gnss_divergence_m": round(gnss_divergence_m, 6),
        "s_obs_aoa": round(s_obs_aoa, 6),
        "verdict": verdict,
        "reason": reason,
        "voltage_v": voltage_v,
        "ancestor": ancestor_hash,
    }
    record["witness_sha256"] = canonical_sha256(record)
    return record


# ---------------------------------------------------------------------------
# Domain IV: VSG Microgrid Screened Dispersion & (2f+1) Quorum Gate
# ---------------------------------------------------------------------------
def evaluate_domain_iv_vsg_quorum(
    omega_rad_s: float,
    mu_eff_rad_s: float,
    active_votes: int,
    f_faults: int = 1,
    other_warrants_ok: bool = True,
    ancestor_hash: str = "0" * 64,
) -> Dict[str, Any]:
    """
    Evaluates screened dispersion gap omega >= mu_eff and multiplicative (2f+1) BFT warrant.
    """
    quorum_required = 2 * f_faults + 1
    w_quorum = 1 if active_votes >= quorum_required else 0
    w_dispersion = 1 if omega_rad_s >= mu_eff_rad_s else 0
    w_other = 1 if other_warrants_ok else 0

    product_warrant = w_quorum * w_dispersion * w_other

    if w_quorum == 0 or w_other == 0:
        verdict = "KILL"
        reason = "WARRANT_LOSS_BFT_KILL"
        voltage_v = 0.00
    elif w_dispersion == 0:
        verdict = "HOLD"
        reason = "EVANESCENT_SUBGAP_HOLD"
        voltage_v = 0.00
    else:
        verdict = "OPEN"
        reason = "VSG_DISPERSION_QUORUM_PASS"
        voltage_v = 5.00

    record = {
        "domain": "IV_VSG_DISPERSION_BFT",
        "omega_rad_s": round(omega_rad_s, 6),
        "mu_eff_rad_s": round(mu_eff_rad_s, 6),
        "active_votes": active_votes,
        "quorum_required": quorum_required,
        "product_warrant": product_warrant,
        "verdict": verdict,
        "reason": reason,
        "voltage_v": voltage_v,
        "ancestor": ancestor_hash,
    }
    record["witness_sha256"] = canonical_sha256(record)
    return record


class TestNORCICSConsequenceGateSuite(unittest.TestCase):
    def test_domain_i_digital_twin_states(self) -> None:
        r_open = evaluate_domain_i_digital_twin((2.0, 3.0), (1.5, -1.0), (0.0, 0.0))
        self.assertEqual(r_open["verdict"], "OPEN")
        self.assertEqual(r_open["voltage_v"], 5.00)

        r_hold = evaluate_domain_i_digital_twin((8.0, 3.0), (4.5, 0.0), (0.0, 0.0), envelope_limit=10.0)
        self.assertEqual(r_hold["verdict"], "HOLD")
        self.assertEqual(r_hold["voltage_v"], 0.00)

        r_kill = evaluate_domain_i_digital_twin((2.0, 3.0), (1.5, -1.0), (0.05, 0.0))
        self.assertEqual(r_kill["verdict"], "KILL")
        self.assertEqual(r_kill["voltage_v"], 0.00)

    def test_domain_ii_constrained_llm_hmi(self) -> None:
        r_open = evaluate_domain_ii_llm_hmi_barrier(h_val=0.50, grad_h_dot_f=0.10)
        self.assertEqual(r_open["verdict"], "OPEN")

        r_hold = evaluate_domain_ii_llm_hmi_barrier(h_val=0.05, grad_h_dot_f=0.10)
        self.assertEqual(r_hold["verdict"], "HOLD")

        r_kill = evaluate_domain_ii_llm_hmi_barrier(h_val=0.20, grad_h_dot_f=-0.50)
        self.assertEqual(r_kill["verdict"], "KILL")

    def test_domain_iii_maritime_uwb(self) -> None:
        r_open = evaluate_domain_iii_maritime_uwb(delta_t_net_ns=100.0, d_gnss_m=15.0, s_obs_aoa=0.5)
        self.assertEqual(r_open["verdict"], "OPEN")

        r_hold = evaluate_domain_iii_maritime_uwb(delta_t_net_ns=100.0, d_gnss_m=45.0, s_obs_aoa=0.5)
        self.assertEqual(r_hold["verdict"], "HOLD")

        r_kill = evaluate_domain_iii_maritime_uwb(delta_t_net_ns=100.0, d_gnss_m=15.0, s_obs_aoa=1.25)
        self.assertEqual(r_kill["verdict"], "KILL")

    def test_domain_iv_vsg_quorum(self) -> None:
        r_open = evaluate_domain_iv_vsg_quorum(omega_rad_s=12.0, mu_eff_rad_s=10.0, active_votes=3, f_faults=1)
        self.assertEqual(r_open["verdict"], "OPEN")

        r_hold = evaluate_domain_iv_vsg_quorum(omega_rad_s=6.0, mu_eff_rad_s=10.0, active_votes=3, f_faults=1)
        self.assertEqual(r_hold["verdict"], "HOLD")

        r_kill = evaluate_domain_iv_vsg_quorum(omega_rad_s=12.0, mu_eff_rad_s=10.0, active_votes=2, f_faults=1)
        self.assertEqual(r_kill["verdict"], "KILL")


def run_deterministic_trace() -> Dict[str, Any]:
    if sys.version_info < (3, 8):
        raise RuntimeError("FAIL_CLOSED_ENV_ERROR: Python >= 3.8 required.")

    chain = []
    h0 = "0" * 64

    s1 = evaluate_domain_i_digital_twin((2.0, 3.0), (1.5, -1.0), (0.05, 0.0), ancestor_hash=h0)
    chain.append(s1)

    s2 = evaluate_domain_ii_llm_hmi_barrier(h_val=0.20, grad_h_dot_f=-0.50, ancestor_hash=s1["witness_sha256"])
    chain.append(s2)

    s3 = evaluate_domain_iii_maritime_uwb(delta_t_net_ns=100.0, d_gnss_m=45.0, s_obs_aoa=0.5, ancestor_hash=s2["witness_sha256"])
    chain.append(s3)

    s4 = evaluate_domain_iv_vsg_quorum(omega_rad_s=12.0, mu_eff_rad_s=10.0, active_votes=3, f_faults=1, ancestor_hash=s3["witness_sha256"])
    chain.append(s4)

    master_digest = canonical_sha256({"chain": [step["witness_sha256"] for step in chain]})
    return {"steps": chain, "master_chain_sha256": master_digest}


if __name__ == "__main__":
    trace = run_deterministic_trace()
    print(json.dumps(trace, indent=2, sort_keys=True))
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestNORCICSConsequenceGateSuite)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
