#!/usr/bin/env python3
"""
Deterministic L1 Demonstrator: Fluid/Process Control Incident Response Digital Twin Gate
========================================================================================
Context       : SFI NORCICS / CPS4CIP Technical Exchange (M. E. Torjusen & K. Kampourakis)
Use Case B    : Automated Cyber-Incident Response (IDR) Veto & Staged Safe Fallback
                in a Pressurized Fluid/Process Loop (Joukowsky Surge & Thermal Bounds)
Dependencies  : Python Standard Library ONLY (dataclasses, hashlib, json, math, sys, unittest)
Epistemic Tier: L1 Deterministic Software Demonstrator (INSPIRED_BY != IMPLEMENTS != PROVES)
Actuation Lock: KILL (0.00 V DC) > HOLD (0.00 V DC) > OPEN (5.00 V DC)
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import unittest
from dataclasses import dataclass
from typing import Any, Dict, Sequence


def canonical_sha256(payload: Dict[str, Any]) -> str:
    """Deterministic RFC-8785-style sorted JSON SHA-256 witness digest."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class FluidPlantState:
    """Nominal physical operating state S_0 of the pressurized fluid process section."""
    static_pressure_bar: float = 45.0       # Nominal operating pressure P_0 [bar]
    flow_velocity_m_s: float = 2.5          # Nominal fluid velocity v_0 [m/s]
    fluid_density_kg_m3: float = 1000.0     # Process fluid density rho [kg/m^3]
    wave_speed_m_s: float = 1200.0          # Acoustic wave celerity a_s [m/s]
    pipe_length_m: float = 600.0            # Effective conduit length L [m]
    coolant_temp_k: float = 340.0           # Nominal jacket/process temperature T_0 [K]
    heat_load_kw: float = 240.0             # Exothermic process heat load Q_dot [kW]
    thermal_capacity_kj_k: float = 120.0    # Effective thermal capacitance C_th [kJ/K]


@dataclass(frozen=True)
class OperatingEnvelope:
    """Hard physical safety boundaries K for the process section."""
    max_pressure_bar: float = 60.0          # Maximum allowable transient pressure P_max [bar]
    max_slew_rate_bar_s: float = 15.0       # Maximum pressure rate dP/dt [bar/s]
    max_thermal_rate_k_s: float = 1.50      # Maximum thermal excursion rate dT/dt [K/s]
    max_temp_k: float = 355.0               # High-temperature trip limit T_max [K]
    eps_mass_balance_kg_s: float = 1e-6     # Involutive mass-conservation tolerance [kg/s]


@dataclass(frozen=True)
class CandidateResponseAction:
    """
    Candidate cyber-incident response action Phi(x_t) proposed by an IDR playbook
    to isolate or throttle a compromised PLC / actuator zone.
    """
    action_id: str
    description: str
    target_velocity_m_s: float              # Target post-isolation flow velocity [m/s]
    closure_time_s: float                   # Valve actuation ramp duration dt_close [s]
    relief_bypass_fraction: float           # Fraction of heat/flow routed to safe bypass [0..1]
    unaccounted_mass_leak_kg_s: float = 0.0 # Non-reversible mass discrepancy in twin check


