# Spillet begynner ved porten

**En taktil felthåndbok i strategisk adgang og bevitnet spill (`KY-OS GAME Layer`)**

> **Epistemisk grenselinje:** `INSPIRED_BY != IMPLEMENTS != PROVES` · Formell spesifikasjon (`L0/L1`-referanse).  
> **Triadeloven:** *OPEN slipper gjennom. HOLD bevarer. KILL beskytter.* (`KILL > HOLD > OPEN`).

---

De fleste spillteoretikere oppfører seg som om virkeligheten er et rent regneark. Du regner ut hva som lønner seg, du flytter brikken, og så får du poengene dine. Ferdig snakka.

I den virkelige verden — og i KY-OS — fungerer det ikke sånn. Et trekk blir ikke til en hendelse bare fordi du har lyst til å gjøre det, eller fordi kalkulatoren din sier at det ser pent ut på papiret. Mellom ønske og virkelighet står det en tung, mekanisk port.

Før du har kjørt trekket gjennom stålet, er det bare en kandidat:

$$a'_{t+1} = \Phi(s_t, i_t)$$

Først når porten har testet om trekket tåler vekten av systemet, og stemplet det som gyldig, skjer det faktisk noe på brettet:

$$a_{t+1} = \Omega\bigl(\Pi_K(\Phi(s_t, i_t))\bigr)$$

Hele maskineriet bak et slikt spill kokes ned til sju deler:

$$\mathrm{GAME} = (N, X, \Phi, \Pi_K, \Omega, W, U)$$

| Del | Hva det er i praksis |
| :---: | :--- |
| $N$ | Spillerne rundt bordet. |
| $X$ | Tilstandsrommet — hvordan brettet ser ut akkurat nå. |
| $\Phi$ | Idémaskinen som spytter ut kandidattrekk. |
| $\Pi_K$ | Stresstesten. Tåler strukturen dette? |
| $\Omega$ | Dommeren med tre stempler: `OPEN`, `HOLD`, `KILL`. |
| $W$ | Vitneboken. Alt som slipper gjennom blir skrevet med uutslettelig blekk (`append-only`). |
| $U$ | Den faktiske gevinsten — etter at du har betalt for slitasje, irreversibilitet og rykte. |

---

## 1. Hvor `GAME` sitter i røret

KY-OS blander ikke sammen idé, sensur og handling. Alt reiser gjennom et stramt samlebånd:

$$\Phi \rightarrow \Pi_K \rightarrow P_\Sigma^K \rightarrow \mathrm{IDC} \rightarrow \mathrm{TERMO} \rightarrow \mathrm{GAME} \rightarrow \Omega \rightarrow W$$

`GAME`-laget sitter med én fot på hver side av porten, og har to helt adskilte jobber:

- **Før porten (null makt til å utføre):** Den foreslår strategiske kandidattrekk basert på tilstand, intensjon og hva som allerede står i vitneboken.
  $$\mathrm{GAME}_{\mathrm{pre}} : (s_t, i_t, W_t) \mapsto a'_{t+1}$$
- **Etter porten (ren bokføring):** Den oppdaterer selve spillet og hva som blir mulig i neste runde, basert utelukkende på overganger som faktisk ble bevitnet.
  $$G_{t+1} = F(G_t, W_{t+1})$$

Et spill er altså ikke bare reglene i esken pluss folkene som sitter der. Spillet er historien om de trekkene som faktisk overlevde porten:

$$H_T = \{ a_t \mid \Omega(\Pi_K(\Phi(s_t, i_t))) = \mathrm{OPEN} \}$$

Alt det andre? Truslene som aldri ble noe av, bløffene som falt i fisk, simuleringene i hodet ditt, de ulovlige snarveiene og de avbrutte forpliktelsene. De havner i restbøtta (*residual*). De er ikke ingenting — de lager støy og lukt i rommet — men de er ikke en hendelse.

---

## 2. Spøkelsesgevinsten (*Ghost Payoff*)

Du har sikkert sett dem før: de geniale trekkene som gir kjempegevinst i teorien, så lenge du later som om bordet tåler at du tenner på det.

