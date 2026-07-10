# Repository Governance Map

Snapshot: 2026-07-10

This document defines the public-safe topology of the Realiseringsgrammatikk research-and-artifact ecosystem. Its purpose is to make repository roles, authority, promotion paths, and archival rules explicit.

Generated material is not automatically canonical. A repository location does not itself authorize a claim, release, or consequence.

## Authority classes

- `PUBLIC_CANON` — stable public definitions and citation anchors.
- `ARTIFACT_AUTHORITY` — verified software artifacts, manifests, run logs, and release packages.
- `WORKING_SPACE` — drafts, notes, protocol candidates, and unstable experiments.
- `PUBLIC_SURFACE` — redacted demonstrators and external communication material.
- `EXTERNAL_NON_CANONICAL` — external collaboration or upstream work that is not part of the internal canon.

## Public-safe repository register

| Repository | Role | Authority | Visibility | Status | Promotion target | Archive rule |
|---|---|---|---|---|---|---|
| `sololys/epistemic-architectures` | Stable theory anchor and citation reference | `PUBLIC_CANON` | Public | `OPEN / STABLE / NON-OPERATIONAL` | None; this is the public conceptual authority | Preserve cited and tagged states; never rewrite release history |
| `sololys/epistemic-architectures-notes` | Working notes, sketches, extensions, and examples | `WORKING_SPACE` | Public | `OPEN / NON-CANONICAL` | Promote reviewed definitions to `epistemic-architectures` | Archive or mark notes after promotion; retain source history and backlinks |
| `sololys/realiseringsgrammatikk-artifact-family` | Artifact family, microtests, specifications, release bundles, and deterministic demonstrations | `ARTIFACT_AUTHORITY` | Private | `OPEN / ACTIVE` | Promote stable public-safe theory to `epistemic-architectures`; promote redacted demonstrations to `ky-rox-public-demonstrators` | Keep superseded artifacts immutable, hashed, and clearly marked as superseded or deprecated |
| `sololys/Poronesis-lab` | Experimental lab for drafts, protocol candidates, RTL/software simulations, and evolving formalization | `WORKING_SPACE` | Private | `OPEN / LAB` | Promote verified artifacts to `realiseringsgrammatikk-artifact-family`; promote stable definitions to `epistemic-architectures` | Retain failed and abandoned experiments with explicit status; tag only after verified PASS |
| `sololys/ky-rox-public-demonstrators` | Public showroom and deterministic demonstration surface | `PUBLIC_SURFACE` | Public | `OPEN / PUBLIC-SAFE` | No authority promotion from presentation alone; reusable verified components return through the artifact authority | Archive replaced demonstrations only after a successor and redirect exist |
| `sololys/loop-engineering` | External collaboration and upstream agent-loop engineering work | `EXTERNAL_NON_CANONICAL` | Public | `EXTERNAL / ACTIVE` | No direct promotion; any imported pattern requires independent review and attribution | Preserve external contribution history; keep forks and internal canon separate |

## Promotion grammar

```text
working note / lab candidate
  -> deterministic verification
  -> artifact authority
  -> editorial and claim review
  -> public theory anchor or public demonstrator
```

Promotion is explicit. Copying, linking, popularity, or repeated use does not make material canonical.

### Theory promotion

```text
notes or lab draft
  -> definition stabilized
  -> conflicting terms resolved
  -> claim scope reviewed
  -> citation surface updated
  -> PUBLIC_CANON
```

### Artifact promotion

```text
candidate implementation
  -> tests
  -> deterministic rerun
  -> run log
  -> manifest / hash verification
  -> release or tagged artifact
```

### Public release promotion

```text
private artifact
  -> protected-core review
  -> redaction
  -> claim review
  -> public demonstrator
```

## Reading order

1. Start with `epistemic-architectures` for the conceptual frame.
2. Use `realiseringsgrammatikk-artifact-family` for concrete artifacts, manifests, and microtests when access is authorized.
3. Use `Poronesis-lab` for evolving protocol work and experimental material when access is authorized.
4. Use `ky-rox-public-demonstrators` for public-facing explanations and deterministic demonstrations.
5. Treat `epistemic-architectures-notes` as exploratory and non-canonical.
6. Treat `loop-engineering` as external collaboration, not as Realiseringsgrammatikk authority.

## Private registry boundary

The full inventory of private control archives, application verticals, IP-sensitive work, dormant repositories, and repository-maintenance decisions is intentionally not enumerated in this public document.

The authoritative complete register is maintained in the private control archive. Public omission is deliberate and must not be interpreted as absence, abandonment, or lack of provenance.

## Governance rules

- One repository must have one primary role.
- Canonical definitions must name their authority source.
- Working repositories must identify themselves as non-canonical or provisional.
- Public repositories must exclude protected thresholds, interlock details, witness internals, unpublished algorithms, and patent-sensitive mechanisms.
- Domain-specific repositories may specialize the grammar but must not silently redefine the shared core.
- Empty or orphaned repositories remain `HOLD` until assigned a role, activated, absorbed, or archived.
- Renaming a repository requires redirect, clone-remote update, documentation update, and link audit.

## Boundary

These repositories contain architectural, conceptual, software, documentation, and research artifacts. They must not be read as deployed safety systems, certified hardware implementations, empirical validation of speculative physics, legal or regulatory certification, or proof of a complexity-class collapse.

```text
CANDIDATE != CONSEQUENCE
LOCATION != AUTHORITY
PUBLICATION != VALIDATION
PROMOTION_REQUIRES_GATE
```