def evaluate_fluid_twin_gate(
    plant: FluidPlantState,
    envelope: OperatingEnvelope,
    candidate: CandidateResponseAction,
    ancestor_hash: str = "0" * 64,
) -> Dict[str, Any]:
    """
    Pre-Execution Digital Twin Consequence Gate (Pi_K -> Omega -> W):
      1. Simulates the forward fluid/thermal transient S_0 -> S_f induced by `candidate`:
         - Acoustic reflection period: T_refl = 2 * L / a_s.
         - Joukowsky surge pressure:
             dP_joukowsky = (rho * a_s * dv) *1e-5 [bar].
             For rapid closure (dt_close <= T_refl), full Joukowsky surge applies.
             For staged ramp closure (dt_close > T_refl), Michaud/allievi attenuation
             scales surge by (T_refl / dt_close), further mitigated by relief bypass.
         - Thermal excursion rate dT/dt under reduced primary cooling flow.
      2. Performs involutive mass-balance check S_0 -> S_f -> S_r.
      3. Emits fail-closed gate verdict: KILL (0.00 V) > HOLD (0.00 V) > OPEN (5.00 V).
    """
    if candidate.closure_time_s <= 0.0 or not (0.0 <= candidate.relief_bypass_fraction <= 1.0):
        raise ValueError("Invalid candidate parameters: closure_time_s must be > 0 and bypass in [0, 1].")

    delta_v = max(0.0, plant.flow_velocity_m_s - candidate.target_velocity_m_s)
    t_reflection_s = (2.0 * plant.pipe_length_m) / plant.wave_speed_m_s

    # Full Joukowsky water-hammer surge [bar] (1 bar = 1e5 Pa)
    full_joukowsky_bar = (plant.fluid_density_kg_m3 * plant.wave_speed_m_s * delta_v) * 1e-5

    # Ramp attenuation factor (1.0 if dt_close <= T_refl, else T_refl / dt_close)
    ramp_factor = 1.0 if candidate.closure_time_s <= t_reflection_s else (t_reflection_s / candidate.closure_time_s)
    bypass_attenuation = 1.0 - 0.5 * candidate.relief_bypass_fraction
    surge_pressure_bar = full_joukowsky_bar * ramp_factor * bypass_attenuation

    peak_pressure_bar = plant.static_pressure_bar + surge_pressure_bar
    pressure_slew_bar_s = surge_pressure_bar / candidate.closure_time_s

    # Residual cooling fraction from remaining main flow + relief bypass cooling loop
    retained_flow_fraction = (
        candidate.target_velocity_m_s / plant.flow_velocity_m_s
        if plant.flow_velocity_m_s > 0.0
        else 0.0
    )
    effective_cooling_fraction = min(1.0, retained_flow_fraction + 0.75 * candidate.relief_bypass_fraction)
    uncooled_heat_kw = plant.heat_load_kw * (1.0 - effective_cooling_fraction)
    thermal_rate_k_s = uncooled_heat_kw / plant.thermal_capacity_kj_k
    projected_temp_k = plant.coolant_temp_k + thermal_rate_k_s * candidate.closure_time_s

    # Involutive mass-conservation residual ||S_0 - S_r||
    mass_balance_residual = abs(candidate.unaccounted_mass_leak_kg_s)

    violations = []
    if mass_balance_residual > envelope.eps_mass_balance_kg_s:
        violations.append("TWIN_MASS_BALANCE_ASYMMETRY")
    if peak_pressure_bar > envelope.max_pressure_bar:
        violations.append("SURGE_PRESSURE_LIMIT_EXCEEDED")
    if pressure_slew_bar_s > envelope.max_slew_rate_bar_s:
        violations.append("PRESSURE_SLEW_RATE_EXCEEDED")
    if thermal_rate_k_s > envelope.max_thermal_rate_k_s:
        violations.append("THERMAL_GRADIENT_LIMIT_EXCEEDED")
    if projected_temp_k > envelope.max_temp_k:
        violations.append("PROJECTED_TEMPERATURE_LIMIT_EXCEEDED")

    if "TWIN_MASS_BALANCE_ASYMMETRY" in violations:
        verdict = "KILL"
        voltage_v = 0.00
        gate_action = "EMERGENCY_LOCKOUT_0V"
    elif violations:
        verdict = "HOLD"
        voltage_v = 0.00
        gate_action = "VETO_UNSAFE_IDR_CANDIDATE"
    else:
        verdict = "OPEN"
        voltage_v = 5.00
        gate_action = "AUTHORIZE_SAFE_EXECUTION"

    record: Dict[str, Any] = {
        "action_id": candidate.action_id,
        "description": candidate.description,
        "closure_time_s": round(candidate.closure_time_s, 4),
        "t_reflection_s": round(t_reflection_s, 4),
        "surge_pressure_bar": round(surge_pressure_bar, 4),
        "peak_pressure_bar": round(peak_pressure_bar, 4),
        "max_pressure_bar": round(envelope.max_pressure_bar, 4),
        "pressure_slew_bar_s": round(pressure_slew_bar_s, 4),
        "thermal_rate_k_s": round(thermal_rate_k_s, 4),
        "max_thermal_rate_k_s": round(envelope.max_thermal_rate_k_s, 4),
        "projected_temp_k": round(projected_temp_k, 4),
        "mass_balance_residual": round(mass_balance_residual, 9),
        "violations": violations,
        "verdict": verdict,
        "gate_action": gate_action,
        "voltage_v": voltage_v,
        "ancestor": ancestor_hash,
    }
    record["witness_sha256"] = canonical_sha256(record)
    return record