En spøkelsesgevinst er en gevinst som lyser skarpt i kandidatrommet, men som ikke eksisterer i virkeligheten:

$$u'(a) > u(a) \quad \land \quad \Omega(\Pi_K(a')) = \mathrm{KILL}$$

Tallene ser deilige ut på papiret, men trekket er strategisk dødt. Hvis et trekk ødelegger selve spillbarheten, er det ikke et smart trekk — det er skrot.

For å unngå hallusinasjoner bruker KY-OS en integritetsjustert gevinstfunksjon. Den tvinger deg til å se hele regningen før du rekker ut hånden:

$$U_i(s) = u_i(s) - C_K(s) - S_{\mathrm{irr}}(s) - R_W(s)$$

- $u_i(s)$: Den lokale, umiddelbare gevinsten (det som glitrer).
- $C_K(s)$: Strukturkostnaden (hvor mye du bøyer og sliter på rammene).
- $S_{\mathrm{irr}}(s)$: Prisen for det som ikke kan gjøres om (brente broer koster).
- $R_W(s)$: Vitnekostnaden (hva dette koster deg i historikk og troverdighet).

En strategi som glemmer $C_K$, $S_{\mathrm{irr}}$ og $R_W$ modellerer ikke et spill. Den modellerer hukommelsestap.

---

## 3. KY-likevekt: Stillheten når ingen god vei står åpen

Klassisk spillteori spør: *«Har noen lyst til å avvike fra strategien sin?»*

KY-likevekt trekker på skuldrene av hva folk har lyst til, og spør noe langt hardere:

$$\text{KY-likevekt} \iff \text{ingen forbedrende } \mathrm{OPEN}\text{-overgang eksisterer.}$$

Det betyr ikke at ingen drømmer om et bedre trekk. Det betyr ikke at det ikke finnes en lur snarvei på baksiden av servietten. Det betyr at det ikke finnes et eneste forbedrende trekk som både kommer seg gjennom porten og lar spillet overleve.

---

## 4. Spilleren som portbærer

I klassiske modeller er en spiller ofte bare en sulten munn med en nyttefunksjon. Her er spilleren en komplett, portbærende agent:

$$P_i = (A_i, K_i, \Omega_i, W_i)$$

- $A_i$: Handlingsrommet (hva du i det hele tatt kan prøve på).
- $K_i$: Din strukturelle kjerne (kapasitet, ressurser, grenser).
- $\Omega_i$: Din interne port (evnen til å si nei til deg selv).
- $W_i$: Din vitnehistorikk (sporet du legger igjen).

Her ligger en underfundig sannhet: En agent uten vitnehistorikk er ikke friere — den er mindre ekte. Uten et spor bak seg kan den true, men den kan ikke binde seg. Den kan bløffe, men den kan aldri bygge opp vekt.

$$\mathrm{Credibility}_i \sim H(W_i, \Omega_i)$$

Slik ser et minimalistisk spillerpass (agentkontrakt) ut i maskinrommet:

```json
{
  "player_id": "agent_001",
  "action_space": ["propose", "hold", "commit", "withdraw"],
  "kernel": {
    "capacity": {},
    "constraints": {},
    "resources": {},
    "credibility": {}
  },
  "internal_gate": {
    "open_conditions": [],
    "hold_conditions": [],
    "kill_conditions": []
  },
  "witness_history": {
    "ledger_ref": "sha256:..."
  },
  "payoff_model": {
    "local_gain": "u_i",
    "structure_cost": "C_K",
    "irreversibility_cost": "S_irr",
    "witness_cost": "R_W"
  }
}
```

---

## 5. Bløff som adgangsangrep

Hva er egentlig en bløff når du skreller av pokerfjeset?

$$\text{Bløff er midlertidig kontroll over motstanderens adgangstest.}$$

Formelt skjer bløffen idet spiller $i$ legger frem et trekk $a'_i$ som $i$ selv ikke klarer å bære, mens spiller $j$ tror at $i$ har dekning for det:

