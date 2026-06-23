# Epistemic Architectures

Stable reference anchor for epistemic architectures, supervisory control, AI governance, and fail-closed realization grammars.

## Start here

Generated candidates are not consequences.

This work studies systems where proposed transitions must pass explicit admissibility, structural, and governance checks before they can become authorized outcomes.

Canonical path:

```text
candidate -> admissibility test -> gate decision -> witnessed consequence
```

In short: dynamics may generate possibilities; the architecture decides what can be safely realized.

---

**Torjusen, M. E. (2026).**  
*Epistemic Architectures: Systems That Know They Know.*  
Working paper, Zenodo.  
DOI: https://doi.org/10.5281/zenodo.18436983

---

## Repository role

This repository is a stable theory anchor and citation point.

It is intentionally conservative: it preserves architectural definitions, separation of concerns, and epistemic constraints. Active demonstrators, implementation artifacts, and experimental software notes are maintained in companion repositories.

Suggested reading path:

- `sololys/epistemic-architectures` — theory anchor and citation reference.
- `sololys/realiseringsgrammatikk-artifact-family` — artifact family, microtests, specifications, and release packages.
- `sololys/Poronesis-lab` — lab notes, drafts, and evolving protocol work.
- `sololys/ky-rox-public-demonstrators` — public-facing demonstrators and external presentation material.

See `REPOSITORY_MAP.md` for the compact ecosystem map.

---

## Scope

This repository focuses on architectural and conceptual structure rather than runtime implementation.

It describes form, separation of concerns, and epistemic constraints for systems that must distinguish generated candidates from realized consequences.

Topics include:

- epistemic uncertainty and confidence-aware operation,
- supervisory control and governance overlays,
- finite-state supervision and graceful degradation,
- admissibility testing before irreversible consequence,
- separation of governance logic from task-level optimization.

---

## Status

Stable reference repository / descriptive architecture / non-operational.

This repository does not provide a deployed safety system, certified control system, physical hardware validation, or empirical physics validation. It is a structured reference point for ongoing work in companion repositories.

---

## Author

**Marius Egerhei Torjusen**  
ORCID: https://orcid.org/0009-0006-0431-6637

---

## Citation

If you reference this repository, please cite the associated working paper:

Torjusen, M. E. (2026).  
*Epistemic Architectures: Systems That Know They Know.*  
Zenodo. https://doi.org/10.5281/zenodo.18436983  
License: CC BY-ND 4.0

---

## About

Epistemic architectures are systems that make uncertainty, admissibility, authorization, and consequence explicit.

This repository is descriptive, not normative. It is designed to be read as an architectural reference, not as an executable runtime or certification claim.
