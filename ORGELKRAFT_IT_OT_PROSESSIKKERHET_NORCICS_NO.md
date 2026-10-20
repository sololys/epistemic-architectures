# Domene IV: Støkiometrisk og maskinvarelåst IT-OT-prosessikkerhet
### *OrgelKraft / SPEC-PODS-PENTAD-RB-12 — Konseptuell syntese og teknisk tillegg for SFI NORCICS og Norsk Regnesentral*

**Forfatter:** Marius Egerhei Torjusen (`ORCID: 0009-0006-0431-6637` // `WoS: PJT-0190-2026`)  
**Referansemonografi:** [*KONSEPTUELL GRANITT: ET FORSØK PÅ SANNHET*](https://github.com/sololys/skrivevaerelset/blob/main/KONSEPTUELL_GRANITT_ET_FORSOK_PA_SANNHET.pdf) (`v1.0.1`, 74 s.)  
**Epistemisk status:** Nivå $\text{L1}$ (deterministisk programvare, eksakt rasjonal hovedbok og RTL-simulering). Fysiske reaktorer og undervannsmaskinvare ($\text{L2}/\text{L3}$) holdes i eksplisitt `HOLD` ved **$0{,}00\text{ V DC}$** i påvente av HIL- og feltkvalifisering ($\text{INSPIRED\_BY} \neq \text{IMPLEMENTS} \neq \text{PROVES}$).

---

## Del I — Konseptuell syntese: Fra digital intensjon til materiell konsekvens

Konvensjonell prosesskontroll bygger på en fatal illusjon: tillit til digital intensjon. I elektrokjemisk prosessindustri, subsea-operasjoner og på den kritiske nettverkskanten utnyttes denne tilliten som en strukturell svakhet. Dokumentet *Domain IV Addendum (OrgelKraft / SPEC-PODS-PENTAD-RB-12)* forlater konseptet om programvarebasert sikkerhet, og forankrer i stedet IT-OT-autorisasjon direkte i maskinvarelåst termodynamikk og eksakt støkiometri. Systemet opererer på det deterministiske verifikasjonsnivået L1, der fysisk maskinvare holdes i en ufravikelig tilstand av ro (`HOLD`) ved 0,00 V DC inntil en endring er matematisk bevist.

Klassiske SCADA- og PLS-arkitekturer kollapser i møte med avanserte cyberangrep og feilslått algoritmeoptimalisering på grunn av tre fundamentale blindsoner:

**Støkiometrisk drift i flyttall.** Standardisert flyttallsaritmetikk (IEEE-754) er bygget for tilnærming og skjuler dermed fysiske avvik. Gjennom en gradvis settpunkt-glidning fordekt som numerisk støy, kan en elektrolysør presses over temperaturgrensen for katalysatordegradering, eller en krystallisator kan drives forbi Ostwalds nukleasjonsgrense, uten at det overliggende kontrollsystemet registrerer brudd på naturlovene.

**Det usikrede revisjonsvinduet.** En klassisk, diskbasert minnetransaksjon krever cirka 5,0 millisekunder, mens en maskinvarebasert sikkerhetssløyfe evaluerer tilstanden hvert 12,5 mikrosekund. Avventer systemet logging før releet brytes – eller loggfører det intensjon før fullbyrdelse – åpnes et gap på 400 klokkesykluser der en aktør fritt kan manipulere systemtilstanden før maskinvaren reagerer.

**Det fysiske realiseringsgapet.** Konvensjonell programvare bokfører en ordre som utført i det øyeblikket signalet forlater registeret. Om en underliggende ventil låser seg mekanisk, forblir systemet uvitende. Deterministisk testing viser at slike kommandobaserte arkitekturer oppviser en falsk realiseringsrate på 25,00 %. Når systemet underkastes OrgelKrafts tverrmodale realiseringsgrammatikk, reduseres denne feilraten til eksakt 0,00 %.

For å eliminere denne farlige asymmetrien mellom digital ordre og materiell konsekvens, bygger OrgelKraft-arkitekturen på tre L1-verifiserte mekanismer.

**Rasjonal massebalanse.** Tilnærming elimineres. En lukket prosesskaskade på seks grunnstoffer – fra lavspent nitrogenfiksering til enzymatisk biokonvertering – modelleres over 45 konserveringssjekker utelukkende ved bruk av eksakt rasjonal aritmetikk. Inngående og utgående masse over en 24-timers syklus balanserer med et residual på nøyaktig null ($\Delta R = 0$). Et uregistrert masseavvik på mer enn ett milligram utløser et umiddelbart maskinvarekutt til 0,00 V DC.

**Asymmetrisk tidsdomene.** Arkitekturen implementerer en 12,5 mikrosekunders maskinvare-giljotin i SystemVerilog som overvåker et reversibelt minne og et monotont sikringsregister. Dette forbyr fysisk enhver tilbakestilling av tilstand. For å innvilge spenning (5,00 V DC), tilbakeholdes aktuatoren i samtlige 400 sykluser inntil vitneloggen er forseglet til disk. Ved en beskyttende utkobling reverseres kausaliteten: Maskinvaren kutter eksitasjonen til null volt momentant på syklus én, og vitneloggen produseres utelukkende som en post-mortem analyse.

**Tofase-verifisering og galvanisk separasjon.** Systemet etablerer et skarpt skille mellom pre-kausal levedyktighet og fysisk fremdrift. Før strøm kan innvilges, kryssjekkes kausale lyskjegler og termodynamiske bremsehorisonter. Etter aktivering overvåkes den virkelige tilstanden direkte gjennom spolemotstand, termisk entalpi og akustisk løpetid innenfor et lukket aktuatorvindu på 38,4 millisekunder. Ekstern støy og tjenestenektangrep absorberes lydløst av en faststoffbasert luftsluse som utmatter angriperens energi uten mekanisk slitasje. Et reelt kjernebrudd bryter derimot en irreversibel kontakt og krever en totrinns, mekanisk frikoblet menneskelig nullstilling.

Denne strukturelle logikken oversettes direkte til alliansepartnerne i SFI NORCICS. I prosessindustrien erstattes KI-styrte settpunkter med ufravikelig støkiometri. For undervannsinstallasjoner overvåkes og blokkeres aktuatorbevegelser som nærmer seg materialets mekaniske bristepunkt. På den kritiske nettverkskanten avvises all manipulert signalstøy av solid-state komponenter.

Konvensjonell sikkerhet gransker intensjonen i uverifisert kode. I den fysiske verden eksisterer imidlertid ikke intensjon; kun termodynamikk, masse og energi dikterer konsekvens. Når et kontrollsystem bindes direkte til eksakte materielle invarianter, fratas ondsinnet programvare sitt handlingsrom. Sikkerhet reduseres ikke lenger til et spørsmål om programvaretillit. Det opphøyes til en ufravikelig egenskap ved selve materien.

\newpage

# Del II — Teknisk spesifikasjon: OrgelKraft (`SPEC-PODS-PENTAD-RB-12`)

**Operasjonelt sammendrag:** Dokumentet *Domain IV Addendum (OrgelKraft / SPEC-PODS-PENTAD-RB-12)* formaliserer en deterministisk, maskinvarelåst sikkerhetsarkitektur for elektrokjemisk prosessindustri, undervannssystemer og kritisk nettverkskant. Arkitekturen eliminerer tre strukturelle blindsoner i klassiske SCADA/PLC-systemer: flyttallsbasert støkiometrisk drift, tidsvinduet mellom høyfrekvent kontrollsløyfe og diskbasert revisjonslogg, samt gapet mellom digitalt logget intensjon og fysisk utført arbeid.

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
