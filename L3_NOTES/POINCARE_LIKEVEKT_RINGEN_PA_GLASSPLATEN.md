# Poincaré-likevekt
### *Ringen på glassplaten — og hvorfor levende HOLD aldri står stille*

> **Epistemisk grenselinje:** `INSPIRED_BY != IMPLEMENTS != PROVES` · Formell og konseptuell felthåndbok (`L3_NOTES`).  
> **Triadeloven:** `OPEN` slipper gjennom. `HOLD` bevarer. `KILL` beskytter. (`KILL > HOLD > OPEN`).

---

Når folk hører ordet *likevekt*, ser de for seg en stein som har sluttet å rulle. Noe dødt. Noe som har gitt opp farten.

På et **Poincaré-snitt** ($\Sigma$) ser du med én gang at virkeligheten er langt smartere enn det.

I stedet for å stirre deg blind på en hel kontinuerlig bane i rommet, stikker du en gjennomsiktig glassplate ($\Sigma$) tvers gjennom bevegelsen. Hver gang banen stikker gjennom glasset, setter du én prikk:

$$x_{n+1} = P(x_n)$$

Én prikk per syklus. Resten av støyen klipper du bort. Da dukker selve skjelettet i bevegelsen opp rett foran øynene dine.

---

## Fire tegninger på glasset

```text
  1. FIKSPUNKT           2. LEVENDE HOLD         3. DEMPET SPIRAL        4. HYPERBOLSK FLUKT
     P(x*) = x*             Elliptisk ring          rho(DP) < 1             rho(DP) > 1
                                                                                      /
    +-----------+          +-----------+           +-----------+           +---------/-+
    |           |          |   . - .   |           |    . .    |           |   .   /   |
    |     *     |          |  :  +  :  |           |   . * .   |           |  /  +     |
    |           |          |   ' - '   |           |    ' '    |           | /         |
    +-----------+          +-----------+           +-----------+           +/----------+
   Samme punkt            Uendelig mange prikker,   Friksjon og varme       Minste dytt
   hver runde.            aldri over kanten dK.     betaler for ro.         kaster deg ut -> KILL
```

---

## 1. De fire regimene på snittet $\Sigma$

Hva som skjer med systemet ditt — og hvilken dom porten må avsi — leses rett av prikkemønsteret og egenverdiene til returkartet $DP$:

* **Fikspunktet ($P(x^\star) = x^\star$):**  
  Banen står ikke stille i rommet — den går runde etter runde i full fart — men hver gang den krysser glassplaten, treffer den eksakt samme prikk $x^\star$. Ren, periodisk gjentakelse.

* **Elliptisk Poincaré-likevekt ($\lvert\lambda\rvert = 1$, for 2D arealbevarende returkart: $\det(DP) = 1$ og $\lvert\operatorname{Tr}(DP)\rvert < 2$):**  
  Her skjer det som får klassiske statikere til å klø seg i hodet. Banen lukker ikke. Prikkene treffer aldri samme sted to ganger. Likevel tegner de en sylskarp, lukket ring rundt $x^\star$ på glassplaten — uendelig mange nye punkter, men ikke én eneste prikk krysser noen gang den tillatte grensen $\partial K$.  
  * **Termodynamisk signatur (ideell Hamiltonsk bane):** $\Delta Q = 0$. Null varmetap.  
  * **Operativ dom:** Det matematiske portrettet på **levende `HOLD`**. Full bevegelse, full spenning, fullstendig bevart stabilitet.

* **Dempet likevekt ($\rho(DP) < 1$):**  
  Prikkene spiraler jevnt inn mot sentrum $x^\star$. Her står ikke bevegelsen gratis på tåspissene — friksjon og varme suger ut avviket runde for runde. Termodynamikken har betalt regningen for å låse punktet fast.

* **Hyperbolsk / ustabil ($\rho(DP) > 1$):**  
  En knivsegg uten nåde. Minste lille forstyrrelse forsterkes for hver runde og skyter prikkene rett ut over kanten av glassplaten:

$$\rho(DP) > 1 \implies \mathrm{KILL}$$

---

## 2. Levende `HOLD` er ikke myr

I portarkitekturen sier regelen at `HOLD` uten retning blir myr. Den elliptiske Poincaré-likevekten viser hva den friske motsetningen er:

**Du holder ikke balansen ved å stivne. Du holder balansen ved å la bevegelsen bli værende i ringen.**

Se på tre helt ulike systemer som deler den samme *geometrien* på snittet $\Sigma$:

* **Klatreren i `HOLD`:** Muskler som jobber kontinuerlig med mikrobevegelser i fingertupper og hofte. Ikke ett sekund i absolutt hvile — men tyngdepunktet slipper aldri ut over $\partial K$. *(Biologisk betaler muskelen naturligvis ATP/varme underveis, mens selve balansegeometrien er den samme ringen.)*
* **Asteroiden i Lagrange-punktene $L_4 / L_5$:** Den sitter ikke limt fast i verdensrommet. Den driver i en uopphørlig, kvasiperiodisk dans rundt likevektspunktet uten å bli slengt ut av systemet ($\Delta Q = 0$).
* **Den kvasiperiodiske banen på $\Sigma$:** Uendelig variasjon i fasen, null brudd på strukturen, $\Delta Q = 0$.

Alle tre viser det samme: **stabilitet krever ikke stillstand — den krever retur.**

---

## 3. Tre likevekter, tre helt ulike spørsmål

Når du legger Nash, KY og Poincaré ved siden av hverandre, forsvinner all begrepsforvirring med én gang:

| Likevekt | Hva som hviler | Hva den faktisk tester | Hva som bryter den |
| :--- | :--- | :--- | :--- |
| **Nash-likevekt** | Hvile i *valg* | Har noen spiller gevinst av å bryte ut? | Et lønnsomt avvik i regnearket. |
| **KY-likevekt** | Hvile i *adgang* | Finnes det noen forbedrende `OPEN` overgang? | En ny vei som både lønner seg og overlever porten. |
| **Poincaré-likevekt** | Hvile i *retur* | Holder banen seg inne på snittet $\Sigma$? | $\rho(DP) > 1$ — prikkene forlater glassplaten (`KILL`). |

---

Én setning å ta med seg fra verkstedet:

> **Nash spør om du har lyst til å gå. Poincaré spør om gulvet holder deg inne mens du danser.**
