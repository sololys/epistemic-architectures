# Det Optiske Laser-Vitnet ($W_{\text{laser}}$): Okklusjonsskranke, FSO-Taushet og $532\text{ nm}$ Undervannskausalitet i Infranett v0.5

**Forfatter:** Marius Egerhei Torjusen (ORCID: [0009-0006-0431-6637](https://orcid.org/0009-0006-0431-6637))  
**Enhet:** Brahman (`sololyset`, Risør, Norge)  
**Dato:** 19. oktober 2026  
**Kanonisk Doktrine (`AGENTS.md`):** $\texttt{INSPIRED\_BY} \neq \texttt{IMPLEMENTS} \neq \texttt{PROVES}$  
**Referansemotor (`L1`):** `engines/infranett_laser_fso_witness_engine.py` (`7/7` enhetstester `PASS` i `tests/test_infranett_laser_fso_witness_engine.py`)  
**Epistemisk Nivå:**
- **`L0` (Optisk-Relativistisk Arkitektur):** Dobbeltvitnet $W_{\text{range}} \land W_{\text{laser}}$, EMCON-lasersamband og $532\text{ nm}$ maritimt transmisjonsvindu.
- **`L1` (Lokalt Demonstrert Deterministisk Programvare):** Gaussisk strålegeometri, vakuum/luft Minkowski-port ($\Delta t_{\text{RTT}} \le 133{,}4256\text{ ns}$), refraktiv sjøvannsport ved $n = 1{,}334$ ($\Delta t_{\text{vann,RTT}} \le 177{,}9898\text{ ns}$), safirglass-dokking ($I_{\text{galvanisk}} = 0{,}0\,\mu\text{A}$) og append-only SHA-256 hash-kjede WAL. Programvare-WAL er append-only hash-kjeder, ikke fysisk WORM-maskinvare.
- **`L2–L3` (`HOLD` — Fysisk Optisk Maskinvare & Feltpilot):** Fysiske $1550\text{ nm}$ øyesikre FSO-lasermoduler, $532\text{ nm}$ Nd:YAG undervannstransceivere og safir-optokoblere på kurerkapsler holdes strengt i `HOLD` inntil fysisk laboratorie- og feltverifikasjon foreligger.

---

## 1. Hvorfor Infranett kombinerer UWB-Radio med Koherent Laser ($W_{\text{range}} \land W_{\text{laser}}$)

Ultra-Wideband (UWB IEEE 802.15.4z) måler lysets gangtid ($c = 299\,792\,458\text{ m/s}$) og avgrenser tilgang til en kausal kule med radius $r_{\max} = 20{,}0\text{ m}$ ($\Delta t_{\text{RTT}} \le 133{,}4256\text{ ns}$). Men mikrobølger i UWB-båndet ($3{,}1\text{--}10{,}6\text{ GHz}$) har én geometrisk begrensning: **De kan trenge gjennom tynne vegger, gipsplater, treverk og vinduer.**

En uautorisert aktør som står $3{,}0\text{ meter}$ unna på *utsiden* av veggen til et kontrollrom eller pumpehus, befinner seg teknisk sett innenfor $20\text{ meters}$ avstand ($\Delta t_{\text{RTT}} \approx 20{,}0\text{ ns} \le 133{,}4256\text{ ns}$), selv om vedkommende ikke er inne i selve rommet.

Ved å tilføre **Det Optiske Laser-Vitnet ($W_{\text{laser}}$)** løser Infranett v0.5 fire fundamentale fysiske oppgaver som radiobølger ikke kan løse alene:

1. **Romlig Innelukking (Okklusjonsskranke ved $1550\text{ nm}$):** Koherent lys går aldri gjennom en ugjennomsiktig vegg. Kreves både UWB og direkte optisk laser-siktlinje, beviser noden at operatøren befinner seg **inne i eksakt samme fysiske rom**.
2. **Total Radiotaushet (EMCON Free-Space Optics):** En kollimert laserstråle med lav divergens har null radiofrekvente sidelober, kan ikke peiles av fiendtlige ESM/ELINT-antenner, og kan ikke jammes utenfra uten å fysisk blokkere selve lysstrålen.
3. **Undervannskausalitet ved $532\text{ nm}$ (Blågrønn Laser i Sjøvann):** I sjøvann dør radiobølger etter få centimeter, mens akustisk sonar er treg ($v_{\text{lyd}} \approx 1500\text{ m/s}$) og røper posisjonen i hele fjorden. Sjøvannets optiske transmisjonsvindu ved $\lambda = 532\text{ nm}$ muliggjør relativistisk avstandsvalidering under vann ved $v_{\text{vann}} = c / n_{\text{vann}} \approx 2{,}247 \times 10^8\text{ m/s}$.
4. **Galvanisk Isolert Kurer-Dokking gjennom Safirglass:** Overfører Write-Ahead Loggen mellom K-POD-kurerkapsel og lokal node med rene fotoner over et dielektrisk safirvindu ($R_{\text{DC}} = \infty\,\Omega$), fullstendig beskyttet mot lyn, jordfeil og EMP.

---

## 2. De Fire Optiske Realiseringsportene i Infranett v0.5

```text
+-----------------------------------------------------------------------------------+
|                 INFRANETT v0.5: DET OPTISKE LASER-VITNET (W_laser)                |
+-------------------+-------------------+---------------------+---------------------+
| 1. ROMSPERRE      | 2. FSO EMCON-LINK | 3. SUBSEA 532 nm    | 4. SAFIR-DOKKING    |
| (1550 nm + UWB)   | (Gaussisk stråle) | (Blågrønn laser)    | (Optisk K-POD)      |
|                   |                   |                     |                     |
| Stopper ved vegg: | 0.0 W RF-lekkasje | Sjøvann n = 1.334   | Galvanisk skille:   |
| Krever fysisk     | Strålebrudd ->    | v = 2.247e8 m/s     | I_lekk = 0.0 uA     |
| sikt i samme rom  | 0.00 V DC HOLD    | RTT <= 177.99 ns    | >= 25 kV EMP-vern   |
+-------------------+-------------------+---------------------+---------------------+
```

### 2.1 Port 1: Romlig Innelukking og Okklusjonsskranke ($W_{\text{range}} \land W_{\text{laser}}$)

For høyrisiko-aktuatorer (f.eks. hovedventiler i vannverk, drivstoffdepot eller transformatorstasjoner) krever konsekvensporten $\Omega_{\text{room}}$ konjunksjonen av både UWB-avstandsbevis og en øyesikker, fasekodet $1550\text{ nm}$ laser-siktlinje:

$$\Omega_{\text{room}} = \begin{cases}
\mathbf{5{,}00\text{ V DC (OPEN)}} & \text{hvis } ds^2_{\text{UWB}} \le 0 \land \Delta t_{\text{laser,RTT}} \le 133{,}4256\text{ ns} \land \text{LOS}_{\text{optisk}} = 1 \land \text{Token}_{\text{valid}} = 1 \\
\mathbf{0{,}00\text{ V DC (HOLD)}} & \text{hvis } \text{LOS}_{\text{optisk}} = 0 \quad (\texttt{OPTICAL\_LOS\_BROKEN\_WALL\_OCCLUSION}) \\
\mathbf{0{,}00\text{ V DC (KILL)}} & \text{hvis } ds^2 > 0 \lor \Delta t > 133{,}4256\text{ ns} \lor \text{Token}_{\text{valid}} = 0
\end{cases}$$

Dersom en angriper står $3{,}0\text{ m}$ unna på utsiden av mur- eller gipsveggen, passerer UWB-testen ($\Delta t_{\text{UWB}} \approx 20{,}0\text{ ns}$), men veggen absorberer $1550\text{ nm}$-fotonene ($\text{LOS}_{\text{optisk}} = 0$). Porten nekter å åpne og forblir i $0{,}00\text{ V DC}$ (`HOLD`).

### 2.2 Port 2: Radiotaus FSO Punkt-til-Punkt Link og Avlyttingsvern (Gaussisk Stråle)

For en Gaussisk laserstråle med bølgelengde $\lambda = 1550\text{ nm}$ og strålemidje (waist) $w_0 = 5{,}0\text{ mm}$ er Rayleigh-lengden:

$$z_R = \frac{\pi w_0^2}{\lambda} \approx 50{,}67\text{ m}$$

Ved avstanden $z = 20{,}0\text{ m}$ er strålens flekkradius kun:

$$w(z) = w_0 \sqrt{1 + \left(\frac{z}{z_R}\right)^2} \approx 5{,}38\text{ mm} \quad (\text{diameter } \approx 1{,}08\text{ cm})$$

Fordi hele energien er samlet i en lysstråle på én centimeter i diameter:
* **Null RF-utstråling ($P_{\text{RF}} = 0{,}0\text{ W}$):** Linken er usynlig for radiofrekvent signaletterretning.
* **Selvdetekterende avlyttingsvern:** En fysisk sonde eller person som forsøker å gå inn i strålen for å tappe eller jamme signalet, kaster en umiddelbar optisk skygge ($\eta_{\text{trans}} = P_{\text{rx}} / P_{\text{tx}} < 0{,}50$). Noden detekterer effektfallet momentant som `BEAM_OCCLUSION_OR_INTERCEPT_DETECTED` og feller utgangen til $0{,}00\text{ V DC}$.
* **Null metallisk multipath:** I maskinrom av stål der radiobølger reflekteres mellom vegger, går laserstrålen snorrett uten flerveisstøy.

### 2.3 Port 3: $532\text{ nm}$ Blågrønn Undervannslaser (Maritim & Subsea Kausalitet)

I sjøvann med brytningsindeks $n_{\text{vann}}(\lambda = 532\text{ nm}) \approx 1{,}334$ forplanter det blågrønne laserlyset seg med fase- og gruppehastigheten:

$$v_{\text{vann}} = \frac{c}{n_{\text{vann}}} = \frac{299\,792\,458\text{ m/s}}{1{,}334} \approx 224\,731\,977{,}51\text{ m/s}$$

For en undersjøisk sikkerhetssone med radius $r_{\max} = 20{,}0\text{ m}$ ($\Delta r = 40{,}0\text{ m}$ tur-retur mellom kaifundament og undervannsfartøy/ventil) er det refraktive tur-retur-tidsbudsjettet:

$$\Delta t_{\text{vann,RTT}} \le \frac{2 \cdot n_{\text{vann}} \cdot r_{\max}}{c} = 133{,}4256\text{ ns} \times 1{,}334 \approx \mathbf{177{,}9898\text{ nanosekunder}}$$

Det refraktive Minkowski-linjeelementet i sjøvann evalueres som:

$$ds^2_{n} = -\left(\frac{c}{n_{\text{vann}}}\right)^2 (\Delta t)^2 + (\Delta r)^2 \le 0$$

Samtidig sjekkes den mottatte optiske effekten etter Beer-Lamberts dempningslov $P_{\text{rx}}(r) = P_{\text{tx}} e^{-c_{\text{att}} r}$. Dette gir maritim infrastruktur (havner, brønnrammer, kystforsvar) en lydløs (sonar-usynlig) avstandslås med nanosekundpresisjon under vann.

### 2.4 Port 4: Galvanisk Isolert Optisk Kurer-Dokking (Safirvindu)

Når en K-POD-kurerkapsel (fra drone, losbåt eller melkebil) dokker mot en lokal node i uvær eller under EMP-trussel, elimineres elektriske pinner til fordel for en optisk høyhastighetslink gjennom et herdet safirglassvindu ($\Delta r_{\text{dock}} \le 50\text{ mm}$):

* **Galvanisk lekkasjestrøm:** $I_{\text{galvanisk}} = 0{,}0\,\mu\text{A}$ (enhver målbar elektrisk strøm $> 0\,\mu\text{A}$ utløser `GALVANIC_ISOLATION_BREACH_CONDUCTIVE_PATH` $\implies \mathbf{KILL}$).
* **Overspenningsvern:** Safirglasset og luftgapet gir $> 25\text{ kV}$ dielektrisk isolasjon, slik at lynnedslag eller kraftnett-sabotasje aldri kan forplante seg mellom kurerkapsel og node.

---

## 3. Sammenligningsmatrise: UWB Radio vs. Koherent Laser i Infranett v0.5

| Egenskap | UWB Radio ($W_{\text{range}}$) | Infranett Laser ($W_{\text{laser}}$: $1550\text{ nm}$ / $532\text{ nm}$) | Kombinert Dobbeltport ($W_{\text{range}} \land W_{\text{laser}}$) |
| :--- | :--- | :--- | :--- |
| **Fysisk bølgebærer** | RF-puls ($3{,}1\text{--}10{,}6\text{ GHz}$) | Koherente fotoner ($1550\text{ nm}$ IR / $532\text{ nm}$ grønn) | Orto-fysisk redundans (RF + Optikk) |
| **RTT-budsjett ($20\text{ m}$ luft)** | $\le 133{,}4256\text{ ns}$ | $\le 133{,}4256\text{ ns}$ | $\max(\Delta t_{\text{UWB}}, \Delta t_{\text{laser}}) \le 133{,}4256\text{ ns}$ |
| **RTT-budsjett ($20\text{ m}$ sjøvann)** | Fungerer ikke (absorberes) | **$\le 177{,}9898\text{ ns}$ ($532\text{ nm}$, $n=1{,}334$)** | Dekkes av $532\text{ nm}$ undervannslaser |
| **Stopper ved innervegg?** | Nei (kan trenge gjennom gips/tre) | **Ja ($100\,\%$ okklusjonsskranke)** | **Garanterer samme fysiske rom** |
| **Radiotaushet (EMCON)?** | Lav spektraltetthet, men RF | **$0{,}0\text{ W}$ RF-utstråling (umulig å radio-peile)** | Kan kjøre i ren laser-EMCON ved krig |

---

## 4. Verifikasjon (`L1` Standardbibliotek)

```bash
PYTHONPATH=. python3 -m unittest tests/test_infranett_laser_fso_witness_engine.py -v
```
