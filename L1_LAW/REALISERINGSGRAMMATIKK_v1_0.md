# REALISERINGSGRAMMATIKK v1.0

**En formell grammatikk for overgangen fra generert kandidat til realisert konsekvens**  
*Kanonisk arbeidsutkast — samlet strukturell versjon*

---

## 0. Grunnpremiss

Realisering er ikke generering.

En kandidat er ikke en konsekvens. Representasjon er ikke validering. Validering er ikke autorisasjon. Autorisasjon er ikke fysisk realisering. Registrering er ikke bevis på at en fysisk konsekvens fant sted.

$$\boxed{\text{GENERATE} \neq \text{VALIDATE} \neq \text{AUTHORIZE} \neq \text{REALIZE} \neq \text{WITNESS}}$$

Realiseringsgrammatikken definerer betingelsene som må være oppfylt før en generert kandidat kan gis overgangsautoritet, og hvordan den faktiske konsekvensen av en autorisert overgang skal skilles fra kandidatens opprinnelige representasjon.

Grammatikken er ikke en generator. Den er ikke en sannhetsmaskin. Den er en overgangs- og avgrensningsgrammatikk.

---

## 1. Ontologisk separasjon

Grammatikken skiller mellom fem forskjellige objekter.

| Objekt | Betydning |
| :--- | :--- |
| **Kandidat (`C`)** | En generert, foreslått eller beregnet tilstand. |
| **Admissibilitet (`A`)** | Om kandidaten oppfyller definerte strukturelle, epistemiske og operative vilkår. |
| **Autorisasjon (`U`)** | Om kandidaten har tillatelse til å passere overgangsgrensen. |
| **Realisering (`R`)** | En faktisk overgang eller konsekvens i det definerte systemet. |
| **Vitne (`W`)** | Et evidensobjekt som dokumenterer observerte forhold rundt overgang eller konsekvens. |

$$C \neq A \neq U \neq R \neq W$$

Dette er en strukturell separasjon, ikke en påstand om at objektene aldri kan relateres.

---

## 2. Kandidatrommet

La $x_t$ betegne den observerte eller etablerte systemtilstanden ved tidspunkt $t$. En kandidat genereres av en kandidatfunksjon:

$$c_t = \Phi(x_t, \eta_t)$$

Generatoren har ingen overgangsautoritet:

$$\boxed{\Phi \not\Rightarrow \Omega}$$

### 2.1 Kandidatens identitet

$$c = (\mathrm{id}, \mathrm{payload}, \mathrm{version}, \mathrm{origin})$$

Kandidatidentitet må ikke forveksles med kandidatens sannhet, gyldighet eller realisering.

---

## 3. Før-port-rommet

Før kandidaten får overgangsautoritet eksisterer et rom for reversibel prøving, simulering, sammenligning, strukturell kontroll, avvisning og tilbakeholdelse. Det tillater aldri at simulert konsekvens automatisk registreres som fysisk realisert konsekvens.

### 3.1 Faseinndeling

$$D_0 \rightarrow D_1 \rightarrow D_{1.2} \rightarrow D_{1.5} \rightarrow D_2 \rightarrow D_3$$

| Fase | Navn | Funksjon |
| :--- | :--- | :--- |
| `D0` | `RAW` | Rå input, representasjon eller ubehandlet kandidatmateriale. |
| `D1` | `REVERSIBLE` | Reversible operasjoner og kandidatbehandling. |
| `D1.2` | `STRUCTURAL` | Struktur, type, integritet og konsistens. |
| `D1.5` | `GATE` | `OPEN`, `HOLD` eller `KILL`. |
| `D2` | `COMMITTED / REALIZED` | Autorisert overgang og registrert realiseringsstatus. |
| `D3` | `WITNESS` | Evidens, dokumentasjon og etterfølgende kontroll. |

### 3.2 Forbudte snarveier

$$D_0 \not\rightarrow D_{1.2}, \qquad D_0 \not\rightarrow D_2, \qquad D_1 \not\Rightarrow D_2$$

---

## 4. Admissibilitetsfunksjonen

La $K$ representere systemets definerte admissibilitetsdomene:

$$\Pi_K(c_t, e_t, p_t)$$

### 4.1 Admissibilitetsdimensjoner

$$A(c) = \left( A_{\mathrm{struct}},\ A_{\mathrm{epist}},\ A_{\mathrm{oper}},\ A_{\mathrm{auth}} \right)$$

| Dimensjon | Kontroll |
| :--- | :--- |
| **Structural** | Type, form, integritet, struktur og kontrakt. |
| **Epistemic** | Evidens, usikkerhet, grunnlag og kunnskapsbegrensninger. |
| **Operational** | Systemgrenser, ressurser, sikkerhetsinvarianter og operative vilkår. |
| **Authorization** | Aktør, tillatelse, scope og overgangsrett. |

### 4.2 Admissibilitet er ikke autorisasjon

$$\boxed{A_{\mathrm{valid}} \not\Rightarrow A_{\mathrm{authorized}}}$$

---

## 5. Passage-grensen: `OPEN / HOLD / KILL`

$$\boxed{\Omega_G(c_t) \in \{\mathrm{OPEN}, \mathrm{HOLD}, \mathrm{KILL}\}}$$

> **OPEN releases. HOLD preserves. KILL protects.**  
> Prioritet: `KILL > HOLD > OPEN`. `HOLD` får aldri skjolde en allerede brutt hard grense.

