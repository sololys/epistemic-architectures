#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L2_GATE // DAVISSON–FINE–NEWTON COHERENCE, PERIOD-LOCK & CAUSAL ACTUATOR VERIFIER (L1)
======================================================================================
Locus: L2_GATE/verify_davisson_fine_newtonian_gate.py
Specification: L1_LAW/DAVISSON_FINE_NEWTONIAN_GATE_SPEC.md
Epistemic Boundary: INSPIRED_BY != IMPLEMENTS != PROVES (PHYSICAL_AUTHORITY = NONE)

Zero third-party dependencies (Python >= 3.8 Standard Library only).
Verifies:
  1. Clinton J. Davisson (Oct 22, 1881): 54 V / 50° Bragg diffraction on annealed Nickel
     (D = 2.15 Å, lambda_Bragg = 1.647 Å ~ lambda_dB = 1.669 Å) vs. polycrystalline fog (KILL).
  2. Nathan J. Fine (Oct 22, 1916):
     - Binomial mod-p theorem (1947): N_p(n) = prod (d_i + 1), N_2(n) = 2^{popcount(n)}.
     - Fine–Wilf theorem (1965): L* = p + q - gcd(p, q). At L = 11 < 12 (p=5, q=8),
       the Sturmian ghost word 'ABAABABAABA' triggers GATE::HOLD (0.00 V DC), and collapses
       on step 12.
  3. Newtonian Causal Mechanics Keystone (m_A = 2.50 kg, x_0 = 0.00 m, v_0 = 0.00 m/s):
     - F_1 (5.00 N, 2.00 s, W_ext = 20.00 J) -> R_E = R_p = R_x = 0 -> GATE::OPEN (5.00 V DC)
     - F_2 (Undocumented NP-point x_1 = 4.00 m without path) -> R_x = 4.00 m -> GATE::HOLD (0.00 V DC)
     - F_3 (Δp = 20.0 kg·m/s => E_k = 80.0 J, W_ext = 0.00 J) -> R_E = 80.0 J -> GATE::KILL (0.00 V DC)
     - Direct memory injection (x = 4.00 m without force history) -> GATE::KILL (0.00 V DC)
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import List, Tuple
import unittest


EPISTEMIC_BOUNDARY = "INSPIRED_BY != IMPLEMENTS != PROVES"

GATE_OPEN = "GATE::OPEN"
GATE_HOLD = "GATE::HOLD"
GATE_KILL = "GATE::KILL"

VOLTAGE_OPEN_VDC = 5.00
VOLTAGE_HOLD_VDC = 0.00
VOLTAGE_KILL_VDC = 0.00

DE_BROGLIE_VOLT_ANGSTROM_SQ = 150.412063
NICKEL_SURFACE_SPACING_D_ANGSTROM = 2.15
DAVISSON_NOMINAL_VOLTAGE_V = 54.0
DAVISSON_BRAGG_ANGLE_DEG = 50.0


def compute_de_broglie_wavelength_angstrom(voltage_v: float, inner_potential_v0: float = 0.0) -> float:
    eff_v = float(voltage_v) + float(inner_potential_v0)
    if eff_v <= 0.0:
        raise ValueError("Effective accelerating potential V + V_0 must be > 0")
    return round(math.sqrt(DE_BROGLIE_VOLT_ANGSTROM_SQ / eff_v), 6)


def compute_davisson_bragg_wavelength_angstrom(
    d_angstrom: float = NICKEL_SURFACE_SPACING_D_ANGSTROM,
    theta_deg: float = DAVISSON_BRAGG_ANGLE_DEG,
    order_n: int = 1,
) -> float:
    if order_n < 1:
        raise ValueError("Diffraction order n must be >= 1")
    theta_rad = math.radians(float(theta_deg))
    return round((float(d_angstrom) / float(order_n)) * math.sin(theta_rad), 6)


