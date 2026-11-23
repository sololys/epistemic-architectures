# KY-OS GAME Layer — Strategic Admissibility and Witnessed Play

> **Epistemic Boundary:** `INSPIRED_BY != IMPLEMENTS != PROVES` · Formal specification & architectural note (`L0/L1` reference).  
> **Triad Law:** *OPEN releases. HOLD preserves. KILL protects.* (`KILL > HOLD > OPEN`).

$$\boxed{\mathrm{GAME} = (N, X, \Phi, \Pi_K, \Omega, W, U)}$$

Where $N$ is the set of players, $X$ is the state space, $\Phi$ generates candidate moves, $\Pi_K$ tests admissibility, $\Omega$ decides `OPEN / HOLD / KILL`, $W$ writes the append-only witness history, and $U$ measures payoff after structure cost, irreversibility, and historical witness load.

A move is not an event merely because a player desires it.

$$\boxed{a'_{t+1} = \Phi(s_t, i_t)}$$

That is only the candidate move. The realized move is:

$$\boxed{a_{t+1} = \Omega\bigl(\Pi_K(\Phi(s_t, i_t))\bigr)}$$

---

## 1. Game Layer in KY-OS

KY-OS separates the passage into explicit layers:

$$\boxed{\Phi \rightarrow \Pi_K \rightarrow P_\Sigma^K \rightarrow \mathrm{IDC} \rightarrow \mathrm{TERMO} \rightarrow \mathrm{GAME} \rightarrow \Omega \rightarrow W}$$

The `GAME` layer straddles the gate cleanly in two distinct roles:

- **Before the gate** — generates strategic candidate moves (zero execution authority):
  $$\boxed{\mathrm{GAME}_{\mathrm{pre}} : (s_t, i_t, W_t) \mapsto a'_{t+1}}$$
- **After the gate** — updates game history and future admissibility from witnessed transitions:
  $$\boxed{G_{t+1} = F(G_t, W_{t+1})}$$

A game is therefore not just its rules plus its players. The game is the history of authorized transitions actually written:

$$\boxed{H_T = \{ a_t \mid \Omega(\Pi_K(\Phi(s_t, i_t))) = \mathrm{OPEN} \}}$$

Everything else remains residual: threats, bluffs, simulations, illegal shortcuts, aborted commits. Not nothing — but not an event.

---

## 2. Ghost Payoff

A **ghost payoff** is a gain visible in the candidate space that does not exist in the realizable sector:

$$\boxed{u'(a) > u(a) \quad \land \quad \Omega(\Pi_K(a')) = \mathrm{KILL}}$$

The gain is mathematically visible on paper, but strategically dead. If an action destroys the admissibility of the game, it is not a valid move — it is a residual.

The integrity-adjusted payoff function is:

$$\boxed{U_i(s) = u_i(s) - C_K(s) - S_{\mathrm{irr}}(s) - R_W(s)}$$

where $u_i$ is local gain, $C_K$ is structural constraint cost, $S_{\mathrm{irr}}$ is irreversibility cost, and $R_W$ is historical/reputational witness cost. A strategy that ignores these costs does not model a game; it models amnesia.

---

## 3. KY Equilibrium

Classical equilibrium asks whether any player has an incentive to deviate. KY-equilibrium is stricter:

$$\boxed{\text{KY-equilibrium} \iff \text{no improving } \mathrm{OPEN}\text{-transition exists.}}$$

Not no desired move, not no conceivable shortcut — no improving transition exists that can both pass the gate and preserve the structure of play.

---

## 4. Player as Gate-Bearing Agent

A player is defined as more than a utility function:

$$\boxed{P_i = (A_i, K_i, \Omega_i, W_i)}$$

where $A_i$ is the action space, $K_i$ is the player's structural kernel, $\Omega_i$ is the player's internal gate, and $W_i$ is the player's witness history. An agent without witness is not freer — it is less real: it can threaten, but cannot bind; it can bluff, but cannot accumulate credibility.

$$\boxed{\mathrm{Credibility}_i \sim H(W_i, \Omega_i)}$$

Minimal agent contract schema:

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

## 5. Bluff as Admissibility Attack

$$\boxed{\text{Bluff is temporary control over the opponent's admissibility test.}}$$

Formally:

$$\boxed{\mathrm{Bluff}_{i \to j} = a'_i : \Omega_i(\Pi_{K_i}(a'_i)) \neq \mathrm{OPEN} \;\land\; \Omega_j(\Pi_{K_j}(a'_i)) = \mathrm{OPEN}}$$

Player $i$ cannot actually bear the move, while player $j$ classifies it as bearable. Witness is the antidote:

$$\boxed{W_i \not\models \Omega_i^{\mathrm{claimed}} \implies \text{credibility degradation}}$$

---

## 6. GAME Gate ($\Omega_G$) and Separation of Admissibility from Selection

To keep admissibility strictly separate from utility optimization (preserving *Safe But Weak* moves as admissible `OPEN` moves that a player may rationally decline, rather than misclassifying them as `HOLD`), the gate verdict $\Omega_G \in \{\mathrm{GAME\_OPEN}, \mathrm{GAME\_HOLD}, \mathrm{GAME\_KILL}\}$ governs passage under `KILL > HOLD > OPEN`:

$$\Omega_G(a') = \begin{cases} \mathrm{GAME\_KILL}, & a' \notin A_i \;\lor\; (\circ \to \bullet\text{ shortcut}) \;\lor\; \Omega(\Pi_K(a')) = \mathrm{KILL} \;\lor\; \text{game-medium collapse} \\ \mathrm{GAME\_HOLD}, & \text{strategic uncertainty, unresolved cost, or unstable credibility} \\ \mathrm{GAME\_OPEN}, & a' \in A_i \;\land\; \Delta K_G < \tau_G \;\land\; W_i \text{ supports commitment} \end{cases}$$

A player's **rational selection** then acts strictly *inside* the admitted set: choosing $a'$ only when $\Omega_G(a') = \mathrm{GAME\_OPEN} \land U_i(a') > U_i(s_t)$.

$$\boxed{\text{No strategic gain from destroying the medium of play.}}$$

---

## 7. The Game Begins Before the Player

A game does not begin with players. It begins at the cut where a possible action asks whether it may become consequence.

- Before strategy, there is passage.
- Before payoff, there is admissibility.
- Before victory, there is the medium that makes victory meaningful.

The mature player masters three movements:

- **OPEN** without leaking. *(OPEN without structure becomes naivety.)*
- **HOLD** without rotting. *(HOLD without direction becomes swamp.)*
- **KILL** without poisoning the field. *(KILL without precision becomes tyranny.)*

---

## 8. Layer Integration Summary

| Layer | Function |
| :--- | :--- |
| **RFM** | Tests what can return. |
| **IDC** | Names what cannot be uncrossed. |
| **TERMO** | Prices the crossing. |
| **GAME** | Tests whether strategic action preserves the medium of play. |
| **E-TOR** | Authorizes or blocks (`KILL > HOLD > OPEN`). |
| **Witness** | Seals what passed (append-only hash chain, distinct from physical WORM). |

> **A move is not real because it is chosen. It is real only when it has survived the gate and entered history.**
