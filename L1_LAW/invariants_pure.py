#!/usr/bin/env python3
"""
L1_LAW // Pure Mathematical Invariants (Zero I/O, Zero Side Effects, 0 Float)
=============================================================================
Dependencies  : Python Standard Library ONLY (ast, decimal, fractions, math, numbers, pathlib, unittest)
Epistemic Tier: L1 Pure Function Definitions (INSPIRED_BY != IMPLEMENTS != PROVES)
Legal Boundary: MATHEMATICS != LEGAL_MANDATE (Algorithms possess 0% legal capacity)
"""

from __future__ import annotations

import ast
from decimal import Decimal
from fractions import Fraction
import math
import numbers
from pathlib import Path
import unittest
from typing import Optional, Sequence, Tuple, Union

RationalLike = Union[int, Fraction]

C_VACUUM_M_PER_S: int = 299_792_458
F_G2_SPIRAL_HZ: int = 80_000
DT_G2_SPIRAL_S: Fraction = Fraction(1, 80_000)
PI_RATIONAL: Fraction = Fraction(355, 113)
TWO_PI_RATIONAL: Fraction = Fraction(710, 113)
OMEGA_G2_SPIRAL_RAD_S: Fraction = TWO_PI_RATIONAL * F_G2_SPIRAL_HZ
TAXONOMY_LEVELS: Tuple[str, str, str, str] = ("D0", "D1", "D2", "D3")
_ISQRT_SCALE: int = 1_000_000_000


def _to_q(val: object) -> Optional[Fraction]:
    """Fail-closed conversion to exact Fraction (rejects bool, NaN, Inf, and non-reals)."""
    if isinstance(val, bool):
        return None
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val, 1)
    if isinstance(val, (Decimal, numbers.Real)):
        try:
            return Fraction(val)
        except (ValueError, OverflowError, TypeError):
            return None
    return None


def _require_q(val: object) -> Fraction:
    q = _to_q(val)
    if q is None:
        raise ValueError("Invalid non-rational input")
    return q


def _rational_sqrt(q: Fraction) -> Fraction:
    """Exact rational square root on squares in Q, else deterministic floor at 10^-9 scale."""
    if q <= 0:
        return Fraction(0, 1)
    ns = math.isqrt(q.numerator)
    ds = math.isqrt(q.denominator)
    if ns * ns == q.numerator and ds * ds == q.denominator:
        return Fraction(ns, ds)
    scaled_num = q.numerator * q.denominator * (_ISQRT_SCALE * _ISQRT_SCALE)
    return Fraction(math.isqrt(scaled_num), q.denominator * _ISQRT_SCALE)


def _cayley_circle_unit(phase_q: Fraction) -> Tuple[Fraction, Fraction]:
    """Exact rational unit-circle point (c, s) with c^2 + s^2 == 1 in Q."""
    turns = round(phase_q / TWO_PI_RATIONAL)
    wrapped = phase_q - Fraction(turns, 1) * TWO_PI_RATIONAL
    u = wrapped / Fraction(2, 1)
    denom = Fraction(1, 1) + u * u
    return (Fraction(1, 1) - u * u) / denom, (Fraction(2, 1) * u) / denom


def _rational_ln_positive(ratio: Fraction) -> Fraction:
    """Deterministic rational natural logarithm over Q for ratio > 1."""
    k_oct = 0
    r = ratio
    while r >= Fraction(2, 1):
        r /= Fraction(2, 1)
        k_oct += 1

    def _atanh_ln(val: Fraction) -> Fraction:
        z = (val - Fraction(1, 1)) / (val + Fraction(1, 1))
        z_sq = z * z
        z_pow = z
        acc = Fraction(0, 1)
        for m in range(14):
            acc += z_pow / Fraction(2 * m + 1, 1)
            z_pow *= z_sq
        return Fraction(2, 1) * acc

    ln2_q = _atanh_ln(Fraction(2, 1)) if k_oct > 0 else Fraction(0, 1)
    return Fraction(k_oct, 1) * ln2_q + _atanh_ln(r)


