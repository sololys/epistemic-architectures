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

* **Memory & Fuse Integrity:** Every $12.5\,\mu\mathrm{s}$ clock cycle verifies an involutive XOR round-trip in reversible phase memory (`(payload_in ^ MASK) ^ MASK == payload_in`) and enforces a 64-bit monotone fuse register (`(F_n & F_{n+1}) == F_n`) that forbids state rollback.
* **Asymmetric 400-Cycle Rule:** For **admission (`OPEN` $\to 5.00\,\mathrm{V\ DC}$)**, the sealed witness log is a mandatory entry ticket (the actuator waits all 400 cycles until `fsync` completes). For **protective cutoff (`KILL` $\to 0.00\,\mathrm{V\ DC}$)**, causality reverses: the FPGA/silicon crowbar drops excitation to $0.00\,\mathrm{V\ DC}$ on **Cycle 1 ($12.5\,\mu\mathrm{s}$ / $4.0\,\mathrm{ns}$)** while the witness log is written in parallel as a post-mortem autopsy.

### C. Two-Phase Verification ($\Pi_K$ vs. $\Pi_{\mathrm{orth}}$) & Anti-DoS Galvanic Separation
To prevent both sensor spoofing and biological alarm-fatigue Denial-of-Service (DoS):

1. **Phase A (Pre-Commit in $\Pi_K$) vs. Phase B (In-Flight in $\Pi_{\mathrm{orth}}$):** $\Pi_K$ verifies pre-commit viability (causal light-cone $\tau_{\mathrm{ToF}} \le 133.425\,\mathrm{ns}$ cross-locked against the $c_{\mathrm{acoustic}} \approx 11,100\,\mathrm{m/s}$ sapphire crystal eigenfrequency within $\pm 5\,\mathrm{ppm}$, Nagumo tangency $\dot{x} \in T_K(x)$, and forward braking horizon across $41$ discrete trajectories) *before* granting $5.00\,\mathrm{V\ DC}$. Once energized, $\Pi_{\mathrm{orth}}$ monitors cross-modal physical realization (coil back-EMF $\int V(t)I(t)\,dt$, thermal enthalpy $\Delta T$, and acoustic ToF) within a $38.4\,\mathrm{ms}$ actuation window, firing a secondary galvanic crowbar (`GATE :: KILL`) on any divergence.
2. **Electronic `CAUSAL_HOLD` ($8.0\,\mu\mathrm{J}$) vs. Mechanical Trip-Free `RESET_BY_L01`:** External network/RF noise is rejected in the solid-state airlock (`CAUSAL_HOLD` at $0.00\,\mathrm{V\ DC}$, $8.0\,\mu\mathrm{J}$ per pulse, yielding a $1.25 \times 10^9$ thermodynamic exhaustion ratio against a $10\,\mathrm{kJ}$ attacker) without tripping mechanical latches. Irreversible spring-return `GATE :: KILL` is reserved strictly for internal core breaches and requires a two-stage mechanical **trip-free `Level 01` human reset** (where the first $45^\circ$ of lever travel drives a shaft magneto to power a read-only $\Pi_{\mathrm{orth}}$ check alongside passive Bourdon/bimetallic anchors before copper contacts can latch).

---

## 3. Summary Extension Matrix (Domain IV — SFI NORCICS Alignment)

