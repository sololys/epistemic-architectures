# Bit-Representation Taxonomy & STACK MAP v0.1 / v1.5-MASTER
**STATUS:** STRUCT / LOCKED AT LOCUS ZERO (`0xABCDEF00`)  
**EPISTEMIC BOUNDARY:** `INSPIRED_BY != IMPLEMENTS != PROVES` · `PHYSICAL_AUTHORITY = NONE`

## 1. Den Kanoniske Konstitusjonen
Bit er ikke mening. Mønster blir først struktur når det types. Struktur blir først konsekvens når den slipper gjennom porten. Konsekvens blir først historie når den bevitnes.

## 2. Den Reviderte Lagdelingen ($D_0 \to D_3$)
- **$D_0$ — RAW BIT FIELD (`○` / `raw`):** Binary code, non-positional binary, finger binary (5 uavhengige D-latcher på én hånd, 0–31), ufortolket 0/1-materiale ($\Phi$). $\operatorname{Authority}(D_0) = 0$.
- **$D_1$ — REVERSIBLE / PERMUTATIONAL PHASE (`∅` / `estimate`):** Kun ekte bijeksjoner og involusjoner med $F(F(s)) = s$: Bit-rotasjoner (`ROL`/`ROR`), $\operatorname{ROX}_m(x) = x \oplus m$ med frossen maske ($q=1, m_{\text{inn}} = m_{\text{ut}}$), `NOT`, Gray-kode ($\Delta = 1$ bit) og ikke-singulære `LFSR`-dynamikker. (Ikke-invertible operatorer som `AND`, `OR`, `SHL`, `SHR` destruerer entropi og er strengt ekskludert fra $D_1$).
- **$D_{1.2}$ — STRUCTURAL NUMERIC TYPES (`□` / `struct`):** Toer-komplement ($\bmod 2^n$), offset-binær, balansert ternært ($-1,0,+1$), redundante binære representasjoner ($O(1)$), Wallace/Dadda-reduksjon, BCD, Kvibinær (IBM 650: eksakt 2 av 7 bits HIGH), IEEE 754. Krever $D_{1.2}$ Codec Roundtrip: $\operatorname{decode}(\operatorname{encode}(v)) = v$.
- **$D_{1.5}$ — VIABILITY / NUMERIC RISK (`◇` / `viability`):** Overløp, underløp, NaN, ugyldige kvibinære kodeord, carry-propagation-risiko, periodiske desimalfeil ($1/3 = 0.333\dots \to \pi_t$ målt mot $\tau_{\text{OPEN}}, \tau_{\text{KILL}}$). I $A_5$-sommerfugllommen ($c = +0.5525 > 0, \lvert x\rvert \le 0.45$) holdes tilstanden i tapsfri stasis ved $2.50\text{ V DC HOLD}$ (`⏸` / `‖`).
- **$D_2$ — COMMITTED SYMBOLIC STATE (`●` / `committed`):** ASCII 7-bit (128 tegn) / **205-byte låst binærramme** (`119 B W_pre` `<QQ32sfBH32s32s` + `86 B W_post` `<QQ32sBfB32s`, RFC 8785 JCS fikspunkt), L1-simulert D-Latch HIGH ($5.00\text{ V DC}$, `OPEN_AS_SOFTWARE_DEMONSTRATION`). Point of No Return ($\eta = 1$). **Alternativ A låst:** `●` er utelukkende en tilstandsnode i kjeden, aldri et suffiks; selve commit-handlingen i suffikset representeres av `!` (`commit_event`) kombinert med `#` (`witness_hash`).
- **$D_3$ — WITNESS / REPLAYABLE SEMANTIC LAYER (`#!` / `audit(hash,commit)`):** Kanonisk glyph-streng `✓(○ → ∅ → □ → ◇ → ●)#! ▸`. Skjema- og proveniensbundet vitnelogg ($W_{t+1}^+$) med eksplisitt demarkasjon mellom **Nivå L1** (append-only programvare-WAL med `os.fsync` og bilateral Merkle-rot $W_t^{\text{bilat}}$) og **Nivå L2/L3** (fysisk WORM-medium / laser-ablatert silisium / eFuse og maskinvarelås). Unicode alene eller frittstående hashkjede uten fysisk L2/L3-verifikasjon kan aldri hevde fysisk WORM (`Standalone Hashchain as WORM = KILL`).

## 3. Frosne Portregistre (v1.5-MASTER Seksjon 6)
- **Registry A (`KILL` — WORM- og Unicode-Restriksjonen):** Unicode alene og *frittstående hash-kjeder alene* får ubetinget `KILL` dersom de presenteres som tilstrekkelig semantisk eller fysisk uforanderlighet. En frittstående SHA-256-kjede uten nøkkelstyrt MAC/Ed25519-signatur eller eksternt anker hindrer ikke at hele journalen erstattes.
- **Registry B (`HOLD` — Hardware D-Latch Gap):** Hardware D-Latch Actuation er låst til `HOLD` i påvente av fysiske telemetrilogger. Utdata fra C++- og Python-kjøringer (`dungeon_imp.cpp`, `merge_interlock.cpp`, `ky_parser.py`) er klassifisert som `OPEN_AS_SOFTWARE_DEMONSTRATION` ("deterministisk demonstrert i simuleringsmotoren" ved `0xABCDEF00`), ikke fysisk målt silisium-spenning, inntil GPIO/FPGA-loggen fra `Gemini-Core` (L2 Silicon HIL) er koblet på.