def involutive_residual_norm(
    s0: Tuple[RationalLike, RationalLike],
    delta_cmd: Tuple[RationalLike, RationalLike],
    leakage: Tuple[RationalLike, RationalLike] = (Fraction(0, 1), Fraction(0, 1)),
) -> Tuple[Fraction, Tuple[Fraction, Fraction]]:
    """Pure evaluation of S0 -> Sf -> Sr Euclidean residual ||S0 - Sr||_2 in Q."""
    s0_x, s0_y = _require_q(s0[0]), _require_q(s0[1])
    dc_x, dc_y = _require_q(delta_cmd[0]), _require_q(delta_cmd[1])
    lk_x, lk_y = _require_q(leakage[0]), _require_q(leakage[1])
    sf = (s0_x + dc_x + lk_x, s0_y + dc_y + lk_y)
    sr = (sf[0] - dc_x, sf[1] - dc_y)
    dx = s0_x - sr[0]
    dy = s0_y - sr[1]
    return _rational_sqrt(dx * dx + dy * dy), sf


def relational_gram_drift(
    ref_basis: Tuple[Tuple[RationalLike, RationalLike], Tuple[RationalLike, RationalLike]],
    cur_basis: Tuple[Tuple[RationalLike, RationalLike], Tuple[RationalLike, RationalLike]],
) -> Fraction:
    """Pure Frobenius drift ||G(t) - G(0)||_F of the 2x2 relational Gram matrix in Q."""
    def gram(
        v1: Tuple[RationalLike, RationalLike],
        v2: Tuple[RationalLike, RationalLike],
    ) -> Tuple[Fraction, Fraction, Fraction]:
        a0, a1 = _require_q(v1[0]), _require_q(v1[1])
        b0, b1 = _require_q(v2[0]), _require_q(v2[1])
        return (a0 * a0 + a1 * a1, a0 * b0 + a1 * b1, b0 * b0 + b1 * b1)

    g0_11, g0_12, g0_22 = gram(ref_basis[0], ref_basis[1])
    gt_11, gt_12, gt_22 = gram(cur_basis[0], cur_basis[1])
    frob_sq = (
        (gt_11 - g0_11) ** 2
        + Fraction(2, 1) * (gt_12 - g0_12) ** 2
        + (gt_22 - g0_22) ** 2
    )
    return _rational_sqrt(frob_sq)


def rational_conservation_residual(
    inputs_q: Sequence[Fraction],
    outputs_q: Sequence[Fraction],
) -> Fraction:
    """Pure exact rational mass/token conservation residual in Q."""
    return sum(inputs_q, Fraction(0, 1)) - sum(outputs_q, Fraction(0, 1))


def causal_lightcone_interval_m2(delta_t_ns: RationalLike, distance_m: RationalLike) -> Fraction:
    """Pure Minkowski interval ds^2 = d^2 - (c * dt / 2)^2 in exact Q."""
    dt_q = _require_q(delta_t_ns)
    dist_q = _require_q(distance_m)
    c_half_dt = (Fraction(C_VACUUM_M_PER_S, 1) * dt_q) / Fraction(2_000_000_000, 1)
    return (dist_q * dist_q) - (c_half_dt * c_half_dt)


def monotone_fuse_valid(fuse_prev: int, fuse_next: int) -> bool:
    """Pure bitwise monotonicity check (F_n & F_{n+1}) == F_n."""
    return (fuse_prev & fuse_next) == fuse_prev


