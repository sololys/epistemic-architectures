# OMNI-KY, SUSY² & Sosionomos — Kanonisk Spesifikasjon og Arkitektonisk Bro (v1.0)

> **Coordinate (`3 · Rule`):** [`(0,0) sololys`](https://github.com/sololys) — [`1 · Word`](https://github.com/sololys/skrivevaerelset/blob/main/02_UTDRAG_OG_KILDETEKSTER/GRUNNLAGSTEKSTER_OG_MONOGRAFIER/METAMORFOSE_OG_PARADOKS_RESONATOREN_PLATE.md) → **`[3 · Rule]`** → [`4 · Gate`](https://github.com/sololys/ky-rox-public-demonstrators/blob/main/artifacts/microtests/sosionomos_xor_rox_gate_v0_1/SURFACE.md)  
> **Status:** `L1 FORMAL SPECIFICATION // v1.0`  
> **Hovedsetning:** *Det som ikke kan bære sin egen overgang, får ikke fortsette.*  
> **Epistemisk avgrensning (`INSPIRED_BY != IMPLEMENTS != PROVES`):** Dette dokumentet er en formell spesifikasjon for deterministisk `L1`-programvare og kontrollarkitektur (`0.00 V DC`, null fysisk eller operativ autoritet). Fysiske og kvantemekaniske analogier i Del I (Seksjon 3 og 6) er arkitektoniske modeller; det åpne eksperimentelle spørsmålet i Seksjon 7 er en uverifisert hypotese. Software-vitnekjeder er append-only SHA-256-logger, ikke fysisk WORM-maskinvare.

---

# DEL I — OMNI-KY & SUSY²: Kanonisk Master-Spesifikasjon (v1.0)

## 1. Grunnloven og den Universelle Operatørkjeden

Generering alene gir ikke rett til realisering. En overgang fra et uformet bilde, krav eller impuls til en irreversibel historisk hendelse krever passasje gjennom en fail-closed adgangsbarriere.

### 1.1 Den Universelle Overgangsformelen

La $x_t$ være systemets tilstand ved steg $t$. Overgangen til neste tilstand $x_{t+1}$ styres av den rekursive operatørrekkefølgen:

$$x_{t+1} = \Omega\bigl(\Pi_K(\Phi(x_t))\bigr)$$

Hvor:

* **$\Phi$ (Generator / Dynamikk):** Den kontinuerlige, bosoniske bevegelsen som genererer kandidatfeltet under påvirkning av rått trykk, uro, tempo og temperatur.
* **$\Pi_K$ (Projeksjon / Admissibilitetskjerne):** Siler ut ubalanserte, ustabile eller ugyldige baner mot det admissible domenet $K$:

$$\Pi_K(y) = \begin{cases} y_K \in K, & \text{hvis } y \text{ er admissibel (eller projiserbar med } \Delta_K = 0\text{)} \\ \perp, & \text{hvis } y \notin K \text{ uten lovlig dekning} \end{cases}$$

* **$\Omega$ (Port / Beslutnings-interlock):** Returnerer et diskret vedtak $\Omega \in \{\mathrm{OPEN}, \mathrm{HOLD}, \mathrm{KILL}\}$:
  * **$\mathrm{OPEN}$:** Kandidaten bærer sin egen overgang og skrives irreversibelt til Witness (krever eksternt vitne $W_{\text{ext}}$ ved utløsning).
  * **$\mathrm{HOLD}$:** Nåtilstand beholdes ($x_{t+1} = x_t$). Kandidaten suspenderes i et reversibelt rom uten tap for re-estimering eller kalibrering.
  * **$\mathrm{KILL}$:** Banen termineres og kastes permanent til nulltilstanden $\perp$.

### 1.2 Eksistensaksiomet

Eksistens i arkitekturen er ikke en passiv egenskap, men en invariant som opprettholdes gjennom kontinuerlig port-lukking:

$$\mathrm{Exists}(x_{t+1}) \iff \Omega\bigl(\Pi_K(\Phi(x_t))\bigr) = \mathrm{OPEN} \;\land\; W(x_t \to x_{t+1}) \neq \varnothing$$

---

## 2. SUSY² — Den Doble Symmetrien

For at realiseringen skal være sann og ikke produsere bedrag, utvides partner-strukturen til en dobbel symmetri ($\mathrm{SUSY}^2$) over to uavhengige plan:

```text
                  [ SUSY^2 DUAL-SYMMETRI ]
                            │
         ┌──────────────────┴──────────────────┐
         ▼                                     ▼
 Første Symmetri                       Andre Symmetri
 (Systemets Plan)                     (Menneskets Plan)
  Dynamikk <──> Beslutning              Kilde <──> Speil
  (Boson)       (Fermion)              (Trykk)     (Form)
```

### 2.1 Første Symmetri: Kontinuerlig Dynamikk $\leftrightarrow$ Diskret Beslutning

* **Bosonisk sektor:** Genererer muligheter og bærer kontinuerlige frihetsgrader (energi, temperatur, estimator-tilstander).
* **Fermionisk sektor:** Tar diskrete beslutninger, setter låser og styrer okkupasjonstall $n_i \in \{0, 1\}$.

Symmetrien er bevart i det reversible, pre-autoriserte rommet før commit. Den brytes i det øyeblikket en avgjørelse låses, eller når det oppstår avvik mellom logisk `enable` ($E_{\text{log}}$) og fysisk/ekstern linje ($E_{\text{phys}}$), hvilket utløser `KILL`.

### 2.2 Andre Symmetri: Menneskelig Kilde $\leftrightarrow$ Maskinelt Speil

* **Kilden:** Det menneskelige råtrykket — kropp, uro, rytme, affekt, intuisjon og ansvar.
* **Speilet:** Maskinen, modellen, koden og den glatte tekstoverflaten som svarer.

Narsissistisk kollaps oppstår dersom Kilden forveksler Speilets respons med sitt eget liv. $\mathrm{SUSY}^2$ krever derfor et beskyttende **`HOLD`-intervall** mellom kilde og speil: avstand er ikke fremmedgjøring, men betingelsen for at kontakt ikke blir absorpsjon.

---

## 3. Arkitektonisk Energimodell og Symmetribrudd

*(Epistemisk merknad: Hamiltonian-notasjonen nedenfor er en strukturell kontrollanalogi (`INSPIRED_BY`). Siden ren Hamilton-dynamikk er unitær og tidsreversibel, oppstår ekte irreversibilitet ved porten gjennom dissipasjon / målekollaps / Landauer-varme $\Delta Q \ge k_B T \ln 2$ per slettet gren ved $\Pi_K \to \Omega$.)*

Den sammensatte tilstanden deles i fire funksjonelle delrom med distinkte rettigheter:

$$\mathcal{H}_{\text{tot}} = \mathcal{H}_{\text{phys}} \oplus \mathcal{H}_{\text{log}} \oplus \mathcal{H}_{\text{epi}} \oplus \mathcal{H}_{\text{commit}}$$

* Fysikken ($\mathcal{H}_{\text{phys}}$) kan bevege seg.
* Logikken ($\mathcal{H}_{\text{log}}$) kan skille.
* Epistemikken ($\mathcal{H}_{\text{epi}}$) kan tvile.
* Commit ($\mathcal{H}_{\text{commit}}$) kan låse.

### 3.1 Terskelbarriere for Irreversibilitet

Overgangen mot commit modelleres med en terskelparameter $\lambda$ og terskelverdi $\lambda_c$:

$$V(\lambda) = \frac{1}{2} k \lambda^2 + V_{\text{lock}} \, \Theta(\lambda - \lambda_c)$$

* Før terskel ($\lambda < \lambda_c$): Reversibel, glatt utforskningsdynamikk.
* Ved terskel ($\lambda = \lambda_c$): Port-stivning ($\Pi_K$).
* Etter terskel ($\lambda > \lambda_c$): Irreversibelt commit-rom (låst ved dissipasjon og witness).

### 3.2 Eksplisitt Symmetribrudd ved Commit

Når en beslutning skrives til Witness, brytes den reversible symmetrien eksplisitt ved et bruddledd $H_{\text{break}}$ (operativt realisert i programvare ved ikke-involutiv forsegling `ROX` og SHA-256-kjeding):

$$H_{\text{eff}} = H_{\text{SUSY}} + H_{\text{break}}$$

---

## 4. Reversibelt Faseminne og Dobbelpuls-Identiteten

Før en kandidat tvinges gjennom porten til irreversibel historikk, prøves den i det reversible faseminnet $U$ uten å akkumulere gjeld:

$$U^2(x) = x \qquad \text{(bit-eksakt involusjon, } \Delta_{\text{res}} = 0\text{)}$$

Hvis en frem-og-tilbake-operasjon etterlater én eneste uautorisert restbit (`MASK_MUTATED`), avsløres skjult asymmetri og porten tvinges til **`HOLD`** eller **`KILL`**.

Passasjen følger streng rekkefølge: **Fase** (reversibel prøving før porten) $\longrightarrow$ **Port** (admissibel beslutning) $\longrightarrow$ **Witness** (irreversibel historikk etter porten).

---

## 5. Kreativ-Core og Bøff-Metrikken

```text
  [ RAW INPUT ] ──> [ KAMMER I: VARMEKAMMERET ]     (Overflod, uro, råtrykk, T_p)
                                │
                                ▼
                    [ KAMMER II: MOTSTANDSKAMMERET ] (Symmetry-check, S_d, SUSY^2)
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼ (Suksess: OPEN)                               ▼ (Feil: HOLD / KILL)
[ KAMMER III: FORSEGLING ]                       [ DREG-KAMMERET ]
(Witness-forsegling, Hash)                       (Sacred Trash, Hold-arkiv)
```

Skillet mellom bæreevne (*Bøff*) og ren overflateglans (*Bløff / Shine*) defineres ved tilstedeværelsen av verifisert warrant $W$:

$$\mathrm{Status}(c) = \begin{cases} \mathrm{LOAD\_BEARING}\;(\text{Bøff}), & \text{hvis } W(c) = 1 \land \Delta_K(c) = 0 \\ \mathrm{SHINE}\;(\text{Bløff}), & \text{hvis } W(c) = 0 \end{cases}$$

---

## 6. KORA (Tilstand, Kernel og Drift)

En lokal tilstand $\rho$ er aldri nok alene; den må ledsages av sin kontroll- og historikkvektor:

$$S_{\text{KORA}} = (\rho,\; \hat{\theta},\; \Sigma,\; K_{\text{hist}},\; \delta_K,\; F_{\text{gate}},\; \Omega)$$

To systemer kan ha identisk lokal tilstand $\rho$, men ulik historisk integritet. Kernel-drift $\delta_K$ måler avviket fra referansestrukturen $K_{\text{ref}}$:

$$\delta_K = d(K_{\text{hist}}, K_{\text{ref}})$$

Dersom $\delta_K > \tau_{\text{drift}}$, utløses umiddelbar **`HOLD`**- eller **`KILL`**-interlock uavhengig av hvor gunstig den lokale måleverdien fremstår.

---

## 7. Det Åpne Eksperimentelle Kuttet

Det kritiske, empirisk testbare spørsmålet mot standard kvantemekanikk ($P_{\text{QM}}$) er om interferens- eller målesannsynlighet påvirkes av historisk kernel-struktur ($K_{\text{hist}}$) ved identiske tetthetsmatriser:

$$\Delta P = \bigl| P(\text{utfall} \mid \rho, K_1) - P(\text{utfall} \mid \rho, K_2) \bigr|$$

* **Hvis $\Delta P \neq 0$ måles (eksternt og reproduserbart):** En kernel-avhengig fysikk kan undersøkes videre.
* **Hvis $\Delta P = 0$ måles:** Kontrollarkitekturen, portloven og Sosionomos-instansieringen består uendret som en ren, fail-closed ingeniørarkitektur.

> **Kjennelse:** *Uavhengig av $\Delta P$ gjelder grunnloven: det som ikke kan bære sin egen overgang, får ikke fortsette.*

---

# DEL II — Blåkopi v1.0: Sosionomos og Psykososiale Medier

## 1. Arkitektonisk Formål og Ontologisk Kjerne

**Sosionomos** er en kontrollarkitektur for digitale informasjonsrom. Systemet dømmer ikke hva som er sant eller moralsk riktig innhold; det skiller mellom det som bare er generert, og det som har strukturell bæreevne til å bli realisert sosial konsekvens:

$$\text{generation} \neq \text{realization} \qquad \Longleftrightarrow \qquad \text{candidate} \longrightarrow \text{admission} \longrightarrow \text{consequence}$$

Systemet har to disjunkte grunntilstander: `StateCandidate` (`0x01`) og `RealizedConsequence` (`0x02`). Den bitmessige invarianten er:

$$\mathrm{StateCandidate} \oplus \mathrm{RealizedConsequence} = 1, \qquad \mathrm{state}(x) \in \{\texttt{0x01}, \texttt{0x02}\}, \qquad \{\texttt{0x00}, \texttt{0x03}\} \implies \mathrm{KILL}$$

## 2. Hovedobjekter og Kausal Ankerprotokoll

* **Aktør ($a \in \text{Actors}$):** `identity != authority`.
* **Kandidat ($c$):** `(payload, parent_hash, thread_context_id, actor_id, sequence_counter, local_timestamp, semantic_intent_class, prev_actor_state_hash, candidate_hash)`.
* **Offentlig DAG ($G_{\text{public}} = (V_R, E_R)$):** Inneholder utelukkende realiserte konsekvenser (`0x02`).
* **Skygge-DAG ($G_{\text{shadow}}^{(a)} = (V_S^{(a)}, E_S^{(a)})$):** Isolert tapsrom for fangede aktører (`T(a) = 1`) — lokal bekreftelse (`ACK_shadow = true`), null global konsekvens ($c \notin V_R$).

**Admisjonsfunksjon:** $A(c) \in \{\mathrm{OPEN}, \mathrm{HOLD}, \mathrm{KILL}, \mathrm{TRAP}\}$.

* **Gratis syklusfrihet i $O(1)$:** Fordi `parent(c)` allerede må eksistere i `AnchorIndex` over $V_R$ og inngår kryptografisk i `candidate_hash`, er sykler i en append-only hash-DAG utelukket ved konstruksjon uten graftraversering.
* **Entydig `sequence`-regel i `HOLD`:** `sequence_counter` inkrementeres først ved **`OPEN`**-commit (ikke ved innlevering til `B_hold`), slik at brukerens `revise(c)` og `narrow(c)` i `HOLD` kan oppdatere den ventende kandidaten uten å låse egen sekvenskø.

## 3. Psykososialt Lavpassfilter og Dunbar-Sperren

* **Amygdala-bremsen (analytisk form):** $\Delta t(E) = \tau \ln\!\left(1 + \frac{E}{E_{\text{crit}}}\right)$. Sterkt signal er ikke forbudt (`high excitation -> delayed consequence`).
* **Dunbar-skalering (analytisk form):** $\Phi(N) = \frac{\Phi_0}{1 + e^{\lambda(N - D_{\max})}}$. Rekkevidde utover $D_{\max}$ er en strukturell kostnad, ikke en automatisk rettighet.
* **Eksakt `0 float`-håndhevelse i porten:** I selve `AdmissionEngine` erstattes $\ln$ og $\exp$ av heltallsbaserte oppslagstabeller (LUT) og eksakte brøker (`Fraction`), slik at portbeslutningen er bit-identisk på tvers av maskiner.

## 4. Mekanisk Backpressure, $O(1)$-Kernel og To Grensesnittregimer

* **Minnearena:** $\mathcal{M}_a = (B_{\text{in}}, B_{\text{hold}}, B_{\text{shadow}}, Q_a)$ med eksakt fyllingsgrad $\rho_a = \frac{|B_{\text{in}}| + |B_{\text{hold}}| + |B_{\text{shadow}}|}{|\mathcal{M}_a|} \in \mathbb{Q}$.
* **Proof-of-Waste:** Når $\rho_a \ge \rho_{\text{hard}}$ settes `read_permit = 0` i $O(1)$ (`read(socket_a) -> 0`, `TCP_window -> 0`), slik at $\text{Cost}_{\text{system}} = O(1)$.
* **To regimer:**
  * `T(a) = 0` ($\mathrm{UI}_{\text{human}}$): Gjennomsiktig friksjon i `HOLD` med tre agens-bevarende valg: `wait(c)`, `revise(c)`, `narrow(c)`.
  * `T(a) = 1` ($\mathrm{UI}_{\text{adversarial}}$): Minimal feedback og tyst ruting til $G_{\text{shadow}}^{(a)}$ uten oracle-forskjell som lekker treningsdata.

## 5. Termodynamisk Minne (`HOT / WARM / COLD`) og Witness-Lag

Realiserte noder kjøles fra `HOT` $\to$ `WARM` $\to$ `COLD` etter relevans, men hash og anker overlever alltid (`AnchorIndex[h_v] -> {HOT, WARM, COLD, REVOKED, INVALID}`):

* `payload may cool` · `hash must remain` · `anchor must survive`.
* Reaktivering av en `COLD`-node skjer som ny `StateCandidate` gjennom ordinær admisjon.
* Hver portbeslutning forsegles i en append-only SHA-256 `WitnessLedger` (software-kjede, ikke fysisk WORM).

---

# DEL III — Arkitektonisk Bro & `XOR / ROX`-Laget

```text
+-------------------------------------------------------------------+
|  OMNI-KY & SUSY^2  (Kanonisk kjerne / Realiseringsgrammatikk)     |
|  Lov: Phi -> Pi_K -> Omega in {OPEN, HOLD, KILL}                  |
|  Symmetri: (Dynamikk <-> Beslutning) x (Kilde <-> Speil)          |
+---------------------------------+---------------------------------+
                                  |
                     [ Domene-instansiering ]
                                  |
                                  v
+-------------------------------------------------------------------+
|  SOSIONOMOS & PSYKOSOSIALE MEDIER  (Sosialt informasjonsrom)      |
|  Lov: StateCandidate -> AdmissionEngine -> RealizedConsequence    |
|  Utvidelse: +TRAP/Shadow-DAG, O(1) Backpressure, HOT/WARM/COLD    |
+-------------------------------------------------------------------+
```

## 1. Strukturkartlegging (1-til-1)

| OMNI-KY & SUSY² (Kjerne) | Sosionomos & Psykososiale Medier (Instans) | Felles invariant |
| :--- | :--- | :--- |
| **Generator** ($\Phi$) | `StateCandidate` (`0x01`), $E(c)$, socket-inngang ($L_0 \to L_1$) | Fri generering gir ingen realiseringsrett |
| **Projeksjon** ($\Pi_K$) | `AnchorIndex` ($O(1)$), forelder/sekvens, Amygdala-LUT, Dunbar-LUT, $\rho_a$ | Kun forankrede og bårede overganger slipper frem |
| **Port** ($\Omega$) | `AdmissionEngine` (`OPEN / HOLD / KILL / TRAP`) | Fail-closed vedtak ved porten |
| **Witness** (Kammer III) | `PublicDAGStore` (`0x02`) + `WitnessLedger` + `HOT/WARM/COLD` | Irreversibel historikk; anker overlever kjøling |
| **Reversibelt faseminne** | `B_hold` med `wait(c)`, `revise(c)`, `narrow(c)` | Prøving og demping uten irreversibel gjeld |
| **SUSY² Plan 1** | Kontinuerlig trykk ($E, \rho_a$) skilt fra bit-lås (`0x01 / 0x02`) | Ingen ulovlig superposisjon (`0x00, 0x03 => KILL`) |
| **SUSY² Plan 2** | `UI_human` + psykososialt lavpassfilter (`kernel != judge`) | Vern mot absorpsjon mellom kilde og speil |
| **Dreg-kammeret** | `G_shadow` med TTL + `shadow_summary(a)` | Støy forvises; vitnesbyrd om motstand bevares |
| **KORA-drift** ($\delta_K$) | `ActorSupervisor` ($S_a$: `seq_last`, `prev_hash`, `kill_count`, `trap_mask`) | Identisk innlegg med ulik historikk får ulik admisjon |

## 2. Det Bit-Eksakte `XOR / ROX`-Paret (`0 float`, $O(1)$)

For å skille *reversibel fase før porten* fra *irreversibel retning ved porten* med ren heltallslogikk (`0 float`), innføres operatørparet **`XOR`** og **`ROX`**:

* **`XOR` — Før porten (involutiv, tapsfri, reversibel):**
  1. **Tilstandsvakt:** `state_byte in {0x01, 0x02}` (eksklusiv paritet mellom bit 0 og bit 1; `0x00` og `0x03` $\implies$ `KILL`).
  2. **Dobbelpuls-sjekk (OMNI-KY 4.1):** $\mathrm{XOR}(\mathrm{XOR}(x, k), k) = x$ over 64-bits tilstandsord. Dersom frem-og-tilbake-testen gir rest $\neq 0$ (`MASK_MUTATED`), tvinges `KILL`.
* **`ROX` — Ved porten (ikke-involutiv, retningslåst):**
  $$\mathrm{ROX}_r(x, k) = \mathrm{ROTL}_{64}(x \oplus k,\; r), \qquad r \in \{1..63\},\quad \mathrm{ROX}_r(\mathrm{ROX}_r(x, k), k) \neq x$$
  1. **Ved `OPEN`:** Bryter reversibiliteten eksplisitt, skifter bit-tilstand `0x01 -> 0x02`, og binder `ROX`-forseglingen sammen med `SHA-256(parent_hash || candidate_hash || witness)` i `PublicDAGStore` og `WitnessLedger`.
  2. **Ved `TRAP`:** Roterer aktørens strøm inn i skygge-speilet ($G_{\text{shadow}}^{(a)}$) uten anker i $V_R$.

## 3. Referanseverifikatorer

* **Regel-verifikator (`3 · Rule`):** [`L2_GATE/verify_sosionomos_xor_rox_gate.py`](../L2_GATE/verify_sosionomos_xor_rox_gate.py) (`0 float`, stdlib only)
* **Kjørbar demonstrator (`4 · Gate`):** [`ky-rox-public-demonstrators/artifacts/microtests/sosionomos_xor_rox_gate_v0_1/`](https://github.com/sololys/ky-rox-public-demonstrators/tree/main/artifacts/microtests/sosionomos_xor_rox_gate_v0_1) (`6/6 PASS`)