$$\mathrm{Bluff}_{i \to j} = a'_i : \Omega_i(\Pi_{K_i}(a'_i)) \neq \mathrm{OPEN} \;\land\; \Omega_j(\Pi_{K_j}(a'_i)) = \mathrm{OPEN}$$

Du later som porten din er åpen. Motstanderen måler deg og tror porten din er åpen. Motgiften er ikke bedre psykologi, men vitneboken:

$$W_i \not\models \Omega_i^{\mathrm{claimed}} \implies \text{troverdigheten forvitrer}$$

Hvis historikken din ikke støtter porten du påstår at du har, mister ordene dine tyngde. Du kan rope høyere, men ingen flytter brikkene sine av den grunn.

---

## 6. Porten ($\Omega_G$) og kunsten å skille «lov» fra «lurt»

En klassisk feil i regelmotorer er å blande sammen hva som er lov og hva som er smart. Et trekk som er trygt, men svakt (*Safe But Weak*), skal ikke stoppes av porten og stemples `HOLD`. Det skal få stempelet `GAME_OPEN` — og så får spilleren selv være klok nok til å la være å velge det.

Derfor holder KY-OS portdommen $\Omega_G \in \{\mathrm{GAME\_OPEN}, \mathrm{GAME\_HOLD}, \mathrm{GAME\_KILL}\}$ klinisk adskilt fra nytteoptimalisering, under jernloven `KILL > HOLD > OPEN`:

$$\Omega_G(a') = \begin{cases} \mathrm{GAME\_KILL}, & a' \notin A_i \;\lor\; (\circ \to \bullet\text{-snarvei}) \;\lor\; \Omega(\Pi_K(a')) = \mathrm{KILL} \;\lor\; \text{spillmediets kollaps} \\ \mathrm{GAME\_HOLD}, & \text{strategisk usikkerhet, uavklart kostnad, eller ustabil troverdighet} \\ \mathrm{GAME\_OPEN}, & a' \in A_i \;\land\; \Delta K_G < \tau_G \;\land\; W_i \text{ støtter forpliktelsen} \end{cases}$$

Først etter at porten har gjort jobben sin, slipper den rasjonelle kalkulatoren til. Spilleren velger $a'$ bare når det ligger inne i det godkjente settet og faktisk lønner seg:

$$\Omega_G(a') = \mathrm{GAME\_OPEN} \;\land\; U_i(a') > U_i(s_t)$$

> **Grunnregelen:** Ingen strategisk gevinst kan hentes ved å ødelegge mediet man spiller i.

---

## 7. Spillet begynner før spilleren

Et spill begynner ikke når folk setter seg ved bordet. Det begynner ved snittet der en mulig handling spør om den får lov til å bli til en konsekvens.

- Før strategi finnes det passasje.
- Før gevinst finnes det adgang.
- Før seier finnes det et medium som gjør seieren meningsfull.

En moden spiller trenger ikke hundre triks. Den trenger å mestre tre rene bevegelser:

- **OPEN uten lekkasje.** *(Åpning uten struktur blir naivitet.)*
- **HOLD uten råte.** *(Utsettelse uten retning blir myr.)*
- **KILL uten å forgifte banen.** *(Stans uten presisjon blir tyranni.)*

---

## 8. Maskinrommet: Slik henger lagene sammen

| Lag | Jobben i samlebåndet |
| :--- | :--- |
| **RFM** | Tester hva som faktisk kan vende tilbake. |
| **IDC** | Navngir grensene som ikke kan krysses tilbake. |
| **TERMO** | Setter prislapp på selve kryssingen. |
| **GAME** | Tester om strategisk handling bevarer mediet man spiller i. |
| **E-TOR** | Slipper gjennom eller blokkerer (`KILL > HOLD > OPEN`). |
| **Witness** | Forsegler det som slapp forbi (`append-only` hash-kjede, adskilt fra fysisk WORM). |

> **Et trekk er ikke virkelig fordi du valgte det. Det er virkelig først når det har overlevd porten og skrevet seg inn i historien.**