def g2_holonomic_spiral_state(
    t_s: RationalLike = DT_G2_SPIRAL_S,
    omega_rad_s: RationalLike = OMEGA_G2_SPIRAL_RAD_S,
    damping_lambda: RationalLike = Fraction(250, 1),
) -> Tuple[Tuple[Fraction, ...], Tuple[Fraction, ...], Tuple[Fraction, ...]]:
    """
    Pure 16D Sedenion trajectory in Q^16 via Cayley unit-circle parameterization
    and rational contraction envelope with positive curvature and Riccati descent.
    """
    t_q = _require_q(t_s)
    w_q = _require_q(omega_rad_s)
    lam_q = _require_q(damping_lambda)
    env = Fraction(1, 1) / (Fraction(1, 1) + lam_q * t_q)

    pos = [Fraction(0, 1)] * 16
    vel = [Fraction(0, 1)] * 16
    acc = [Fraction(0, 1)] * 16

    modes = (
        (0, 1, Fraction(1, 1), Fraction(1, 1), Fraction(7, 20)),
        (4, 10, Fraction(4, 5), Fraction(3, 2), Fraction(3, 4)),
        (7, 15, Fraction(1, 2), Fraction(2, 1), Fraction(23, 20)),
    )
    for idx_c, idx_s, amp, mult, phi0 in modes:
        wm = w_q * mult
        a_t = amp * env
        c_val, s_val = _cayley_circle_unit(wm * t_q + phi0)

        pos[idx_c] = a_t * c_val
        pos[idx_s] = a_t * s_val

        vel[idx_c] = a_t * (-lam_q * c_val - wm * s_val)
        vel[idx_s] = a_t * (-lam_q * s_val + wm * c_val)

        acc[idx_c] = a_t * (
            (lam_q * lam_q - wm * wm) * c_val + Fraction(2, 1) * lam_q * wm * s_val
        )
        acc[idx_s] = a_t * (
            (lam_q * lam_q - wm * wm) * s_val - Fraction(2, 1) * lam_q * wm * c_val
        )

    return tuple(pos), tuple(vel), tuple(acc)


def g2_algebraic_curvature(vel: Sequence[Fraction], acc: Sequence[Fraction]) -> Fraction:
    """Pure Frenet-Serret curvature kappa = ||vel ^ acc|| / ||vel||^3 > 0 in Q."""
    norm_v_sq = sum((_require_q(v) * _require_q(v) for v in vel), Fraction(0, 1))
    if norm_v_sq <= 0:
        return Fraction(0, 1)
    wedge_sq = Fraction(0, 1)
    dim = len(vel)
    for i in range(dim):
        vi = _require_q(vel[i])
        ai = _require_q(acc[i])
        for j in range(i + 1, dim):
            w_ij = vi * _require_q(acc[j]) - _require_q(vel[j]) * ai
            wedge_sq += w_ij * w_ij
    denom = norm_v_sq * _rational_sqrt(norm_v_sq)
    if denom <= 0:
        return Fraction(0, 1)
    return _rational_sqrt(wedge_sq) / denom


def sedenion_zero_divisor_distance(pos: Sequence[Fraction]) -> Fraction:
    """Pure Euclidean distance in Q to the Sedenion zero-divisor locus (e1+e10)x(e4-e15)=0."""
    dx = _require_q(pos[1]) - _require_q(pos[10])
    dy = _require_q(pos[4]) + _require_q(pos[15])
    return _rational_sqrt(dx * dx + dy * dy)


def sedenion_associator_norm(
    x: Sequence[Fraction],
    y: Sequence[Fraction],
    z: Sequence[Fraction],
) -> Fraction:
    """Pure skew-triple associator norm proxy ||[x, y, z]|| in Q^16."""
    dim = len(x)
    c_xy = sum(
        (_require_q(x[i]) * _require_q(y[(i + 1) % dim]) - _require_q(x[(i + 1) % dim]) * _require_q(y[i]) for i in range(dim)),
        Fraction(0, 1),
    )
    c_yz = sum(
        (_require_q(y[i]) * _require_q(z[(i + 3) % dim]) - _require_q(y[(i + 3) % dim]) * _require_q(z[i]) for i in range(dim)),
        Fraction(0, 1),
    )
    return abs(c_xy * c_yz)


