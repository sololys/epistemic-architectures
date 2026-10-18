# Introduction

Distributed resilience cannot be achieved by delegating trust to
centralized hyperscalers. When cloud connections sever, nodes operating
under fail-open models crash or hang. Infranett implements an
*Offline-by-Default* architecture where local storage and peer-to-peer
physical proximity form the fundamental ground state
($\mathbf{GATE::HOLD}$).

# Protocol Mechanics

![Infranett Airgap Courier Still Life: Titanium hardware courier data
capsule, Morandi ceramic jugs, and a vacuum-tube node projecting the
20-meter
geofence.](art/03_morandi_infranett_capsule.jpg){#fig:infranett_art
width="\\columnwidth"}

## Physical Geofence & Inverse Square Law

Proximity is enforced at the physical radio layer:
$$P_r(r) \propto \frac{P_t}{r^2}, \quad r > 20\text{ m} \implies \text{SNR} < \text{SNR}_{\text{min}} \iff \mathbf{GATE::HOLD}.$$

## Durable-First POSIX Invariant

To prevent torn writes and memory corruption during power cuts,
Infranett enforces:
$$\boxed{\text{fsync}(\text{COMMIT}) \prec \text{RAM-Mutation} \prec \text{Network-ACK}}$$

## Noise_KK Cryptography

Mutual identity is established via pre-shared Ed25519 and Curve25519
static keys with zero-roundtrip initial payloads.

## Airgap Courier Transport (Sneakernet)

When physical radio is unavailable, state is exported to cryptographic
capsules:
$$\text{Sign}_{\text{Ed25519}}(\text{RFC8785}(\text{Capsule})) \implies \text{Return Receipt}.$$

# Verification and Results

The protocol is verified across 89 monorepo test modules, including real
operating system crash tests
('test_infranett_posix_crash_real_process.py') and cursor
synchronization ('test_infranett_courier_engine.py'), yielding 100%
deterministic pass rates.

::: thebibliography
1 M. E. Torjusen, *Infranett Protocol Specification v0.4*, Risør, 2026.
:::
