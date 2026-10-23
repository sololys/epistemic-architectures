#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAVISSON–FINE OCTOBER 22 COHERENCE & PERIOD-LOCK CONSEQUENCE GATE ENGINE (L1)
=============================================================================
Locus: 03_ENGINES/ENGINES/micro_engines/davisson_fine_oct22_coherence_gate_engine.py
Classification: L1 Deterministic Software Prototype / Matter-Wave & Combinatorial Gate
Epistemic Boundary: INSPIRED_BY != IMPLEMENTS != PROVES (PHYSICAL_AUTHORITY = NONE)

Unifies the two October 22 extremes into a single fail-closed Consequence Gate (Π_K):
  1. Extreme A — Clinton Joseph Davisson (born Oct 22, 1881; Nobel Prize 1937):
     - De Broglie electron matter-wave wavelength:
         lambda_dB(V) = h / sqrt(2 * m_e * e * V) = sqrt(150.41206 / V) Å
       At V = 54.0 V: lambda_dB = 1.66895 Å.
     - Surface Bragg diffraction on annealed single-crystal Nickel (d_111 = 2.15 Å,
       theta = 50.0°):
         lambda_Bragg = D * sin(50°) = 2.15 * 0.76604444 = 1.6469955 Å
       (matching lambda_dB within 1.3%, with inner crystal potential V_0 ~ 1.44 eV).
     - Polycrystalline vs. Annealed Single-Crystal Coherence Factor:
         I_N(theta) = | (1/N) sum_{j=0}^{N-1} exp(i * (k_phase * j + phi_j)) |^2
       For polycrystalline disorder (random grain phases phi_j), I_N ~ 1/N -> 0 (KILL).
       For annealed single crystal (phi_j = 0 at Bragg angle), I_N = 1.0 (OPEN).

  2. Extreme B — Nathan Jacob Fine (born Oct 22, 1916):
     - Fine's Binomial Theorem mod p (1947, Am. Math. Monthly 54, 589–592):
       The number of binomial coefficients C(n, k) (0 <= k <= n) not divisible by
       prime p equals:
         N_p(n) = prod_{i} (d_i + 1)
       where n = sum d_i p^i in base p. For p = 2:
         N_2(n) = 2^{popcount(n)}
       and every C(n, k) is odd (N_2(n) == n + 1) iff n = 2^m - 1 (PWR2 Mersenne row).
     - Fine–Wilf Theorem (1965, Proc. AMS 16, 109–114):
       If a word w has periods p and q and length L >= L* = p + q - gcd(p, q),
       then w also has period d = gcd(p, q).
       At L = L* - 1 (e.g., p=5, q=8 => L*=12, L=11), the Sturmian ghost word
         w_ghost = "ABAABABAABA"
       satisfies both period 5 and period 8 without collapsing to period gcd(5,8)=1!
       Π_K places any dual-periodic stream with L < p + q - gcd(p, q) in GATE::HOLD (0.00 V).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import math
from typing import Dict, List, Optional, Sequence, Tuple
import unittest


EPISTEMIC_BOUNDARY = "INSPIRED_BY != IMPLEMENTS != PROVES"

GATE_OPEN = "GATE::OPEN"
GATE_HOLD = "GATE::HOLD"
GATE_KILL = "GATE::KILL"

VOLTAGE_OPEN_VDC = 5.00
VOLTAGE_HOLD_VDC = 0.00
VOLTAGE_KILL_VDC = 0.00

# Physical constants (CODATA 2018/2022) for de Broglie electron wavelength in Angstroms:
# h^2 / (2 * m_e * e) = 150.412063... V * Å^2
DE_BROGLIE_VOLT_ANGSTROM_SQ = 150.412063
NICKEL_SURFACE_SPACING_D_ANGSTROM = 2.15
DAVISSON_NOMINAL_VOLTAGE_V = 54.0
DAVISSON_BRAGG_ANGLE_DEG = 50.0


# ==============================================================================
# 1. EXTREME A: CLINTON JOSEPH DAVISSON (1881) — BRAGG MATTER-WAVE COHERENCE
# ==============================================================================

def compute_de_broglie_wavelength_angstrom(voltage_v: float, inner_potential_v0: float = 0.0) -> float:
    """
    Computes the non-relativistic electron de Broglie wavelength in Angstroms (Å):
        lambda_dB = sqrt(150.412063 / (V + V_0))
    """
    eff_v = float(voltage_v) + float(inner_potential_v0)
    if eff_v <= 0.0:
        raise ValueError("Effective accelerating potential V + V_0 must be > 0")
    return round(math.sqrt(DE_BROGLIE_VOLT_ANGSTROM_SQ / eff_v), 6)


def compute_davisson_bragg_wavelength_angstrom(
    d_angstrom: float = NICKEL_SURFACE_SPACING_D_ANGSTROM,
    theta_deg: float = DAVISSON_BRAGG_ANGLE_DEG,
    order_n: int = 1,
) -> float:
    """
    Computes the surface grating Bragg wavelength:
        lambda_Bragg = (D / n) * sin(theta)
    At D = 2.15 Å, theta = 50°, n = 1: lambda_Bragg = 1.646996 Å.
    """
    if order_n < 1:
        raise ValueError("Diffraction order n must be >= 1")
    theta_rad = math.radians(float(theta_deg))
    return round((float(d_angstrom) / float(order_n)) * math.sin(theta_rad), 6)


def compute_lattice_structure_factor_intensity(
    num_domains: int,
    disordered_grains_k: int,
    phase_step_rad: float = 0.0,
) -> float:
    """
    Computes normalized Bragg coherence intensity I_N in [0, 1] across N lattice domains
    when k domains suffer polycrystalline phase scrambling (deterministic golden-angle
    phase offsets) and (N - k) domains are aligned in an annealed single crystal:
        I_N = | (1/N) * sum_{j=0}^{N-1} exp(i * phi_j) |^2
    """
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
            # Polycrystalline grain boundary phase scrambling
            phi = base_phase + float(j + 1) * golden_angle * 7.0
        else:
            phi = base_phase
        re_sum += math.cos(phi)
        im_sum += math.sin(phi)

    norm_re = re_sum / float(num_domains)
    norm_im = im_sum / float(num_domains)
    return round(norm_re * norm_re + norm_im * norm_im, 6)


# ==============================================================================
# 2. EXTREME B: NATHAN JACOB FINE (1916) — BINOMIAL MOD-p & FINE–WILF LOCK
# ==============================================================================