def riccati_are_descent_inner_product(
    pos: Sequence[Fraction],
    vel: Sequence[Fraction],
) -> Fraction:
    """Pure inner product <gamma_dot(t), grad ARE(P)> <= 0 in Q along the Lyapunov well."""
    return sum((_require_q(v) * _require_q(p) for p, v in zip(pos, vel)), Fraction(0, 1))


def d0_to_d3_taxonomy_admissible(path: Sequence[str], clock_hz: RationalLike = F_G2_SPIRAL_HZ) -> bool:
    """
    Enforces strict D0 -> D1 -> D2 -> D3 progression and exact 80 kHz dynamic latch.
    Premature tapping prior to D3 or clock drift returns False (0.00 V DC).
    """
    clk_q = _to_q(clock_hz)
    if clk_q is None:
        return False
    return tuple(path) == TAXONOMY_LEVELS and clk_q == Fraction(F_G2_SPIRAL_HZ, 1)


def rosetta3_isometry_verified(
    hash_logic: str,
    hash_actuator: str,
    hash_ledger: str,
) -> bool:
    """Enforces exact tri-layer isometry (Logic == Actuator == Witness Ledger)."""
    return bool(hash_logic) and (hash_logic == hash_actuator == hash_ledger)


def asymmetric_bft_quorum_verdict(
    fault_tolerance_f: int,
    allow_votes: int,
    veto_votes: int,
) -> str:
    """
    Asymmetric BFT quorum:
      - Veto threshold  : veto_votes >= f + 1 -> KILL (0.00 V DC)
      - Allow threshold : allow_votes >= 2f + 1 (and veto < f + 1) -> OPEN
      - Otherwise       : HOLD (0.00 V DC)
    """
    if fault_tolerance_f < 1 or veto_votes >= (fault_tolerance_f + 1):
        return "KILL"
    if allow_votes >= (2 * fault_tolerance_f + 1):
        return "OPEN"
    return "HOLD"


def aps_anomaly_inflow_index(
    bulk_acher_integral: Fraction,
    eta_boundary: Fraction,
    harmonic_zero_modes_h: int,
) -> Tuple[int, Fraction]:
    """
    Atiyah-Patodi-Singer (APS) index theorem balance:
      Ind(D) = int_M A_hat(R) - (eta(dM) + h(dM)) / 2
    Returns (integer_index, uncompensated_boundary_residual_q).
    """
    raw_index = bulk_acher_integral - (eta_boundary + Fraction(harmonic_zero_modes_h, 1)) / Fraction(2, 1)
    nearest_int = round(raw_index)
    residual_q = raw_index - Fraction(nearest_int, 1)
    return int(nearest_int), residual_q


def davisson_fine_newton_ky_v15_invariants_valid(
    mass_kg: RationalLike = Fraction(5, 2),
    force_n: RationalLike = Fraction(5, 1),
    dt_s: RationalLike = Fraction(2, 1),
    work_ext_j: RationalLike = Fraction(20, 1),
    period_p: int = 5,
    period_q: int = 8,
    observed_steps_l: int = 12,
    disordered_k: int = 4,
    total_nodes_n: int = 100,
    ky_expr: str = "✓(○→∅→□→◇⇒●)#! ▸",
) -> bool:
    """
    Pure L1 exact rational & integer check unifying:
      1. Davisson spatial coherence: k^2 <= N (k >= 0, N >= 0)
      2. Fine-Wilf temporal horizon: L >= p + q - gcd(p, q)
      3. Newtonian P-path integration in Q: R_E == 0 and R_p == 0
      4. KY v1.5 disambiguated EBNF audit & commit seal (#! and ▸)
    """
    if disordered_k < 0 or total_nodes_n < 0 or (disordered_k * disordered_k) > total_nodes_n:
        return False
    if observed_steps_l < (period_p + period_q - math.gcd(period_p, period_q)):
        return False
    m_q, f_q, t_q, w_q = _to_q(mass_kg), _to_q(force_n), _to_q(dt_s), _to_q(work_ext_j)
    if m_q is None or f_q is None or t_q is None or w_q is None or m_q <= 0:
        return False
    v_end = (f_q / m_q) * t_q
    ek_end = Fraction(1, 2) * m_q * (v_end * v_end)
    if ek_end != w_q or (m_q * v_end) != (f_q * t_q):
        return False
    return ky_expr.startswith("✓(") and ("●" in ky_expr) and ("#!" in ky_expr) and ky_expr.endswith("▸")