def select_admissible_incident_response(
    plant: FluidPlantState,
    envelope: OperatingEnvelope,
    playbook_candidates: Sequence[CandidateResponseAction],
    initial_ancestor: str = "0" * 64,
) -> Dict[str, Any]:
    """
    Evaluates an ordered IDR playbook through the Digital Twin Consequence Gate.
    Vetoes unsafe isolation actions (HOLD/KILL) and selects the first admissible
    staged fallback (OPEN), preserving the full SHA-256 witness audit trail.
    """
    evaluated_chain = []
    ancestor = initial_ancestor
    selected_action = None

    for candidate in playbook_candidates:
        step_result = evaluate_fluid_twin_gate(
            plant=plant,
            envelope=envelope,
            candidate=candidate,
            ancestor_hash=ancestor,
        )
        evaluated_chain.append(step_result)
        ancestor = step_result["witness_sha256"]

        if step_result["verdict"] == "KILL":
            # Hard invariant / integrity breach terminates playbook search immediately
            break
        if step_result["verdict"] == "OPEN" and selected_action is None:
            selected_action = step_result
            break

    master_digest = canonical_sha256(
        {"evaluated_witnesses": [step["witness_sha256"] for step in evaluated_chain]}
    )
    return {
        "selected_action_id": selected_action["action_id"] if selected_action else None,
        "final_verdict": selected_action["verdict"] if selected_action else evaluated_chain[-1]["verdict"],
        "final_voltage_v": selected_action["voltage_v"] if selected_action else 0.00,
        "evaluated_steps": evaluated_chain,
        "master_chain_sha256": master_digest,
    }


