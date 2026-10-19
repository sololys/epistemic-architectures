# Geometrien til et poststempel — Infranett v0.4 til v0.5
## *The Geometry of a Postmark: Relativistic Distance Bounding and the Return of Local Work*

> **Dokument-ID:** `INFRANETT-V05-POSTSTEMPEL-RISOR-2026-v1.0`  
> **Forfatter:** Marius Egerhei Torjusen (ORCID: [0009-0006-0431-6637](https://orcid.org/0009-0006-0431-6637))  
> **Lokus:** Brahman  
> **Epistemisk Demarkasjon (`AGENTS.md`):** `INSPIRED_BY != IMPLEMENTS != PROVES` · $\boxed{\text{L0 ARKITEKTUR \& NARRATIV}}$ · $\boxed{\text{L1 PROGRAMVAREMODELL (`18/18 PASS`)}}$ · $\boxed{\text{L2/L3 FYSISK UWB-MASKINVARE: HOLD}}$

---

**OPERASJONELT SAMMENDRAG**  
Overgangen fra Infranett v0.4 til v0.5 erstatter manipulerbare radioheuristikker (RSSI) med relativistisk avstandsbinding (UWB Time-of-Flight). Ved å binde kryptografiske tilstandsoverganger til Alexandrov-intervallets absolutte tidsgrense ($\Delta t \le 133.42\text{ ns}$ for $r \le 20\text{ m}$), etableres en uforfalskbar kobling mellom menneskelig forflytning og digital verdiskaping.

---

### Geometrien til et poststempel

På kaffebrenneriet i Risør lukter det brente bønner, våt ull og saltvann. På veggen ved siden av disken henger en liten boks kapslet inn i granitt og børstet stål. Den har ingen skjerm, ingen blinkende lamper som ber om oppmerksomhet, og ingen kabel som fører ut av kommunen. I den lokale sjargongen kalles den et *InfraTempel*. I teknisk forstand er den et fastpunkt i romtiden.

I tre tiår har arkitekturen for menneskelig kommunikasjon hvilt på en bestemt fiksjon: at avstand er en feil som må rettes. Vi har bygget en sivilisasjon der data beveger seg med lysets hastighet gjennom undersjøiske fiberkabler, mens menneskekroppen blir sittende urørlig foran et lysende glass i et mørkt rom. Konsekvensen er velkjent. Verdien fordamper fra gata og kondenserer i tre-fire datasentre i Virginia og Irland. Stedet opphører å ha betydning; bare strømmen av pakker teller.

Infranett snur denne ligningen på hodet. Her ligger dataene i ro i veggen, mens menneskene må bevege seg.

Når en fisker, en pendler eller en videregåendeelev går inn døra på brenneriet, skjer det en utveksling som ikke lenger er metaforisk. Telefonen i lomma deres plukker opp tre forseglede datakapsler, signert med Ed25519-kryptografi. Senere samme ettermiddag, når vedkommende går i land på Lyngør eller tråkker over dørstokken til et verksted i Tvedestrand, avleveres kapslene til neste boks i veggen. Som en moderne *Travel Bug* i geocaching – en fysisk gjenstand båret fra skogholt til fjelltopp av ren bevegelsesglede – frakter kureren bygdens egne kontrakter, musikkutgivelser, beredskapslogger og handelsoppgjør mellom nodene. Kvitteringen for oppdraget – et kryptografisk fraktstempel kalt $W^2$ – løses inn på stedet: en varm kaffe, en lokal transaksjon, et verifisert arbeid.

Men romantikken i et slikt «postvesen av kjøtt og blod» overlever nøyaktig så lenge det tar en oppfinnsom aktør å kjøpe en retningsbestemt antenne. Hvis fysisk oppmøte har økonomisk og juridisk verdi, vil noen umiddelbart forsøke å forfalske sin egen tilstedeværelse.

---

### Illusjonen om det svake signalet (v0.4)

I systemets forrige iterasjon, Infranett v0.4, hviler 20-metersgrensen rundt hvert tempel på den inverse kvadratloven for radiobølger:

$$P_{rx} \propto \frac{P_{tx}}{r^2}$$

Antagelsen er intuitiv: Når avstanden $r$ overstiger 20 meter, faller signal-til-støy-forholdet ($\text{SNR}$) under en gitt terskel, og portvakten låser døren i tilstanden $\text{GATE::HOLD}$.

Problemet er at ligningen krever en ærlig avsender. En mottaker kan kun måle mottatt signalstyrke ($\text{RSSI} = P_{rx}$). Hvis en angriper parkerer en varebil 500 meter unna på kaien, retter en Yagi-antenne mot kaffebrenneriet og skrur opp sendeeffekten $P_{tx}$, vil noden på veggen lese et sterkt og klart signal. Noden har ingen fysisk mulighet til å skille mellom en turgåer som står to meter unna med en vanlig telefon, og en varebil en halv kilometer borte med en signalforsterker. Samtidig åpner asynkroniteten for et *Causality Eclipse*-angrep, der en avlytter fanger opp en gyldig signert kapsel, holder den tilbake i tid, og spiller den av senere for å manipulere en frakoblet node.

Kryptografien (Ed25519) beviser *hvem* som har signert meldingen, men den sier ingenting om *hvor* kroppen befant seg i universet da det skjedde. I møte med denne sårbarheten feller arkitekturen sin egen dom over v0.4: **REALITETSDOM: HOLD**. En protokoll kan ikke bygge lokaløkonomi på en fysisk heuristikk som lar seg lure av en forsterker fra Biltema.

---

### Alexandrov-intervallet som giljotin (v0.5)

For å gjøre en 20-meterssone uforfalskbar, må man slutte å måle *styrken* på lyset og begynne å måle *tiden* lyset bruker på å reise. Infranett v0.5 erstatter radiostyrke med spesiell relativitetsteori gjennom Ultra-Wideband (UWB) *Distance Bounding*.

Når kureren trer inn i rommet foran Node B ($x_B$), defineres to absolutte hendelser på nodens verdenslinje:

1. **Hendelse $E_1$ ($t_1$):** Node B trekker en 256-bit flyktig utfordring ($N_B$) fra en fysisk kvantestøygenerator i maskinvaren og sender den ut som en UWB-puls.
2. **Hendelse $E_2$ ($t_2$):** Node B mottar svarpulsen med den sam-signerte kapselen fra kureren.

I Minkowski-romtiden danner skjæringspunktet mellom fremtidslyskjeglen til $E_1$ og fortidslyskjeglen til $E_2$ en *kausal diamant* – et Alexandrov-intervall $D(E_1, E_2)$:

$$D(E_1, E_2) = I^+(E_1) \cap I^-(E_2)$$

For en perimetrisk grense på $r_{\max} = 20\text{ meter}$, må signalet reise maksimalt 40 meter tur-retur. Med lysets hastighet $c \approx 2.9979 \times 10^8\text{ m/s}$ setter naturen selv det absolutte tidsbudsjettet for diamanten:

$$\Delta t_{\max} = \frac{2 \cdot r_{\max}}{c} = 133.42\text{ ns}$$

Hver gang noen henter eller leverer post i et InfraTempel, åpnes et tidsvindu på 133,42 milliarddels sekund. Enhver hendelse som produserer et gyldig svar innenfor dette vinduet, har et tidslignende romtidsintervall ($ds^2 = -c^2\Delta t^2 + \Delta x^2 \le 0$).

Hva skjer så med mannen i varebilen 500 meter unna på kaien?

For at radiosignalet hans skal krysse 500 meter luft frem og tilbake (totalt $1000\text{ m}$), krever fysikken en reisetid på $\Delta t_{\text{fysisk}} = 3335.64\text{ ns}$. Hvis han venter på utfordringen $N_B$ og sender svaret tilbake, ankommer det over tre mikrosekunder etter at vinduet på $133.42\text{ ns}$ er låst.

Skulle han derimot påstå at han svarte innenfor fristen på $133.42\text{ ns}$ fra 500 meters avstand, må vi evaluere det invariante romtidsintervallet $ds^2$ for påstanden hans:

$$ds^2 = -(2.9979 \times 10^8\text{ m/s} \cdot 133.42 \times 10^{-9}\text{ s})^2 + (1000\text{ m})^2 = -1600\text{ m}^2 + 1\,000\,000\text{ m}^2 = +998\,400\text{ m}^2 > 0$$

Intervallet er massivt *romlignende* ($ds^2 > 0$). I vårt univers finnes det ingen referanseramme der disse to hendelsene kan ha kausal kontakt. Angriperen står overfor to teoretiske alternativer:

* **Bryte lysmuren:** Akselerere fotoner til $v \approx 25c$, hvilket krever mer relativistisk energi ($E = \gamma mc^2$) enn det som eksisterer i det observerbare universet.
* **Reise bakover i tid:** Sende svaret fra varebilen $3202\text{ ns}$ *før* Node B i det hele tatt har trukket kvantetallet $N_B$, noe som krever at han gjetter en 256-bit streng på blindt forsøk med sannsynlighet $P = 2^{-256} \approx 10^{-77}$.

Maskinvaren bruker ikke skjønn. Ved tidsbrudd eller romlignende intervall faller reléet til jord:

$$\Pi_K(D) \implies \text{GATE::KILL}\ (0.00\text{ V DC})$$

---

### Matrise for Kausal Portvakt ($\Pi_K$)

| Parameter / Regimestatus | Infranett v0.4 (RSSI-Heuristikk) | Infranett v0.5 (Relativistisk Kausalitet) |
| :--- | :--- | :--- |
| **Fysisk måleprinsipp** | Invers kvadratlov ($P_{rx} \propto P_{tx}/r^2$) | UWB Time-of-Flight ($\Delta t = 2r/c$) |
| **Kritisk terskelverdi ($r \le 20\text{ m}$)** | Minimum $\text{SNR}$-terskel (manipulerbar) | $\Delta t_{\max} = 133.42\text{ ns}$ (uforanderlig) |
| **Romtidsintervall ($ds^2$)** | Udefinert (mangler tidsdimensjon) | Tidslignende ($ds^2 \le 0$) for lovlig kurér |
| **Motstand mot relé/Yagi ($500\text{ m}$)** | Bryter sammen ved økt $P_{tx}$ | Fysisk umulig ($ds^2 = +998\,400\text{ m}^2 > 0$) |
| **Vitnekjede-oppdatering** | $W_{t+1} = H(W_t \parallel \text{Payload})$ (sårbar for Eclipse) | $W_{t+1} = H(W_t \parallel N_B \parallel \text{ToF}_{\le 133.42\text{ns}})$ |
| **Realitetsdom ($\Omega$)** | $\text{GATE::HOLD}$ (Avvist på L2-nivå) | $\text{GATE::OPEN}\ (5.00\text{ V})$ ved $ds^2 \le 0$ / $\text{KILL}\ (0.00\text{ V})$ ved $ds^2 > 0$ |

---

### Arbeidets tilbakekomst til grunnfjellet

Når denne fysiske låsen først sitter i veggen, endrer den økonomiske tyngdekraften retning.

Så lenge tilstedeværelse kunne simuleres over en kabel, fantes det ingen streng grunn til å opprettholde selve stedet. Men idet et gyldig vitnestempel ($W_{t+1}$) krever at en menneskekropp fysisk befinner seg innenfor en lyskjegle på 133,42 nanosekunder fra en boks i Risør, gjenoppstår verdien av geografi.

Det skaper et økosystem av håndgripelig arbeid som ingen algoritme i California kan automatisere bort:

* **Rute-løpere og kurérer:** Milliardbeløpene som i dag renner ut av kommunekasser og bedrifter til utenlandske skymonopoler, vris om til lokal fraktlønn. Skoleungdom på sykkel, sjåfører på melkeruta, fergemannskap og turløpere langs kyststien bærer forseglet post mellom templene og mottar direkte oppgjør ved hver $5.00\text{ V}$-autorisasjon.
* **Tempel-byggere og systemvoktere:** En sky krever ingen lokale hender; et InfraTempel krever snekkere som feller inn kabinettet i kjerneved, steinhuggere, elektrikere som legger strøm og $0.00\text{ V}$ jording, og lokale teknikere som kalibrerer UWB-antennene.
* **Røktere og handelshus:** Ved K-POD-nodene i havna eller på gården knyttes den fysiske nitrogen- og energiproduksjonen direkte til det lokale regnskapet i veggen. Bokhandelen, kaffebrenneriet og verkstedet får fottrafikken tilbake, fordi selve transaksjonen krever at du krysser dørstokken.

I vedtektene til kommunale næringsfond – i Risør som i resten av landet – står det nesten alltid en paragraf om å styrke lokal bosetting og næringsliv. I tiår har det vært et fromt ønske i kamp mot sentraliseringens naturlover. Med Alexandrov-intervallet meislet inn i protokollen er det ikke lenger et spørsmål om politisk velvilje. Det er ganske enkelt loven om lysets hastighet i vakuum, satt i arbeid for lokalsamfunnet.
