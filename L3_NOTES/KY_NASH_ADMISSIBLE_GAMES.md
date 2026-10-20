# KY–Nash Spillteori: Håndbok for Admissible Overganger
## Admissible Equilibrium: A KY–Nash Theory of Strategic Consequence

> **Abstract:** Classical game theory studies strategic choice within an unconstrained possibility tree, naively identifying choice with actuation. In human, institutional, and fail-closed cyber-physical systems, however, a game is not the set of all conceivable actions, but **the history of authorized transitions**. Between intention and realization stands a consequence gate ($\Omega$). We formalize the **KY–Nash Theory of Admissible Games**, wherein candidate moves ($a' \in \Phi$) must pass structural admissibility tests ($\Pi_K$) and gate authorization ($\Omega \in \{\mathrm{OPEN}, \mathrm{HOLD}, \mathrm{KILL}\}$) before entering realized history ($a_{t+1}$). We introduce the **Integrity-Adjusted Payoff** ($U_i = u_i - C_K - S_{\mathrm{irr}} - R_W$) accounting for structural friction, thermodynamic irreversibility, and public witness cost. We prove that a KY–Nash equilibrium is defined by the absence of improving $\mathrm{OPEN}$-vectors on the two-dimensional strategic surface ($\text{Payoff} \times \text{Admissibility}$), eliminating the illusion of *Ghost Wins*.
> 
> $$\boxed{\mathbf{Nash\;stabiliserer\;handling;\;KY\;stabiliserer\;feltet\;der\;handling\;fortsatt\;betyr\;noe.}}$$
> $$\boxed{\mathbf{Nash\;stabilises\;action;\;KY\;stabilises\;the\;field\;in\;which\;action\;remains\;meaningful.}}$$

---

## 1. Ontologisk Fundament: Spillet som Filter

Klassisk spillteori antar for lettvint at en handling er identisk med et realisert trekk. Den tegner opp trestrukturer og payoff-matriser der enhver gren og enhver rute representerer en farbar vei, forutsatt at aktøren har ressursene og viljen til å velge den.

Dette er en dyp antropologisk og strukturell misforståelse.

I menneskelige, institusjonelle og fysiske systemer er et spill **ikke** mengden av alle tenkelige eller kalkulerbare handlinger. 

$$\boxed{\mathbf{Et\;spill\;er\;ikke\;mengden\;av\;mulige\;handlinger,\;men\;historien\;av\;autoriserte\;overganger.}}$$

Mellom aktørens intensjon og handlingens realisering ligger det alltid en **port** ($\Omega$) – et sosialt, juridisk, rituelt eller fysisk filter. Før en handling har passert dette filteret, har den ingen spillteoretisk realitet; den er utelukkende en *strategisk kandidat*.

**KY–Nash-rammeverket skifter fokus fra valgfrie muligheter til strukturell admisjon.** Vi studerer ikke bare hva aktørene ønsker å gjøre, men hvordan systemets porter sorterer handlinger inn i kategoriene:
1. **Realisering** ($\mathrm{OPEN}$),
2. **Utsettelse / Suspensjon** ($\mathrm{HOLD}$), eller
3. **Sletting / Terminering** ($\mathrm{KILL}$).

---

## 2. Den Formelle Realiseringsgrammatikken

For å analysere overganger opererer vi med en firedelt formell kjede for ethvert forsøk på et trekk:

```
[ KANDIDAT Φ ] ──▶ [ STRUKTURTEST Π_K ] ──▶ [ PORTFUNKSJON Ω ] ──▶ [ REALISERT TREKK a_{t+1} ]
  (Vilje / Beregning)     (Stil / Grammatikk)       (OPEN / HOLD / KILL)      (Strategisk Historie)
```

### 1. Kandidatgenerering
En aktør $i$ i en gitt systemtilstand $s_t$ genererer en handlingskandidat $a'_{t+1}$:

$$a'_{t+1} = \Phi(s_t, i_t)$$

Her representerer $i_t$ aktørens kapasitet, vilje, latente preferanser og lokale strategiske beregning. Dette er foreløpig ikke et trekk, men ren kognitiv eller algoritmisk intensjon.

### 2. Strukturtest
Kandidaten måles umiddelbart mot spillets bærestruktur $K$. Denne testen produserer et prøvetrekk $\tilde{a}_{t+1}$:

$$\tilde{a}_{t+1} = \Pi_K(a'_{t+1})$$

Strukturtesten $\Pi_K$ sjekker om handlingen i det hele tatt er gjenkjennelig, regelkompatibel og syntaktisk gyldig innenfor spillets grammatikk (isometri, typekontroll, invariant bevaring).

### 3. Portfunksjonen
Prøvetrekkets skjebne avgjøres av den feil-lukkede portfunksjonen $\Omega$:

$$\Omega(\tilde{a}_{t+1}) \in \{\mathbf{OPEN}, \mathbf{HOLD}, \mathbf{KILL}\}$$

* **$\mathbf{OPEN}$:** Handlingen autoriseres. Den trer inn i spillets historie, endrer systemtilstanden irreversibelt, og genererer en gyldig overgang.
* **$\mathbf{HOLD}$:** Handlingen suspenderes. Den nektes umiddelbar realisering, men slettes ikke. Den eksisterer som en latent spenning som krever kontinuerlig ressursbruk og overvåking å opprettholde.
* **$\mathbf{KILL}$:** Handlingen avvises kontant og termineres. Den etterlater seg ingen spor i spillets gyldige tilstandsrom, utover ressursene aktøren sløste bort på å generere den.

### 4. Realisert Trekk
Bare handlinger der porten erklærer $\mathrm{OPEN}$ blir en del av spillets offisielle historie:

$$\boxed{a_{t+1} = \begin{cases} 
\tilde{a}_{t+1}, & \Omega(\tilde{a}_{t+1}) = \mathbf{OPEN} \\ 
s_t, & \Omega(\tilde{a}_{t+1}) = \mathbf{HOLD} \\ 
\bot, & \Omega(\tilde{a}_{t+1}) = \mathbf{KILL} 
\end{cases}}$$

$$\boxed{\mathbf{Bare\;OPEN\;kan\;v\mathring{a}re\;strategi.}}$$

---

## 3. Integritetsjustert Payoff ($U_i$)

I klassisk spillteori måles gevinst ($u_i$) ofte som en umiddelbar, lokal akkumulering av poeng, profitt eller territorium. I KY–Nash-analysen må payoffen alltid justeres for de systemiske friksjons- og ødeleggelseskostnadene ved å tvinge en overgang gjennom porten.

Den **integritetsjusterte payoffen** $U_i(s)$ defineres som:

$$\boxed{U_i(s) = u_i(s) - C_K(s) - S_{\mathrm{irr}}(s) - R_W(s)}$$

Hvor:
* **$u_i(s)$ (Lokal gevinst):** Den rå, umiddelbare gevinsten aktøren oppnår dersom trekket lykkes isolert sett.
* **$C_K(s)$ (Strukturkostnad):** Kostnaden ved å opprettholde, bøye eller utfordre spillets spilleregler og arkitektoniske rammer for å få trekket gjennom porten.
* **$S_{\mathrm{irr}}(s)$ (Irreversibilitetskostnad):** Tapet av fremtidig strategisk fleksibilitet. Trekk som brenner broer, stenger dører permanent eller låser systemet i stive tilstander, bærer en høy $S_{\mathrm{irr}}$.
* **$R_W(s)$ (Witness- og historiekostnad):** Kostnaden ved å bli observert, husket og stilt til ansvar av omverdenen (vitnene og audit-loggen $W$). Dette inkluderer tap av omdømme, tillit, ære, juridisk etterspill og fremtidig adgang til andre spill.

> **Teorem om Systemisk Kollaps:**  
> En strategi som maksimerer lokal gevinst $u_i$ på bekostning av en ukontrollert vekst i $C_K + S_{\mathrm{irr}} + R_W$ produserer en **Ghost Win** som uunngåelig fører til systemisk kollaps for aktøren.

---

## 4. De Fire Strategiske Sonene: KY–Nash-Flaten

Vi projiserer spillets tilstandsrom på et todimensjonalt strategisk koordinatsystem:

$$\boxed{\mathbf{KY\text{–}Nash\text{-}flaten} = \mathbf{Payoff} \times \mathbf{Admissibility}}$$

* **Vertikal akse (Payoff):** Hvor mye aktøren kan vinne lokalt dersom trekket får virke ($u_i$).
* **Horisontal akse (Admissibility):** Hvor godt trekket bevarer spillets struktur, grenser, bæreflate og tillit ($A(a')$).

```
                         HØY PAYOFF (u_i)
                                ↑
                                |
             GHOST WIN          |        TRUE STRATEGY
       Høy lokal gevinst        |      Høy lokal gevinst
       Lav integritet           |      Høy integritet
       KILL / Integritetskollaps|      OPEN-kandidat (Bærekraftig)
                                |
                 \              |              /
                  \             |             /
                   \            |            /
  ------------------\-----------+-----------/------------------→ HØY ADMISSIBILITY (A)
                     \          |          /
                      \   HOLD-BELTE      /
                       \ (Nær terskel)   /
                                |
             DEAD NOISE         |        SAFE BUT WEAK
       Lav lokal gevinst        |      Lav lokal gevinst
       Lav integritet           |      Høy integritet
       KILL / Avvisning         |      HOLD / Konservativ stasis
                                |
                         LAV PAYOFF (u_i)
```

### Sonenes Karakteristikk:

1. **TRUE STRATEGY (Høy Payoff, Høy Admissibility):**  
   Den gylne banen. Trekket gir reell gevinst samtidig som det styrker eller bevarer spillets fremtidige spillbarhet. Det glir gjennom porten med minimal motstand ($\Omega = \mathrm{OPEN}$). Dette er Nash-forbedringer som respekterer KY-rammen.
2. **GHOST WIN (Høy Payoff, Lav Admissibility):**  
   En tilsynelatende overlegen seier i det snevre, lokale regnskapet, men som krever et trekk som forurenser eller ødelegger spillets medium. Vinneren står igjen på et askeberg av ødelagt tillit og stengte porter. Porten responderer med $\mathrm{KILL}$ eller residualstraff.
3. **SAFE BUT WEAK (Lav Payoff, Høy Admissibility):**  
   Posisjonen til aktører som aldri utfordrer portene. De overlever og er respekterte, men akkumulerer aldri nok strategisk moment til å endre spillets retning. Typisk fanget i evig $\mathrm{HOLD}$ eller lav-intensitets vedlikehold.
4. **DEAD NOISE (Lav Payoff, Lav Admissibility):**  
   Handlinger født av desperasjon, sinne eller ren kognitiv feilberegning. Koster mye energi å generere, men blir kontant tilintetgjort i porten ($\Omega = \mathrm{KILL}$). Etterlater aktøren utmattet og sårbar.
5. **HOLD-beltet:**  
   Sonen rundt terskelverdien $\tau_A$ hvor et trekk er lovende, men ennå ikke modent for autorisasjon. Det krever tålmodighet, testing og ressursmarginer.

---

## 5. Formell Definisjon av KY–Nash-Likevekt

I klassisk spillteori er en Nash-likevekt definert ved at ingen spiller kan oppnå høyere nytte ved ensidig avvik. Men klassisk teori spør aldri om avviket faktisk er *admissibelt* eller *fysisk/juridisk realiserbart*.

I KY–Nash-teorien kan et avvik kun telle dersom det kan autoriseres av konsekvensporten:

$$\boxed{s^* \in E_{K\text{-Nash}} \iff \forall i, \; \nexists a_i' : \left[ \Omega\Big(\Pi_K\big(\Phi(s^*, a_i')\big)\Big) = \mathbf{OPEN} \quad \land \quad U_i(s_{-i}^*, a_i') > U_i(s^*) \right]}$$

### På menneskespråk:
> **Spillet er i KY–Nash-likevekt når ingen aktør kan forbedre sin posisjon gjennom en overgang som BÅDE kan passere porten som OPEN OG bevare spillets integritet under integritetsjustert payoff.**

$$\boxed{\mathbf{KY\text{–}Nash\text{-}likevekt\;er\;frav\mathring{a}r\;av\;forbedrende\;OPEN\text{-}vektorer\;p\mathring{a}\;spillflaten.}}$$

$$\boxed{\mathbf{KY\text{–}Nash\;equilibrium\;is\;the\;absence\;of\;improving\;OPEN\text{-}vectors\;on\;the\;strategic\;surface.}}$$

Et spill er ikke i ro fordi ingen kan drømme om mer. Det er i ro når ingen forbedrende overgang kan passere porten uten å ødelegge flaten spillet står på.

---

## 6. Begrepsapparat

* **Ghost Payoff:** En kalkulert gevinst i kandidatrommet $\Phi$ som ser blendende ut på papiret, men som aldri kan realiseres fordi portfunksjonen dikterer $\mathrm{KILL}$.
* **Ghost Win:** En seier oppnådd gjennom trekk som utløser et umiddelbart *integrity collapse*. Man vinner runden lokalt, men terminerer selve spillets fremtidige gyldighet.
* **HOLD-strategi:** Strategisk suspensjon. Å holde en kandidat aktiv i porten uten å trekke den tilbake eller kreve umiddelbar avgjørelse. Dette binder opp motpartens analyse- og reaksjonsressurser, men tærer også på egne marginer.
* **KILL:** Portens aktive, objektive forsvar av spillets overlevelse. Det er ikke et uttrykk for emosjonell motstand, men en strukturell nødvendighet for å hindre at spillet forfaller til støy eller kaos.
* **Admissibility Dominance:** En tilstand der et trekk dominerer andre kandidater, ikke fordi den lokale gevinsten $u_i$ er størst, men fordi det påfører minimale struktur- og vitnekostnader ($C_K + S_{\mathrm{irr}} + R_W \approx 0$). Det vinner fordi det er bærbart.
* **Integrity Collapse:** Den systemiske tilstanden som oppstår når en aktør tvinger et uadmissibelt trekk gjennom porten ved hjelp av rå makt, slik at spillets fremtidige regler mister autoritet og tillit opphører.
* **Closed-Game Asymmetry:** En situasjon der aktørene har fundamentalt ulik tilgang til porten. Den dominerende parten får sine mest aggressive handlinger autorisert som $\mathrm{OPEN}$ (lest som nødvendig strategi), mens den svakere partens defensive trekk konsekvent klassifiseres som $\mathrm{KILL}$ eller $\mathrm{HOLD}$ (lest som illojalitet, trusler eller støy).

---

## 7. Den Antropologiske Regelen

Vi må aldri analysere et spill som om handlingene svever i et friksjonsfritt vakuum av abstrakte tall. Reelle overganger skjer gjennom levde kropper, fysiske ressurser og sosiale rom.

Før du tegner et spilltre, må du stille fire ufravikelige spørsmål:
1. **Hvordan blir handlingen gjenkjent?** (Finnes det et språk og en type-definisjon for den?)
2. **Hvem har autoritet til å fortolke den?** (Hvem eier og vokter porten $\Omega$?)
3. **Hvem vitner handlingen?** (Hvem fører audit-loggen, og hvem bærer historiekostnaden $R_W$?)
4. **Hvem får svare, og hvem blir stående målløs tilbake?** (Hvem har handlefrihet under porten?)

$$\boxed{\mathbf{Frihet\;i\;et\;spill\;handler\;ikke\;om\;hvor\;mange\;ting\;du\;kan\;tenke\;deg\;opp.\;Frihet\;er\;differensiert\;adgang\;til\;OPEN.}}$$

---

## 8. Kasusstudie: Varslerens Dilemma i det Lukkede System

For å demonstrere kraften i KY–Nash-rammeverket analyserer vi et klassisk asymmetrisk spill: En ansatt (Varsleren, $V$) oppdager omfattende økonomisk svindel begått av ledelsen i et mektig konsern (Ledelsen, $L$).

### 1. Aktørene
* **Varsleren ($V$):** Ønsker å stanse svindelen og beskytte sin profesjonelle og moralske integritet.
* **Ledelsen ($L$):** Ønsker å opprettholde svindelen (høy lokal gevinst $u_L$) og beskytte selskapets fasade.

### 2. Kandidatrommet ($\Phi$)
* $V$s kandidater ($a_V \in \Phi_V$):
  - $a_{V,1}$: Tie stille og være lojal.
  - $a_{V,2}$: Gå til intern kontroll/revisjon (intern varsling).
  - $a_{V,3}$: Gå til media eller Økokrim (ekstern lekkasje).
* $L$s kandidater ($a_L \in \Phi_L$):
  - $a_{L,1}$: Korrigere svindelen i stillhet og takke varsleren.
  - $a_{L,2}$: Isolere og diskreditere $V$.
  - $a_{L,3}$: Saksøke og politianmelde $V$ for brudd på taushetsplikten.

### 3. De To Konkurrerende Portene
I dette asymmetriske spillet eksisterer det to rivaliserende porter:
* **Den interne porten ($\Omega_{\mathrm{int}}$):** Fullstendig kontrollert og eid av Ledelsen ($L$).
* **Den eksterne porten ($\Omega_{\mathrm{ext}}$):** Kontrollert av uavhengig rettsvesen, presse og offentlighet.

### 4. Vurdering av OPEN, HOLD og KILL
* **Dersom $V$ varsler internt ($a_{V,2}$):**  
  Ledelsen bruker sin kontroll over $\Omega_{\mathrm{int}}$ til å sette saken på **$\mathbf{HOLD}$**. Dette er en kalkulert strategisk suspensjon. Ved å holde saken "under intern granskning", nøytraliserer de trusselen uten å avvise den åpenlyst. $V$ utmattes over tid, mens $L$ sletter bevis og forbereder motangrep.
* **Dersom $V$ varsler eksternt ($a_{V,3}$):**  
  Dette er et forsøk på å omgå $\Omega_{\mathrm{int}}$ til fordel for $\Omega_{\mathrm{ext}}$. Ledelsen vil umiddelbart aktivere advokater og PR-byråer for å erklære overgangen for **$\mathbf{KILL}$** internt (avskjedigelse), og forsøke å stemple varselet overfor $\Omega_{\mathrm{ext}}$ som "ondsinnet støy fra en ustabil ansatt".

### 5. Integritetsjustert Payoff-Beregning
Dersom $V$ lekker eksternt og $L$ knuser $V$ juridisk og PR-messig:

* **For Ledelsen ($L$):**
  - Lokal gevinst $u_L$: Meget høy (svindelen holdes skjult en stund til, $V$ er fjernet).
  - Strukturkostnad $C_K$: Høy (massive utgifter til advokater, kriserådgivere og hemmelighold).
  - Irreversibilitetskostnad $S_{\mathrm{irr}}$: Høy (organisasjonen blir paranoid, rigid og fryktstyrt).
  - Witness-kostnad $R_W$: **Katastrofal.** Offentligheten og markedet ser hva de gjorde. Tilliten til merkevaren forvitrer, rekrutteringen kollapser, og tilsynsmyndigheter åpner etterforskning.
  - **Konklusjon:** Ledelsens "seier" er en arketypisk **Ghost Win**. Lokalt ser regnskapet grønt ut, men de har påført seg selv et dødelig *integrity collapse*.

* **For Varsleren ($V$):**
  - Lokal gevinst $u_V$: Nær null eller negativ (mister jobben, inntekten stopper).
  - Strukturkostnad $C_K$: Ekstrem (personlig belastning, isolasjon, rettssaker).
  - Irreversibilitetskostnad $S_{\mathrm{irr}}$: Høy (brent karriere i etablert bransje).
  - Witness-kostnad $R_W$: Positiv eller lav (offentlig heder, moralsk oppreisning, men med personlig arrdannelse).

### 6. Klassisk Nash vs. KY–Nash
* **Klassisk Nash:** Spillet stabiliserer seg i at varsleren tier stille ($a_{V,1}$) fordi trusselen om personlig ruin overgår enhver lokal gevinst. Klassisk Nash legitimerer undertrykkelse basert på rå maktfordeling.
* **KY–Nash:** Å tie stille under en pågående svindel øker systemets totale historiekostnad $R_W$ eksponensielt over tid inntil hele konsernet krasjer utenfra. 
  En reell KY–Nash-likevekt oppstår først når det etableres en **uavhengig, feil-lukket tredjepartsport ($\Omega_{\mathrm{ext}}$)** hvor overganger kan skje uten at varsleren må lide personlig utslettelse, og uten at ledelsen kan manipulere porten til vilkårlig $\mathrm{KILL}$.

---

## 9. Syntese: Spillets Voktere

| Spørsmål | Det Lukkede Spillet (Maktmonopol) | Det Admissible Spillet (KY–Nash) |
| :--- | :--- | :--- |
| **Hva det beskytter:** | Beskytter elitens monopol på tolkning og makt. | Beskytter spillets langsiktige overlevelse og spillbarhet. |
| **Hva det åpner:** | Kortsiktig, rovdrift-basert profitt for portvokterne. | Bærekraftige, verdiskapende $\mathrm{OPEN}$-vektorer med lav vitnekostnad. |
| **Hva det holder:** | Holder svakere parter i lammende suspensjon ($\mathrm{HOLD}$). | Bruker $\mathrm{HOLD}$ som et kortsiktig test- og avklaringskammer. |
| **Hva det nekter:** | Nekter uavhengige vitner og transparens. | Nekter falske seire (*Ghost Wins*) og uadmissible trekk. |

```
Klassisk teori:    Handling = Trekk (så lenge aktøren har makt).
KY–Nash-teori:     Bare OPEN-overganger kan være strategi.
                   Virkeligheten skapes av det porten slipper igjennom.
```

$$\boxed{\mathbf{Et\;spill\;er\;ikke\;i\;ro\;fordi\;ingen\;kan\;dr\mathring{o}mme\;om\;mer.\;Det\;er\;i\;ro\;n\mathring{a}r\;ingen\;forbedrende\;overgang\;kan\;passere\;porten\;uten\;\mathring{a}\;skade\;flaten\;den\;st\mathring{a}r\;p\mathring{a}.}}$$