| SFI NORCICS Sector | Untrusted Candidate ($\Phi$) | Deterministic Gate & Invariant ($\Pi_K, \Pi_{\mathrm{orth}}$) | Fail-Closed Verdict ($\Omega$) | `L1` Verification Artifact |
| :--- | :--- | :--- | :--- | :--- |
| **Electrochemical & Process OT** *(Yara / Hydro)* | PLC/AI voltage, temperature or feedstock setpoint | Exact rational stoichiometry ($\Delta R = 0$, 45 checks), $V \le 0.998\,\mathrm{V\ DC}$, Ostwald $S \in [1.80, 3.20]$, XOR & monotone fuse | $12.5\,\mu\mathrm{s}$ RTL cutoff to $0.00\,\mathrm{V\ DC}$ on Cycle 1 | `kpod_fpga` ($12.5\,\mu\mathrm{s}$) & `fractions` suite |
| **Subsea & Kinematic Actuation** *(Equinor / Kongsberg)* | Valve / actuator trajectory near structural limit $Q_{\mathrm{LIMIT}}$ | 41-candidate braking horizon ($\lvert\mathcal{A}(x)\rvert \ge 1$) + $38.4\,\mathrm{ms}$ in-flight $\Pi_{\mathrm{orth}}$ (EM + $\Delta T$ + acoustic ToF) | Auto-reverse at $\partial K$; Crowbar `KILL` if actuator seizes | `etor_pik` gate (`seed=42`) & 8,000 MC runs |
| **Grid, Police & Hospital Edge** *(Elvia / Politiet / Sykehuset)* | Contested fiber/RF command or high-entropy 6G ISAC waveform | $\partial A / \partial C_{\mathrm{fiber}} \equiv 0$, sapphire-locked $\tau_{\mathrm{ToF}} \le 133.425\,\mathrm{ns}$, Woodward $\chi(\tau,\nu)$ vs. $H(X)$ | $8.0\,\mu\mathrm{J}$ `CAUSAL_HOLD` on channel noise; trip-free `L01` on core fault | Local-first SHA-256 ledger & ISAC covariance gate |

---

## 4. Architectural Grounding

Conventional cybersecurity attempts to infer the intent of a code packet before allowing it through a firewall. In physical process industry, intent is irrelevant; only thermodynamics, stoichiometry, and the conservation of mass and energy hold validity. When the control loop is anchored directly in exact rational mass balance ($\Delta R = 0$) and orthogonal physical feedback ($\Pi_{\mathrm{orth}}$), adversarial code loses its operational leverage. A compromised network may propose any conceivable state transition ($\Phi$), but as long as the proposal violates the reactor's physical invariants, excitation drops unconditionally to **$0.00\,\mathrm{V\ DC}$**. Security ceases to be a question of software trust and becomes an intrinsic property of matter itself.

\newpage

# Domene IV: Støkiometrisk og maskinvarelåst IT-OT-prosessikkerhet (Norsk Stamme)
### *OrgelKraft / SPEC-PODS-PENTAD-RB-12 — Teknisk tillegg for SFI NORCICS og Norsk Regnesentral*

