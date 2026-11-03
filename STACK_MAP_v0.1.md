# Bit-Representation Taxonomy & STACK MAP v0.1 / v1.5-MASTER
**STATUS:** STRUCT / LOCKED AT LOCUS ZERO (`0xABCDEF00`)  
**EPISTEMIC BOUNDARY:** `INSPIRED_BY != IMPLEMENTS != PROVES` · `PHYSICAL_AUTHORITY = NONE`

## 1. Den Kanoniske Konstitusjonen
Bit er ikke mening. Mønster blir først struktur når det types. Struktur blir først konsekvens når den slipper gjennom porten. Konsekvens blir først historie når den bevitnes.

## 2. Den Reviderte Lagdelingen ($D_0 \to D_3$)
- **$D_0$ — RAW BIT FIELD (`○` / `raw`):** Binary code, non-positional binary, finger binary (5 uavhengige D-latcher på én hånd, 0–31), ufortolket 0/1-materiale ($\Phi$). $\operatorname{Authority}(D_0) = 0$.
- **$D_1$ — REVERSIBLE / PERMUTATIONAL PHASE (`∅` / `estimate`):** Bit-rotasjoner, $\operatorname{ROX}_m(x) = x \oplus m$ ($q=1$), NOT, Gray-kode ($\Delta = 1$ bit), selektive LFSR-dynamikker. (AND, OR, SHL, SHR er ekskludert som primærsymmetrier).
- **$D_{1.2}$ — STRUCTURAL NUMERIC TYPES (`□` / `struct`):** Toer-komplement ($\bmod 2^n$), offset-binær, balansert ternært ($-1,0,+1$), redundante binære representasjoner ($O(1)$), Wallace/Dadda-reduksjon, BCD, Kvibinær (IBM 650: eksakt 2 av 7 bits HIGH), IEEE 754. Krever $D_{1.2}$ Codec Roundtrip: $\operatorname{decode}(\operatorname{encode}(v)) = v$.
- **$D_{1.5}$ — VIABILITY / NUMERIC RISK (`◇` / `viability`):** Overløp, underløp, NaN, ugyldige kvibinære kodeord, carry-propagation-risiko, periodiske desimalfeil ($1/3 = 0.333\dots \to \pi_t$ målt mot $\tau_{\text{OPEN}}, \tau_{\text{KILL}}$).
- **$D_2$ — COMMITTED SYMBOLIC STATE (`●` / `committed`):** 7-bits ASCII (128 tegn), låste byte-sekvenser, L1-simulert D-Latch HIGH ($5.00\text{ V DC}$, `OPEN_AS_SOFTWARE_DEMONSTRATION`). Point of No Return ($\eta = 1$). **Alternativ A låst:** `●` er utelukkende en tilstandsnode i kjeden, aldri et suffiks; selve commit-handlingen i suffikset representeres av `!` (`commit_event`) kombinert med `#` (`witness_hash`).
- **$D_3$ — WITNESS / REPLAYABLE SEMANTIC LAYER (`#!` / `audit(hash,commit)`):** Kanonisk glyph-streng `✓(○ → ∅ → □ → ◇ → ●)#! ▸`. Krever eksplisitt Rosetta-skjema/versjon samt eksternt anker, signert sjekkpunkt (HMAC-SHA256 / Ed25519) eller fysisk WORM-kontroll.

## 3. Frosne Portregistre (v1.5-MASTER Seksjon 6)
- **Registry A (`KILL` — WORM- og Unicode-Restriksjonen):** Unicode alene og *frittstående hash-kjeder alene* får ubetinget `KILL` dersom de presenteres som tilstrekkelig semantisk eller fysisk uforanderlighet. En frittstående SHA-256-kjede uten nøkkelstyrt MAC/signatur eller eksternt anker hindrer ikke at hele journalen erstattes.
- **Registry B (`HOLD` — Hardware D-Latch Gap):** Hardware D-Latch Actuation er låst til `HOLD` i påvente av fysiske telemetrilogger. Utdata fra C++- og Python-kjøringer (`dungeon_imp.cpp`, `merge_interlock.cpp`, `ky_parser.py`) er klassifisert som `OPEN_AS_SOFTWARE_DEMONSTRATION` ("deterministisk demonstrert i simuleringsmotoren" ved `0xABCDEF00`), ikke fysisk målt silisium-spenning, inntil GPIO/FPGA-loggen fra `Gemini-Core` (L2 Silicon HIL) er koblet på.