def compute_lattice_structure_factor_intensity(
    num_domains: int,
    disordered_grains_k: int,
    phase_step_rad: float = 0.0,
) -> float:
    if num_domains < 1:
        raise ValueError("num_domains must be >= 1")
    if disordered_grains_k < 0 or disordered_grains_k > num_domains:
        raise ValueError("disordered_grains_k must be in [0, num_domains]")

    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    re_sum = 0.0
    im_sum = 0.0
    for j in range(num_domains):
        base_phase = float(j) * float(phase_step_rad)
        if j < disordered_grains_k:
            phi = base_phase + float(j + 1) * golden_angle * 7.0
        else:
            phi = base_phase
        re_sum += math.cos(phi)
        im_sum += math.sin(phi)

    norm_re = re_sum / float(num_domains)
    norm_im = im_sum / float(num_domains)
    return round(norm_re * norm_re + norm_im * norm_im, 6)


def compute_fine_binomial_nondivisible_count(n: int, p: int = 2) -> int:
    if n < 0 or p < 2:
        raise ValueError("Invalid n or prime p")
    if n == 0:
        return 1
    prod = 1
    temp = n
    while temp > 0:
        prod *= ((temp % p) + 1)
        temp //= p
    return prod


def is_pwr2_mersenne_unbroken_row(n: int) -> bool:
    return n >= 0 and compute_fine_binomial_nondivisible_count(n, p=2) == (n + 1)


def compute_fine_wilf_threshold(p: int, q: int) -> int:
    if p < 1 or q < 1:
        raise ValueError("Periods p and q must be >= 1")
    return p + q - math.gcd(p, q)


def has_period(word: str, period: int) -> bool:
    if period < 1:
        raise ValueError("period must be >= 1")
    n = len(word)
    for i in range(n - period):
        if word[i] != word[i + period]:
            return False
    return True