- **`OPEN`:** Alle passasjekrav og gyldig autorisasjon er oppfylt. $\mathrm{OPEN} \not\Rightarrow \mathrm{REALIZED}$.
- **`HOLD`:** Overgangsautoritet gis ikke nå ($\neg \mathrm{TRANSITION\_AUTHORIZED}$). Bevarer skillet mellom kandidatens eksistens og rett til å passere.
- **`KILL`:** Fail-closed utfall ved kontraktbrudd eller terminal avvisning. $\mathrm{KILL} \not\Rightarrow \mathrm{UNDO}$. Skiller mellom kandidat-`REJECT` (i `HOLD`), strømsyklus-låst `KILL` og strømbrudd-varig fysisk `KILL` (Level 01 kobber).

---

## 6. Grenselikhet, toleranse og splitting

- **Eksakt likhet:** $a = b$ (med eksplisitt sammenligningssemantikk).
- **Toleransebasert kontroll:** $\delta(a, b) \le \varepsilon$ (eksplisitt, begrunnet, begrenset). $\mathrm{TOLERANCE} \neq \mathrm{EQUALITY}$.
- **Splitting:** $\boxed{\mathrm{FAIL\_EQUALITY} \not\Rightarrow \mathrm{SPLIT}}$. Splitting krever egen kontrakt:
  $$\mathrm{SPLIT}_{\mathrm{authorized}} \land \mathrm{SPLIT}_{\mathrm{admissible}} \land \mathrm{STRUCTURE}_{\mathrm{preserved}}$$
- **Tre utfall:** $\mathrm{MATCH} \lor \mathrm{WITHIN\_TOLERANCE} \lor \mathrm{UNRESOLVED}$.

---

## 7. Realiseringsfunksjonen

$$x_{t+1} = \Omega_R(x_t, a_t, u_t)$$

$$\mathrm{AUTHORIZED} \not\Rightarrow \mathrm{EXECUTED}, \qquad \mathrm{DISPATCHED} \not\Rightarrow \mathrm{DELIVERED}, \qquad \mathrm{COMMITTED} \not\Rightarrow \mathrm{PHYSICAL\_EFFECT}$$

---

## 8. Realiseringsstatus og usikker konsekvens

$$\mathcal{I} = \{\mathrm{INTENT\_RECORDED},\ \mathrm{DISPATCHED},\ \mathrm{CONSEQUENCE\_UNCERTAIN}\}$$

$$\mathrm{TIMEOUT} \rightarrow \mathrm{CONSEQUENCE\_UNCERTAIN} \rightarrow \mathrm{HOLD}$$

$$\boxed{\mathrm{UNKNOWN} \neq \mathrm{ZERO}}$$

Ukjent konsekvens er ikke null konsekvens og ikke bevis på at systemet er trygt.

---

## 9. Witness — evidens etter grensen

$$W = \mathrm{RECORD}(e_{\mathrm{observed}}, m, t, s)$$

$$W_{\mathrm{claim}} \neq W_{\mathrm{observation}}, \qquad W \not\Rightarrow \mathrm{TRUTH}$$

Witness er en passiv arkivkomponent uten genererings-, autorisasjons- eller endringsmyndighet.

---

## 10. Formelle invarianter (`I–XI`)

| Nr. | Invariant |
| :--- | :--- |
| **I** | $c \neq x_{t+1}$ (kandidat og konsekvens er separert) |
| **II** | $\Phi \not\Rightarrow \mathrm{AUTHORIZED}$ |
| **III** | $\mathrm{ADMISSIBLE} \not\Rightarrow \mathrm{AUTHORIZED}$ |
| **IV** | $\mathrm{OPEN} \not\Rightarrow \mathrm{REALIZED}$ |
| **V** | $\mathrm{HOLD} \not\Rightarrow \mathrm{TRANSITION}$ |
| **VI** | $\mathrm{KILL} \not\Rightarrow \mathrm{UNDO}$ |
| **VII** | $W \not\Rightarrow R$ |
| **VIII** | $\mathrm{CLAIM}_R \Rightarrow \mathrm{EVIDENCE}_R$ |
| **IX** | $\mathrm{UNKNOWN} \not\equiv \mathrm{ZERO}$ |
| **X** | $a \neq b \not\Rightarrow \mathrm{SPLIT}$ |
| **XI** | $\delta(a, b) \le \varepsilon \Rightarrow \mathrm{ADMISSIBLE}_{\varepsilon}$ (kun under eksplisitt kontrakt) |

---

## 11. Epistemisk grammatikk

$$\mathrm{INSPIRED\_BY} \not\Rightarrow \mathrm{IMPLEMENTS} \not\Rightarrow \mathrm{PROVES}$$

---

## 12–14. Kompakt formalisme og endelig aksiom

$$\mathcal{G}_R = (\Phi, \Pi_K, \Omega_G, \Omega_R, W, \mathcal{I})$$

$$\boxed{\mathrm{Represented} \neq \mathrm{Validated} \neq \mathrm{Authorized} \neq \mathrm{Realized} \neq \mathrm{Witnessed}}$$

---

## Referanseimplementasjon (`L2_GATE`)

Flyttallsfri C11-kjerne, passivt FIPS 180-4 SHA-256-vitne, QNX Neutrino 8.0 Resource Manager (`/dev/realization_gate`) og invariant-testbenk (`I–XI`) ligger under `L2_GATE/realization_grammar_qnx/`.