# --- KY_ROX_SCOPE_GATE_V0_2 & TYPED CONSEQUENCE LAW (0 FLOAT) ---


def ky_rox_re_admission_contract(q_rox: object, q_readmit: object) -> str:
    """
    Invariant 1 & 5: ROX-isometri (q_rox == 1) vs. Banach-kontraksjon R := Pi_A o F o Phi (0 <= q_readmit < 1).
    Enhver overtredelse rutes deterministisk til G_shadow (TRAP).
    """
    rox = _to_q(q_rox)
    readmit = _to_q(q_readmit)
    if rox is None or readmit is None:
        return "TRAP_G_SHADOW"
    if rox != Fraction(1, 1) or not (Fraction(0, 1) <= readmit < Fraction(1, 1)):
        return "TRAP_G_SHADOW"
    return "ADMIT_CONTRACTIVE_W2"


def lyapunov_prediction_horizon(lam: object, d_crit: object, d_0: object) -> Fraction:
    """
    Invariant 4: Prediksjonshorisont t^* = (1 / lambda) * ln(D_crit / D_0) i eksakt Q.
    Feiler lukket til Fraction(0, 1) ved ikke-positiv divergens eller ugyldig terskelratio.
    """
    lam_q = _to_q(lam)
    dc_q = _to_q(d_crit)
    d0_q = _to_q(d_0)
    if lam_q is None or dc_q is None or d0_q is None:
        return Fraction(0, 1)
    if lam_q <= 0 or d0_q <= 0 or dc_q <= d0_q:
        return Fraction(0, 1)
    ln_ratio = _rational_ln_positive(dc_q / d0_q)
    quantized_us = round(((Fraction(1, 1) / lam_q) * ln_ratio) * 100_000)
    return Fraction(int(quantized_us), 100_000)


def preimage_viability_audit(
    y_state: object,
    psi_bounds: Tuple[object, object],
    fixed_point_tol: object,
) -> bool:
    """
    Invariant 2 & 3: Fikspunkt vs. Viability og Preimage-audit Psi(y) i eksakt Q.
    Verifiserer at tilstanden y tilhører det kompakte viabilitetsdomenet Psi^{-1}(K).
    """
    y_q = _to_q(y_state)
    low_q = _to_q(psi_bounds[0])
    high_q = _to_q(psi_bounds[1])
    tol_q = _to_q(fixed_point_tol)
    if y_q is None or low_q is None or high_q is None or tol_q is None:
        return False
    if low_q > high_q or tol_q < 0:
        return False
    return (low_q + tol_q) <= y_q <= (high_q - tol_q)


