# EPISTEMIC ARCHITECTURES // MORANDI-CORE PROOF INDEX

$$\boxed{\text{GENERATION} \neq \text{AUTHORIZATION} \neq \text{WITNESSED CONSEQUENCE}}$$

$$\Phi(x_t) \;\xrightarrow{\;\text{Candidate}\;}\; \Pi_K \;\xrightarrow{\;\text{Residual }\Delta_K\;}\; \Omega \in \{\mathrm{KILL}, \mathrm{HOLD}, \mathrm{OPEN}\} \;\xrightarrow{\;\text{Pre-Commit}\;}\; W^2 = \langle W_{\mathrm{machine}}, W_{\mathrm{human}}\rangle$$

* **Author:** Marius Egerhei Torjusen · Brahman, Risør, Norway ([ORCID: `0009-0006-0431-6637`](https://orcid.org/0009-0006-0431-6637) · [Zenodo DOI: `10.5281/zenodo.18436983`](https://doi.org/10.5281/zenodo.18436983))
* **Epistemic Boundary:** `INSPIRED_BY != IMPLEMENTS != PROVES` · `PHYSICAL_AUTHORITY = NONE` · $\Sigma_{\mathrm{ext}} = \emptyset$ (Python Standard Library only)

---

## I. EXECUTION CONTRACT (`Makefile`)

The root directory contains only this surface index (`README.md`) and the formal build contract ([`Makefile`](Makefile)). Implicit execution (`make`) is rejected fail-closed.

```bash
make verify                                            # [1/3] L1_LAW (*_pure.py) -> [2/3] L2_GATE (Pi_K) -> [3/3] HOLD (0.00 V DC)
python3 L2_GATE/verify_w2_five_proof_chains.py         # Verifies all 5 W^2 mathematical proof chains (OPEN / HOLD / KILL)
python3 L2_GATE/verify_norcics_digital_twin_llm_gate.py # Verifies SFI NORCICS / CPS4CIP Domains I-IV (4/4 PASS, 0.000s)
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

## II. DOMAIN SEGREGATION (THE FOUR ROOMS)

| Room | Epistemic Rule | Primary Artifacts |
| :--- | :--- | :--- |
| **[`L1_LAW/`](L1_LAW/)** | Pure mathematical definitions & formal contracts. Zero I/O, zero side effects. | • [`L1_LAW/IT_OT_CONSEQUENCE_GATE_NORCICS_BRIEF.md`](L1_LAW/IT_OT_CONSEQUENCE_GATE_NORCICS_BRIEF.md) · [**PDF Brief**](L1_LAW/IT_OT_CONSEQUENCE_GATE_NORCICS_BRIEF.pdf)<br>• [`L1_LAW/W2_FIVE_PROOF_CHAINS_SPEC.md`](L1_LAW/W2_FIVE_PROOF_CHAINS_SPEC.md)<br>• [`L1_LAW/invariants_pure.py`](L1_LAW/invariants_pure.py) |
| **[`L2_GATE/`](L2_GATE/)** | Consequence gate ($\Omega \circ \Pi_K$) & deterministic boundary evaluation. | • [`L2_GATE/evaluate_boundaries.py`](L2_GATE/evaluate_boundaries.py)<br>• [`L2_GATE/verify_w2_five_proof_chains.py`](L2_GATE/verify_w2_five_proof_chains.py)<br>• [`L2_GATE/verify_norcics_digital_twin_llm_gate.py`](L2_GATE/verify_norcics_digital_twin_llm_gate.py)<br>• [`L2_GATE/verify_cos45_kms_spectral_series.py`](L2_GATE/verify_cos45_kms_spectral_series.py)<br>• [`L2_GATE/verify_public_surface.py`](L2_GATE/verify_public_surface.py) |
| **[`L3_WITNESS/`](L3_WITNESS/)** | Append-only cryptographic SHA-256 receipts ($W^2$) of verified transitions. | • [`L3_WITNESS/audit_log.jsonl`](L3_WITNESS/audit_log.jsonl) |
| **[`L3_NOTES/`](L3_NOTES/)** | Theoretical monographs, working derivations & counterexamples ($\text{THEORY} \neq \text{DEMONSTRATOR}$). | • [`L3_NOTES/W2_BOUNDARY_COUNTEREXAMPLES.md`](L3_NOTES/W2_BOUNDARY_COUNTEREXAMPLES.md)<br>• [`L3_NOTES/LAW_OF_CAUSAL_INERTIA.md`](L3_NOTES/LAW_OF_CAUSAL_INERTIA.md)<br>• [`L3_NOTES/MORISSETTE_TORJUSEN_COS45_FRONTIER_AND_PROTOCOL.md`](L3_NOTES/MORISSETTE_TORJUSEN_COS45_FRONTIER_AND_PROTOCOL.md)<br>• [`L3_NOTES/DOCUMENT_173_AUTHORIZED_REALIZATIONS.md`](L3_NOTES/DOCUMENT_173_AUTHORIZED_REALIZATIONS.md)<br>• [`L3_NOTES/KY_NASH_ADMISSIBLE_GAMES.md`](L3_NOTES/KY_NASH_ADMISSIBLE_GAMES.md)<br>• [`L3_NOTES/00`–`26` Causal Inertia Suite](L3_NOTES/) |

---

## III. STATE-MACHINE AUTHORIZATION LAW

$$V_{\mathrm{out}} = \lim_{\Delta_K \to 0} \left( \mathbb{I}(\Omega(\Pi_K) == \mathrm{OPEN}) \cdot W^2 \cdot 5.00\,\mathrm{V\ DC} \right) = \begin{cases} 5.00\,\mathrm{V\ DC}\;(\text{L1-simulated}), & \text{if } \prod_{k=1}^5 \mathbb{I}(\Delta_{K,k} \le \epsilon_k) = 1 \land W^2 = 1 \\ 0.00\,\mathrm{V\ DC}, & \text{default fail-closed stasis (HOLD / KILL)} \end{cases}$$

---

## Citation

Torjusen, M. E. (2026). *Epistemic Architectures: Systems That Know They Know.* Zenodo. [https://doi.org/10.5281/zenodo.18436983](https://doi.org/10.5281/zenodo.18436983).