## 4. Arkitekturkart: $D_0 \longrightarrow D_3$ & Port-Topologi (`0xABCDEF00`)

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║  KY REALIZATION GRAMMAR v1.5-MASTER // D0 -> D3 CAUSAL PROJECTION PIPELINE   ║
║  State Anchor: 0xABCDEF00  │  Σ_state (●) ∩ Σ_suffix (!) = ∅ (Option A)      ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [D0: RAW BIT FIELD]           ○  (raw)       Uninterpreted bits Φ, Authority(D0) = 0
           │
           ▼  (→)
  [D1: REVERSIBLE PHASE]        ∅  (estimate)  ROX_m(x) = x ⊕ m (q=1), Gray Δ=1, LFSR
           │
           ▼  (→)
  [D1.2: STRUCTURAL NUMERIC]    □  (struct)    Bijective Codec: from_ascii(to_ascii(x)) ≡ x
  ┌────────────────────────────────────────────────────────────────────────────┐
  │  Unicode : ✓(○ → ∅ → □ → ◇ → ●)#! ▸                                        │
  │  ASCII   : validate(raw -> estimate -> struct -> viability -> committed)#! OPEN
  └────────────────────────────────────────────────────────────────────────────┘
           │
           ▼  (→)
  [D1.5: VIABILITY / RISK]      ◇  (viability) Overflow/NaN guard, π_t vs (τ_OPEN, τ_KILL)
           │
           ▼  (→)  [REQUIRES_AUDIT: '#' witness_hash ∧ '!' commit_event]
  [D2: COMMITTED STATE]         ●  (committed) Strictly state node (● ∉ Σ_suffix -> KILL)
           │
           ╠═══════════════════════════════════════════════════════════════════╗
           ▼                                                                   ▼
  ╔════════════════════════════════════════╗         ╔════════════════════════════════════════╗
  ║  D3 // REGISTRY A: IMMUTABILITY GATE   ║         ║  L1->L3 // REGISTRY B: SILICON GATE    ║
  ╠════════════════════════════════════════╣         ╠════════════════════════════════════════╣
  ║  • Raw Unicode / Bare Hash  ──► [KILL] ║         ║  • No ADC Telemetry         ──► [HOLD] ║
  ║  • 208B Rosetta v1.5 Header            ║         ║    (OPEN_AS_SOFTWARE_DEMONSTRATION)    ║
  ║    + Ed25519 Signature (64B)           ║         ║  • Physical 74HC74 / FPGA Q:           ║
  ║    + Monotonic Counter C > C_hw        ║         ║    V_Q ∈ [4750,5250]mV ∧ I ∈ [0.5,25]mA║
  ║                             ──► [PASS] ║         ║    + Causal 4-Point Timing  ──► [OPEN] ║
  ╚════════════════════════════════════════╝         ╚════════════════════════════════════════╝
```

## 5. Göteborg-Triaden & `1664-bit` (`208B`) $\leftrightarrow$ `1640-bit` (`205B`) RTL Master-Bro (`SPEC-414..416`)

Toppmodulen `gothenburg_corridor_rosetta_top.sv` (`IEEE 1800-2012`) binder sammen $D_3$ Rosetta-konvolutten (`208B` / `1664 bits`, `>4sHBBQ32s32s32s32s64s`) med `fpga_capsule_frame_205b_decoder.sv` (`SPEC-213`), `spec415_kpod_cdc_gate.sv` (`SPEC-415`) og `spec416_infranett_witness_gate.sv` (`SPEC-416`):

| Spesifikasjon | Domene & RTL/Python-Modul | Verifisert Bit-Kontrakt & Invariant | L1 / L1.5 Status | Utgang uten L3 HIL |
| :--- | :--- | :--- | :--- | :--- |
| **`SPEC-414`** | **77 GHz ISAC Radar** (`spec414_415_416_gothenburg_corridor_gate.py`) | Euklidsk fasekjegle $\Pi_K$, Staggered-PRF Fine–Wilf $\gcd(n_1..n_k)=1$, Joseph-EKF PSD | `[L1_VERIFIED]` | `[HOLD // 0.00V_DC]` |
| **`SPEC-415`** | **`-240 m` Benthic K-POD** (`spec415_kpod_cdc_gate.sv`) | $5\times$ Async 2-FF CDC-låser, $<145.0\text{ dB SPL}$ sabotasjeklemme, $\vert d_{532\text{nm}} - d_{\text{UWB}}\vert \le 15\text{ mm}$ | `[L1_VERIFIED]` · `[RTL_PASS]` | `[HOLD // 0.00V_DC]` |
| **`SPEC-416`** | **Infranett Grid & Fiber** (`spec416_infranett_witness_gate.sv`) | `1640-bit` (`205B`: `119B W_pre` `>4sQI3BqqIiQ32s36s` + `86B W_post` `>Q32s32sIIHI`), Kirchhoff $\Delta R \equiv 0/1 \in \mathbb{Q}$, 1550 nm OTDR $\le 0.050\text{ dB}$, PTP $\le 100\text{ ns}$, VSG $50\text{ Hz}$ ($2f+1$ BFT) | `[L1_VERIFIED]` · `[RTL_PASS]` | `[HOLD // 0.00V_DC]` |
| **`MASTER_TOP`** | **Rosetta $D_3 \leftrightarrow L_2$ Bro** (`gothenburg_corridor_rosetta_top.sv`) | `1664-bit` (`208B`) Rosetta $D_3$ + `SPEC-213` + `SPEC-415` + `SPEC-416` konjunksjonslås (`8/8 PASS` i `iverilog -g2012`) | `[L1.5_RTL_COSIM_PASS]` | `[HOLD // 0.00V_DC]` |