**Forfatter:** Marius Egerhei Torjusen (`ORCID: 0009-0006-0431-6637` // `WoS: PJT-0190-2026`)  
**Referansemonografi:** [*KONSEPTUELL GRANITT: ET FORSØK PÅ SANNHET*](https://github.com/sololys/skrivevaerelset/blob/main/KONSEPTUELL_GRANITT_ET_FORSOK_PA_SANNHET.pdf) (`v1.0.1`, 74 s.)  
**Operasjonelt sammendrag:** Dokumentet *Domain IV Addendum (OrgelKraft / SPEC-PODS-PENTAD-RB-12)* formaliserer en deterministisk, maskinvarelåst sikkerhetsarkitektur for elektrokjemisk prosessindustri, undervannssystemer og kritisk nettverkskant. Arkitekturen eliminerer tre strukturelle blindsoner i klassiske SCADA/PLC-systemer: flyttallsbasert støkiometrisk drift, tidsvinduet mellom høyfrekvent kontrollsløyfe og diskbasert revisjonslogg, samt gapet mellom digitalt logget intensjon og fysisk utført arbeid.  
**Epistemisk status:** Nivå $\text{L1}$ (deterministisk programvare, eksakt rasjonal hovedbok og RTL-simulering). Fysiske reaktorer og undervannsmaskinvare ($\text{L2}/\text{L3}$) holdes i eksplisitt `HOLD` ved **$0{,}00\text{ V DC}$** i påvente av HIL- og feltkvalifisering ($\text{INSPIRED\_BY} \neq \text{IMPLEMENTS} \neq \text{PROVES}$).

---

## I. Strukturell diagnose: Tre blindsoner i klassisk prosesskontroll

I kontinuerlige kjemiske, elektrokjemiske og subseabaserte prosessanlegg utnytter Stuxnet-lignende IT-OT-angrep og feilslått AI-optimalisering tre fundamentale svakheter i klassiske SCADA/PLC- og Simplex/SOTIF-arkitekturer:

1. **Flyttallsbasert støkiometrisk drift:** Toleransegrensene i IEEE-754 flyttallsaritmetikk skjuler uregistrerte masseavvik, skjult råstoffinjeksjon og gradvis settpunkt-glidning i numerisk støy. En elektrolysør kan dermed presses over grensen for katalysatordegradering ved vannspalting, eller en krystallisator kan drives over Ostwalds nukleasjonsgrense, uten at kontrollsystemet registrerer brudd på konserveringslovene.
2. **Revisjonsvinduet på 400 klokkesykluser:** En POSIX `fsync()`-skriveoperasjon til disk krever **$\sim 5{,}0\text{ ms}$**, mens en $80\text{ kHz}$ FPGA-sikkerhetssløyfe opererer med en klokkepuls på **$12{,}5\,\mu\text{s}$**. Dersom kontrollsystemet avventer disklogging før utkobling – eller logger intensjonen før den fysiske aktuatoren beveger seg – oppstår et tidsvindu på 400 klokkesykluser der en aktør kan korrumpere tilstanden før releet åpner.
3. **Transduser- og realiseringsgapet ($\Psi \neq \text{programvarelogg}$):** Klassiske kontrollere bokfører en kommando som «utført» i det øyeblikket bit-verdien forlater det digitale utgangsregisteret ($Q_{\text{math}} \sim k_B T \ln 2$). Systemet forblir blindt dersom ventilen låser seg mekanisk nedstrøms. Over $8\,000$ deterministiske Monte Carlo-simuleringer med feilinjeksjon ($\text{L1}$, `seed=42`) oppviser klassiske kommandobaserte arkitekturer en falsk realiseringsrate på **$25{,}00\,\%$** ($2\,000$ av $8\,000$ tilfeller). Realiseringsgrammatikken $T_{KY} = \Omega \circ \Pi_K \circ \Phi$ reduserer denne feilraten til **$0{,}00\,\%$** ($0$ av $8\,000$).

*En digital ordre er kun et potensial. Fysisk virkelighet krever verifisert konsekvens.*

---

## II. Tre L1-verifiserte mekanismer i OrgelKraft

### A. Eksakt rasjonal massebalanse-kompilator ($\Delta R = 0$ over 45 konserveringssjekker)
OrgelKraft erstatter flyttallstilnærminger med eksakt rasjonal aritmetikk (`fractions.Fraction`) for å modellere en lukket kaskade av seks grunnstoffer ($\text{C, H, N, O, Mg, P}$). Over en 24-timers referansesyklus dekker modellen fire koblede prosesser:
* **K-POD:** Lavspennings nitrogenfiksering i parallell cellestabel ved **$0{,}998\text{ V DC}$**, **$2\,204{,}41\text{ A}$** og **$2\,200\text{ W}$**.
* **C8:** Aromatisk reduksjon ved **$1{,}050\text{ V DC}$**.
* **P-POD:** Fosforgjenvinning via struvitt, låst innenfor Ostwalds metastabile vindu $S_{\text{struvite}} \in [1{,}80, 3{,}20]$.
* **POD-Mycelin:** Enzymatisk biokonvertering av lignocellulose ved **$50{,}0\text{ W} \pm 0{,}5\text{ W}$**.

Total inngående masse er eksakt **$141{,}10099788325846\text{ kg}$**, og total utgående masse er eksakt **$141{,}10099788325846\text{ kg}$**, med et rasjonalt residual på $\Delta R = 0$. Ethvert uregistrert masseavvik som overstiger **$1\text{ mg}$** ($\Delta q_{\text{mg}} > 1$) utløser umiddelbar port-utkobling til **$0{,}00\text{ V DC}$**.

### B. $12{,}5\,\mu\text{s}$ SystemVerilog-giljotin og asymmetrisk tidsdomene-bifurkasjon
I RTL-referansemodulene `kpod_fpga_guillotine_12u5` og `etor_pik_boundary_gate` håndheves to maskinvareinvarianter ved hver $12{,}5\,\mu\text{s}$ klokkesyklus:

* **Minne- og sikringsintegritet:** En involutiv XOR-rundtur i reversibelt faseminne (`(payload_in ^ MASK) ^ MASK == payload_in`) verifiseres kontinuerlig, kombinert med et 64-bits monotont sikringsregister ($(F_n \,\&\, F_{n+1}) == F_n$) som fysisk umuliggjør tilbakestilling av tilstand (*state rollback*).
* **Den asymmetriske 400-syklusregelen:** Tidsdomenet splittes asymmetrisk mellom autorisasjon og nødstopp. For tilgang (`OPEN` $\rightarrow$ **$5{,}00\text{ V DC}$**) fungerer den forseglede vitneloggen som en ufravikelig inngangsbillett; aktuatoren holdes tilbake i samtlige 400 sykluser inntil `fsync()` er bekreftet på disk. Ved beskyttende utkobling (`KILL` $\rightarrow$ **$0{,}00\text{ V DC}$**) reverseres kausaliteten: FPGA- og silisium-crowbaren kutter eksitasjonen til **$0{,}00\text{ V DC}$** på syklus 1 (**$12{,}5\,\mu\text{s}$ / $4{,}0\text{ ns}$**), mens vitneloggen skrives parallelt som en post-mortem obduksjon. *Tillatelse krever fullført bevis. Beskyttelse krever kun brudd.*

### C. Tofase-verifisering ($\Pi_K$ mot $\Pi_{\text{orth}}$) og galvanisk separasjon mot utmattelsesangrep
Arkitekturen skiller skarpt mellom pre-kausal levedyktighet og post-kausal fysisk realisering for å forhindre både sensorspoofing og operatørutmattelse (*alarm-fatigue DoS*):

1. **Fase A (Pre-Commit i $\Pi_K$) mot Fase B (In-Flight i $\Pi_{\text{orth}}$):** Før **$5{,}00\text{ V DC}$** innvilges, verifiserer $\Pi_K$ kausal lyskjegle ($\tau_{\text{ToF}} \le 133{,}425\text{ ns}$ krysslåst mot safirkrystallets akustiske egenfrekvens $c_{\text{acoustic}} = 11\,100\text{ m/s}$ innenfor $\pm 5\text{ ppm}$), Nagumo-tangensbetingelse $T_K(x)$ og fremadrettet bremsehorisont over 41 diskrete baner. Når kretsen først er strømsatt, overvåker $\Pi_{\text{orth}}$ tverrmodal fysisk realisering – spole-mot-EMK $\int V(t)I(t)\,dt$, termisk entalpi $\Delta T$ og akustisk løpetid (ToF) – innenfor et aktuatorvindu på **$38{,}4\text{ ms}$**. Enhver divergens mellom forventet og observert fysikk utløser en sekundær galvanisk crowbar (`GATE: KILL`).
2. **Elektronisk `CAUSAL_HOLD` ($8{,}0\,\mu\text{J}$) mot mekanisk frikoblet `RESET_BY_L01`:** Ekstern nettverks- og RF-støy avvises i den faststoffbaserte luftslusen (`CAUSAL_HOLD` ved **$0{,}00\text{ V DC}$**, **$8{,}0\,\mu\text{J}$** per puls). Dette gir et termodynamisk utmattelsesforhold på $1{,}25 \times 10^9$ mot en angriper med **$10\text{ kJ}$** energibudsjett, uten at mekaniske låser løses ut. Irreversibel fjærbelastet `GATE: KILL` er reservert utelukkende for interne kjernebrudd og krever en totrinns mekanisk frikoblet (*trip-free*) tilbakestilling utført av **Level 01 menneskelig autoritet**. De første $45^\circ$ av spakens vandring driver en akselmagneto som strømsetter en skrivebeskyttet $\Pi_{\text{orth}}$-sjekk, parallelt med passive Bourdon- og bimetall-ankre, før kobberkontaktene fysisk kan låses.

---

## III. Utvidelsesmatrise for Domene IV (SFI NORCICS-allokering)

| SFI NORCICS-sektor | Uprøvd kandidat ($\Phi$) | Deterministisk port & invariant ($\Pi_K, \Pi_{\text{orth}}$) | Fail-Closed kjennelse ($\Omega$) | L1-verifikasjonsartefakt |
| :--- | :--- | :--- | :--- | :--- |
| **Elektrokjemisk & Prosess-OT** *(Yara / Norsk Hydro)* | PLC/AI-settpunkt for spenning, temperatur eller råstofftilførsel | Eksakt rasjonal støkiometri ($\Delta R = 0$, 45 sjekker), $V \le 0{,}998\text{ V DC}$, Ostwald $S \in [1{,}80, 3{,}20]$, involutiv XOR & monoton sikring | **$12{,}5\,\mu\text{s}$** RTL-kutt til **$0{,}00\text{ V DC}$** på syklus 1 | `kpod_fpga` ($12{,}5\,\mu\text{s}$) & `fractions`-testsuiten |
| **Subsea & Kinematisk aktuering** *(Equinor / Kongsberg)* | Ventil- eller aktuatorbane nær strukturell grense $Q_{\text{LIMIT}}$ | Bremsehorisont med 41 kandidater ($\lvert\mathcal{A}(x)\rvert \ge 1$) + **$38{,}4\text{ ms}$** in-flight $\Pi_{\text{orth}}$ ($\text{EM} + \Delta T + \text{akustisk ToF}$) | Automatisk reversering ved $\partial K$; Crowbar `KILL` ved mekanisk låsing | `etor_pik` (`seed=42`) & $8\,000$ MC-kjøringer |
| **Kraftnett, Politi & Sykehuskant** *(Elvia / Politiet / Sykehuset)* | Omstridt fiber-/RF-kommando eller høy-entropi 6G ISAC-bølgeform | $\partial A / \partial C_{\text{fiber}} \equiv 0$, safirlåst $\tau_{\text{ToF}} \le 133{,}425\text{ ns}$, Woodward $\chi(\tau, \nu)$ mot $H(X)$ | **$8{,}0\,\mu\text{J}$** `CAUSAL_HOLD` ved kanalstøy; frikoblet `L01`-reset ved kjernefeil | Lokal-først SHA-256 hovedbok & ISAC kovariansport |

---

## IV. Arkitektonisk forankring

Konvensjonell cybersikkerhet forsøker å tolke intensjonen i en kodepakke før den slipper gjennom brannmuren. I fysisk prosessindustri er intensjon irrelevant; kun termodynamikk, støkiometri og bevaring av masse og energi har gyldighet. Når kontrollsystemet forankres direkte i rasjonal massebalanse ($\Delta R = 0$) og ortogonal fysisk tilbakekobling ($\Pi_{\text{orth}}$), mister angrepskoden sitt handlingsrom. Et kompromittert nettverk kan foreslå enhver tenkelig tilstandsendring ($\Phi$), men så lenge forslaget bryter med reaktorens fysiske invarianter, faller spenningen til **$0{,}00\text{ V DC}$**. Sikkerhet opphører å være et spørsmål om programvaretillit og blir en ufravikelig egenskap ved selve materien.
