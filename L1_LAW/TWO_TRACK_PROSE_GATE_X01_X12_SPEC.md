# L1_LAW // Two-Track Prose Consequence Gate Specification (`X.01`–`X.12`)

$$\boxed{\text{GENERATION} \neq \text{AUTHORIZATION} \neq \text{WITNESSED CONSEQUENCE}}$$

* **Surface:** `L1_LAW/TWO_TRACK_PROSE_GATE_X01_X12_SPEC.md`
* **Executable Gate Verifier:** [`L2_GATE/verify_two_track_prose_gate_x01_x12.py`](../L2_GATE/verify_two_track_prose_gate_x01_x12.py) (`4/4 PASS`, Python 3.10+ Standard Library only, `0 float` AST-verified)
* **Companion Notes:** [`REALISERINGSGRAMMATIKK_OG_PROSAENS_SUBTRAKTIVE_GEOMETRI.md`](../L3_NOTES/REALISERINGSGRAMMATIKK_OG_PROSAENS_SUBTRAKTIVE_GEOMETRI.md) · [`18_GODELS_INCOMPLETENESS_PHYSICAL_WITNESS.md`](../L3_NOTES/18_GODELS_INCOMPLETENESS_PHYSICAL_WITNESS.md) · [`24_FAIL_CLOSED_COGNITIVE_FRICTION_ODYSSEUS_PACT.md`](../L3_NOTES/24_FAIL_CLOSED_COGNITIVE_FRICTION_ODYSSEUS_PACT.md)
* **Epistemic Boundary:** `INSPIRED_BY != IMPLEMENTS != PROVES` · `STANDALONE_COMMIT_AUTHORITY = NONE` · `PHYSICAL_AUTHORITY = NONE` (`L1` deterministic software only)
* **Ledger Boundary:** Append-only POSIX `SHA-256` hash chain (`os.fsync` on file and parent directory at creation); not physical WORM hardware media.

---

## I. State Space, Galvanic Voltage Law & Exact Arithmetic

All arithmetic inside the gate operates strictly over exact integers (`int`, with `bool` rejected by `require_strict_int`) and exact rationals (`fractions.Fraction`, enforced by `require_strict_fraction`). Zero floating-point literals or `float` identifiers are permitted in the verifier source (`test_01_ast_zero_float`).

| `GateState` | Modeled Rail (`mV DC`) | Role across the Galvanic Air Gap |
| :--- | :---: | :--- |
| **`KILL`** | `0` | Grounded cutoff inside $\mathcal{F}$ for counterfeited scope, trope smuggling, domain collapse, SI violation, or sovereignty breach |
| **`HOLD`** | `0` | Reversible workshop / occupied Zero-Window deferral / uncertainty boundary straddle / Odysseus fatigue latch |
| **`ESCALATED_P_EXT`** | `0` | Internal `HOLD` deadline exceeded ($\tau > \tau_{\max}$): jurisdiction transfers `P_int -> P_ext` without auto-opening or silent `KILL` |
| **`KLAR`** | `0` | Outermost dry contact inside $\mathcal{F}$ ($\Delta_K = 0$, $\sum \text{permit} \le 1$) exposing `fracture_bound` with zero commit authority |
| **`REST_RESET`** | `0` | Witnessed rest-recovery record appended to the `SHA-256` chain (`rest_elapsed_ms >= min_rest_ms`) without erasing history |
| **`OPEN`** | `5000` | Simulated `L1` commit exclusively below the galvanic air gap via `cross_airgap(step_id, witness)` |

**Default Clock & Odysseus Bounds (`TwoTrackProseGateX01X12`):**
`tau_max_ms = 300_000`, `dtau_min_ms = 8_000`, `dtau_max_ms = 600_000`, `max_consecutive_opens = 7`, `min_rest_ms = 120_000`, `MAX_ECHO_JACCARD = Fraction(4, 5)`, `SPEED_OF_LIGHT_M_S = Fraction(299_792_458, 1)`.

---

## II. Twelve-Coordinate Fracture Matrix (`X.01`–`X.12`, 1-to-1 with `L2_GATE`)

