# Domain IV Addendum: Stoichiometric & Hardware-Gated IT-OT Process Security (`OrgelKraft` / `SPEC-PODS-PENTAD-RB-12`)
### *Pre-Meeting One-Pager for SFI NORCICS & Norwegian Computing Center (Process Industry, Subsea & Grid Alignment)*

**Author:** Marius Egerhei Torjusen (`ORCID: 0009-0006-0431-6637` // `WoS: PJT-0190-2026`)  
**Context:** Pre-meeting technical addendum extending `IT_OT_CONSEQUENCE_GATE_NORCICS_BRIEF.md` (Domains I–III) to **Domain IV: Electrochemical, Subsea & Process-Industry OT Security** (relevant to SFI NORCICS user partners such as Yara, Norsk Hydro, Equinor, Kongsberg, Elvia, and Sykehuset Innlandet)  
**Full Monograph (`v1.0.1`, 74 pp.):** [`KONSEPTUELL_GRANITT_ET_FORSOK_PA_SANNHET.pdf`](https://github.com/sololys/skrivevaerelset/blob/main/KONSEPTUELL_GRANITT_ET_FORSOK_PA_SANNHET.pdf)  
**Epistemic Status:** `L1` Deterministic Software, Exact Rational Ledger & RTL Simulation (`INSPIRED_BY != IMPLEMENTS != PROVES`; `L2/L3` physical reactors and subsea hardware held in explicit `HOLD` at $0.00\,\mathrm{V\ DC}$ pending HIL/field qualification)

---

## 1. Architectural Motivation: Closing the Process-Control & Transducer Gap

In continuous chemical, electrochemical, and subsea process plants, Stuxnet-class IT-OT attacks and AI-driven optimization failures exploit three structural blind spots in classical SCADA/PLC and Simplex/SOTIF architectures:

1. **Floating-Point Stoichiometric Drift:** IEEE-754 floating-point tolerances allow covert mass-balance deviations, unrecorded feedstock injection, or gradual setpoint creep (e.g., pushing an electrolyzer above its water-splitting catalyst-degradation ceiling or driving a crystallizer across the Ostwald nucleation boundary) to hide inside numerical noise.
2. **The 400-Clock-Cycle Audit Window:** A `POSIX fsync()` disk commit requires $\sim 5.0\,\mathrm{ms}$, whereas an $80\,\mathrm{kHz}$ FPGA safety loop ticks every $12.5\,\mu\mathrm{s}$. If a control system waits for disk logging before tripping—or logs intention before physical actuation—an adversary gains a **400-cycle window** to corrupt state before the relay opens.
3. **The Transducer & False-Realization Gap ($W \not\equiv \text{software log}$):** Classical controllers log a command as "executed" once it leaves the digital output register ($Q_{\mathrm{math}} \sim k_B T \ln 2$), remaining blind if a valve seizes mechanically downstream. Across $8,000$ deterministic Monte Carlo fault-injection runs (`L1`, `seed=42`), classical command-based architectures exhibit a **$25.00\%$ false-realization rate** ($2,000 / 8,000$), whereas the $T_{KY} = \Omega \circ \Pi_K \circ \Phi$ realization grammar achieves **$0.00\%$ false positives** ($0 / 8,000$).

---

## 2. Three `L1`-Verified Mechanisms in `OrgelKraft` (`SPEC-PODS-PENTAD-RB-12`)

### A. Exact Rational Mass-Balance Compiler ($\Delta R = 0$ across 45 Conservation Checks)
Rather than approximating process flows in floating-point arithmetic, the `OrgelKraft` reference balance models a closed six-element cascade ($\mathrm{C, H, N, O, Mg, P}$) using exact rational arithmetic (`fractions.Fraction`). Across a reference 24-hour cycle—spanning low-voltage nitrogen fixation (`K-POD`, parallel cell stack at $\le 0.998\,\mathrm{V\ DC}$, $2,204.41\,\mathrm{A}$, $2,200\,\mathrm{W}$), aromatic reduction (`C8` at $1.050\,\mathrm{V\ DC}$), struvite phosphorus recovery (`P-POD` locked inside the Ostwald metastable window $S_{\mathrm{struvite}} \in [1.80, 3.20]$), and enzymatic lignocellulose bioconversion (`POD-Mycelin` at $50.0\,\mathrm{W} \pm 0.5\,\mathrm{W}$)—total mass enters at $141.10099788325846\,\mathrm{kg}$ and exits at $141.10099788325846\,\mathrm{kg}$ with **zero rational residual ($\Delta R = 0$)**. Any unrecorded mass deviation exceeding $1\,\mathrm{mg}$ (`delta_q_mg > 1`) immediately trips the gate to $0.00\,\mathrm{V\ DC}$.

### B. $12.5\,\mu\mathrm{s}$ SystemVerilog Guillotine & Asymmetric Time-Domain Bifurcation
In the RTL reference modules `kpod_fpga_guillotine_12u5` and `etor_pik_boundary_gate`:
- **Memory & Fuse Integrity:** Every $12.5\,\mu\mathrm{s}$ clock cycle verifies an involutive XOR round-trip in reversible phase memory (`(payload_in ^ MASK) ^ MASK == payload_in`) and enforces a 64-bit monotone fuse register (`(F_n & F_{n+1}) == F_n`) that forbids state rollback.
- **Asymmetric 400-Cycle Rule:** For **admission (`OPEN` $\to 5.00\,\mathrm{V\ DC}$)**, the sealed witness log is a mandatory entry ticket (the actuator waits all 400 cycles until `fsync` completes). For **protective cutoff (`KILL` $\to 0.00\,\mathrm{V\ DC}$)**, causality reverses: the FPGA/silicon crowbar drops excitation to $0.00\,\mathrm{V\ DC}$ on **Cycle 1 ($12.5\,\mu\mathrm{s}$ / $4.0\,\mathrm{ns}$)** while the witness log is written in parallel as a post-mortem autopsy.

### C. Two-Phase Verification ($\Pi_K$ vs. $\Pi_{\mathrm{orth}}$) & Anti-DoS Galvanic Separation
To prevent both sensor spoofing and biological alarm-fatigue Denial-of-Service (DoS):
1. **Phase A (Pre-Commit in $\Pi_K$) vs. Phase B (In-Flight in $\Pi_{\mathrm{orth}}$):** $\Pi_K$ verifies pre-commit viability (causal light-cone $\tau_{\mathrm{ToF}} \le 133.425\,\mathrm{ns}$ cross-locked against the $c_{\mathrm{acoustic}} \approx 11,100\,\mathrm{m/s}$ sapphire crystal eigenfrequency within $\pm 5\,\mathrm{ppm}$, Nagumo tangency $\dot{x} \in T_K(x)$, and forward braking horizon across $41$ discrete trajectories) *before* granting $5.00\,\mathrm{V\ DC}$. Once energized, $\Pi_{\mathrm{orth}}$ monitors cross-modal physical realization (coil back-EMF $\int V(t)I(t)\,dt$, thermal enthalpy $\Delta T$, and acoustic ToF) within a $38.4\,\mathrm{ms}$ actuation window, firing a secondary galvanic crowbar (`GATE :: KILL`) on any divergence.
2. **Electronic `CAUSAL_HOLD` ($8.0\,\mu\mathrm{J}$) vs. Mechanical Trip-Free `RESET_BY_L01`:** External network/RF noise is rejected in the solid-state airlock (`CAUSAL_HOLD` at $0.00\,\mathrm{V\ DC}$, $8.0\,\mu\mathrm{J}$ per pulse, yielding a $1.25 \times 10^9$ thermodynamic exhaustion ratio against a $10\,\mathrm{kJ}$ attacker) without tripping mechanical latches. Irreversible spring-return `GATE :: KILL` is reserved strictly for internal core breaches and requires a two-stage mechanical **trip-free `Level 01` human reset** (where the first $45^\circ$ of lever travel drives a shaft magneto to power a read-only $\Pi_{\mathrm{orth}}$ check alongside passive Bourdon/bimetallic anchors before copper contacts can latch).

---

## 3. Summary Extension Matrix (Domain IV — SFI NORCICS Alignment)

| SFI NORCICS Sector | Untrusted Candidate ($\Phi$) | Deterministic Gate & Invariant ($\Pi_K, \Pi_{\mathrm{orth}}$) | Fail-Closed Verdict ($\Omega$) | `L1` Verification Artifact |
| :--- | :--- | :--- | :--- | :--- |
| **Electrochemical & Process OT** *(Yara / Hydro)* | PLC/AI voltage, temperature or feedstock setpoint | Exact rational stoichiometry ($\Delta R = 0$, 45 checks), $V \le 0.998\,\mathrm{V\ DC}$, Ostwald $S \in [1.80, 3.20]$, XOR & monotone fuse | $12.5\,\mu\mathrm{s}$ RTL cutoff to $0.00\,\mathrm{V\ DC}$ on Cycle 1 | `kpod_fpga_guillotine_12u5` & `fractions.Fraction` suite |
| **Subsea & Kinematic Actuation** *(Equinor / Kongsberg)* | Valve / actuator trajectory near structural limit $Q_{\mathrm{LIMIT}}$ | 41-candidate braking horizon (`\|A(x)\| >= 1`) + $38.4\,\mathrm{ms}$ in-flight $\Pi_{\mathrm{orth}}$ (EM + $\Delta T$ + acoustic ToF) | Auto-reverse at $\partial K$; Crowbar `KILL` if actuator seizes | `etor_pik_boundary_gate` (150 cycles, `seed=42`) & 8,000 MC runs |
| **Grid, Police & Hospital Edge** *(Elvia / Politiet / Sykehuset)* | Contested fiber/RF command or high-entropy 6G ISAC waveform | $\partial A / \partial C_{\mathrm{fiber}} \equiv 0$, sapphire-locked $\tau_{\mathrm{ToF}} \le 133.425\,\mathrm{ns}$, Woodward $\chi(\tau,\nu)$ vs. $H(X)$ | $8.0\,\mu\mathrm{J}$ `CAUSAL_HOLD` on channel noise; trip-free `L01` on core fault | Local-first SHA-256 ledger & ISAC covariance gate |