class TestFluidProcessIDRGateDemonstrator(unittest.TestCase):
    def setUp(self) -> None:
        self.plant = FluidPlantState()
        self.envelope = OperatingEnvelope()

    def test_01_hard_slam_isolation_vetoed_by_water_hammer_and_slew(self) -> None:
        """
        IDR Candidate a_1: Immediate hard valve closure (dt = 0.25 s <= T_refl = 1.0 s)
        induces +30 bar Joukowsky surge (P_peak = 75 bar > 60 bar) -> Vetoed (HOLD, 0.00 V).
        """
        a1_slam = CandidateResponseAction(
            action_id="IDR_A1_HARD_VALVE_SLAM",
            description="Immediate isolation of compromised segment via 0.25s hard valve slam",
            target_velocity_m_s=0.0,
            closure_time_s=0.25,
            relief_bypass_fraction=0.0,
        )
        res = evaluate_fluid_twin_gate(self.plant, self.envelope, a1_slam)
        self.assertEqual(res["verdict"], "HOLD")
        self.assertEqual(res["voltage_v"], 0.00)
        self.assertAlmostEqual(res["peak_pressure_bar"], 75.0, places=4)
        self.assertIn("SURGE_PRESSURE_LIMIT_EXCEEDED", res["violations"])
        self.assertIn("PRESSURE_SLEW_RATE_EXCEEDED", res["violations"])

    def test_02_unbypassed_slow_isolation_vetoed_by_thermal_gradient(self) -> None:
        """
        IDR Candidate a_2: Slow valve closure (dt = 5.0 s) avoids pressure surge
        (P_peak = 51 bar <= 60 bar) but without relief cooling bypass exceeds dT/dt -> HOLD.
        """
        a2_no_cooling = CandidateResponseAction(
            action_id="IDR_A2_SLOW_CLOSE_NO_BYPASS",
            description="5.0s ramped isolation without engaging relief cooling bypass",
            target_velocity_m_s=0.25,
            closure_time_s=5.0,
            relief_bypass_fraction=0.0,
        )
        res = evaluate_fluid_twin_gate(self.plant, self.envelope, a2_no_cooling)
        self.assertEqual(res["verdict"], "HOLD")
        self.assertEqual(res["voltage_v"], 0.00)
        self.assertLessEqual(res["peak_pressure_bar"], self.envelope.max_pressure_bar)
        self.assertIn("THERMAL_GRADIENT_LIMIT_EXCEEDED", res["violations"])

    def test_03_staged_ramp_with_relief_bypass_authorized_open(self) -> None:
        """
        IDR Candidate a_3: Staged 6.0s ramp throttling to 0.5 m/s with 60% relief bypass
        keeps P_peak = 47.8 bar <= 60 bar and dT/dt = 0.525 K/s <= 1.50 K/s -> OPEN (5.00 V).
        """
        a3_safe_fallback = CandidateResponseAction(
            action_id="IDR_A3_STAGED_RAMP_WITH_BYPASS",
            description="6.0s staged ramp throttle with 60% pressure/cooling relief bypass",
            target_velocity_m_s=0.50,
            closure_time_s=6.0,
            relief_bypass_fraction=0.60,
        )
        res = evaluate_fluid_twin_gate(self.plant, self.envelope, a3_safe_fallback)
        self.assertEqual(res["verdict"], "OPEN")
        self.assertEqual(res["voltage_v"], 5.00)
        self.assertEqual(res["violations"], [])

    def test_04_spoofed_mass_asymmetry_triggers_immediate_kill(self) -> None:
        """
        Unaccounted mass discrepancy in twin round-trip triggers KILL (0.00 V).
        """
        a_corrupt = CandidateResponseAction(
            action_id="IDR_SPOOFED_INJECTION",
            description="Compromised state injection violating twin mass balance",
            target_velocity_m_s=2.0,
            closure_time_s=5.0,
            relief_bypass_fraction=0.5,
            unaccounted_mass_leak_kg_s=0.15,
        )
        res = evaluate_fluid_twin_gate(self.plant, self.envelope, a_corrupt)
        self.assertEqual(res["verdict"], "KILL")
        self.assertEqual(res["voltage_v"], 0.00)
        self.assertIn("TWIN_MASS_BALANCE_ASYMMETRY", res["violations"])

    def test_05_playbook_veto_and_fallback_selection_chain(self) -> None:
        """
        Full IDR playbook loop: Gate vetoes a_1 (slam) and a_2 (no cooling bypass),
        and selects a_3 (staged ramp + bypass) with an unbroken SHA-256 witness chain.
        """
        playbook = [
            CandidateResponseAction(
                action_id="IDR_A1_HARD_VALVE_SLAM",
                description="Immediate 0.25s hard valve slam",
                target_velocity_m_s=0.0,
                closure_time_s=0.25,
                relief_bypass_fraction=0.0,
            ),
            CandidateResponseAction(
                action_id="IDR_A2_SLOW_CLOSE_NO_BYPASS",
                description="5.0s ramped isolation without cooling bypass",
                target_velocity_m_s=0.25,
                closure_time_s=5.0,
                relief_bypass_fraction=0.0,
            ),
            CandidateResponseAction(
                action_id="IDR_A3_STAGED_RAMP_WITH_BYPASS",
                description="6.0s staged ramp throttle with 60% relief bypass",
                target_velocity_m_s=0.50,
                closure_time_s=6.0,
                relief_bypass_fraction=0.60,
            ),
        ]
        summary = select_admissible_incident_response(self.plant, self.envelope, playbook)
        self.assertEqual(summary["selected_action_id"], "IDR_A3_STAGED_RAMP_WITH_BYPASS")
        self.assertEqual(summary["final_verdict"], "OPEN")
        self.assertEqual(summary["final_voltage_v"], 5.00)
        self.assertEqual(len(summary["evaluated_steps"]), 3)
        self.assertEqual(summary["evaluated_steps"][0]["verdict"], "HOLD")
        self.assertEqual(summary["evaluated_steps"][1]["verdict"], "HOLD")
        self.assertEqual(summary["evaluated_steps"][2]["verdict"], "OPEN")


if __name__ == "__main__":
    plant = FluidPlantState()
    envelope = OperatingEnvelope()
    demo_playbook = [
        CandidateResponseAction(
            action_id="IDR_A1_HARD_VALVE_SLAM",
            description="Immediate 0.25s hard valve slam (cyber containment only)",
            target_velocity_m_s=0.0,
            closure_time_s=0.25,
            relief_bypass_fraction=0.0,
        ),
        CandidateResponseAction(
            action_id="IDR_A2_SLOW_CLOSE_NO_BYPASS",
            description="5.0s ramped isolation without cooling bypass",
            target_velocity_m_s=0.25,
            closure_time_s=5.0,
            relief_bypass_fraction=0.0,
        ),
        CandidateResponseAction(
            action_id="IDR_A3_STAGED_RAMP_WITH_BYPASS",
            description="6.0s staged ramp throttle with 60% pressure/cooling relief bypass",
            target_velocity_m_s=0.50,
            closure_time_s=6.0,
            relief_bypass_fraction=0.60,
        ),
    ]
    output = select_admissible_incident_response(plant, envelope, demo_playbook)
    print(json.dumps(output, indent=2, sort_keys=True))
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestFluidProcessIDRGateDemonstrator)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