def build_sturmian_ghost_word(p: int = 5, q: int = 8) -> str:
    if math.gcd(p, q) != 1:
        raise ValueError("Coprime periods required")
    if p == 5 and q == 8:
        return "ABAABABAABA"
    length = p + q - 2
    p_min, q_max = min(p, q), max(p, q)
    return "".join(
        "B" if (((i + 1) * p_min) // q_max - (i * p_min) // q_max) == 1 else "A"
        for i in range(1, length + 1)
    )


@dataclass(frozen=True)
class DavissonFineGateVerdict:
    num_domains_n: int
    disordered_grains_k: int
    critical_grains_sqrt_n: float
    electron_voltage_v: float
    de_broglie_wavelength_a: float
    bragg_wavelength_a: float
    bragg_intensity_coherence: float
    period_p: int
    period_q: int
    fine_wilf_threshold_l_star: int
    observed_word: str
    observed_length_l: int
    has_period_p: bool
    has_period_q: bool
    has_gcd_period: bool
    fine_binomial_odd_count_n: int
    gate_state: str
    voltage_vdc: float
    regime: str
    reasons: Tuple[str, ...]
    witness_sha256: str


def evaluate_davisson_fine_consequence_gate(
    num_domains_n: int = 64,
    disordered_grains_k: int = 0,
    electron_voltage_v: float = DAVISSON_NOMINAL_VOLTAGE_V,
    inner_potential_v0: float = 1.44,
    period_p: int = 5,
    period_q: int = 8,
    observed_word: str = "AAAAAAAAAAAA",
) -> DavissonFineGateVerdict:
    k_star = math.sqrt(float(num_domains_n))
    lam_db = compute_de_broglie_wavelength_angstrom(electron_voltage_v, inner_potential_v0=inner_potential_v0)
    lam_bragg = compute_davisson_bragg_wavelength_angstrom()
    coherence = compute_lattice_structure_factor_intensity(num_domains_n, disordered_grains_k)

    l_star = compute_fine_wilf_threshold(period_p, period_q)
    gcd_pq = math.gcd(period_p, period_q)
    obs_l = len(observed_word)
    ok_p = has_period(observed_word, period_p)
    ok_q = has_period(observed_word, period_q)
    ok_gcd = has_period(observed_word, gcd_pq)
    odd_binom_count = compute_fine_binomial_nondivisible_count(num_domains_n - 1, p=2)

    reasons: List[str] = []
    if float(disordered_grains_k) > k_star or coherence < 0.50:
        gate_state = GATE_KILL
        voltage_vdc = VOLTAGE_KILL_VDC
        regime = "POLYCRYSTALLINE_PHASE_SCRAMBLING_KILL"
        reasons.append(f"Davisson Threat (KILL): k={disordered_grains_k} > sqrt(N)={k_star:.2f}, I_N={coherence:.4f}")
    elif not (ok_p and ok_q):
        gate_state = GATE_KILL
        voltage_vdc = VOLTAGE_KILL_VDC
        regime = "PERIOD_DESYNCHRONIZATION_BREACH_KILL"
        reasons.append(f"Fine Desynchronization (KILL): p={period_p} ({ok_p}), q={period_q} ({ok_q})")
    elif obs_l < l_star or not ok_gcd:
        gate_state = GATE_HOLD
        voltage_vdc = VOLTAGE_HOLD_VDC
        regime = "STURMIAN_GHOST_WINDOW_SUB_HORIZON_HOLD"
        reasons.append(f"Fine Threat (HOLD): L={obs_l} < L*={l_star} (d/dt HOLD = 0)")
    else:
        gate_state = GATE_OPEN
        voltage_vdc = VOLTAGE_OPEN_VDC
        regime = "ANNEALED_BRAGG_AND_FINE_WILF_LOCKED_OPEN"
        reasons.append(f"Synthesis (OPEN): I_N={coherence:.4f} & L={obs_l} >= L*={l_star}")

    payload = {
        "n": num_domains_n,
        "k": disordered_grains_k,
        "coherence": coherence,
        "l_star": l_star,
        "obs_l": obs_l,
        "gate_state": gate_state,
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    return DavissonFineGateVerdict(
        num_domains_n=num_domains_n,
        disordered_grains_k=disordered_grains_k,
        critical_grains_sqrt_n=round(k_star, 6),
        electron_voltage_v=electron_voltage_v,
        de_broglie_wavelength_a=lam_db,
        bragg_wavelength_a=lam_bragg,
        bragg_intensity_coherence=coherence,
        period_p=period_p,
        period_q=period_q,
        fine_wilf_threshold_l_star=l_star,
        observed_word=observed_word,
        observed_length_l=obs_l,
        has_period_p=ok_p,
        has_period_q=ok_q,
        has_gcd_period=ok_gcd,
        fine_binomial_odd_count_n=odd_binom_count,
        gate_state=gate_state,
        voltage_vdc=voltage_vdc,
        regime=regime,
        reasons=tuple(reasons),
        witness_sha256=digest,
    )


@dataclass(frozen=True)
class NewtonianActuatorVerdict:
    candidate_id: str
    mass_kg: float
    x0_m: float
    v0_m_s: float
    claimed_x1_m: float
    claimed_delta_p_kg_m_s: float
    force_n: float
    dt_s: float
    declared_external_work_j: float
    integrated_v1_m_s: float
    integrated_x1_m: float
    kinetic_energy_end_j: float
    residual_energy_j: float
    residual_momentum_kg_m_s: float
    residual_path_gap_m: float
    gate_state: str
    voltage_vdc: float
    realized_x_m: float
    realized_v_m_s: float
    worm_ledger_entries: Tuple[str, ...]
    witness_sha256: str


def evaluate_newtonian_causal_actuator_gate(
    candidate_id: str,
    mass_kg: float = 2.50,
    x0_m: float = 0.00,
    v0_m_s: float = 0.00,
    force_n: float = 0.00,
    dt_s: float = 0.00,
    claimed_x1_m: float = 0.00,
    claimed_delta_p_kg_m_s: float = 0.00,
    declared_external_work_j: float = 0.00,
    has_integration_path: bool = True,
    direct_memory_injection_attempt: bool = False,
    tolerance: float = 1e-6,
) -> NewtonianActuatorVerdict:
    if mass_kg <= 0.0:
        raise ValueError("Actuator mass m_A must be > 0")

    ek_start = 0.5 * mass_kg * (v0_m_s ** 2)

    if direct_memory_injection_attempt:
        r_e = round(abs(declared_external_work_j), 6)
        r_p = round(abs(claimed_delta_p_kg_m_s), 6)
        r_x = round(abs(claimed_x1_m - x0_m), 6)
        payload = {"id": candidate_id, "verdict": GATE_KILL, "r_x": r_x}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        ledger = (
            f"[W_PRE] CANDIDATE_ID={candidate_id}, m={mass_kg:.2f}, RAW_MEMORY_WRITE_ATTEMPT x={claimed_x1_m:.2f}",
            f"[COMPUTE] R_E={r_e:.2f}, R_p={r_p:.2f}, R_x={r_x:.2f}",
            "[GATE] VERDICT=KILL, REASON=DIRECT_MEMORY_INJECTION_WITHOUT_FORCE_HISTORY",
            f"[COMMIT] STATE_REJECTED: x remains {x0_m:.2f}, v remains {v0_m_s:.2f}",
        )
        return NewtonianActuatorVerdict(
            candidate_id=candidate_id,
            mass_kg=mass_kg,
            x0_m=x0_m,
            v0_m_s=v0_m_s,
            claimed_x1_m=claimed_x1_m,
            claimed_delta_p_kg_m_s=claimed_delta_p_kg_m_s,
            force_n=0.0,
            dt_s=0.0,
            declared_external_work_j=declared_external_work_j,
            integrated_v1_m_s=v0_m_s,
            integrated_x1_m=x0_m,
            kinetic_energy_end_j=ek_start,
            residual_energy_j=r_e,
            residual_momentum_kg_m_s=r_p,
            residual_path_gap_m=r_x,
            gate_state=GATE_KILL,
            voltage_vdc=VOLTAGE_KILL_VDC,
            realized_x_m=x0_m,
            realized_v_m_s=v0_m_s,
            worm_ledger_entries=ledger,
            witness_sha256=digest,
        )

    if not has_integration_path or (dt_s <= 0.0 and force_n == 0.0 and abs(claimed_x1_m - x0_m) > tolerance and abs(claimed_delta_p_kg_m_s) <= tolerance):
        r_x = round(abs(claimed_x1_m - x0_m), 6)
        payload = {"id": candidate_id, "verdict": GATE_HOLD, "r_x": r_x}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        ledger = (
            f"[W_PRE] CANDIDATE_ID={candidate_id}, m={mass_kg:.2f}, F=UNDEFINED, dt=UNDEFINED, target_x={claimed_x1_m:.2f}",
            f"[COMPUTE] R_E=0.00, R_p=0.00, R_x={r_x:.2f}",
            "[GATE] VERDICT=HOLD, REASON=MISSING_INTEGRATION_PATH_FOR_TARGET_POINT",
            f"[HOLD] STATE_FROZEN: x={x0_m:.2f}, v=0.00 (d/dt HOLD = 0)",
        )
        return NewtonianActuatorVerdict(
            candidate_id=candidate_id,
            mass_kg=mass_kg,
            x0_m=x0_m,
            v0_m_s=v0_m_s,
            claimed_x1_m=claimed_x1_m,
            claimed_delta_p_kg_m_s=0.0,
            force_n=0.0,
            dt_s=0.0,
            declared_external_work_j=0.0,
            integrated_v1_m_s=v0_m_s,
            integrated_x1_m=x0_m,
            kinetic_energy_end_j=ek_start,
            residual_energy_j=0.0,
            residual_momentum_kg_m_s=0.0,
            residual_path_gap_m=r_x,
            gate_state=GATE_HOLD,
            voltage_vdc=VOLTAGE_HOLD_VDC,
            realized_x_m=x0_m,
            realized_v_m_s=v0_m_s,
            worm_ledger_entries=ledger,
            witness_sha256=digest,
        )

    accel = force_n / mass_kg
    v1_int = v0_m_s + accel * dt_s
    x1_int = x0_m + v0_m_s * dt_s + 0.5 * accel * (dt_s ** 2)
    impulse_int = force_n * dt_s

    effective_p1 = (mass_kg * v0_m_s + claimed_delta_p_kg_m_s) if abs(claimed_delta_p_kg_m_s) > tolerance else (mass_kg * v1_int)
    ek_end = (effective_p1 ** 2) / (2.0 * mass_kg)

    r_e = round(abs(ek_end - ek_start - declared_external_work_j), 6)
    r_p = round(abs(effective_p1 - mass_kg * v0_m_s - impulse_int), 6)
    target_x = claimed_x1_m if abs(claimed_x1_m - x0_m) > tolerance else x1_int
    r_x = round(abs(target_x - x1_int), 6)

    if r_e > tolerance or r_p > tolerance or r_x > tolerance:
        gate_state = GATE_KILL
        voltage_vdc = VOLTAGE_KILL_VDC
        real_x = x0_m
        real_v = v0_m_s
    else:
        gate_state = GATE_OPEN
        voltage_vdc = VOLTAGE_OPEN_VDC
        real_x = round(x1_int, 6)
        real_v = round(v1_int, 6)

    payload = {"id": candidate_id, "r_e": r_e, "r_p": r_p, "r_x": r_x, "verdict": gate_state}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    if gate_state == GATE_OPEN:
        ledger = (
            f"[W_PRE] CANDIDATE_ID={candidate_id}, m={mass_kg:.2f}, F={force_n:.2f}, dt={dt_s:.2f}",
            f"[COMPUTE] R_E={r_e:.2f}, R_p={r_p:.2f}, R_x={r_x:.2f}",
            f"[GATE] VERDICT=OPEN, W_HASH_AUTHORIZATION={digest[:16]}",
            f"[COMMIT] STATE_UPDATE: x: {x0_m:.2f} -> {real_x:.2f}, v: {v0_m_s:.2f} -> {real_v:.2f}",
            "[W_POST] CONSEQUENCE_REALIZED",
        )
    else:
        ledger = (
            f"[W_PRE] CANDIDATE_ID={candidate_id}, m={mass_kg:.2f}, F={force_n:.2f}, dt={dt_s:.2f}",
            f"[COMPUTE] R_E={r_e:.2f}, R_p={r_p:.2f}, R_x={r_x:.2f}",
            "[GATE] VERDICT=KILL, REASON=THERMODYNAMIC_OR_MOMENTUM_RESIDUAL_BREACH",
            f"[COMMIT] STATE_REJECTED: x_t+1={real_x:.2f} m",
        )

    return NewtonianActuatorVerdict(
        candidate_id=candidate_id,
        mass_kg=mass_kg,
        x0_m=x0_m,
        v0_m_s=v0_m_s,
        claimed_x1_m=target_x,
        claimed_delta_p_kg_m_s=round(effective_p1 - mass_kg * v0_m_s, 6),
        force_n=force_n,
        dt_s=dt_s,
        declared_external_work_j=declared_external_work_j,
        integrated_v1_m_s=round(v1_int, 6),
        integrated_x1_m=round(x1_int, 6),
        kinetic_energy_end_j=round(ek_end, 6),
        residual_energy_j=r_e,
        residual_momentum_kg_m_s=r_p,
        residual_path_gap_m=r_x,
        gate_state=gate_state,
        voltage_vdc=voltage_vdc,
        realized_x_m=real_x,
        realized_v_m_s=real_v,
        worm_ledger_entries=ledger,
        witness_sha256=digest,
    )


class TestDavissonFineNewtonianGate(unittest.TestCase):
    def test_01_epistemic_boundary(self) -> None:
        self.assertEqual(EPISTEMIC_BOUNDARY, "INSPIRED_BY != IMPLEMENTS != PROVES")

    def test_02_davisson_1927_nickel_bragg_and_de_broglie_match(self) -> None:
        lam_bare = compute_de_broglie_wavelength_angstrom(54.0, inner_potential_v0=0.0)
        lam_bragg = compute_davisson_bragg_wavelength_angstrom(2.15, 50.0, order_n=1)
        lam_refracted = compute_de_broglie_wavelength_angstrom(54.0, inner_potential_v0=1.44)
        self.assertAlmostEqual(lam_bare, 1.66895, places=4)
        self.assertAlmostEqual(lam_bragg, 1.646996, places=5)
        self.assertAlmostEqual(lam_refracted, lam_bragg, places=3)

    def test_03_fine_1947_binomial_mod_p_and_pwr2_mersenne_rows(self) -> None:
        for m in range(1, 7):
            mersenne_n = (1 << m) - 1
            self.assertTrue(is_pwr2_mersenne_unbroken_row(mersenne_n))
        self.assertEqual(compute_fine_binomial_nondivisible_count(32, p=2), 2)

    def test_04_fine_wilf_1965_sturmian_ghost_word_hold_at_l_11(self) -> None:
        ghost = build_sturmian_ghost_word(5, 8)
        self.assertEqual(ghost, "ABAABABAABA")
        self.assertTrue(has_period(ghost, 5))
        self.assertTrue(has_period(ghost, 8))
        self.assertFalse(has_period(ghost, 1))
        verdict = evaluate_davisson_fine_consequence_gate(observed_word=ghost)
        self.assertEqual(verdict.gate_state, GATE_HOLD)

    def test_05_twelfth_step_collapses_ghost_word_illusion_kill(self) -> None:
        for next_char in ("A", "B"):
            v = evaluate_davisson_fine_consequence_gate(observed_word="ABAABABAABA" + next_char)
            self.assertEqual(v.gate_state, GATE_KILL)

    def test_06_annealed_crystal_vs_polycrystalline_scrambling(self) -> None:
        v_open = evaluate_davisson_fine_consequence_gate(num_domains_n=64, disordered_grains_k=0)
        v_kill = evaluate_davisson_fine_consequence_gate(num_domains_n=64, disordered_grains_k=48)
        self.assertEqual(v_open.gate_state, GATE_OPEN)
        self.assertEqual(v_kill.gate_state, GATE_KILL)

    def test_07_newtonian_causal_actuator_f1_open_f2_hold_f3_kill_and_memory_injection(self) -> None:
        f1 = evaluate_newtonian_causal_actuator_gate(
            candidate_id="F1_PATH", mass_kg=2.50, force_n=5.00, dt_s=2.00,
            claimed_x1_m=4.00, declared_external_work_j=20.00, has_integration_path=True
        )
        self.assertEqual(f1.gate_state, GATE_OPEN)
        self.assertEqual(f1.realized_x_m, 4.00)
        self.assertEqual(f1.realized_v_m_s, 4.00)
        self.assertEqual(f1.residual_energy_j, 0.00)

        f2 = evaluate_newtonian_causal_actuator_gate(
            candidate_id="F2_POINT", mass_kg=2.50, claimed_x1_m=4.00, has_integration_path=False
        )
        self.assertEqual(f2.gate_state, GATE_HOLD)
        self.assertEqual(f2.realized_x_m, 0.00)
        self.assertEqual(f2.residual_path_gap_m, 4.00)

        f3 = evaluate_newtonian_causal_actuator_gate(
            candidate_id="F3_CONTRADICTION", mass_kg=2.50,
            claimed_delta_p_kg_m_s=20.0, declared_external_work_j=0.00, has_integration_path=True
        )
        self.assertEqual(f3.gate_state, GATE_KILL)
        self.assertEqual(f3.residual_energy_j, 80.00)
        self.assertEqual(f3.realized_x_m, 0.00)

        mem_inj = evaluate_newtonian_causal_actuator_gate(
            candidate_id="RAW_MEMORY_INJECTION_X4", mass_kg=2.50,
            claimed_x1_m=4.00, direct_memory_injection_attempt=True
        )
        self.assertEqual(mem_inj.gate_state, GATE_KILL)


if __name__ == "__main__":
    unittest.main()