| Coord. | Fracture Mode | Exact Law Enforced in `L2_GATE/verify_two_track_prose_gate_x01_x12.py` | Fail-Closed Verdict & Detail Code |
| :--- | :--- | :--- | :--- |
| **`X.01`** | **Scope Drift, Proof-Verb & WORM Overclaim** | Two-track delivery `(prose_surface, SkeletonTrack)`. Incomplete `claim`/`law_or_source`/`fracture_bound`, empty `premise_domain`, or invalid source tags outside `{"INSPIRED_BY", "IMPLEMENTS", "PROVES"}` hold. Pure `INSPIRED_BY` cannot carry proof-verbs (`PROOF_CLAIM_TOKENS`), universal quantifiers (`UNIVERSAL_SCOPE_TOKENS`), or negated existentials. Mixed `INSPIRED_BY` + `PROVES`/`IMPLEMENTS` and any universal prose quantifier require non-empty `negated_domains`. Software ledgers mentioning `WORM_CLAIM_TOKENS` without `"Hardware_WORM_Verified"` in `premise_domain` are cut. | `HOLD`: `DELTA_K_INCOMPLETE_SKELETON`, `DELTA_K_EMPTY_PREMISE_DOMAIN`, `DELTA_K_INVALID_SOURCE_TAG` · `KILL`: `AESTHETIC_USURPATION`, `X01_PROOF_VERB_WITHOUT_ANCHOR`, `X01_MIXED_SOURCE_UNFENCED_DRIFT`, `X01_UNBOUNDED_UNIVERSAL_DRIFT`, `X01_SOFTWARE_LEDGER_CLAIMED_AS_PHYSICAL_WORM` |
| **`X.02`** | **Co-Generative Strike & Dual-Clock Law** | When `co_generative_strike=True` without `decompiled_from_hold=True`, freeze at `0 mV DC`. When `hold_elapsed_ms > tau_max_ms`, clear matching pending `KLAR` frame and escalate `P_int -> P_ext` at `0 mV DC` (never silent `KILL`). | `HOLD`: `X02_COGENERATIVE_FREEZE_DECOMPILE_REQUIRED` · `ESCALATED_P_EXT`: `HOLD_TIMEOUT_ESCALATED_TO_P_EXT` |
| **`X.03`** | **Witness Reflex & Identity Gate** | Crossing the air gap via `cross_airgap` requires `witness.elapsed_ms >= dtau_min_ms` and non-empty `witness_id` and `evidence_id`, against an exact staged `_pending_klar` `step_id`. | `HOLD`: `AIRGAP_NO_MATCHING_KLAR_FRAME`, `X03_REFLEX_SIGNATURE_BLOCKED`, `X03_MISSING_WITNESS_ID` |
| **`X.04`** | **Kuleshov Prose Quarantine (`chmod 444`)** | Explicit `prose_refs` are forbidden. On every `OPEN`, prose-only content words (`content_words(prose_surface) - skeleton_all_words - domain_lexicon`) enter `_quarantined_tropes`; downstream reuse in `sk.claim` or `sk.premise_domain` is cut. | `KILL`: `X04_PROSE_SURFACE_LEAK`, `X04_ORTHOGONAL_TROPE_SMUGGLING::<tok>` |
| **`X.05`** | **Penrose Domain Collapse & Zero-Window** | At most one candidate may occupy `_pending_klar` ($\sum \text{permit} \le 1$). All `upstream_refs` must be previously `OPEN`. Cumulative `(active_domains | premise_domain) & (forbidden_domains | negated_domains)` must remain empty. | `HOLD`: `ZERO_WINDOW_AIRLOCK_OCCUPIED`, `UNVERIFIED_UPSTREAM_SKELETON` · `KILL`: `X05_DOMAIN_INTERSECTION_EMPTY::<clash>` |
| **`X.06`** | **Anti-Parrot Asymmetric Witness Receipt** | `witness.counter_bound` cannot be empty or a subset of `RUBBER_STAMP_TOKENS`, cannot claim physical `WORM` without `"Hardware_WORM_Verified"`, must have $\ge 3$ content words plus an explicit falsifier marker (`FALSIFIER_MARKERS`) or digit, and must have exact rational Jaccard overlap with `sk.fracture_bound` strictly below `Fraction(4, 5)`. | `HOLD`: `X06_RUBBER_STAMP_REJECTED`, `X06_COUNTER_BOUND_CLAIMS_PHYSICAL_WORM`, `X06_UNDERSPECIFIED_COUNTER_BOUND`, `X06_PARROT_OR_TRIVIAL_EDIT_REJECTED` |
| **`X.07`** | **7-Tuple SI Dimensions & Three-Way $\mathbb{Q}$-Interval Inclusion** | `RationalBound` carries 7-tuple SI exponents $(\text{kg}, \text{m}, \text{s}, \text{A}, \text{K}, \text{mol}, \text{cd})$ and exact `(low_closed, high_closed)` flags. Coupled `QuotientLaw` (`si_sub`) and `ProductLaw` (`si_add`) propagate exact interval bounds. For measurement box $M$ against law domain $K$: $M \cap K = \varnothing \to \mathrm{KILL}$; $M \cap K \neq \varnothing \land M \not\subseteq K \to \mathrm{HOLD}$; $M \subseteq K \to \mathrm{KLAR}$. | `KILL`: `X07_SI_DIMENSION_MISMATCH`, `X07_RATIONAL_INTERVAL_EMPTY`, `X07_QUOTIENT_SI_MISMATCH`, `X07_DERIVED_QUOTIENT_VIOLATION`, `X07_PRODUCT_SI_MISMATCH`, `X07_DERIVED_PRODUCT_VIOLATION` · `HOLD`: `X07_UNCERTAINTY_STRADDLES_BOUNDARY`, `X07_NONPOSITIVE_DENOMINATOR`, `X07_DERIVED_QUOTIENT_STRADDLE`, `X07_NEGATIVE_FACTOR`, `X07_DERIVED_PRODUCT_STRADDLE` |
| **`X.08`** | **Norwegian Morphological Stem Quarantine** | Deterministic inflection stripping (`NO_INFLECTION_SUFFIXES`, minimum stem length `4`) records prose-only stems outside `TECHNICAL_BASE_STEMS` on `OPEN`; downstream skeleton tokens matching exact stem or compound boundary (`len(q_stem) >= 5`) are cut. | `KILL`: `X08_MORPHOLOGICAL_TROPE_SMUGGLING::<tok><-<stem>@<origin>` |
| **`X.09`** | **Experimental Modality Orthogonality** | When `PhysicalTrack.requires_empirical_yield=True`, the union of locked and proposed `MeasurementChannel.modality_family` values must contain at least `2` distinct physical modalities. | `HOLD`: `X09_MISSING_ORTHOGONAL_MODALITY` |
| **`X.10`** | **Sovereignty Invariant & Latched Odysseus Rest Shield** | `SkeletonTrack.ai_authority_share` must equal `Fraction(0, 1)`. Claims of internal `OPEN` before `W_ext` (`claims_internal_open_before_witness=True`) are cut. Inside `cross_airgap`, hitting `consecutive_opens >= max_consecutive_opens` or `elapsed_ms > dtau_max_ms` latches `_fatigue_latched = True` at `0 mV DC` until `witness_rest_reset(witness_id, rest_elapsed_ms >= min_rest_ms)` records `REST_RESET`. | `KILL`: `X10_SOVEREIGNTY_INVARIANT_BREACH`, `GODEL_AIRGAP_BREACH_INTERNAL_OPEN_CLAIMED` · `HOLD`: `X10_ULYSSES_FATIGUE_LATCHED_0MV`, `X10_STALE_ATTENTION_LATCHED_0MV`, `REST_INSUFFICIENT` |
| **`X.11`** | **Hume's Guillotine & Three Closed Carriers** | `OntologicalCarrier` partitions steps into `OBS_SOMATIC`, `LEX_SOVEREIGN`, and `LAW_FORMAL_PHYS`. Neither `OBS_SOMATIC` nor `LEX_SOVEREIGN` may claim `PROVES`. `LAW_FORMAL_PHYS` with `PROVES` cannot derive solely from `OBS_SOMATIC` upstream. `LEX_SOVEREIGN` with upstream references cannot derive solely from descriptive carriers without an upstream `LEX_SOVEREIGN` step or a constitutional `IMPLEMENTS:` prefix (`lex_`, `ulysses_`, `const_`, `arch_axiom`). | `KILL`: `X11_CARRIER_CANNOT_PROVE_THEOREM::<carrier>`, `X11_SOMATIC_TO_FORMAL_USURPATION`, `X11_HUMES_GUILLOTINE_IS_TO_OUGHT` |
| **`X.12`** | **V2-Safe Negated Existential Window** | `has_negated_existential_window(tokens, max_gap=2)` detects existential verbs (`EXISTENTIAL_VERBS`) followed within `1..3` tokens by `NEGATION_OR_UNIVERSAL_MODIFIERS` (e.g., *«finnes ikke»*, *«finnes det ikke»*). Any match without non-empty `negated_domains` is cut. | `KILL`: `X12_NEGATED_EXISTENTIAL_WITHOUT_BOUNDARY` |