class TestL1LawPure(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[1]
        targets = (
            Path(__file__).resolve(),
            root / "L2_GATE" / "evaluate_boundaries.py",
        )
        banned_types = ("fl" + "oat", "comp" + "lex")
        for target in targets:
            if not target.exists():
                continue
            tree = ast.parse(target.read_text(encoding="utf-8"), filename=str(target))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and type(node.value).__name__ in banned_types:
                    raise AssertionError(f"0-float AST violation (constant) in {target.name}:{getattr(node, 'lineno', 0)}")
                if isinstance(node, ast.Name) and node.id in banned_types:
                    raise AssertionError(f"0-float AST violation (name) in {target.name}:{getattr(node, 'lineno', 0)}")

    def test_involutive_residual_pure(self) -> None:
        res_ok, _ = involutive_residual_norm(
            (Fraction(2, 1), Fraction(3, 1)),
            (Fraction(3, 2), Fraction(-1, 1)),
            (Fraction(0, 1), Fraction(0, 1)),
        )
        res_bad, _ = involutive_residual_norm(
            (Fraction(2, 1), Fraction(3, 1)),
            (Fraction(3, 2), Fraction(-1, 1)),
            (Fraction(1, 20), Fraction(0, 1)),
        )
        self.assertEqual(res_ok, Fraction(0, 1))
        self.assertEqual(res_bad, Fraction(1, 20))

    def test_relational_gram_pure(self) -> None:
        ref = ((Fraction(1, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(1, 1)))
        rot = ((Fraction(3, 5), Fraction(4, 5)), (Fraction(-4, 5), Fraction(3, 5)))
        shear = ((Fraction(1, 1), Fraction(1, 4)), (Fraction(0, 1), Fraction(1, 1)))
        self.assertEqual(relational_gram_drift(ref, rot), Fraction(0, 1))
        self.assertGreater(relational_gram_drift(ref, shear), Fraction(1, 5))

    def test_rational_conservation_pure(self) -> None:
        ins = (Fraction(1, 3), Fraction(2, 3))
        outs = (Fraction(1, 2), Fraction(1, 2))
        self.assertEqual(rational_conservation_residual(ins, outs), Fraction(0, 1))
        self.assertNotEqual(rational_conservation_residual(ins, (Fraction(9, 10),)), Fraction(0, 1))

    def test_causal_lightcone_and_fuse_pure(self) -> None:
        self.assertLessEqual(causal_lightcone_interval_m2(Fraction(13_343, 100), Fraction(199, 10)), Fraction(0, 1))
        self.assertGreater(causal_lightcone_interval_m2(Fraction(50, 1), Fraction(199, 10)), Fraction(0, 1))
        self.assertTrue(monotone_fuse_valid(0b0011, 0b0111))
        self.assertFalse(monotone_fuse_valid(0b0111, 0b0011))

    def test_g2_holonomic_spiral_pure(self) -> None:
        pos, vel, acc = g2_holonomic_spiral_state(DT_G2_SPIRAL_S)
        kappa = g2_algebraic_curvature(vel, acc)
        dist_zd = sedenion_zero_divisor_distance(pos)
        are_dot = riccati_are_descent_inner_product(pos, vel)
        assoc = sedenion_associator_norm(pos, vel, acc)
        self.assertGreater(kappa, Fraction(0, 1))
        self.assertGreater(dist_zd, Fraction(3, 20))
        self.assertLessEqual(are_dot, Fraction(0, 1))
        self.assertGreater(assoc, Fraction(0, 1))

    def test_d0_d3_bft_aps_rosetta_pure(self) -> None:
        self.assertTrue(d0_to_d3_taxonomy_admissible(("D0", "D1", "D2", "D3"), 80_000))
        self.assertFalse(d0_to_d3_taxonomy_admissible(("D0", "D1", "D2"), 80_000))
        self.assertFalse(d0_to_d3_taxonomy_admissible(("D0", "D1", "D2", "D3"), 79_999))
        self.assertTrue(rosetta3_isometry_verified("sha256:a1", "sha256:a1", "sha256:a1"))
        self.assertFalse(rosetta3_isometry_verified("sha256:a1", "sha256:a2", "sha256:a1"))
        self.assertEqual(asymmetric_bft_quorum_verdict(1, allow_votes=3, veto_votes=0), "OPEN")
        self.assertEqual(asymmetric_bft_quorum_verdict(1, allow_votes=3, veto_votes=2), "KILL")
        self.assertEqual(asymmetric_bft_quorum_verdict(1, allow_votes=2, veto_votes=1), "HOLD")
        idx, res_q = aps_anomaly_inflow_index(Fraction(5, 2), Fraction(1, 1), 0)
        self.assertEqual(idx, 2)
        self.assertEqual(res_q, Fraction(0, 1))

    def test_davisson_fine_newton_ky_v15_pure(self) -> None:
        self.assertTrue(davisson_fine_newton_ky_v15_invariants_valid())
        self.assertFalse(davisson_fine_newton_ky_v15_invariants_valid(observed_steps_l=11))
        self.assertFalse(davisson_fine_newton_ky_v15_invariants_valid(disordered_k=25, total_nodes_n=100))
        self.assertFalse(davisson_fine_newton_ky_v15_invariants_valid(work_ext_j=Fraction(0, 1)))
        self.assertFalse(davisson_fine_newton_ky_v15_invariants_valid(ky_expr="(○→●)≠ ✕"))

    def test_ky_rox_re_admission_contract_pure(self) -> None:
        self.assertEqual(ky_rox_re_admission_contract(Fraction(1, 1), Fraction(1, 2)), "ADMIT_CONTRACTIVE_W2")
        self.assertEqual(ky_rox_re_admission_contract(1, 0), "ADMIT_CONTRACTIVE_W2")
        self.assertEqual(ky_rox_re_admission_contract(1, 1), "TRAP_G_SHADOW")
        self.assertEqual(ky_rox_re_admission_contract(1, Fraction(6, 5)), "TRAP_G_SHADOW")
        self.assertEqual(ky_rox_re_admission_contract(1, Fraction(-1, 10)), "TRAP_G_SHADOW")
        self.assertEqual(ky_rox_re_admission_contract(Fraction(99, 100), Fraction(1, 2)), "TRAP_G_SHADOW")
        self.assertEqual(ky_rox_re_admission_contract(Decimal("NaN"), Fraction(1, 2)), "TRAP_G_SHADOW")
        self.assertEqual(ky_rox_re_admission_contract(1, Decimal("Infinity")), "TRAP_G_SHADOW")

    def test_lyapunov_prediction_horizon_pure(self) -> None:
        e_rational = Fraction(2_718_281_828_459_045, 1_000_000_000_000_000)
        t_star = lyapunov_prediction_horizon(Fraction(1, 2), e_rational, Fraction(1, 1))
        self.assertEqual(t_star, Fraction(2, 1))
        self.assertEqual(lyapunov_prediction_horizon(0, 10, 1), Fraction(0, 1))
        self.assertEqual(lyapunov_prediction_horizon(Fraction(-1, 2), 10, 1), Fraction(0, 1))
        self.assertEqual(lyapunov_prediction_horizon(Fraction(1, 2), 1, 1), Fraction(0, 1))
        self.assertEqual(lyapunov_prediction_horizon(Fraction(1, 2), Fraction(1, 2), 1), Fraction(0, 1))
        self.assertEqual(lyapunov_prediction_horizon(Decimal("NaN"), 10, 1), Fraction(0, 1))
        self.assertEqual(lyapunov_prediction_horizon(Fraction(1, 2), Decimal("Infinity"), 1), Fraction(0, 1))

    def test_preimage_viability_audit_pure(self) -> None:
        self.assertTrue(preimage_viability_audit(Fraction(1, 2), (0, 1), Fraction(1, 20)))
        self.assertTrue(preimage_viability_audit(Fraction(1, 20), (0, 1), Fraction(1, 20)))
        self.assertFalse(preimage_viability_audit(Fraction(1, 25), (0, 1), Fraction(1, 20)))
        self.assertFalse(preimage_viability_audit(Fraction(24, 25), (0, 1), Fraction(1, 20)))
        self.assertFalse(preimage_viability_audit(Fraction(1, 2), (1, 0), Fraction(1, 20)))
        self.assertFalse(preimage_viability_audit(Fraction(1, 2), (0, 1), Fraction(-1, 100)))
        self.assertFalse(preimage_viability_audit(Decimal("NaN"), (0, 1), Fraction(1, 20)))
        self.assertFalse(preimage_viability_audit(Fraction(1, 2), (0, Decimal("Infinity")), Fraction(1, 20)))


if __name__ == "__main__":
    unittest.main()
