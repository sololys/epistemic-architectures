# MARKEDS- OG PRODUKTBESKRIVELSE: SOLOLYS (EPISTEMIC ARCHITECTURES)
### *Vedlegg til søknad — Regionalt næringsfond for Østregionen (Risør / Agder)*

**Søker / Gründer:** Marius Egerhei Torjusen — *Founder & Chief Systems Architect, Sololys / ReismannPoint Systems*  
**Lokalisering:** Risør kommune (Østregionen, Agder)  
**Kontakt:** `sololyset@gmail.com` // Tlf: `+47 93 29 45 26` // ORCID: `0009-0006-0431-6637`  
**Teknisk referansearkiv:** [`github.com/sololys/epistemic-architectures`](https://github.com/sololys/epistemic-architectures) // CERN Zenodo Master DOI: [`10.5281/zenodo.18436983`](https://doi.org/10.5281/zenodo.18436983)  
**Modenhets- og verifikasjonsstatus:** Nivå $\text{L1}$ ferdigstilt (deterministisk programvare, eksakt rasjonal hovedbok og RTL-maskinvaresimulering). Søknaden gjelder markedsavklaring, kommersiell lisenspakking og pilotforberedelse mot $\text{L2}$ (*Hardware-in-the-Loop* / testbed) i samarbeid med nasjonale forsknings- og industripartnere ($\text{INSPIRED\_BY} \neq \text{IMPLEMENTS} \neq \text{PROVES}$).

---

## 1. Sammendrag og forretningsidé

**Sololys** utvikler og lisensierer deterministiske sikkerhets- og styringsarkitekturer i skjæringspunktet mellom **informasjonsteknologi (IT / kunstig intelligens)** og **operasjonell teknologi (OT / fysisk industri, kraftnett, skipsfart og prosessanlegg)**.

Når industribedrifter, rederier, nettselskaper og offentlig beredskap kobler moderne programvare og kunstig intelligens (AI) på fysiske maskiner, oppstår en kritisk sikkerhetsrisiko: En digital algoritme kan foreslå feilaktige eller manipulerte kommandoer uten kostnad i minnet, mens en fysisk feilkobling i en ventil, et skip, en batteripakke eller en trafo er irreversibel.

Sololys løser dette ved å plassere en matematisk og maskinvarelåst **konsekvensport ($\Phi \to \Pi_K \to \Omega \to W^2$)** mellom det digitale styringslaget og den fysiske aktuatoren. Ingen digital kommando eller AI-modell får direkte skrivemyndighet til fysisk utstyr (`standalone_commit_authority = NONE`). Fysisk spenning (**$5{,}00\text{ V DC}$**) innvilges kun dersom endringen på forhånd er matematisk bevist innenfor anleggets fysiske bevaringslover; ved ethvert avvik tvinges systemet til en betingelsesløs hviletilstand (**$0{,}00\text{ V DC}$**).

Hele grunnarkitekturen og de kjørbare $\text{L1}$-motorene er utviklet fra Risør. Selskapet går nå over i **kommersialiserings- og pilotfasen**, etter å ha oppnådd konkret faglig respons og møteinvitasjon fra **Norsk Regnesentral (NR)** og **SFI NORCICS (Norwegian Centre for Cybersecurity in Critical Sectors ved NTNU)**.

---

## 2. Produktportefølje (Tre modulære kjerneprodukter)

Produktene leveres som lisensierbare programvarekjerner (Python/C/Rust), syntetiserbare maskinvaremoduler (SystemVerilog RTL for FPGA) og protokollspesifikasjoner:

### Produkt A: $\Pi_K$ Consequence Gate — Sikkerhetslås for AI og industriell styring (HMI/PLS)
* **Kundeproblem:** Klassiske SCADA/PLS-systemer logger en ordre som «utført» i det sekundet signalet forlater det digitale registeret, uten å verifisere om ventilen faktisk beveget seg fysisk, og etterlater et usikret tidsvindu på **400 klokkesykluser ($\sim 5{,}0\text{ ms}$)** ved diskskriving (`fsync`). I deterministiske feilinjeksjonsforsøk ($\text{L1}$, `seed=42`, $8\,000$ kjøringer) gir klassiske arkitekturer en falsk realiseringsrate på **$25{,}00\,\%$** ved mekanisk ventillåsing.
* **Løsning og kundeverdi:**
  1. **Pre-Commit barriere ($\Pi_K$):** Sjekker alle AI- og operatørsettpunkter mot en fremadrettet Nagumo-sikkerhetsbarriere og 41 diskrete bremsebaner før strøm settes på.
  2. **Asymmetrisk 400-syklusregel ($12{,}5\,\mu\text{s}$ FPGA-giljotin):** For å *åpne* en port ($5{,}00\text{ V DC}$) kreves ferdig forseglet vitnelogg på disk. For å *kutte* ved fare (`KILL` $\to 0{,}00\text{ V DC}$) kuttes spenningen momentant på **syklus 1 ($12{,}5\,\mu\text{s}$)**, mens loggen skrives etterpå.
  3. **Tverrmodal fysisk kontroll ($\Pi_{\text{orth}}$):** Måler faktisk spole-EMK, varme ($\Delta T$) og akustisk løpetid innen **$38{,}4\text{ ms}$** og reduserer falsk realisering fra **$25{,}00\,\%$ til $0{,}00\,\%$**.

### Produkt B: Infranett — Sky-uavhengig beredskapsnett og maritim anti-spoofing
* **Kundeproblem:** Maritim sektor langs kysten, kraftnettet, politiet og helsevesenet er sårbare når satellittnavigasjon (GNSS/GPS) utsettes for jamming/spoofing, eller når fiber- og skyforbindelsen til omverdenen brytes under uvær eller sabotasje.
* **Løsning og kundeverdi:**
  1. **Lokal-først autonomi ($\partial A / \partial C_{\text{fiber}} \equiv 0$):** Systemet krever null skyforbindelse for å opprettholde sikker drift og kryptografisk sporbarhet (lokal append-only SHA-256-forfedrekjede).
  2. **Fysisk lyskjegle-navigasjon:** Avslører falske GPS-signaler i havner og kystfarvann ved å låse posisjonsautoritet til lysets hastighet via Ultra-Wideband Time-of-Flight ($d_{\text{ToF}} \le c\Delta t/2$) og euklidsk fasevinkelkontroll ($\lvert\sin\theta\rvert \le 1{,}0$).
  3. **Gnistfri elektronisk luftsluse ($8{,}0\,\mu\text{J}$):** Absorberer eksterne tjenestenektangrep (DoS) og støy i faststoff ved $0{,}00\text{ V DC}$ uten mekanisk slitasje på brytere og releer.

### Produkt C: OrgelKraft & GSC-X — Støkiometrisk prosess- og batterisikkerhet
* **Kundeproblem:** I elektrokjemisk prosessindustri (hydrogen, ammoniakk, smelteverk, karbonfangst/CCS) og i store batterisystemer (BMS på skip og i bygg) kan små avrundingsfeil i flyttall (IEEE-754) eller manipulerte sensorer skjule farlig gassutvikling, lekkasjer eller gryende batteribrann (*thermal runaway*).
* **Løsning og kundeverdi:**
  1. **Eksakt rasjonal massebalanse ($\Delta R = 0$):** Erstatter flyttalls-tilnærminger med eksakt brøkregning (`fractions.Fraction`) over 45 konserveringssjekker. Ethvert uregistrert masseavvik over **$1\text{ mg}$** utløser automatisk maskinvarekutt til $0{,}00\text{ V DC}$.
  2. **Deterministisk batteri- og spenningslås:** Håndhever harde spenningsgrenser (f.eks. $0{,}998\text{ V DC}$ under vannspaltingsgrensen for knallgass) og termisk/elektrisk BMS-interlock ($T \ge 55\,^\circ\text{C}$ eller impedansvekst $> 80\text{ m}\Omega$).
  3. **Bygnings- og parkintegrerte moduler:** Arkitekturen er dimensjonert for berøringssikker integrasjon i klimanøytrale bygg, sykehus og urbane beredskapsnoder.

\newpage

## 3. Dokumentert markedsbekreftelse og traksjon (Oktober 2026)

Sololys har allerede passert den mest krevende terskelen for et dypteknologisk oppstartsselskap: **uavhengig faglig anerkjennelse fra Norges ledende forskningsmiljø på cybersikkerhet i kritisk infrastruktur.**

1. **Bekreftet møte og samarbeidsdialog med Norsk Regnesentral (NR) & SFI NORCICS (NTNU):**
   Etter gjennomgang av vår tekniske spesifikasjon (*Non-AI Consequence Gating for IT-OT Integration*) i forbindelse med CPS4CIP 2026, responderte **Dr. Habtamu Abie** – *Chief Research Scientist ved Norsk Regnesentral og leder for Focus Area 1 (IT-OT Integration) i SFI NORCICS* – med direkte invitasjon til samarbeidsmøte i uke 44:
   > *«Thank you for sharing the technical brief and for the thoughtful work you have put into aligning the consequence gate framework with the three IT-OT domains discussed in the CPS4CIP 2026 thread. The explicit distinction between reference architecture, software-level verification, and operational HIL/field qualification is particularly valuable. I appreciate your contribution and your interest in exploring these topics further with the SFI NORCICS team at the Norwegian Computing Center. I would be very happy to arrange a meeting to discuss your work, exchange perspectives, and explore potential synergies with our ongoing activities.»*  
   > — **Dr. Habtamu Abie**, Chief Research Scientist, Norsk Regnesentral / SFI NORCICS (Oktober 2026).

2. **Internasjonal forskningsinteresse (6G & Industriell kontroll):**
   Konkret henvendelse i oktober 2026 fra seniorforskernivå ved **BTU Cottbus / IHP Microelectronics (Tyskland)** om faglig utforskning og mulig samarbeid innen deterministiske sikkerhetsporter for 6G URLLC trådløs industristyring.

3. **Dokumentert og tidsstemplet IP-grunnlag:**
   Arkitekturen er dokumentert gjennom en publisert hovedmonografi (*Konseptuell Granitt*, 74 sider), kjørbare $\text{L1}$-testsuiter og over 180 tidsstemplede arbeider på **CERN / Zenodo**, som sikrer Sololys suveren *Background IP* i møte med større konsortier og industrikunder.

---

## 4. Marked, målgrupper og relevans for Agder / Østregionen

Gjennom dialogen med **SFI NORCICS** får Sololys en direkte faglig inngangsport til de mest betalingsdyktige kundesegmentene i Norge og Norden, med særskilt relevans for Agders egne satsingsområder:

| Marked & Sektor | Konkrete målgrupper / Partnere i økosystemet | Sololys-produkt | Regional kobling til Østregionen & Agder |
| :--- | :--- | :--- | :--- |
| **1. Batteri & Prosessindustri** | Batteriverdikjeden i Agder (*Battery Coast*), Norsk Hydro, Yara, Glencore, Elkem | **OrgelKraft & GSC-X** ($\Delta R = 0$, BMS termisk interlock) | Direkte overførbart til batteri- og prosessindustrien langs Agder-kysten (Arendal/Østregionen/Kristiansand). |
| **2. Maritim & Kystberedskap** | Kongsberg Maritime, Equinor, havner, kystfart og autonome fartøy | **Infranett & $\Pi_K^{\text{maritime}}$** (UWB ToF anti-spoofing) | Kystkommunene i Østregionen (Risør/Tvedestrand) og Skagerrak-korridoren. |
| **3. Kraftnett & Fornybar Energi** | Elvia, Agder Energi / Å Energi, Statnett, mikronett og sol/vind | **$\Pi_K^{\text{VSG}}$** (Dispersjonsport & $2f+1$ kvorum) | Stabilisering av distribuerte strømnett og lokale energilagre i distriktskommuner. |
| **4. Kommune, Helse & Politi** | Sykehus, politi, kommunal vann/avløp og kriseledelse | **Infranett** ($\partial A / \partial C_{\text{fiber}} \equiv 0$) | Sikrer at kommunal infrastruktur i Østregionen fungerer lokalt ved nettverks- og strømbortfall. |

---

## 5. Forretningsmodell og bruk av midler fra Regionalt næringsfond

Sololys opererer etter en **kapitallett «Open-Core»- og IP-lisensieringsmodell** med hovedbase i **Risør**:
1. **Fase 1 — FoU- og Testbed-partnere (Nåværende fase):** Felles testbed-validering ($\text{L1} \to \text{L2}$ HIL) med forskningsinstitutter (Norsk Regnesentral / SFI NORCICS / NTNU) finansiert gjennom nasjonale og europeiske FoU-programmer (Forskningsrådet, ENFIELD, EU-CIP, SkatteFUNN og NATO DIANA).
2. **Fase 2 — B2B Evaluerings- og PoC-lisenser:** Betalte *Proof-of-Concept*- og HIL-lisenser til industripartnere som tester $\Pi_K$-porten, *Infranett* eller *OrgelKraft* på egne anlegg.
3. **Fase 3 — Kommersielle produksjonslisenser og Royalties:** Løpende lisensinntekter per installert kontrollnode/FPGA-port i maritim sektor, kraftnett og prosessindustri.

### Hva søknadsmidlene fra Regionalt næringsfond for Østregionen skal brukes til:
* **Aktivitet 1 — Markeds- og partnerforhandlinger (Norsk Regnesentral / SFI NORCICS / Industri):** Gjennomføring av oppfølgingsmøter, pilotspesifisering og konsortieforankring i Oslo, Trondheim og Agder.
* **Aktivitet 2 — Kompakt fysisk demonstratorrigg ($\text{L1} \to \text{L2}$ HIL-bro):** Klargjøring av en bærbar demonstratorpakke (FPGA/mikrokontroller-grensesnitt med fysisk $0{,}00\text{ V DC} / 5{,}00\text{ V DC}$ utgangstrinn og live telemetri) som kan tas med direkte i møter med kunder og testlaboratorier.
* **Aktivitet 3 — Kommersielt lisens- og avtaleverk:** Kvalitetssikring av standardiserte B2B PoC- og lisensavtaler for å sikre at IP-rettigheter og langsiktig verdiskaping forblir forankret i **Risør og Østregionen**.
