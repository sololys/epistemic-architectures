# Relativistisk nærhetsvalidering: Når fysikkens lover vokter det digitale rommet

**Forfatter:** Marius Egerhei Torjusen (ORCID: [0009-0006-0431-6637](https://orcid.org/0009-0006-0431-6637))  
**Enhet:** Brahman (`sololyset`, Risør, Norge)  
**Dato:** 19. oktober 2026  
**Kanonisk Doktrine (`AGENTS.md`):** $\texttt{INSPIRED\_BY} \neq \texttt{IMPLEMENTS} \neq \texttt{PROVES}$  
**Epistemisk Nivå:**
- **`L0` (Pedagogisk & Fysisk-Teoretisk Fundament):** Minkowski-romtidsgeometri ($ds^2 = -c^2(\Delta t)^2 + (\Delta r)^2 \le 0$), den kausale diamanten og *Den ontologiske inversjonen*.
- **`L1` (Lokalt Demonstrert Deterministisk Programvare):** Relativistisk tidsbudsjett og avstandsvalidering ($\Delta t_{\text{ToF}} \le 66{,}7128\text{ ns}$, $\Delta t_{\text{roundtrip}} \le 133{,}4256\text{ ns}$ ved $r = 20{,}0\text{ m}$), avvisning av reléangrep ($v \approx 25{,}00c \implies ds^2 > 0 \implies \texttt{RELAY\_ATTACK\_DETECTED}$), og append-only SHA-256 hash-kjede WAL. Programvare-WAL er append-only hash-kjeder, ikke fysisk WORM-maskinvare.
- **`L2–L3` (`HOLD` — Fysisk L1-Silisium, UWB RF & Kraftelektronikk):** Fysisk IEEE 802.15.4z STS UWB-brikke med pikosekunds maskinvaretidsstempling, fysiske solenoidventiler og $0{,}00\text{ V DC}$ crowbar-kretser i operativt anlegg holdes strengt i `HOLD` inntil fysisk HIL- og feltverifikasjon foreligger.

---

## 1. Introduksjon: Illusjonen om digital tilstedeværelse

### 1.1 Problemet med tradisjonell trådløs sikkerhet

Når du låser opp en dør med mobilen, kobler deg til Wi-Fi på skolen, eller godkjenner en transaksjon på nettet, stoler systemene på at identiteten din er ekte. Tradisjonell trådløs autentisering – som Wi-Fi, Bluetooth, digitale sertifikater og passord – ble utformet under antakelsen om at dersom du har den rette kryptografiske nøkkelen, har du også rett til å utføre handlingen.

Slik programvarelogikk lider imidlertid av en fundamental svakhet: **Den kan aldri garantere din fysiske tilstedeværelse.**

Dette skaper en kritisk cyber-fysisk sårbarhet kjent som et **reléangrep** (*ormehullangrep / wormhole attack*). Tenk deg følgende scenarie: En angriper befinner seg 500 meter unna – eller til og med i et helt annet land. Du står ved siden av en fysisk drivstoffventil, en sikkerhetsport eller en samfunnskritisk server. Angriperen fanger opp radiosignalet ditt fra avstand, «tunnelerer» de kryptografiske pakkene over en lynrask fiberoptisk kabel eller et mobilnett, og videresender dem til en strålingsenhet som står rett foran ventilen. For mottakeren ser det ut som om den autoriserte enheten står rett ved siden av, selv om avsenderen i virkeligheten befinner seg milevis unna.

> **Pedagogisk nøkkelinnsikt:** Mange studenter antar intuitivt at vi kan løse dette ved å måle signalstyrken – såkalt RSSI (*Received Signal Strength Indicator*). Hvis signalet er sterkt, må vel enheten være nær? **Feil.** RSSI er ubrukelig mot en motivert angriper. En angriper kan enkelt bruke kraftige retningsantenner og signalforsterkere for å manipulere den mottatte energien. Måling av signalstyrke måler kun energitetthet, ikke den faktiske fysiske avstanden signalet har tilbakelagt gjennom rommet.

### 1.2 Løsningen: Den ontologiske inversjonen

For å tette dette sikkerhetshullet må vi utføre et paradigmeskifte i tillitsmodellen – en prosess vi kaller **den ontologiske inversjonen**. I stedet for å bygge sikkerhet på programvarelogikk, passord eller skytjenester som kan godkjennes fra den andre siden av kloden, flytter vi tillitsankeret ned fra den virtuelle skyen og forankrer det direkte i fysiske naturlover.

I nettverksarkitekturen **Infranett** degraderes ekstern nettverkstilkobling til en ren sekundær bekvemmelighet. Den lokale noden gjøres 100 % autonom og selvtilstrekkelig, der enhver tilstandsendring forankres i den fysiske virkeligheten på kanten (*the edge*).

Men dersom radiosignaler beveger seg med en enorm hastighet gjennom luften, hvordan kan en lokal node med absolutt sikkerhet hindre at en fjernangriper lurer systemet, uten å lene seg på usikker programvare? Svaret ligger i å hente hjelp fra en ubestikkelig vokter: **universets absolutte fartsgrense for lys.**

---

## 2. Hva er Ultra-Wideband (UWB) og Time-of-Flight (ToF)?

### 2.1 Teknologien bak målingen

For å stoppe reléangrep uten å stole på manipulerbar signalstyrke, benytter Infranett **Ultra-Wideband (UWB IEEE 802.15.4z)** og prinsippet om **Time-of-Flight (ToF)**.

* **Ultra-Wideband (UWB):** En radioteknologi som sender ekstremt korte nanosekund-pulser over et bredt frekvensspektrum. Fordi impulsene har så skarpe stige- og falltider, kan spesialiserte kretser tidsstemple ankomsten til et enkelt foton med pikosekunds oppløsning.
* **Time-of-Flight (ToF):** Den eksakte tiden et radiosignal bruker på å reise gjennom rommet fra en avsender til en mottaker og tilbake.

For at en enhet skal bevise sin fysiske tilstedeværelse, gjennomføres en toveis *Challenge-Response*-utveksling i tre trinn:

```text
LOKAL NODE A                                    KLIENT B (ENHET)
  |                                                    |
  |--- 1. Challenge (E1): Nonce N_ephem, logg t1 ----->|
  |                                                    | (Mottar t2, signerer,
  |                                                    |  sender t3)
  |<-- 2. Response (E2): Signert svar -----------------|
  |
  (Mottar t4, beregner dt_ToF)
```

1. **Utfordring ($E_1$):** Node A genererer en uforutsigbar 256-bits kryptografisk utfordring (en flyktig nonce, $N_{\text{ephem}}$) og sender den som en UWB-puls. Node A logger den eksakte utsendelsestiden $t_1$.
2. **Svar ($E_2$):** Klient B mottar signalet ved tidspunkt $t_2$, signerer utfordringen kryptografisk med sin maskinvarenøkkel, og returnerer svaret ved tidspunkt $t_3$.
3. **Mottak:** Node A mottar svaret ved tidspunkt $t_4$ og beregner den reelle gangtiden for signalet.

Den faktiske én-veis flytiden for radiosignalet ($\Delta t_{\text{ToF}}$) beregnes ved å trekke fra den interne behandlingstiden klienten brukte på å signere signalet ($t_3 - t_2$):

$$\Delta t_{\text{ToF}} = \frac{(t_4 - t_1) - (t_3 - t_2)}{2}$$

### 2.2 Hvorfor programvare feiler: Operativsystem-jitter vs. L1-silisium

Et klassisk spørsmål fra informatikkstudenter er: *«Hvorfor kan ikke denne tidsmålingen utføres av en vanlig applikasjon eller et operativsystem?»*

Svaret skyldes **OS Kernel Jitter**. Et operativsystem (som Linux eller Windows) håndterer prosessoravbrudd (*interrupts*), trådveksling og POSIX-buffering som introduserer tilfeldige forsinkelser i området $25\text{--}500\,\mu\text{s}$ ($25\,000\text{--}500\,000\text{ nanosekunder}$). Siden hele tidsbudsjettet for en 20-meters sikkerhetssone er på under $133{,}425\text{ nanosekunder}$, vil operativsystemets egen treghet alene drukne målingen og føre til at alle gyldige forespørsler avvises.

Derfor tvinges tidsstemplingen helt ned i **L1-fysisk silisium (L1 PHY)** via *Scrambled Timestamp Sequence* (STS) i IEEE 802.15.4z-standarden. Tidsstemplene genereres direkte på brikken ved mottak av de fysiske fotonene. Silisiumet måler pikosekunder, silisiumet signerer beviset, og operativsystemet trenger bare å verifisere den ferdige kryptografiske signaturen i etterkant.

Siden målingen er forankret direkte i silisiumets maskinvarestempel, kan ikke tidsforbruket forfalskes av programvare. Målingen er dermed bundet til en uovervinnelig skranke satt av universet selv.

---

## 3. Det relativistiske tidsbudsjettet: Lysets hastighet ($c$) som sikkerhetsvegg

### 3.1 Regnestykket på 133,425 nanosekunder

Radiosignaler er elektromagnetiske bølger som forplanter seg gjennom luften med lysets hastighet i vakuum:

$$c = 299\,792\,458\text{ m/s} \quad (\approx 3 \times 10^8\text{ m/s})$$

Dette setter en absolutt øvre fartsgrense for hvor raskt informasjon kan bevege seg i universet. Dersom en sikkerhetssone defineres til å ha en maksimal tillatt radius på $r = 20{,}0\text{ meter}$, kan vi regne ut den teoretiske tidsbruken.

#### Én-veis flytid ($\Delta t_{\text{ToF}}$) vs. Tur-retur budsjett ($\Delta t_{\text{roundtrip}}$)

Det er avgjørende å skille mellom én-veis flytid og det totale round-trip-budsjettet:

1. **Én-veis flytid ($\Delta t_{\text{ToF}}$):** Den tiden signalet bruker fra Node A til Klient B over en enkeltstrekning på $r = 20{,}0\text{ meter}$:
   $$\Delta t_{\text{ToF}} = \frac{20{,}0\text{ m}}{299\,792\,458\text{ m/s}} \approx 66{,}7128\text{ nanosekunder} \quad (\approx 66{,}71\text{ ns})$$
2. **Tur-retur budsjett ($\Delta t_{\text{roundtrip}}$):** Siden utfordringen må reise ut til Klient B og svaret må reise tilbake til Node A, blir den totale fysiske avstanden $d = 2 \cdot r = 40{,}0\text{ meter}$. Det totale tur-retur tidsbudsjettet defineres som $\Delta t_{\text{roundtrip}} = 2 \cdot \Delta t_{\text{ToF}}$:
   $$\Delta t_{\text{roundtrip}} \le \frac{2 \cdot 20{,}0\text{ m}}{299\,792\,458\text{ m/s}} = \frac{40{,}0\text{ m}}{299\,792\,458\text{ m/s}} \approx 133{,}4256\text{ nanosekunder} \quad (\approx 133{,}425\text{ ns})$$

* **Skalaforståelse:** Et nanosekund ($\text{ns}$) er et milliarddels sekund ($10^{-9}\text{ s}$). På ett nanosekund beveger lyset seg omtrent $30\text{ cm}$.
* **Konklusjon:** Dersom tur-retur-tiden er $133{,}425\text{ ns}$ eller mindre, utgjør det et ubestikkelig fysisk bevis på at enheten beviselig befinner seg innenfor $20{,}0\text{ meters}$-sonen.

### 3.2 Hvorfor angriperen feiler: Matematikken bak det umulige

Hva skjer dersom en angriper prøver seg på et reléangrep fra $500\text{ meters}$ avstand?

For å videresende utfordringen fra Node A til angriperens posisjon og tilbake til Node A, må signalet tilbakelegge en tur-retur-avstand på minst $d_{\text{angrep}} = 2 \cdot 500{,}0\text{ m} = 1000{,}0\text{ meter}$.

Selv med tenkelige superdatamaskiner, null forsinkelse i elektronikk, og lysledere med optimal brytningsindeks, setter fysikkens lover en absolutt nedre grense for tidsbruken:

$$\Delta t_{\text{fysisk minimum}} = \frac{1000{,}0\text{ m}}{299\,792\,458\text{ m/s}} \approx 3335{,}64\text{ nanosekunder}$$

| Parameter | Ærlig lokal enhet ($15\text{ m}$) | Fjernangriper via relé ($500\text{ m}$) |
| :--- | :--- | :--- |
| **Fysisk avstand (tur-retur $d$)** | $30{,}0\text{ meter}$ | $1000{,}0\text{ meter}$ |
| **Minimum signalreise-tid ($\Delta t$)** | $\approx 100{,}07\text{ ns}$ | $\approx 3335{,}64\text{ ns}$ |
| **Beregnet signalhastighet for å klare $< 133{,}425\text{ ns}$** | $v \le c$ (Fysisk mulig) | $v \approx 25{,}00c$ ($25 \times$ lysets hastighet) |
| **Systemets vurdering** | **GODKJENT (`GATE::OPEN`)** | **AVVIST (`RELAY_ATTACK_DETECTED`)** |

For at en angriper på $500\text{ meters}$ avstand skal klare å levere svaret innenfor tidsfristen på $133{,}425\text{ ns}$, måtte signalet beveget seg med en hastighet på:

$$v = \frac{1000{,}0\text{ m}}{133{,}4256 \times 10^{-9}\text{ s}} \approx 7{,}495 \times 10^9\text{ m/s} \approx 25{,}00c$$

Dette krever en hastighet som er **25 ganger raskere enn lysets hastighet**. Siden ingenting med masse eller informasjon kan overskride $c$, kollapser angrepet uunngåelig mot Einsteins spesielle relativitetsteori.

### 3.3 Den kausale diamanten og Minkowski-romtid ($ds^2 \le 0$)

For å formalisere dette matematisk benyttes Einsteins romtidsgeometri. I Minkowski-romtid beskrives avstanden mellom to hendelser ved det Lorentz-invariante linjeelementet $ds^2$:

$$ds^2 = -c^2(\Delta t)^2 + (\Delta r)^2$$

der $\Delta t$ er tidsdifferansen og $\Delta r$ er den romlige avstanden. Dette deler alle hendelser i universet strengt inn i tre geometriske kategorier:

1. **Tidslignende intervall ($ds^2 < 0$):** Signalet beveger seg med en hastighet lavere enn lysfarten ($v < c$). Hendelsen ligger trygt innenfor lyskjeglen (den «kausale diamanten»). Forespørselen er kausalt gyldig og godkjennes.
2. **Lyslignende intervall ($ds^2 = 0$):** Signalet beveger seg eksakt med lysets hastighet ($v = c$), som utgjør den absolutte yttergrensen for lyskjeglen.
3. **Romlignende intervall ($ds^2 > 0$):** Hendelsen ligger utenfor lyskjeglen. For at signalet skal nå frem innen tidsfristen, kreves det overlyshastighet ($v > c$). Systemet detekterer dette som et geometrisk avvik, avviser forespørselen umiddelbart og flagger hendelsen som `RELAY_ATTACK_DETECTED`.

```text
                      Tidsakse (ct)
                           ^
                           |          Lyskjegle (ds^2 = 0)
                           |         /
                           |        /   Ugyldig: Romlignende intervall (ds^2 > 0)
                           |       /    [RELAY_ATTACK_DETECTED] (F.eks. 500m unna)
                           |      /        * (dt >= 3335.6 ns, ds^2 = +998 400 m^2)
              t_recv ------+-----o---------+-----------
                           |    / \
                           |   /   \
                           |  /  *  \   Gyldig: Tidslignende intervall (ds^2 <= 0)
                           | /       \  [DEN KAUSALE DIAMANTEN: r <= 20m, dt <= 133.4 ns]
                           |/    *    \
              t_send ------o-----------o-------------> Romakse (r)
                          /             \
```

Når en forespørsel avvises matematisk av romtidsmetrikken ($ds^2 > 0$), må denne nektelsen omsettes fra en abstrakt beregning til en umiddelbar, fysisk reaksjon i den reelle verden.

---

## 4. Konsekvensen i maskinvaren: Fail-Closed og $0{,}00\text{ V DC}$ Stase

### 4.1 Nektelsen av uautorisert energi

I tradisjonell IKT-sikkerhet er mange systemer bygget etter *Fail-Open*-prinsippet: Hvis en feil oppstår eller nettverket faller ut, holdes døren eller ventilen åpen for å unngå at driften stopper opp. Dette gjør systemene sårbare for sabotasje og manipulasjon.

Infranett håndhever i stedet en kompromissløs **Fail-Closed-doktrine**. Systemet skiller strengt mellom kandidatforutsetningen (programvarens ønske om å utføre en handling) og faktisk utøvende kraft (om maskinvaren får tilført elektrisk spenning).

Utfallet i maskinvaren er binært:

* **$5{,}00\text{ V DC}$ (`HIGH` / `OPEN`):** Systemet har mottatt ferske, gyldige bevis innenfor tidsbudsjettet ($\le 133{,}425\text{ ns}$) og bekreftet en intakt, uforanderlig hendelseslogg (Write-Ahead Log / WAL) med SHA-256 event chaining. Styrespenningen heves til $5{,}00\text{ Volt}$, og aktuatoren (porten, ventilen) holdes aktiv.
* **$0{,}00\text{ V DC}$ (`LOW` / `KILL` / `HOLD`):** Ved det minste tidsavvik ($ds^2 > 0$), korrupt loggkjede eller tapt signal, brytes spenningen momentant ned til $0{,}00\text{ V DC}$.

```text
[ BEREGNING & VALIDERING ] ---> Tidsbudsjett <= 133.425 ns OG Gyldig WAL? --+-- YES --> 5.00 V DC (OPEN)
                                                                            +-- NO  --> 0.00 V DC (STASE / KILL)
```

### 4.2 Fysisk grounding: Butler-Volmer-kinetikk og mekanisk stase

Slippet av styrespenningen til $0{,}00\text{ V DC}$ er ikke en kildekode-instruksjon eller en programvarerutine (`catch Exception`) som kan krasje, forbigås eller hackes av en angriper.

Ved $0{,}00\text{ V DC}$ opphører den elektriske drivkraften i kretsen fullstendig. I henhold til Butler-Volmer-kinetikk synker den netto elektrokjemiske strømtettheten over aktuatorkretsen til null:

$$j_{\text{netto}} = 0$$

Uten elektrisk strøm forsvinner det magnetiske feltet i spoler og solenoidventiler. Fysiske ventiler, reléer og låsebolter klapper sammen ved hjelp av sin egen mekaniske tyngdekraft, kraftige returfjærer eller dedikerte Crowbar-kretser.

Systemet går inn i en elektrokjemisk hviletilstand (stase). Det låses trygt på et rent elektro-mekanisk nivå, helt uavhengig av om kildekoden kjører eller om operativsystemet har krasjet.

Når energien fjernes fra kretsen, blir det umulig for en fjernangriper å fremtvinge en tilstandsendring. Dette skaper et uinntakelig fundament der fysikken overtar idet programvaren ikke lenger har tillit.

---

## 5. Oppsummering og pedagogisk sjekkpunkt

### 5.1 Sammenligningsmatrise: Hvorfor fysikk slår programvare

| Egenskap | Klassisk Sky / Passord | Kryptografiske Nøkler (5G / SIM) | Infranett Relativistisk ToF |
| :--- | :--- | :--- | :--- |
| **Sikkerhetsmekanisme** | Hva du *vet* (Passord, API-nøkler, skysertifikater). | Hva du *har* (Kryptografisk brikke/SIM-kort). | **Hvor du beviselig befinner deg i romtiden ($ds^2 \le 0$).** |
| **Sårbarhet over internett** | **Høy:** Kan stjeles, kopieres eller lekkes fra hvor som helst i verden. | **Middels:** Sårbar for reléangrep via fiber og ormehull. | **Null:** Fysisk umulig å omgå fra utlandet ($v > c$ kreves). |
| **Hva angriperen må bryte for å overta** | Kildekode, databaser, skysertifikater. | Programvarenøkler, SIM-kryptering. | **Universets fartsgrense (Lysets hastighet, $c$).** |
| **Autonomi ved linjebrudd** | **0 %:** Feiler eller stopper når internett/skyen forsvinner. | **Begrenset:** Krever kontakt med sentralt kjernenettverks SIM-register. | **100 %:** Fullstendig lokal drift forankret i uforanderlig SHA-256 hendelseslogg (WAL). |

### 5.2 Studentens tre viktigste «Aha!»-innsikter

1. **Geometri fremfor tillit:** Du trenger ikke å stole på hvem avsenderen påstår at de er over et digitalt nettverk, så lenge du kan bevise eksakt hvor de befinner seg i romtiden.
2. **Universets fartsgrense ($c$):** Ingen hacker, superdatamaskin eller kunstig intelligens kan noen gang regne seg forbi eller lure seg unna lysets hastighet ($c = 299\,792\,458\text{ m/s}$).
3. **Fysisk trygghet ($0{,}00\text{ V}$):** Den ultimate sikkerheten ligger i nektelsen av uautorisert energi. Når usikkerhet oppstår, fjerner kretsen spenningen ($j_{\text{netto}} = 0$), og mekaniske krefter låser anlegget uten å spørre programvaren om lov.