---

## III. Data Contracts & Verification Interface (`L2_GATE`)

* **Input Structures:** `CandidateLine`, `SkeletonTrack`, `PhysicalTrack`, `RationalBound`, `QuotientLaw`, `ProductLaw`, `MeasurementChannel`, `ExternalWitness`.
* **Gate Methods (`TwoTrackProseGateX01X12`):**
  1. `evaluate_in_f(cand, phys=PhysicalTrack(), hold_elapsed_ms=0) -> tuple[GateState, str]` — evaluates all `F`-side invariants and stages at most one `KLAR` frame at `0 mV DC`.
  2. `cross_airgap(step_id, witness) -> tuple[GateState, str]` — enforces `X.03`, `X.06`, and `X.10`, commits state/quarantine/domain updates on `OPEN (5000 mV DC)`, and appends a `SHA-256`-linked record with `os.fsync`.
  3. `witness_rest_reset(witness_id, rest_elapsed_ms) -> tuple[bool, GateState, str]` — clears `_fatigue_latched` and `_consecutive_opens` only when `rest_elapsed_ms >= min_rest_ms`, appending `REST_RESET (0 mV DC)`.
* **Chain Audit (`verify_wal_chain(wal_path)`):** Verifies genesis link (`"0" * 64`), sequential `prev` chaining, `millivolts_dc == state_millivolts_dc(state)`, and canonical `SHA-256` digest parity (`BROKEN_PREV_LINK`, `VOLTAGE_INVARIANT_VIOLATION`, `DIGEST_MISMATCH`). Startup fails closed (`RuntimeError("CORRUPT_WAL::...")`) on any tampered log.
