# Epistemic Architectures — Specifications & Transition Rules

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24032510.svg)](https://doi.org/10.5281/zenodo.24032510)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--0431--6637-A6CE39?style=flat-square)](https://orcid.org/0009-0006-0431-6637)
[![Granitum Physics](https://img.shields.io/badge/SALON-Granitum_Physics_(LinkedIn)-0A66C2?style=flat-square)](https://www.linkedin.com/groups/40622443/)

> **Coordinate (`3 · Rule`):** [`(0,0) sololys`](https://github.com/sololys) — [`1 · Word`](https://github.com/sololys/skrivevaerelset) → [`2 · Draft`](https://github.com/sololys/epistemic-architectures-notes) → **`[3 · Rule]`** → [`4 · Gate`](https://github.com/sololys/ky-rox-public-demonstrators) → [`5 · Seal`](https://github.com/sololys/monolitt)

Formal specifications, transition rules, and standalone Python verifiers separating cheap candidate proposals from authorized state transitions. Ongoing mathematical drafts live upstream in [`epistemic-architectures-notes`](https://github.com/sololys/epistemic-architectures-notes); runnable multi-domain and SystemVerilog gate prototypes live downstream in [`ky-rox-public-demonstrators`](https://github.com/sololys/ky-rox-public-demonstrators).

$$\Phi(x_t) \;\xrightarrow{\;\text{Candidate}\;}\; \Pi_K \;\xrightarrow{\;\text{Residual }\Delta_K\;}\; \Omega \in \{\mathrm{KILL}, \mathrm{HOLD}, \mathrm{OPEN}\} \;\xrightarrow{\;\text{Pre-Commit}\;}\; W^2 = \langle W_{\mathrm{machine}}, W_{\mathrm{human}}\rangle$$

* **Author:** Marius Egerhei Torjusen · Risør, Norway ([ORCID `0009-0006-0431-6637`](https://orcid.org/0009-0006-0431-6637))
* **Epistemic Boundary (`INSPIRED_BY != IMPLEMENTS != PROVES`):** Local `L1` software specifications and deterministic verifiers only (`0.00 V DC`, zero physical authority). Uses only the Python 3.10+ Standard Library (`pip install` not needed).

---

## I. Run & Verify (`Makefile`)

Implicit execution (`make`) fails closed by design; pass an explicit verification target:

```bash
make verify                                              # [1/3] L1_LAW (*_pure.py) -> [2/3] L2_GATE (Pi_K) -> [3/3] HOLD (0.00 V DC)
python3 L2_GATE/verify_ky_nash_and_dual_clock_gate.py    # Exact rational KY-Nash & Dual-Clock Law gate (5/5 PASS, zero float)
python3 L2_GATE/verify_w2_five_proof_chains.py           # Verifies all 5 W^2 proof chains (OPEN / HOLD / KILL, 5/5 PASS)
python3 L2_GATE/verify_norcics_digital_twin_llm_gate.py  # SFI NORCICS / CPS4CIP Domains I-IV (SHA-256 chain below)
python3 L2_GATE/verify_fluid_process_idr_twin_gate.py    # Fluid/process IDR digital twin gate (Joukowsky surge & thermal veto)
python3 L2_GATE/verify_mpolynomial_1wl_molecular_gate.py # M-Polynomial & 1-WL Molecular Gate Pi_K ([Fe7MoS9C], 6/6 PASS)
python3 L2_GATE/verify_pwr2_scrambling_collective_gate.py # PWR2 & Power-Law Spin Scrambling vs. Collective Gate (6/6 PASS)
python3 L2_GATE/verify_davisson_fine_newtonian_gate.py   # Davisson-Fine-Newtonian Consequence Gate (20/20 PASS)
python3 L2_GATE/verify_cos45_kms_spectral_series.py      # KMS Toeplitz cos(45 deg) spectral convergence trace
python3 L2_GATE/verify_public_surface.py                 # Verifies exact allowlisted public file tree
```

<details>
<summary><strong>Zero-Trust Static Verification Trace (Pre-Computed SHA-256 Witness Chain: <code>a30d7c93...ba785</code>)</strong></summary>

For reviewers inspecting without local script execution, [`L2_GATE/verify_norcics_digital_twin_llm_gate.py`](L2_GATE/verify_norcics_digital_twin_llm_gate.py) evaluates Domains I–IV deterministically using only the Python Standard Library (`hashlib`, `json`, `math`, `sys`, `unittest`):

```json
{
  "master_chain_sha256": "a30d7c934eaaa8b08600ae5ca54376df5440ac757a23fb6c6d4f2cbbd32ba785",
  "steps": [
    {
      "ancestor": "0000000000000000000000000000000000000000000000000000000000000000",
      "domain": "I_DIGITAL_TWIN_DOOR25",
      "reason": "TWIN_ASYMMETRY_DETECTED",
      "residual_iso": 0.05,
      "s0": [2.0, 3.0],
      "sf": [3.55, 2.0],
      "sr": [2.05, 3.0],
      "verdict": "KILL",
      "voltage_v": 0.0,
      "within_envelope": true,
      "witness_sha256": "1f85263c6a18673da92bc5d2c4969abef545880934b35e55dde1938f4a9c2691"
    },
    {
      "ancestor": "1f85263c6a18673da92bc5d2c4969abef545880934b35e55dde1938f4a9c2691",
      "domain": "II_CONSTRAINED_LLM_HMI",
      "h_val": 0.2,
      "nagumo_lhs": -0.3,
      "reason": "RC-BARRIER-BREACH-KILL",
      "verdict": "KILL",
      "voltage_v": 0.0,
      "w2_valid": true,
      "witness_sha256": "051345c452bcbb22cd7908d0e44cc0a3380e18d00fb76972e914e04c5f2023f0"
    },
    {
      "ancestor": "051345c452bcbb22cd7908d0e44cc0a3380e18d00fb76972e914e04c5f2023f0",
      "d_tof_m": 14.989623,
      "domain": "III_MARITIME_UWB_LIGHTCONE",
      "gnss_divergence_m": 30.010377,
      "reason": "RC-CAUSAL-LIGHTCONE-VIOLATION",
      "s_obs_aoa": 0.5,
      "verdict": "HOLD",
      "voltage_v": 0.0,
      "witness_sha256": "b7ca2668dc98096554910cd2a5ebe12c0e2f487d16202bfa303ecebae551cd07"
    },
    {
      "active_votes": 3,
      "ancestor": "b7ca2668dc98096554910cd2a5ebe12c0e2f487d16202bfa303ecebae551cd07",
      "domain": "IV_VSG_DISPERSION_BFT",
      "mu_eff_rad_s": 10.0,
      "omega_rad_s": 12.0,
      "product_warrant": 1,
      "quorum_required": 3,
      "reason": "VSG_DISPERSION_QUORUM_PASS",
      "verdict": "OPEN",
      "voltage_v": 5.0,
      "witness_sha256": "0dd48e7eb23a5bdf56a7f9840ee29d4ab2560ef3ce8c470e1e86c365fcd920f2"
    }
  ]
}
```
</details>

---

## II. Directory Map

| Directory | Role | Primary Artifacts |
| :--- | :--- | :--- |
| **[`L1_LAW/`](L1_LAW/)** | Pure mathematical definitions & formal contracts (zero I/O, zero side effects). | • [`L1_LAW/IT_OT_CONSEQUENCE_GATE_NORCICS_BRIEF.md`](L1_LAW/IT_OT_CONSEQUENCE_GATE_NORCICS_BRIEF.md) · [**PDF Brief**](L1_LAW/IT_OT_CONSEQUENCE_GATE_NORCICS_BRIEF.pdf)<br>• [`L1_LAW/KY_NASH_SPILLTEORI_HANDBOK.pdf`](L1_LAW/KY_NASH_SPILLTEORI_HANDBOK.pdf) · [`KY_NASH_GAME_THEORY_ONEPAGER.pdf`](L1_LAW/KY_NASH_GAME_THEORY_ONEPAGER.pdf)<br>• [`L1_LAW/W2_FIVE_PROOF_CHAINS_SPEC.md`](L1_LAW/W2_FIVE_PROOF_CHAINS_SPEC.md)<br>• [`L1_LAW/MPOLYNOMIAL_1WL_MOLECULAR_GATE_SPEC.md`](L1_LAW/MPOLYNOMIAL_1WL_MOLECULAR_GATE_SPEC.md)<br>• [`L1_LAW/PWR2_SCRAMBLING_COLLECTIVE_GATE_SPEC.md`](L1_LAW/PWR2_SCRAMBLING_COLLECTIVE_GATE_SPEC.md)<br>• [`L1_LAW/DAVISSON_FINE_NEWTONIAN_GATE_SPEC.md`](L1_LAW/DAVISSON_FINE_NEWTONIAN_GATE_SPEC.md)<br>• [`L1_LAW/122_G2_HOLONOMIC_SPIRAL_ZERO_DIVISOR_EVASION_SPEC.md`](L1_LAW/122_G2_HOLONOMIC_SPIRAL_ZERO_DIVISOR_EVASION_SPEC.md) · [**PDF Spec**](L1_LAW/122_G2_HOLONOMIC_SPIRAL_ZERO_DIVISOR_EVASION_SPEC.pdf)<br>• [`L1_LAW/invariants_pure.py`](L1_LAW/invariants_pure.py) · [`STACK_MAP_v0.1.md`](STACK_MAP_v0.1.md) |
| **[`L2_GATE/`](L2_GATE/)** | Consequence gate ($\Omega \circ \Pi_K$) & deterministic boundary verifiers. | • [`L2_GATE/evaluate_boundaries.py`](L2_GATE/evaluate_boundaries.py)<br>• [`L2_GATE/verify_ky_nash_and_dual_clock_gate.py`](L2_GATE/verify_ky_nash_and_dual_clock_gate.py)<br>• [`L2_GATE/verify_w2_five_proof_chains.py`](L2_GATE/verify_w2_five_proof_chains.py)<br>• [`L2_GATE/verify_norcics_digital_twin_llm_gate.py`](L2_GATE/verify_norcics_digital_twin_llm_gate.py)<br>• [`L2_GATE/verify_fluid_process_idr_twin_gate.py`](L2_GATE/verify_fluid_process_idr_twin_gate.py)<br>• [`L2_GATE/verify_mpolynomial_1wl_molecular_gate.py`](L2_GATE/verify_mpolynomial_1wl_molecular_gate.py)<br>• [`L2_GATE/verify_pwr2_scrambling_collective_gate.py`](L2_GATE/verify_pwr2_scrambling_collective_gate.py)<br>• [`L2_GATE/verify_davisson_fine_newtonian_gate.py`](L2_GATE/verify_davisson_fine_newtonian_gate.py)<br>• [`L2_GATE/verify_cos45_kms_spectral_series.py`](L2_GATE/verify_cos45_kms_spectral_series.py)<br>• [`L2_GATE/verify_public_surface.py`](L2_GATE/verify_public_surface.py) |
| **[`L3_WITNESS/`](L3_WITNESS/)** | Append-only SHA-256 hash-chain log ($W^2$) of local `make witness` runs. | • [`L3_WITNESS/audit_log.jsonl`](L3_WITNESS/audit_log.jsonl) *(software hash chain, not physical WORM hardware)* |
| **[`L3_NOTES/`](L3_NOTES/)** | Archived background monographs & counterexamples (`00`–`26`); active working derivations live in [`epistemic-architectures-notes`](https://github.com/sololys/epistemic-architectures-notes). | • [`L3_NOTES/KY_NASH_ADMISSIBLE_GAMES.md`](L3_NOTES/KY_NASH_ADMISSIBLE_GAMES.md) · [`L3_NOTES/THE_UNIFIED_FIELD_NASH_DUALITY.md`](L3_NOTES/THE_UNIFIED_FIELD_NASH_DUALITY.md) · [`L3_NOTES/NASH_MATHEMATICAL_INVARIANTS_AND_STRUCTURES.md`](L3_NOTES/NASH_MATHEMATICAL_INVARIANTS_AND_STRUCTURES.md) *(L2 verifier: [`verify_ky_nash_and_dual_clock_gate.py`](L2_GATE/verify_ky_nash_and_dual_clock_gate.py))*<br>• [`L3_NOTES/W2_BOUNDARY_COUNTEREXAMPLES.md`](L3_NOTES/W2_BOUNDARY_COUNTEREXAMPLES.md)<br>• [`L3_NOTES/LAW_OF_CAUSAL_INERTIA.md`](L3_NOTES/LAW_OF_CAUSAL_INERTIA.md)<br>• [`L3_NOTES/MORISSETTE_TORJUSEN_COS45_FRONTIER_AND_PROTOCOL.md`](L3_NOTES/MORISSETTE_TORJUSEN_COS45_FRONTIER_AND_PROTOCOL.md)<br>• [`L3_NOTES/DOCUMENT_173_AUTHORIZED_REALIZATIONS.md`](L3_NOTES/DOCUMENT_173_AUTHORIZED_REALIZATIONS.md)<br>• [`L3_NOTES/00`–`26` Causal Inertia Archive](L3_NOTES/) ([Zenodo DOI: `10.5281/zenodo.22229111`](https://doi.org/10.5281/zenodo.22229111)) |

---

## III. State-Machine Authorization Rule

A simulated transition leaves `0.00 V DC` (`HOLD` / `KILL`) only when every bounded residual $\Delta_{K,k}$ is within tolerance $\epsilon_k$ and an explicit pre-commit witness $W^2$ is present:

$$V_{\mathrm{out}} = \begin{cases} 5.00\,\mathrm{V\ DC}\;\text{(L1-simulated)}, & \text{if } \Omega(\Pi_K(x)) = \mathrm{OPEN} \;\land\; \prod_{k=1}^5 \mathbb{I}(\Delta_{K,k} \le \epsilon_k) = 1 \;\land\; W^2 = 1 \\ 0.00\,\mathrm{V\ DC}, & \text{otherwise (default fail-closed HOLD / KILL)} \end{cases}$$

---

## Citation & License

* Torjusen, M. E. (2026). *Epistemic Architectures: Formal Realization Grammar, KY-Nash Mechanism Design & IT/OT Consequence Specifications.* Zenodo. [https://doi.org/10.5281/zenodo.24032510](https://doi.org/10.5281/zenodo.24032510).
* Torjusen, M. E. (2026). *Epistemic Architectures: Systems That Know They Know.* Zenodo. [https://doi.org/10.5281/zenodo.18436983](https://doi.org/10.5281/zenodo.18436983).
* Torjusen, M. E. (2026). *The Law of Causal Inertia: Scientific & Architectural Monograph Series.* Zenodo. [https://doi.org/10.5281/zenodo.22229111](https://doi.org/10.5281/zenodo.22229111).
* **Metadata & Terms:** [`CITATION.cff`](CITATION.cff) · [`LICENSE`](LICENSE) · [`NOTICE`](NOTICE)