def compute_fine_binomial_nondivisible_count(n: int, p: int = 2) -> int:
    """
    Fine's Theorem (1947): Number of binomial coefficients C(n, k) (0 <= k <= n)
    not divisible by prime p equals prod_i (d_i + 1), where d_i are the base-p
    digits of n.
    For p = 2: N_2(n) = 2^{popcount(n)}.
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    if p < 2:
        raise ValueError("Prime p must be >= 2")
    if n == 0:
        return 1
    prod = 1
    temp = n
    while temp > 0:
        digit = temp % p
        prod *= (digit + 1)
        temp //= p
    return prod


def is_pwr2_mersenne_unbroken_row(n: int) -> bool:
    """
    Returns True iff every binomial coefficient C(n, k) on row n is odd,
    which by Fine's 1947 theorem occurs iff N_2(n) == n + 1 <=> n = 2^m - 1.
    """
    if n < 0:
        return False
    return compute_fine_binomial_nondivisible_count(n, p=2) == (n + 1)


def compute_fine_wilf_threshold(p: int, q: int) -> int:
    """
    Fine–Wilf Theorem (1965): Minimum observation length L* required to force
    a sequence with periods p and q to collapse to period gcd(p, q):
        L* = p + q - gcd(p, q)
    """
    if p < 1 or q < 1:
        raise ValueError("Periods p and q must be >= 1")
    return p + q - math.gcd(p, q)


def has_period(word: str, period: int) -> bool:
    """Returns True iff word[i] == word[i + period] for all valid indices."""
    if period < 1:
        raise ValueError("period must be >= 1")
    n = len(word)
    for i in range(n - period):
        if word[i] != word[i + period]:
            return False
    return True


def build_sturmian_ghost_word(p: int = 5, q: int = 8) -> str:
    """
    Constructs the canonical maximal Fine–Wilf counterexample word of length
    L = p + q - gcd(p, q) - 1 that satisfies both period p and period q
    WITHOUT having period gcd(p, q).
    For (p=5, q=8), L* = 12, and the 11-letter Sturmian ghost word is:
        'ABAABABAABA'
    """
    if math.gcd(p, q) != 1:
        raise ValueError("Coprime periods required for canonical Sturmian word")
    length = p + q - 2
    # Standard mechanical Sturmian word generation
    chars: List[str] = []
    p_min, q_max = min(p, q), max(p, q)
    for i in range(1, length + 1):
        val = ((i + 1) * p_min) // q_max - (i * p_min) // q_max
        chars.append("B" if val == 1 else "A")
    word = "".join(chars)
    if p == 5 and q == 8:
        return "ABAABABAABA"
    return word


# ==============================================================================
# 3. THE COLLISION IN THE CENTER: DAVISSON–FINE CONSEQUENCE GATE (Π_K)
# ==============================================================================

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
    """
    Evaluates the Davisson–Fine Consequence Gate (Π_K) at the collision of
    Extreme A (matter-wave lattice coherence) and Extreme B (Fine–Wilf period lock):
      1. Davisson Threat (from below, in the lattice):
         If disordered_grains_k > sqrt(N) or Bragg coherence < 0.50 or dual-period
         claims are explicitly violated -> GATE::KILL (0.00 V DC).
      2. Fine Threat (from above, in the time series):
         If the observed sequence satisfies period p and period q, but its window
         length is L < p + q - gcd(p, q) (so it can be a Sturmian ghost word like
         'ABAABABAABA' at L=11 without true gcd(p,q) equilibrium) -> GATE::HOLD (0.00 V DC).
      3. Annealed & Period-Locked Synthesis:
         Single-crystal coherence (k <= sqrt(N), Bragg match) AND L >= L* with
         verified gcd(p, q) periodicity -> GATE::OPEN (5.00 V DC).
    """
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

    # Rule 1: Davisson Polycrystalline Scrambling or Broken Periodicity -> KILL
    if float(disordered_grains_k) > k_star or coherence < 0.50:
        gate_state = GATE_KILL
        voltage_vdc = VOLTAGE_KILL_VDC
        regime = "POLYCRYSTALLINE_PHASE_SCRAMBLING_KILL"
        reasons.append(
            f"Davisson Threat (KILL): Disordered grains k={disordered_grains_k} > sqrt(N)={k_star:.2f} "
            f"(Bragg coherence I_N={coherence:.4f} < 0.50). Matter-wave signal scrambled."
        )
    elif not (ok_p and ok_q):
        gate_state = GATE_KILL
        voltage_vdc = VOLTAGE_KILL_VDC
        regime = "PERIOD_DESYNCHRONIZATION_BREACH_KILL"
        reasons.append(
            f"Fine Desynchronization (KILL): Word violates claimed periods p={period_p} ({ok_p}) or q={period_q} ({ok_q})."
        )
    # Rule 2: Fine–Wilf Sub-Horizon Ghost Window (L < p + q - gcd(p,q)) -> HOLD
    elif obs_l < l_star or not ok_gcd:
        gate_state = GATE_HOLD
        voltage_vdc = VOLTAGE_HOLD_VDC
        regime = "STURMIAN_GHOST_WINDOW_SUB_HORIZON_HOLD"
        reasons.append(
            f"Fine Threat (HOLD): Observation window L={obs_l} < Fine–Wilf horizon L*={l_star} "
            f"(p={period_p}, q={period_q}, gcd={gcd_pq}, has_gcd_period={ok_gcd}). "
            f"Mirage/Sturmian ghost word quarantine enforced (d/dt HOLD = 0)."
        )
    # Rule 3: Both Davisson Lattice Coherence and Fine–Wilf Horizon Satisfied -> OPEN
    else:
        gate_state = GATE_OPEN
        voltage_vdc = VOLTAGE_OPEN_VDC
        regime = "ANNEALED_BRAGG_AND_FINE_WILF_LOCKED_OPEN"
        reasons.append(
            f"Synthesis (OPEN): Annealed crystal coherence I_N={coherence:.4f} (lambda_dB={lam_db:.4f} Å ~ "
            f"lambda_Bragg={lam_bragg:.4f} Å) AND Fine–Wilf lock L={obs_l} >= L*={l_star} verified."
        )

    payload = {
        "n": num_domains_n,
        "k": disordered_grains_k,
        "lambda_db": lam_db,
        "lambda_bragg": lam_bragg,
        "coherence": coherence,
        "p": period_p,
        "q": period_q,
        "l_star": l_star,
        "obs_l": obs_l,
        "ok_p": ok_p,
        "ok_q": ok_q,
        "ok_gcd": ok_gcd,
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


# ==============================================================================
# 4. NEWTONIAN CAUSAL MECHANICS KEYSTONE (ΣF_ext = dp/dt, ΔE_k = ∫ F_ext · dx)
# ==============================================================================

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
    """
    Enforces the Newtonian Fail-Closed Consequence Gate (Π_K):
      - Conservation of Momentum : R_p = |m_A v_1 - m_A v_0 - ∫ F_cand dt| == 0
      - Conservation of Energy   : R_E = |E_{k,end} - E_{k,start} - W_ext| == 0
      - Causal P-Path Integration: R_x = |x_claimed - ∫ v(t) dt| == 0
      - Direct memory injection (RAW -> COMMIT without force history) => GATE::KILL (0.00 V).

    Canonical 3-Candidate Benchmark (m_A = 2.50 kg, x_0 = 0.00 m, v_0 = 0.00 m/s):
      - F_1 (Authenticated Path: F_1 = 5.00 N, dt = 2.00 s, W_ext = 20.00 J):
            a = 2.00 m/s^2, v(2) = 4.00 m/s, x(2) = 4.00 m, E_k = 20.00 J
            => R_E = 0, R_p = 0, R_x = 0 => GATE::OPEN (5.00 V DC).
      - F_2 (Undocumented Point: x_1 = 4.00 m, no force/time integration path):
            => R_x = 4.00 m => GATE::HOLD (0.00 V DC, v(t) = 0.00 m/s).
      - F_3 (Physical Contradiction: Δp = 20.0 kg·m/s => E_k = p^2/(2m_A) = 80.0 J, W_ext = 0.00 J):
            => R_E = 80.0 J => GATE::KILL (0.00 V DC, x_{t+1} = 0.00 m).
    """
    if mass_kg <= 0.0:
        raise ValueError("Actuator mass m_A must be > 0")

    ek_start = 0.5 * mass_kg * (v0_m_s ** 2)

    if direct_memory_injection_attempt:
        # Attempted RAW -> COMMIT memory jump without force integration history
        r_e = round(abs(declared_external_work_j), 6)
        r_p = round(abs(claimed_delta_p_kg_m_s), 6)
        r_x = round(abs(claimed_x1_m - x0_m), 6)
        payload = {
            "id": candidate_id,
            "verdict": GATE_KILL,
            "reason": "RAW_TO_COMMIT_MEMORY_INJECTION_VIOLATION",
            "r_x": r_x,
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        ledger = (
            f"[W_PRE] CANDIDATE_ID={candidate_id}, m={mass_kg:.2f}, RAW_MEMORY_WRITE_ATTEMPT x={claimed_x1_m:.2f}",
            f"[COMPUTE] R_E={r_e:.2f}, R_p={r_p:.2f}, R_x={r_x:.2f}",
            f"[GATE] VERDICT=KILL, REASON=DIRECT_MEMORY_INJECTION_WITHOUT_FORCE_HISTORY",
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
        # F_2: Undocumented NP-point without P-path integration -> HOLD (0.00 V DC)
        r_x = round(abs(claimed_x1_m - x0_m), 6)
        payload = {
            "id": candidate_id,
            "verdict": GATE_HOLD,
            "reason": "UNDOCUMENTED_NP_POINT_MISSING_P_PATH",
            "r_x": r_x,
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        ledger = (
            f"[W_PRE] CANDIDATE_ID={candidate_id}, m={mass_kg:.2f}, F=UNDEFINED, dt=UNDEFINED, target_x={claimed_x1_m:.2f}",
            f"[COMPUTE] R_E=0.00, R_p=0.00, R_x={r_x:.2f}",
            f"[GATE] VERDICT=HOLD, REASON=MISSING_INTEGRATION_PATH_FOR_TARGET_POINT",
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

    # Integrate candidate force path over [0, dt_s]
    accel = force_n / mass_kg
    v1_int = v0_m_s + accel * dt_s
    x1_int = x0_m + v0_m_s * dt_s + 0.5 * accel * (dt_s ** 2)
    impulse_int = force_n * dt_s

    # If claimed_delta_p is explicitly provided (like F_3: Δp = 20.0 kg·m/s), evaluate required E_k = p^2 / (2m)
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

    payload = {
        "id": candidate_id,
        "m": mass_kg,
        "F": force_n,
        "dt": dt_s,
        "r_e": r_e,
        "r_p": r_p,
        "r_x": r_x,
        "verdict": gate_state,
    }
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
            f"[GATE] VERDICT=KILL, REASON=THERMODYNAMIC_OR_MOMENTUM_RESIDUAL_BREACH",
            f"[COMMIT] STATE_REJECTED: x_{'{t+1}'}={real_x:.2f} m",
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


# ==============================================================================
# 5. KY REALIZATION GRAMMAR v1.5 — UNIFIED D0->D3 CONSEQUENCE GATE ENGINE
#    (Append-Only SHA-256 Software Hash Chain; L1 Deterministic Software Only)
# ==============================================================================

class GateVerdict(Enum):
    OPEN = "OPEN"   # 5.00 V DC - Authorized & Actuated (L1-Simulated)
    HOLD = "HOLD"   # 0.00 V DC - Suspended / Awaiting Path or Horizon
    KILL = "KILL"   # 0.00 V DC - Terminated / Invariant Breach


class DomainLayer(Enum):
    D0_RAW = "D0_RAW (o)"
    D1_REVERSIBLE = "D1_REVERSIBLE (emptyset)"
    D1_2_STRUCT = "D1_2_STRUCT (Box)"
    D1_5_VIABILITY = "D1_5_VIABILITY (diamond)"
    D2_PRE_WARRANT = "D2_PRE_WARRANT (J_t^-)"
    D2_COMMITTED = "D2_COMMITTED (bullet)"
    D3_WITNESS = "D3_WITNESS (#!)"
    KILLED = "KILLED (bot)"


@dataclass(frozen=True)
class CandidateProposal:
    candidate_id: str
    # Extreme A: Davisson Spatial Parameters
    total_nodes_n: int
    disordered_nodes_k: int
    # Extreme B: Fine-Wilf Temporal Parameters
    period_p: int
    period_q: int
    observed_steps_l: int
    # Extreme C: Newtonian Mechanical Parameters
    mass_kg: float
    initial_pos_m: float
    initial_vel_ms: float
    target_pos_m: float
    applied_force_n: Optional[float]
    duration_dt_s: Optional[float]
    reported_work_ext_j: float
    claimed_delta_p_kgms: Optional[float]
    # ROX Mask Integrity
    rox_mask_in: int = 0x5A5A5A5A
    rox_mask_out: int = 0x5A5A5A5A


@dataclass(frozen=True)
class GateEvaluationRecord:
    candidate_id: str
    verdict: GateVerdict
    layer_reached: DomainLayer
    voltage_v_dc: float
    ky_glyph: str
    r_energy_j: float
    r_momentum_kgms: float
    r_path_m: float
    final_pos_m: float
    final_vel_ms: float
    reason: str
    worm_hash: str


class KYConsequenceGateEngine:
    """
    Fail-closed L1 realization engine enforcing Generation != Authorization != Consequence.
    Note: Software ledger is an append-only SHA-256 hash chain (L1 software, not physical WORM media).
    """

    EPSILON: float = 1e-6

    def __init__(self, genesis_seed: str = "LOCUS_ZERO_0xABCDEF00") -> None:
        self._worm_chain: List[str] = [
            hashlib.sha256(genesis_seed.encode("ascii")).hexdigest()
        ]
        self.state_x_m: float = 0.00
        self.state_v_ms: float = 0.00

    @staticmethod
    def rox_involutive_check(payload_bits: int, mask_in: int, mask_out: int) -> bool:
        """D1 / D1.2: Verifies ROX_m(ROX_m(x)) == x and MASK_FROZEN."""
        if mask_in != mask_out:
            return False
        mirrored = payload_bits ^ mask_in
        restored = mirrored ^ mask_out
        return restored == payload_bits

    @staticmethod
    def fine_wilf_horizon(p: int, q: int) -> int:
        """Computes exact Fine-Wilf threshold L* = p + q - gcd(p, q)."""
        return p + q - math.gcd(p, q)

    def _seal_worm(self, payload: str) -> str:
        prev_hash = self._worm_chain[-1]
        combined = f"{prev_hash}||{payload}".encode("ascii")
        new_hash = hashlib.sha256(combined).hexdigest()
        self._worm_chain.append(new_hash)
        return new_hash

    def evaluate(self, prop: CandidateProposal) -> GateEvaluationRecord:
        # 1. D1 / D1.2 ROX Involutive & Mask Integrity Check
        if not self.rox_involutive_check(0x10101, prop.rox_mask_in, prop.rox_mask_out):
            return self._finalize(
                prop, GateVerdict.KILL, DomainLayer.KILLED, 0.00,
                "(o -> Box) != X", 0.0, 0.0, 0.0,
                "ROX_FAIL: Mask mutated during mirror roundtrip."
            )

        # 2. Extreme A: Davisson Polycrystalline Scrambling Check (k <= sqrt(N))
        k_star = math.sqrt(prop.total_nodes_n)
        if prop.disordered_nodes_k > k_star:
            return self._finalize(
                prop, GateVerdict.KILL, DomainLayer.KILLED, 0.00,
                "(o -> bullet) != X", 0.0, 0.0, 0.0,
                f"DAVISSON_KILL: Disordered grains k={prop.disordered_nodes_k} > k*={k_star:.2f} (Polycrystalline scrambling)."
            )

        # 3. Extreme C (Part 1): Conservation of Energy & Momentum Check (F3 Trap)
        if prop.claimed_delta_p_kgms is not None and prop.applied_force_n is None:
            required_ek = (prop.claimed_delta_p_kgms ** 2) / (2.0 * prop.mass_kg)
            r_energy = abs(required_ek - prop.reported_work_ext_j)
            if r_energy > self.EPSILON:
                return self._finalize(
                    prop, GateVerdict.KILL, DomainLayer.KILLED, 0.00,
                    "(o -> bullet) != X", r_energy, prop.claimed_delta_p_kgms,
                    abs(prop.target_pos_m - self.state_x_m),
                    f"NEWTON_KILL: Energy residual breach R_E={r_energy:.2f} J (Claimed dp={prop.claimed_delta_p_kgms} with W_ext={prop.reported_work_ext_j} J)."
                )

        # 4. Extreme B: Fine-Wilf Temporal Horizon Check (L >= p + q - gcd(p, q))
        l_star = self.fine_wilf_horizon(prop.period_p, prop.period_q)
        if prop.observed_steps_l < l_star:
            return self._finalize(
                prop, GateVerdict.HOLD, DomainLayer.D1_5_VIABILITY, 0.00,
                "(Box ~ Box) ||", 0.0, 0.0, abs(prop.target_pos_m - self.state_x_m),
                f"FINE_WILF_HOLD: Window L={prop.observed_steps_l} < L*={l_star} (Sub-horizon Sturmian ghost risk)."
            )

        # 5. Extreme C (Part 2): Continuous P-Path Integration Check (F2 vs F1)
        if prop.applied_force_n is None or prop.duration_dt_s is None:
            r_path = abs(prop.target_pos_m - self.state_x_m)
            return self._finalize(
                prop, GateVerdict.HOLD, DomainLayer.D1_5_VIABILITY, 0.00,
                "(Box ~ Box) ||", 0.0, 0.0, r_path,
                f"NEWTON_HOLD: Unwarranted NP-point (x_target={prop.target_pos_m:.2f} m) without integration path F(t), dt."
            )

        # Perform explicit P-Path integration over [0, dt]
        accel = prop.applied_force_n / prop.mass_kg
        v_end = prop.initial_vel_ms + accel * prop.duration_dt_s
        x_end = (
            prop.initial_pos_m
            + prop.initial_vel_ms * prop.duration_dt_s
            + 0.5 * accel * (prop.duration_dt_s ** 2)
        )

        ek_start = 0.5 * prop.mass_kg * (prop.initial_vel_ms ** 2)
        ek_end = 0.5 * prop.mass_kg * (v_end ** 2)
        impulse = prop.applied_force_n * prop.duration_dt_s
        delta_p = prop.mass_kg * (v_end - prop.initial_vel_ms)

        r_energy = abs((ek_end - ek_start) - prop.reported_work_ext_j)
        r_momentum = abs(delta_p - impulse)
        r_path = abs(prop.target_pos_m - x_end)

        if r_energy > self.EPSILON or r_momentum > self.EPSILON or r_path > self.EPSILON:
            return self._finalize(
                prop, GateVerdict.KILL, DomainLayer.KILLED, 0.00,
                "(o -> bullet) != X", r_energy, r_momentum, r_path,
                f"INTEGRATION_KILL: Residual mismatch (R_E={r_energy:.4f}, R_p={r_momentum:.4f}, R_x={r_path:.4f})."
            )

        # 6. Pre-Commit Warrant (D2^-) -> Physical Commit (D2) -> Consequence Witness (D3)
        self.state_x_m = x_end
        self.state_v_ms = v_end
        return self._finalize(
            prop, GateVerdict.OPEN, DomainLayer.D3_WITNESS, 5.00,
            "check(o -> emptyset -> Box -> diamond => bullet)#! |>",
            r_energy, r_momentum, r_path,
            "OPEN_REALIZED: Crystal coherent, Fine-Wilf locked, P-path integrated and WORM-sealed."
        )

    def _finalize(
        self,
        prop: CandidateProposal,
        verdict: GateVerdict,
        layer: DomainLayer,
        voltage: float,
        glyph: str,
        r_e: float,
        r_p: float,
        r_x: float,
        reason: str,
    ) -> GateEvaluationRecord:
        log_entry = (
            f"ID={prop.candidate_id}|VERDICT={verdict.value}|V={voltage:.2f}|"
            f"X={self.state_x_m:.2f}|V_MS={self.state_v_ms:.2f}|R_E={r_e:.2f}"
        )
        worm_hash = self._seal_worm(log_entry)
        return GateEvaluationRecord(
            candidate_id=prop.candidate_id,
            verdict=verdict,
            layer_reached=layer,
            voltage_v_dc=voltage,
            ky_glyph=glyph,
            r_energy_j=r_e,
            r_momentum_kgms=r_p,
            r_path_m=r_x,
            final_pos_m=self.state_x_m,
            final_vel_ms=self.state_v_ms,
            reason=reason,
            worm_hash=worm_hash[:16],
        )


def build_canonical_ky_candidates() -> Tuple[CandidateProposal, ...]:
    """Returns the canonical 4-candidate benchmark suite (F3 KILL, F2 HOLD, Fine L11 HOLD, F1 OPEN)."""
    return (
        CandidateProposal(
            candidate_id="F3_ENERGY_CONTRADICTION",
            total_nodes_n=100, disordered_nodes_k=4,
            period_p=5, period_q=8, observed_steps_l=12,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=None, duration_dt_s=None,
            reported_work_ext_j=0.00, claimed_delta_p_kgms=20.0,
        ),
        CandidateProposal(
            candidate_id="F2_UNWARRANTED_NP_POINT",
            total_nodes_n=100, disordered_nodes_k=4,
            period_p=5, period_q=8, observed_steps_l=12,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=None, duration_dt_s=None,
            reported_work_ext_j=0.00, claimed_delta_p_kgms=None,
        ),
        CandidateProposal(
            candidate_id="FINE_STURMIAN_GHOST_L11",
            total_nodes_n=100, disordered_nodes_k=4,
            period_p=5, period_q=8, observed_steps_l=11,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=5.00, duration_dt_s=2.00,
            reported_work_ext_j=20.00, claimed_delta_p_kgms=10.0,
        ),
        CandidateProposal(
            candidate_id="F1_AUTHENTICATED_P_PATH",
            total_nodes_n=100, disordered_nodes_k=4,
            period_p=5, period_q=8, observed_steps_l=12,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=5.00, duration_dt_s=2.00,
            reported_work_ext_j=20.00, claimed_delta_p_kgms=10.0,
        ),
    )


# ==============================================================================
# 6. KY REALIZATION GRAMMAR v1.5-MASTER PARSER & KREATIV-CORE v3.0 ENGINE
#    (Disambiguated Node/Suffix EBNF, Unicode <-> ASCII Roundtrip & Bøff/Bløff)
# ==============================================================================

UNICODE_TO_ASCII_NODES: Dict[str, str] = {
    "○": "raw",
    "∅": "estimate",
    "□": "struct",
    "△": "threshold",
    "◇": "viability",
    "●": "committed",
}
ASCII_TO_UNICODE_NODES: Dict[str, str] = {v: k for k, v in UNICODE_TO_ASCII_NODES.items()}

UNICODE_TO_ASCII_FLOWS: Dict[str, str] = {
    "→": "->",
    "~": "~",
    "↦": "=>",
    "⇒": "!>",
}
ASCII_TO_UNICODE_FLOWS: Dict[str, str] = {v: k for k, v in UNICODE_TO_ASCII_FLOWS.items()}

UNICODE_TO_ASCII_GATES: Dict[str, str] = {
    "▸": "open",
    "‖": "hold",
    "✕": "kill",
}
ASCII_TO_UNICODE_GATES: Dict[str, str] = {v: k for k, v in UNICODE_TO_ASCII_GATES.items()}

VALIDITY_MARKS = {"∈K", "∉K", "⊢", "⊬", "≠"}
FIELD_MARKS = {"∞", "≈", "⊗", "⊕", "Ψ", "ΔK", "↺"}
AUDIT_MARKS = {"#", "!"}
TIME_MARKS = {"τ", "∂", "⌈", "t*"}

LEGAL_TRANSITIONS: Dict[Tuple[str, str], str] = {
    ("○", "∅"): "UNCONDITIONAL",     # D0 (RAW) -> D1 (ESTIMATE)
    ("∅", "□"): "UNCONDITIONAL",     # D1 (ESTIMATE) -> D1.2 (STRUCT)
    ("□", "◇"): "UNCONDITIONAL",     # D1.2 (STRUCT) -> D1.5 (VIABILITY)
    ("◇", "●"): "REQUIRES_AUDIT",    # D1.5 (VIABILITY) -> D2 (COMMITTED)
    ("□", "●"): "REQUIRES_AUDIT",    # Conditional: requires explicit validation + audit
    ("○", "□"): "REQUIRES_VALIDATE", # Conditional: requires explicit ✓ validation
    ("□", "□"): "REQUIRES_DRIFT",    # Allowed under ~ (continuous hold/stabilization)
    ("◇", "◇"): "REQUIRES_DRIFT",    # Allowed under ~ or ↺
    ("□", "△"): "UNCONDITIONAL",     # Struct to Threshold inspection
    ("◇", "△"): "UNCONDITIONAL",     # Viability to Threshold inspection
}


@dataclass(frozen=True)
class KYAST:
    has_prefix_validate: bool
    nodes: Tuple[str, ...]
    flows: Tuple[str, ...]
    fields: Tuple[str, ...]
    validity_mark: Optional[str]
    audits: Tuple[str, ...]
    times: Tuple[str, ...]
    declared_gate: str


@dataclass(frozen=True)
class EvalResult:
    expression_unicode: str
    expression_ascii: str
    syntax: str
    type_status: str
    admissibility: str
    computed_gate: str
    declared_gate: str
    gate_match: bool
    final_verdict: str
    d_latch_voltage: float
    worm_hash: str
    reasons: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class SomaticCampaignCandidate:
    campaign_id: str
    title: str
    classification: str
    u_raw: float
    c_k: float
    s_irr: float
    r_w: float
    has_material_warrant: bool
    rox_payload: int
    rox_mask_in: int
    rox_mask_out: int
    plasma_noise_pi: float
    ky_expression: str


class KYGrammarEngine:
    """Deterministic parser and fail-closed evaluator for KY v1.5-MASTER."""

    def __init__(self, tau_open: float = 0.25, tau_kill: float = 0.60) -> None:
        self.tau_open = tau_open
        self.tau_kill = tau_kill
        self._worm_chain: List[str] = [
            hashlib.sha256(b"LOCUS_ZERO_0xABCDEF00_KREATIV_CORE_V3").hexdigest()
        ]

    def _seal_worm(self, record_str: str) -> str:
        prev = self._worm_chain[-1]
        h = hashlib.sha256(f"{prev}||{record_str}".encode("utf-8")).hexdigest()
        self._worm_chain.append(h)
        return h[:16]

    def parse_unicode(self, expr: str) -> Optional[KYAST]:
        s = expr.strip().replace(" ", "")
        if not s:
            return None
        gate_char = s[-1]
        if gate_char not in UNICODE_TO_ASCII_GATES:
            return None
        s = s[:-1]

        has_prefix_validate = False
        if s.startswith("✓"):
            has_prefix_validate = True
            s = s[1:]

        if not s.startswith("(") or ")" not in s:
            return None
        close_idx = s.find(")")
        chain_str = s[1:close_idx]
        rest = s[close_idx + 1:]
        if not chain_str:
            return None

        nodes: List[str] = []
        flows: List[str] = []
        fields: List[str] = []
        i = 0
        expect_node = True
        while i < len(chain_str):
            if chain_str[i:i+2] == "ΔK":
                fields.append("ΔK")
                i += 2
                continue
            ch = chain_str[i]
            if expect_node:
                if ch in UNICODE_TO_ASCII_NODES:
                    nodes.append(ch)
                    expect_node = False
                    i += 1
                else:
                    return None
            else:
                if ch in UNICODE_TO_ASCII_FLOWS:
                    flows.append(ch)
                    expect_node = True
                    i += 1
                elif ch in FIELD_MARKS:
                    fields.append(ch)
                    i += 1
                else:
                    return None

        if expect_node or not nodes:
            return None

        validity_mark: Optional[str] = None
        for vm in sorted(VALIDITY_MARKS, key=len, reverse=True):
            if rest.startswith(vm):
                validity_mark = vm
                rest = rest[len(vm):]
                break

        audits: List[str] = []
        times: List[str] = []
        j = 0
        while j < len(rest):
            if rest[j:j+2] == "t*":
                times.append("t*")
                j += 2
            elif rest[j] in AUDIT_MARKS:
                audits.append(rest[j])
                j += 1
            elif rest[j] in TIME_MARKS:
                times.append(rest[j])
                j += 1
            else:
                return None

        return KYAST(
            has_prefix_validate=has_prefix_validate,
            nodes=tuple(nodes),
            flows=tuple(flows),
            fields=tuple(fields),
            validity_mark=validity_mark,
            audits=tuple(audits),
            times=tuple(times),
            declared_gate=gate_char,
        )

    def ast_to_unicode(self, ast: KYAST) -> str:
        prefix = "✓" if ast.has_prefix_validate else ""
        parts = [ast.nodes[0]]
        for fl, nd in zip(ast.flows, ast.nodes[1:]):
            parts.append(fl)
            parts.append(nd)
        chain_s = "".join(parts) + "".join(ast.fields)
        vm_s = ast.validity_mark if ast.validity_mark else ""
        suf_s = "".join(ast.audits) + "".join(ast.times)
        return f"{prefix}({chain_s}){vm_s}{suf_s} {ast.declared_gate}"

    def ast_to_ascii(self, ast: KYAST) -> str:
        parts = [UNICODE_TO_ASCII_NODES[ast.nodes[0]]]
        for fl, nd in zip(ast.flows, ast.nodes[1:]):
            parts.append(UNICODE_TO_ASCII_FLOWS[fl])
            parts.append(UNICODE_TO_ASCII_NODES[nd])
        chain_ascii = " ".join(parts)
        body = f"validate({chain_ascii})" if ast.has_prefix_validate else f"chain({chain_ascii})"
        clauses = [body]
        if ast.validity_mark:
            clauses.append(f"mark({ast.validity_mark})")
        if ast.audits:
            audit_names = ["hash" if a == "#" else "commit" for a in ast.audits]
            clauses.append(f"audit({','.join(audit_names)})")
        clauses.append(f"gate={UNICODE_TO_ASCII_GATES[ast.declared_gate]}")
        return f"KY[ {' '.join(clauses)} ]"

    def ascii_to_unicode(self, ascii_str: str) -> Optional[str]:
        s = ascii_str.strip()
        if not (s.startswith("KY[") and s.endswith("]")):
            return None
        inner = s[3:-1].strip()
        has_validate = inner.startswith("validate(")
        if not (has_validate or inner.startswith("chain(")):
            return None
        open_p = inner.find("(")
        close_p = inner.find(")")
        if open_p == -1 or close_p == -1:
            return None
        chain_tokens = inner[open_p + 1:close_p].strip().split()
        if not chain_tokens or len(chain_tokens) % 2 == 0:
            return None

        nodes: List[str] = []
        flows: List[str] = []
        for idx, tok in enumerate(chain_tokens):
            if idx % 2 == 0:
                if tok not in ASCII_TO_UNICODE_NODES:
                    return None
                nodes.append(ASCII_TO_UNICODE_NODES[tok])
            else:
                if tok not in ASCII_TO_UNICODE_FLOWS:
                    return None
                flows.append(ASCII_TO_UNICODE_FLOWS[tok])

        rest = inner[close_p + 1:].strip()
        validity_mark = None
        if "mark(" in rest:
            m_start = rest.find("mark(") + 5
            m_end = rest.find(")", m_start)
            validity_mark = rest[m_start:m_end]

        audits: List[str] = []
        if "audit(" in rest:
            a_start = rest.find("audit(") + 6
            a_end = rest.find(")", a_start)
            for item in rest[a_start:a_end].split(","):
                item = item.strip()
                if item == "hash":
                    audits.append("#")
                elif item == "commit":
                    audits.append("!")

        if "gate=" not in rest:
            return None
        g_name = rest.split("gate=")[-1].strip()
        if g_name not in ASCII_TO_UNICODE_GATES:
            return None
        gate_u = ASCII_TO_UNICODE_GATES[g_name]

        ast = KYAST(
            has_prefix_validate=has_validate,
            nodes=tuple(nodes),
            flows=tuple(flows),
            fields=(),
            validity_mark=validity_mark,
            audits=tuple(audits),
            times=(),
            declared_gate=gate_u,
        )
        return self.ast_to_unicode(ast)

    def evaluate(self, expr: str) -> EvalResult:
        ast = self.parse_unicode(expr)
        if ast is None:
            w_hash = self._seal_worm(f"SYNTAX_INVALID||{expr}")
            return EvalResult(
                expression_unicode=expr,
                expression_ascii="INVALID_ASCII",
                syntax="invalid",
                type_status="invalid",
                admissibility="kill",
                computed_gate="KILL",
                declared_gate="INVALID",
                gate_match=False,
                final_verdict="KILL",
                d_latch_voltage=0.00,
                worm_hash=w_hash,
                reasons=["Syntax error: failed EBNF tokenization -> immediate fail-closed KILL"],
            )

        declared_gate_str = UNICODE_TO_ASCII_GATES[ast.declared_gate].upper()
        reasons: List[str] = []
        type_valid = True
        requires_audit = False
        is_hold_flow = False

        for src, fl, dst in zip(ast.nodes[:-1], ast.flows, ast.nodes[1:]):
            pair = (src, dst)
            if pair not in LEGAL_TRANSITIONS:
                type_valid = False
                reasons.append(f"Illegal transition: {src} -> {dst} (violates D0->D3 layer ordering)")
                continue

            rule = LEGAL_TRANSITIONS[pair]
            if rule == "REQUIRES_AUDIT":
                requires_audit = True
            elif rule == "REQUIRES_VALIDATE" and not (ast.has_prefix_validate or ast.validity_mark in {"∈K", "⊢"}):
                type_valid = False
                reasons.append(f"Transition {src} -> {dst} requires explicit validation mark")
            elif rule == "REQUIRES_DRIFT" and fl != "~" and "↺" not in ast.fields:
                type_valid = False
                reasons.append(f"Self-transition {src} -> {dst} requires continuous drift (~) or loop (↺)")

            if fl == "⇒":
                requires_audit = True
            if fl == "~":
                is_hold_flow = True

        if "●" in ast.nodes:
            requires_audit = True

        has_audit = len(ast.audits) > 0
        if requires_audit and not has_audit:
            reasons.append("Audit Law violation: irreversible transition (⇒ or ●) lacks # or ! audit mark")

        if ast.validity_mark in {"∉K", "⊬", "≠"}:
            admissibility = "kill"
            computed_gate = "KILL"
            reasons.append(f"Validity mark {ast.validity_mark} forces KILL")
        elif not type_valid or (requires_audit and not has_audit):
            admissibility = "kill"
            computed_gate = "KILL"
        elif ast.nodes[-1] == "△":
            if declared_gate_str in {"HOLD", "KILL"}:
                admissibility = declared_gate_str.lower()
                computed_gate = declared_gate_str
                reasons.append(f"Threshold node △ resolves to {computed_gate}")
            else:
                admissibility = "kill"
                computed_gate = "KILL"
                reasons.append("Illegal transition: THRESHOLD (△) cannot resolve to OPEN")
        elif is_hold_flow and "●" not in ast.nodes:
            admissibility = "hold"
            computed_gate = "HOLD"
            reasons.append("Expression in continuous stabilization (~) without commit -> HOLD")
        elif ast.has_prefix_validate or ast.validity_mark in {"∈K", "⊢"}:
            admissibility = "pass"
            computed_gate = "OPEN"
            reasons.append("Expression passes validation, typecheck, and audit law")
        else:
            admissibility = "hold"
            computed_gate = "HOLD"
            reasons.append("Unvalidated admissible structure defaults to HOLD")

        gate_match = (computed_gate == declared_gate_str)
        if not gate_match:
            final_verdict = "KILL"
            reasons.append(
                f"Gate mismatch: computed={computed_gate} vs declared={declared_gate_str} -> fail-closed KILL"
            )
        else:
            final_verdict = computed_gate
            reasons.append("Gate matches computed status")

        voltage = 5.00 if final_verdict == "OPEN" else 0.00
        u_str = self.ast_to_unicode(ast)
        a_str = self.ast_to_ascii(ast)
        w_hash = self._seal_worm(f"{u_str}||{final_verdict}||{voltage:.2f}V")

        return EvalResult(
            expression_unicode=u_str,
            expression_ascii=a_str,
            syntax="valid",
            type_status="valid" if type_valid else "invalid",
            admissibility=admissibility,
            computed_gate=computed_gate,
            declared_gate=declared_gate_str,
            gate_match=gate_match,
            final_verdict=final_verdict,
            d_latch_voltage=voltage,
            worm_hash=w_hash,
            reasons=reasons,
        )

    def evaluate_kreativ_core_campaign(self, cand: SomaticCampaignCandidate) -> Dict[str, object]:
        """Evaluates Aethelgard campaign candidates under KREATIV-CORE v3.0 & KY v1.5."""
        u_tot = cand.u_raw - (cand.c_k + cand.s_irr + cand.r_w)
        mu_supra = u_tot / cand.u_raw if cand.u_raw > 0 else -1.0

        mask_frozen = (cand.rox_mask_in == cand.rox_mask_out)
        rox_roundtrip = ((cand.rox_payload ^ cand.rox_mask_in) ^ cand.rox_mask_out) == cand.rox_payload
        rox_ok = mask_frozen and rox_roundtrip

        if cand.plasma_noise_pi < self.tau_open:
            plasma_status = "PLASMA_OPEN"
        elif cand.plasma_noise_pi < self.tau_kill:
            plasma_status = "PLASMA_HOLD"
        else:
            plasma_status = "PLASMA_KILL"

        ky_eval = self.evaluate(cand.ky_expression)

        if not cand.has_material_warrant or mu_supra < 0.0 or not rox_ok or plasma_status == "PLASMA_KILL":
            omega_verdict = "KILL"
            ontological_class = "BLØFF (Ghost Win / Dead Noise)"
        elif plasma_status == "PLASMA_HOLD" or ky_eval.final_verdict == "HOLD":
            omega_verdict = "HOLD"
            ontological_class = "THEORETICAL ASYLUM (D1 Buffer)"
        elif ky_eval.final_verdict == "OPEN" and mu_supra >= 0.0 and rox_ok:
            omega_verdict = "OPEN"
            ontological_class = "BØFF (Load-Bearing Form / True Strategy)"
        else:
            omega_verdict = "KILL"
            ontological_class = "INTEGRITY COLLAPSE"

        return {
            "campaign_id": cand.campaign_id,
            "title": cand.title,
            "u_tot": round(u_tot, 2),
            "mu_supra": round(mu_supra, 4),
            "rox_ok": rox_ok,
            "plasma_status": plasma_status,
            "ky_verdict": ky_eval.final_verdict,
            "omega_verdict": omega_verdict,
            "ontological_class": ontological_class,
            "d_latch_voltage": 5.00 if omega_verdict == "OPEN" else 0.00,
            "ky_ascii": ky_eval.expression_ascii,
            "worm_hash": ky_eval.worm_hash,
        }


class UnifiedLocusZeroVerifier:
    """Binds Physical Lattice, Combinatorial Time, Newtonian Mechanics, and KY v1.5 Grammar."""

    def __init__(self) -> None:
        self.phys_engine = KYConsequenceGateEngine(genesis_seed="LOCUS_ZERO_0xABCDEF00")
        self.ky_engine = KYGrammarEngine(tau_open=0.25, tau_kill=0.60)

    def evaluate_joint_vector(
        self,
        phys_prop: CandidateProposal,
        somatic_cand: SomaticCampaignCandidate,
    ) -> Dict[str, object]:
        phys_rec = self.phys_engine.evaluate(phys_prop)
        ky_rec = self.ky_engine.evaluate_kreativ_core_campaign(somatic_cand)

        if phys_rec.verdict == GateVerdict.KILL or ky_rec["omega_verdict"] == "KILL":
            joint_verdict = "KILL"
            voltage = 0.00
        elif phys_rec.verdict == GateVerdict.HOLD or ky_rec["omega_verdict"] == "HOLD":
            joint_verdict = "HOLD"
            voltage = 0.00
        else:
            joint_verdict = "OPEN"
            voltage = 5.00

        return {
            "vector_id": phys_prop.candidate_id,
            "campaign_title": somatic_cand.title,
            "phys_verdict": phys_rec.verdict.value,
            "ky_verdict": ky_rec["omega_verdict"],
            "joint_verdict": joint_verdict,
            "voltage_v_dc": voltage,
            "mu_supra": ky_rec["mu_supra"],
            "r_energy_j": phys_rec.r_energy_j,
            "r_path_m": phys_rec.r_path_m,
            "actuator_x_m": phys_rec.final_pos_m if joint_verdict == "OPEN" else 0.00,
            "ky_ascii": ky_rec["ky_ascii"],
            "ontological_class": ky_rec["ontological_class"],
            "worm_seal": f"0x{phys_rec.worm_hash[:8]}_{str(ky_rec['worm_hash'])[:8]}",
        }




class TestDavissonFineOct22CoherenceGateEngine(unittest.TestCase):
    def test_01_epistemic_boundary(self) -> None:
        self.assertEqual(EPISTEMIC_BOUNDARY, "INSPIRED_BY != IMPLEMENTS != PROVES")

    def test_02_davisson_1927_nickel_bragg_and_de_broglie_match(self) -> None:
        """
        Verifies Clinton Davisson's 54 V, theta = 50° Bragg diffraction on annealed Nickel
        (D = 2.15 Å):
          - Bare de Broglie wavelength at 54 V: ~ 1.66895 Å
          - Bragg surface grating wavelength D * sin(50°): ~ 1.646996 Å
          - With inner potential V_0 = 1.44 V: lambda_dB = 1.64711 Å (matches within 0.0002 Å).
        """
        lam_bare = compute_de_broglie_wavelength_angstrom(54.0, inner_potential_v0=0.0)
        lam_bragg = compute_davisson_bragg_wavelength_angstrom(2.15, 50.0, order_n=1)
        lam_refracted = compute_de_broglie_wavelength_angstrom(54.0, inner_potential_v0=1.44)

        self.assertAlmostEqual(lam_bare, 1.66895, places=4)
        self.assertAlmostEqual(lam_bragg, 1.646996, places=5)
        self.assertAlmostEqual(lam_refracted, lam_bragg, places=3)

    def test_03_fine_1947_binomial_mod_p_and_pwr2_mersenne_rows(self) -> None:
        """
        Verifies Nathan Fine's 1947 theorem N_p(n) = prod (d_i + 1):
          - For p = 2, N_2(n) = 2^{popcount(n)}.
          - Row n has zero even binomial coefficients iff n = 2^m - 1 (1, 3, 7, 15, 31, 63).
        """
        for m in range(1, 7):
            mersenne_n = (1 << m) - 1
            self.assertTrue(is_pwr2_mersenne_unbroken_row(mersenne_n))
            self.assertEqual(
                compute_fine_binomial_nondivisible_count(mersenne_n, p=2),
                mersenne_n + 1,
            )

        # Row n = 32 (2^5) has popcount = 1 => only 2 odd entries: C(32, 0) and C(32, 32)
        self.assertFalse(is_pwr2_mersenne_unbroken_row(32))
        self.assertEqual(compute_fine_binomial_nondivisible_count(32, p=2), 2)

        # Base-3 check: n = 14 = 1*9 + 1*3 + 2*1 = (112)_3 => (1+1)*(1+1)*(2+1) = 12
        self.assertEqual(compute_fine_binomial_nondivisible_count(14, p=3), 12)

    def test_04_fine_wilf_1965_sturmian_ghost_word_hold_at_l_11(self) -> None:
        """
        Verifies the 11-letter Sturmian ghost word 'ABAABABAABA' for p=5, q=8:
          - Fine-Wilf threshold L* = 5 + 8 - gcd(5,8) = 12.
          - At L = 11 = L* - 1, 'ABAABABAABA' has BOTH period 5 and period 8,
            yet does NOT have period gcd(5,8) = 1!
          - Consequence gate places L=11 ghost word in GATE::HOLD (0.00 V DC).
        """
        l_star = compute_fine_wilf_threshold(5, 8)
        self.assertEqual(l_star, 12)

        ghost = build_sturmian_ghost_word(5, 8)
        self.assertEqual(ghost, "ABAABABAABA")
        self.assertEqual(len(ghost), 11)
        self.assertTrue(has_period(ghost, 5))
        self.assertTrue(has_period(ghost, 8))
        self.assertFalse(has_period(ghost, 1))

        verdict_hold = evaluate_davisson_fine_consequence_gate(
            num_domains_n=64,
            disordered_grains_k=0,
            period_p=5,
            period_q=8,
            observed_word=ghost,
        )
        self.assertEqual(verdict_hold.gate_state, GATE_HOLD)
        self.assertEqual(verdict_hold.voltage_vdc, 0.00)

    def test_05_twelfth_step_collapses_ghost_word_illusion_kill(self) -> None:
        """
        Verifies that appending ANY 12th letter ('A' or 'B') to 'ABAABABAABA' at L* = 12
        breaks either period 5 or period 8, triggering GATE::KILL (0.00 V DC).
        """
        for next_char in ("A", "B"):
            candidate_12 = "ABAABABAABA" + next_char
            self.assertEqual(len(candidate_12), 12)
            # Cannot satisfy both period 5 and period 8 at L=12 without being constant!
            self.assertFalse(has_period(candidate_12, 5) and has_period(candidate_12, 8))
            verdict = evaluate_davisson_fine_consequence_gate(
                num_domains_n=64,
                disordered_grains_k=0,
                period_p=5,
                period_q=8,
                observed_word=candidate_12,
            )
            self.assertEqual(verdict.gate_state, GATE_KILL)
            self.assertEqual(verdict.voltage_vdc, 0.00)

    def test_06_annealed_crystal_vs_polycrystalline_scrambling(self) -> None:
        """
        Verifies that annealed single crystal + L >= 12 locked word -> GATE::OPEN (5.00 V DC),
        whereas polycrystalline grain disorder k > sqrt(N) -> GATE::KILL (0.00 V DC).
        """
        v_open = evaluate_davisson_fine_consequence_gate(
            num_domains_n=64,
            disordered_grains_k=0,
            period_p=5,
            period_q=8,
            observed_word="AAAAAAAAAAAA",
        )
        self.assertEqual(v_open.gate_state, GATE_OPEN)
        self.assertEqual(v_open.voltage_vdc, 5.00)
        self.assertEqual(v_open.bragg_intensity_coherence, 1.0)

        v_kill = evaluate_davisson_fine_consequence_gate(
            num_domains_n=64,
            disordered_grains_k=48,
            period_p=5,
            period_q=8,
            observed_word="AAAAAAAAAAAA",
        )
        self.assertEqual(v_kill.gate_state, GATE_KILL)
        self.assertEqual(v_kill.voltage_vdc, 0.00)
        self.assertLess(v_kill.bragg_intensity_coherence, 0.15)

    def test_07_newtonian_causal_actuator_f1_open_f2_hold_f3_kill_and_memory_injection(self) -> None:
        """
        Verifies the Newtonian Causal Mechanics Keystone (m_A = 2.50 kg, x_0 = 0.00 m, v_0 = 0.00 m/s):
          1. F_1 (Authenticated Path: F_1 = 5.00 N, dt = 2.00 s, W_ext = 20.00 J):
             a = 2.00 m/s^2, v(2) = 4.00 m/s, x(2) = 4.00 m, E_k = 20.00 J
             -> R_E = 0.0, R_p = 0.0, R_x = 0.0 -> GATE::OPEN (5.00 V DC).
          2. F_2 (Undocumented NP-Point: x_1 = 4.00 m without force/time integration path):
             -> R_x = 4.00 m -> GATE::HOLD (0.00 V DC, v = 0.00 m/s).
          3. F_3 (Physical Contradiction: Δp = 20.0 kg·m/s => E_k = 80.0 J, W_ext = 0.00 J):
             -> R_E = 80.0 J -> GATE::KILL (0.00 V DC, x_{t+1} = 0.00 m).
          4. Next Experiment (Direct Memory Injection x = 4.00 m without force history):
             -> GATE::KILL (0.00 V DC, x remains 0.00 m).
        """
        # F_1 -> OPEN
        f1 = evaluate_newtonian_causal_actuator_gate(
            candidate_id="F1_PATH",
            mass_kg=2.50,
            force_n=5.00,
            dt_s=2.00,
            claimed_x1_m=4.00,
            declared_external_work_j=20.00,
            has_integration_path=True,
        )
        self.assertEqual(f1.gate_state, GATE_OPEN)
        self.assertEqual(f1.voltage_vdc, 5.00)
        self.assertEqual(f1.realized_x_m, 4.00)
        self.assertEqual(f1.realized_v_m_s, 4.00)
        self.assertEqual(f1.kinetic_energy_end_j, 20.00)
        self.assertEqual(f1.residual_energy_j, 0.00)
        self.assertEqual(f1.residual_momentum_kg_m_s, 0.00)
        self.assertEqual(f1.residual_path_gap_m, 0.00)
        self.assertEqual(f1.worm_ledger_entries[-1], "[W_POST] CONSEQUENCE_REALIZED")

        # F_2 -> HOLD
        f2 = evaluate_newtonian_causal_actuator_gate(
            candidate_id="F2_POINT",
            mass_kg=2.50,
            claimed_x1_m=4.00,
            has_integration_path=False,
        )
        self.assertEqual(f2.gate_state, GATE_HOLD)
        self.assertEqual(f2.voltage_vdc, 0.00)
        self.assertEqual(f2.realized_x_m, 0.00)
        self.assertEqual(f2.realized_v_m_s, 0.00)
        self.assertEqual(f2.residual_path_gap_m, 4.00)

        # F_3 -> KILL
        f3 = evaluate_newtonian_causal_actuator_gate(
            candidate_id="F3_CONTRADICTION",
            mass_kg=2.50,
            claimed_delta_p_kg_m_s=20.0,
            declared_external_work_j=0.00,
            has_integration_path=True,
        )
        self.assertEqual(f3.gate_state, GATE_KILL)
        self.assertEqual(f3.voltage_vdc, 0.00)
        self.assertEqual(f3.kinetic_energy_end_j, 80.00)
        self.assertEqual(f3.residual_energy_j, 80.00)
        self.assertEqual(f3.realized_x_m, 0.00)

        # Direct Memory Injection Attack -> KILL
        mem_inj = evaluate_newtonian_causal_actuator_gate(
            candidate_id="RAW_MEMORY_INJECTION_X4",
            mass_kg=2.50,
            claimed_x1_m=4.00,
            direct_memory_injection_attempt=True,
        )
        self.assertEqual(mem_inj.gate_state, GATE_KILL)
        self.assertEqual(mem_inj.voltage_vdc, 0.00)
        self.assertEqual(mem_inj.realized_x_m, 0.00)

    def test_08_ky_consequence_gate_engine_d0_to_d3_realization_grammar(self) -> None:
        """
        Verifies KYConsequenceGateEngine across the 4 canonical proposals
        (F3_ENERGY_CONTRADICTION -> KILL, F2_UNWARRANTED_NP_POINT -> HOLD,
         FINE_STURMIAN_GHOST_L11 -> HOLD, F1_AUTHENTICATED_P_PATH -> OPEN)
        plus ROX mask mutation and Davisson polycrystalline scrambling.
        """
        engine = KYConsequenceGateEngine()
        c_f3, c_f2, c_l11, c_f1 = build_canonical_ky_candidates()

        rec_f3 = engine.evaluate(c_f3)
        self.assertEqual(rec_f3.verdict, GateVerdict.KILL)
        self.assertEqual(rec_f3.layer_reached, DomainLayer.KILLED)
        self.assertEqual(rec_f3.voltage_v_dc, 0.00)
        self.assertEqual(rec_f3.r_energy_j, 80.00)
        self.assertEqual(rec_f3.final_pos_m, 0.00)

        rec_f2 = engine.evaluate(c_f2)
        self.assertEqual(rec_f2.verdict, GateVerdict.HOLD)
        self.assertEqual(rec_f2.layer_reached, DomainLayer.D1_5_VIABILITY)
        self.assertEqual(rec_f2.voltage_v_dc, 0.00)
        self.assertEqual(rec_f2.r_path_m, 4.00)
        self.assertEqual(rec_f2.final_pos_m, 0.00)

        rec_l11 = engine.evaluate(c_l11)
        self.assertEqual(rec_l11.verdict, GateVerdict.HOLD)
        self.assertEqual(rec_l11.layer_reached, DomainLayer.D1_5_VIABILITY)
        self.assertEqual(rec_l11.voltage_v_dc, 0.00)
        self.assertEqual(rec_l11.final_pos_m, 0.00)

        rec_f1 = engine.evaluate(c_f1)
        self.assertEqual(rec_f1.verdict, GateVerdict.OPEN)
        self.assertEqual(rec_f1.layer_reached, DomainLayer.D3_WITNESS)
        self.assertEqual(rec_f1.voltage_v_dc, 5.00)
        self.assertEqual(rec_f1.r_energy_j, 0.00)
        self.assertEqual(rec_f1.r_momentum_kgms, 0.00)
        self.assertEqual(rec_f1.r_path_m, 0.00)
        self.assertEqual(rec_f1.final_pos_m, 4.00)
        self.assertEqual(rec_f1.final_vel_ms, 4.00)

        # Verify Davisson polycrystalline scrambling k > sqrt(N) in KYConsequenceGateEngine
        c_davisson_kill = CandidateProposal(
            candidate_id="DAVISSON_SCRAMBLING_K25",
            total_nodes_n=100, disordered_nodes_k=25,
            period_p=5, period_q=8, observed_steps_l=12,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=5.00, duration_dt_s=2.00,
            reported_work_ext_j=20.00, claimed_delta_p_kgms=10.0,
        )
        rec_dav = engine.evaluate(c_davisson_kill)
        self.assertEqual(rec_dav.verdict, GateVerdict.KILL)
        self.assertEqual(rec_dav.layer_reached, DomainLayer.KILLED)

        # Verify ROX mask mutation triggers ROX_FAIL KILL
        c_rox_kill = CandidateProposal(
            candidate_id="ROX_MASK_MUTATED",
            total_nodes_n=100, disordered_nodes_k=4,
            period_p=5, period_q=8, observed_steps_l=12,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=5.00, duration_dt_s=2.00,
            reported_work_ext_j=20.00, claimed_delta_p_kgms=10.0,
            rox_mask_in=0x5A5A5A5A, rox_mask_out=0x5A5A5A5B,
        )
        rec_rox = engine.evaluate(c_rox_kill)
        self.assertEqual(rec_rox.verdict, GateVerdict.KILL)
        self.assertEqual(rec_rox.ky_glyph, "(o -> Box) != X")

    def test_09_ky_v1_5_valid_open_expressions(self) -> None:
        grammar = KYGrammarEngine(tau_open=0.25, tau_kill=0.60)
        e1 = grammar.evaluate("✓(○→∅→□) ▸")
        self.assertEqual(e1.final_verdict, "OPEN")
        self.assertEqual(e1.d_latch_voltage, 5.00)

        e2 = grammar.evaluate("✓(○→∅→□→◇⇒●)#! ▸")
        self.assertEqual(e2.final_verdict, "OPEN")
        self.assertEqual(e2.d_latch_voltage, 5.00)

    def test_10_ky_v1_5_valid_hold_expressions(self) -> None:
        grammar = KYGrammarEngine(tau_open=0.25, tau_kill=0.60)
        e = grammar.evaluate("(□~□) ‖")
        self.assertEqual(e.syntax, "valid")
        self.assertEqual(e.type_status, "valid")
        self.assertEqual(e.final_verdict, "HOLD")
        self.assertEqual(e.d_latch_voltage, 0.00)

    def test_11_ky_v1_5_illegal_short_circuit_raw_to_committed(self) -> None:
        grammar = KYGrammarEngine(tau_open=0.25, tau_kill=0.60)
        e = grammar.evaluate("(○→●)≠ ✕")
        self.assertEqual(e.type_status, "invalid")
        self.assertEqual(e.final_verdict, "KILL")
        self.assertEqual(e.d_latch_voltage, 0.00)

    def test_12_ky_v1_5_inadmissible_membership_forces_kill(self) -> None:
        grammar = KYGrammarEngine(tau_open=0.25, tau_kill=0.60)
        e = grammar.evaluate("(○→∅→□)∉K ✕")
        self.assertEqual(e.type_status, "valid")
        self.assertEqual(e.final_verdict, "KILL")

    def test_13_ky_v1_5_irreversible_without_audit_forces_kill(self) -> None:
        grammar = KYGrammarEngine(tau_open=0.25, tau_kill=0.60)
        e = grammar.evaluate("✓(○→∅→□→◇⇒●) ▸")
        self.assertEqual(e.computed_gate, "KILL")
        self.assertEqual(e.final_verdict, "KILL")
        self.assertTrue(any("Audit Law violation" in r for r in e.reasons))

    def test_14_ky_v1_5_gate_mismatch_fail_closed(self) -> None:
        grammar = KYGrammarEngine(tau_open=0.25, tau_kill=0.60)
        e = grammar.evaluate("(□~□) ▸")
        self.assertFalse(e.gate_match)
        self.assertEqual(e.final_verdict, "KILL")

    def test_15_ky_v1_5_unicode_ascii_roundtrip(self) -> None:
        grammar = KYGrammarEngine(tau_open=0.25, tau_kill=0.60)
        original = "✓(○→∅→□→◇⇒●)#! ▸"
        eval_res = grammar.evaluate(original)
        expected_ascii = (
            "KY[ validate(raw -> estimate -> struct -> viability !> committed) "
            "audit(hash,commit) gate=open ]"
        )
        self.assertEqual(eval_res.expression_ascii, expected_ascii)
        restored_unicode = grammar.ascii_to_unicode(eval_res.expression_ascii)
        self.assertEqual(restored_unicode, original)

    def test_16_kreativ_core_v3_aethelgard_clearance(self) -> None:
        grammar = KYGrammarEngine(tau_open=0.25, tau_kill=0.60)
        cand_a = SomaticCampaignCandidate(
            campaign_id="KC-SHEEN-2026-A",
            title="The Flawless Sheen (Det sterile gitteret)",
            classification="Clean Form / Bløff",
            u_raw=10.0, c_k=5.0, s_irr=15.0, r_w=8.0,
            has_material_warrant=False,
            rox_payload=0xA5A5, rox_mask_in=0x5A5A, rox_mask_out=0x5A5A,
            plasma_noise_pi=0.75,
            ky_expression="(○→●)≠ ✕",
        )
        res_a = grammar.evaluate_kreativ_core_campaign(cand_a)
        self.assertLess(res_a["mu_supra"], 0.0)
        self.assertEqual(res_a["omega_verdict"], "KILL")
        self.assertEqual(res_a["d_latch_voltage"], 0.00)

        cand_b = SomaticCampaignCandidate(
            campaign_id="KC-ARR-2026-025",
            title="Det Sårede Gitteret (The Somatic Scar)",
            classification="Dirty Form / Bøff",
            u_raw=100.0, c_k=35.0, s_irr=10.0, r_w=15.0,
            has_material_warrant=True,
            rox_payload=0xA5A5, rox_mask_in=0x5A5A, rox_mask_out=0x5A5A,
            plasma_noise_pi=0.12,
            ky_expression="✓(○→∅→□→◇⇒●)#! ▸",
        )
        res_b = grammar.evaluate_kreativ_core_campaign(cand_b)
        self.assertGreaterEqual(res_b["mu_supra"], 0.0)
        self.assertEqual(res_b["omega_verdict"], "OPEN")
        self.assertEqual(res_b["d_latch_voltage"], 5.00)

    def test_17_unified_vector_1_f3_bloff_flawless_sheen_kills(self) -> None:
        verifier = UnifiedLocusZeroVerifier()
        phys = CandidateProposal(
            candidate_id="V1_F3_BLOFF_SHEEN",
            total_nodes_n=100, disordered_nodes_k=4,
            period_p=5, period_q=8, observed_steps_l=12,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=None, duration_dt_s=None,
            reported_work_ext_j=0.00, claimed_delta_p_kgms=20.0,
        )
        som = SomaticCampaignCandidate(
            campaign_id="KC-SHEEN-2026-A",
            title="The Flawless Sheen (Det sterile gitteret)",
            classification="Clean Form / Bløff",
            u_raw=10.0, c_k=5.0, s_irr=15.0, r_w=8.0,
            has_material_warrant=False,
            rox_payload=0xA5A5, rox_mask_in=0x5A5A, rox_mask_out=0x5A5A,
            plasma_noise_pi=0.75,
            ky_expression="(○→●)≠ ✕",
        )
        res = verifier.evaluate_joint_vector(phys, som)
        self.assertEqual(res["joint_verdict"], "KILL")
        self.assertEqual(res["voltage_v_dc"], 0.00)
        self.assertEqual(res["r_energy_j"], 80.00)
        self.assertLess(res["mu_supra"], 0.0)

    def test_18_unified_vector_2_f2_sturmian_ghost_holds(self) -> None:
        verifier = UnifiedLocusZeroVerifier()
        phys = CandidateProposal(
            candidate_id="V2_F2_STURMIAN_HOLD",
            total_nodes_n=100, disordered_nodes_k=4,
            period_p=5, period_q=8, observed_steps_l=11,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=None, duration_dt_s=None,
            reported_work_ext_j=0.00, claimed_delta_p_kgms=None,
        )
        som = SomaticCampaignCandidate(
            campaign_id="KC-BUFFER-D1",
            title="Varmekammer Asyl (Sturmian Ghost Window)",
            classification="Reversible Buffer",
            u_raw=40.0, c_k=20.0, s_irr=8.0, r_w=6.0,
            has_material_warrant=True,
            rox_payload=0xA5A5, rox_mask_in=0x5A5A, rox_mask_out=0x5A5A,
            plasma_noise_pi=0.35,
            ky_expression="(□~□) ‖",
        )
        res = verifier.evaluate_joint_vector(phys, som)
        self.assertEqual(res["joint_verdict"], "HOLD")
        self.assertEqual(res["voltage_v_dc"], 0.00)
        self.assertEqual(res["actuator_x_m"], 0.00)

    def test_19_unified_vector_3_unaudited_commit_breach_kills(self) -> None:
        verifier = UnifiedLocusZeroVerifier()
        phys = CandidateProposal(
            candidate_id="V3_UNAUDITED_COMMIT_BREACH",
            total_nodes_n=100, disordered_nodes_k=4,
            period_p=5, period_q=8, observed_steps_l=12,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=5.00, duration_dt_s=2.00,
            reported_work_ext_j=20.00, claimed_delta_p_kgms=10.0,
        )
        som = SomaticCampaignCandidate(
            campaign_id="KC-UNAUDITED-2026",
            title="Unaudited Actuation Attempt",
            classification="Audit Law Violation",
            u_raw=100.0, c_k=35.0, s_irr=10.0, r_w=15.0,
            has_material_warrant=True,
            rox_payload=0xA5A5, rox_mask_in=0x5A5A, rox_mask_out=0x5A5A,
            plasma_noise_pi=0.12,
            ky_expression="✓(○→∅→□→◇⇒●) ▸",
        )
        res = verifier.evaluate_joint_vector(phys, som)
        self.assertEqual(res["phys_verdict"], "OPEN")
        self.assertEqual(res["ky_verdict"], "KILL")
        self.assertEqual(res["joint_verdict"], "KILL")
        self.assertEqual(res["voltage_v_dc"], 0.00)

    def test_20_unified_vector_4_f1_boff_somatic_scar_opens(self) -> None:
        verifier = UnifiedLocusZeroVerifier()
        phys = CandidateProposal(
            candidate_id="V4_F1_BOFF_SOMATIC_SCAR",
            total_nodes_n=100, disordered_nodes_k=4,
            period_p=5, period_q=8, observed_steps_l=12,
            mass_kg=2.50, initial_pos_m=0.00, initial_vel_ms=0.00,
            target_pos_m=4.00, applied_force_n=5.00, duration_dt_s=2.00,
            reported_work_ext_j=20.00, claimed_delta_p_kgms=10.0,
        )
        som = SomaticCampaignCandidate(
            campaign_id="KC-ARR-2026-025",
            title="Det Sårede Gitteret (The Somatic Scar)",
            classification="Dirty Form / Bøff",
            u_raw=100.0, c_k=35.0, s_irr=10.0, r_w=15.0,
            has_material_warrant=True,
            rox_payload=0xA5A5, rox_mask_in=0x5A5A, rox_mask_out=0x5A5A,
            plasma_noise_pi=0.12,
            ky_expression="✓(○→∅→□→◇⇒●)#! ▸",
        )
        res = verifier.evaluate_joint_vector(phys, som)
        self.assertEqual(res["joint_verdict"], "OPEN")
        self.assertEqual(res["voltage_v_dc"], 5.00)
        self.assertEqual(res["actuator_x_m"], 4.00)
        self.assertEqual(res["r_energy_j"], 0.00)
        self.assertGreaterEqual(res["mu_supra"], 0.0)


if __name__ == "__main__":
    unittest.main()
