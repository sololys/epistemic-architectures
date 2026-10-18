# 📡 INFRANETT v0.4: LOCAL-FIRST MESH PROTOCOL & DURABLE POSIX PERSISTENCE
### *Offline-by-Default Resilience, 20-Meter Physical Geofencing, and Airgap Courier Transport*

```text
========================================================================================
TEKNISK SPESIFIKASJON / MONOGRAF:
  DOKUMENT-ID             : INFRANETT-PROTOCOL-TORJUSEN-2026-v0.4
  FORFATTER               : Marius Egerhei Torjusen (ORCID: 0009-0006-0431-6637)
  SELSKAP & LOKUS         : TORJUSEN / ReismannPoint Systems / Brahman Ventures, Risør
  EPISTEMISK STATUS       : L1 DETERMINISTISK PROGRAMVARE · KANONISK PROTOKOLLSPESIFIKASJON
========================================================================================
```

---

## 1. Introduction

Distributed resilience cannot be achieved by delegating trust to centralized hyperscalers. When cloud connections sever, nodes operating under fail-open models crash or hang. Infranett implements an *Offline-by-Default* architecture where local storage and peer-to-peer physical proximity form the fundamental ground state ($\mathbf{GATE::HOLD}$).

---

## 2. Protocol Mechanics

### 2.1 Physical Geofence & Inverse Square Law

Proximity is enforced at the physical radio layer:

$$P_r(r) \propto \frac{P_t}{r^2}, \quad r > 20\text{ m} \implies \text{SNR} < \text{SNR}_{\text{min}} \iff \mathbf{GATE::HOLD}.$$

### 2.2 Durable-First POSIX Invariant

To prevent torn writes and memory corruption during power cuts, Infranett enforces:

$$\boxed{\text{fsync}(\text{COMMIT}) \prec \text{RAM-Mutation} \prec \text{Network-ACK}}$$

### 2.3 Noise_KK Cryptography

Mutual identity is established via pre-shared Ed25519 and Curve25519 static keys with zero-roundtrip initial payloads.

### 2.4 Airgap Courier Transport (Sneakernet)

When physical radio is unavailable, state is exported to cryptographic capsules:

$$\text{Sign}_{\text{Ed25519}}(\text{RFC8785}(\text{Capsule})) \implies \text{Return Receipt}.$$

---

## 3. Verification and Results

The protocol is verified across 89 deterministic test modules (`L1` software verification), including operating system process-kill crash tests (`test_infranett_posix_crash_real_process.py`) and idempotent cursor synchronization (`test_infranett_courier_engine.py`), yielding 100% deterministic pass rates.

## References

1. M. E. Torjusen, *Infranett Protocol Specification v0.4*, Risør, 2026 (see also [`06_TECHNICAL_CORE_DECENTRALIZED_SOVEREIGNTY_KPOD_INFRANETT.md`](06_TECHNICAL_CORE_DECENTRALIZED_SOVEREIGNTY_KPOD_INFRANETT.md)).
