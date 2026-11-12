# Nash’s Duality, Viability Filtering, and KY–Nash Admissibility

**Author:** Marius Egerhei Torjusen¹  
*Independent Systems Builder — Risør, Norway*  
¹ ORCID: [0009-0006-0431-6637](https://orcid.org/0009-0006-0431-6637) · Email: marius0.of.1@gmail.com  

> **Epistemic Demarcation (`INSPIRED_BY != IMPLEMENTS != PROVES`):**  
> This note separates three distinct levels of claim so no analogy is mistaken for physical or experimental proof:
> 1. **Self-contained mathematical propositions:** Sphere-transitivity characterization of inner-product spaces (Section 1.2), realization separation $\mathcal{X}_{\mathrm{realized}} \subsetneq \mathcal{X}_{\mathrm{safe}}$ (Theorem 1), interlock-bypass detection logic (Theorem 2), and non-holomorphy of exact binary gates on connected complex domains (Theorem 3).
> 2. **Deterministic software & RTL architecture (`L1` / `L1.5`):** Fail-closed consequence gating (`OPEN`, `HOLD`, `KILL`, `TRAP`), pre-actuation blocking, and append-only SHA-256 hash chains in software. Software hash chains are tamper-evident logs, **not** physical WORM media unless backed by separately verified hardware fuses. No millikelvin or superconducting qubit laboratory experiment (`L3`) is claimed in this work.
> 3. **Structural analogies (`INSPIRED_BY`):** Parallels drawn between John F. Nash Jr.’s game-theoretic equilibrium (1950), Nash–Moser smoothing (1956), and his Oslo lecture on fourth-order curvature equations (2015) serve as **structural motivation** for `KY–Nash` integrity costs — not as a physical theory of gravitation.

---

## Abstract

Classical game theory and unconstrained control models share a structural blind spot: they treat every mathematically writable action or trajectory as immediately realizable. Building on viability theory (Aubin, 1991) and the **KY–Nash framework** of admissible transitions, this note formalizes consequence control around a simple premise: **a candidate proposal is never identical to an authorized action**.

We connect two sides of John F. Nash Jr.’s mathematical legacy as a structural lens for gated systems:
1. **Static resting states ($C^0$ fixed points, Nash 1950):** characterizing when no actor possesses an improving *authorized* move ($s^* \in E_{\mathrm{KY\text{-}Nash}}$).
2. **Active regularization under perturbation ($C^\infty$ Nash–Moser smoothing, Nash 1956, and higher-order curvature stabilization, Nash 2015 / Zampino 2015):** motivating why systems pushed out of equilibrium must pay explicit structural, irreversibility, and witness costs ($U_i(s) = u_i(s) - C_K(s) - S_{\mathrm{irr}}(s) - R_W(s)$) to keep runaway *"Ghost Win"* modes from consuming the underlying field.

We prove three elementary structural results for fail-closed gates: that static safety never implies actuation authority ($\mathcal{X}_{\mathrm{realized}} \subsetneq \mathcal{X}_{\mathrm{safe}}$), that current flow under a closed gate constitutes a decidable hardware interlock breach, and that an exact binary indicator $\{0,1\}$ on a connected complex domain cannot be holomorphic — requiring smooth interior estimation paired with a sharp outer cut. Finally, we illustrate boundary collapse through Napoleon’s 1812 Moscow campaign and specify the four-valued shadow gate (`OPEN`, `HOLD`, `KILL`, `TRAP`) for financial transaction rails.

---

## 1. Access Before Trajectory: Viability and Projection

Traditional action models assume that if a state update can be computed, it can be enacted. Here we invert that order:

$$\boxed{\mathbf{Trajectory\;is\;proposed.\;Access\;is\;granted\;at\;the\;gate.}}$$

We represent an operational system as a triad:

$$\mathcal{S} = (\mathcal{X}, \Phi, \mathcal{K})$$

* $\mathcal{X}$: The kinematic candidate space of all expressible configurations, metrics, and action profiles.
* $\Phi$: The unregulated proposal generator (free vector-field updates, search heuristics, or best-response proposals).
* $\mathcal{K} \subseteq \mathcal{X}$: The admissible subset defined by invariants, resource bounds, and transition rules.

Operational updates do not arise from $\Phi$ alone. A proposed step survives without modification only in the fixed-point kernel of the projection mismatch:

$$E(x) = \Phi(x) - \Pi_{\mathcal{K}}(\Phi(x)), \qquad \mathcal{X}_{\mathrm{adm\text{-}step}} = \ker(E)$$

Following Aubin (1991), sustained operation is restricted to the **viability kernel** $\mathrm{Viab}(\mathcal{K})$ — the subset of initial states from which forward gated evolution remains inside $\mathcal{K}$ for all steps:

$$\mathrm{Viab}(\mathcal{K}) = \left\{ x_0 \in \mathcal{K} \;\middle|\; (\Pi_{\mathcal{K}} \circ \Phi)^t(x_0) \in \mathcal{K}, \; \forall t \in \mathbb{N} \right\}$$

### 1.1 Orthogonal State Split

On discrete steps $t \in \mathbb{N}$, the system state $\mathbf{x}_t$ is separated into three non-overlapping records so proposal data can never overwrite authorization state:

$$\mathcal{X} = \mathcal{X}_{\mathrm{cand}} \oplus \mathcal{X}_{\mathrm{phase}} \oplus \mathcal{X}_{\mathrm{lock}}, \qquad \mathbf{x}_t = \begin{bmatrix} \mathbf{c}_t \\ \boldsymbol{\phi}_t \\ \boldsymbol{\lambda}_t \end{bmatrix}$$

* **$\mathbf{c}_t \in \mathcal{X}_{\mathrm{cand}}$ (Candidate):** Proposal ID, origin, intended action, payload digest, sequence index, and parent hash.
* **$\boldsymbol{\phi}_t \in \mathcal{X}_{\mathrm{phase}}$ (Diagnostic / Phase State):** Measured drift, spectral residuals, and constraint margins.
* **$\boldsymbol{\lambda}_t \in \mathcal{X}_{\mathrm{lock}}$ (Lock & Witness State):** Gate verdict ($\Omega \in \{\mathrm{OPEN}, \mathrm{HOLD}, \mathrm{KILL}, \mathrm{TRAP}\}$), physical interlock status, and append-only witness hash.

### 1.2 Why Inner-Product Projections Are Canonical Under Symmetry

Using orthogonal projections in finite-dimensional state-space checks is not arbitrary; it follows whenever the norm treats all directions on the unit sphere symmetrically (a classical result of Banach–Mazur–Auerbach):

> **Proposition 1 (Sphere-Transitivity Implies Inner-Product Space):** Let $(V, \|\cdot\|)$ be a finite-dimensional real normed space. The norm $\|\cdot\|$ is induced by an inner product if and only if for every pair $x, y \in V$ with $\|x\| = \|y\|$, there exists a linear isometry $T : V \to V$ such that $T(x) = y$.

*Proof:*  
*($\implies$)* In an inner-product space, any two vectors $x, y$ of equal norm span a subspace of dimension at most $2$, on which a rotation or reflection maps $x \mapsto y$ while preserving the inner product; extending $T$ as the identity on the orthogonal complement gives a global linear isometry.  
*($\impliedby$)* Because $\dim V < \infty$, the linear isometry group $G = \mathrm{Iso}(V, \|\cdot\|)$ is a closed, bounded subgroup of $\mathrm{GL}(V)$ and is therefore compact by Heine–Borel. Let $\mu$ be the unique normalized Haar measure on $G$, and choose any auxiliary inner product $\langle \cdot, \cdot \rangle_0$ on $V$. Averaging over $G$,
$$\langle u, v \rangle_{\mathrm{avg}} = \int_G \langle T(u), T(v) \rangle_0 \, d\mu(T),$$
defines a $G$-invariant inner product with norm $\|x\|_{\mathrm{avg}}$. Since $G$ acts transitively on the unit sphere $S = \{x \in V \mid \|x\| = 1\}$, $\|x\|_{\mathrm{avg}}$ takes a single constant value $c > 0$ across all $x \in S$. By positive homogeneity, $\|x\| = c^{-1}\|x\|_{\mathrm{avg}}$ for all $x \in V$, so $\|\cdot\|$ is induced by $c^{-2}\langle \cdot, \cdot \rangle_{\mathrm{avg}}$. $\blacksquare$

---

## 2. Layered Control Hierarchy (`L0`–`L6`)

To prevent high-level optimization goals from overriding low-level safety bounds, system responsibilities are ordered from physical cutoff at the bottom to long-horizon planning at the top. No upper layer holds write-access to bypass a lower layer’s invariants:

* **`L6` (Long-Horizon Objective):** Chooses candidate policies only inside the admissible set ($\max_{\pi \in \mathrm{Adm}} \sum_{t=0}^\infty \gamma^t U(\mathbf{x}_t)$).
* **`L5` (Model–Reality Audit):** Compares internal model predictions against independent sensor and witness records to catch self-confirming drift.
* **`L4` (Strategic Governance / `KY–Nash`):** Filters out locally profitable moves that degrade shared system integrity (*Ghost Wins*) or exploit asymmetric gate capture.
* **`L3` (Trajectory Stabilization):** Applies bounded smoothing and damping so noisy inputs do not cause chattering at the gate threshold.
* **`L2` (Constraint Sensing):** Computes exact margin residuals ($\Delta_K$) before actuation.
* **`L1` (Tamper-Evident Witness Log):** Append-only SHA-256 hash chain recording `OPEN`, `HOLD`, `KILL`, and `TRAP` decisions without silent overwrite.
* **`L0` (Physical Cutoff Anchor):** Hardware interlocks, relays, and fail-closed $0.00\,\text{V}$ de-energized defaults when authorization is absent.

---

## 3. Nash’s Duality as Structural Lens (`INSPIRED_BY`)

John F. Nash Jr.’s work spans two seemingly distant worlds — strategic equilibrium and geometric analysis — plus a late return to higher-order field equations:

1. **Equilibrium Existence ($C^0$ / Kakutani, Nash 1950):** Proves that compact, convex finite games admit a resting profile $s^*$ where no player gains by unilateral deviation. Classical Nash assumes every deviation in the action set is automatically executable.
2. **Smoothing Under Derivative Loss ($C^\infty$ / Nash–Moser, Nash 1956):** Solving the isometric embedding system
   $$g_{ij} = \sum_{\alpha=1}^N \frac{\partial y^\alpha}{\partial x^i}\frac{\partial y^\alpha}{\partial x^j}$$
   fails under naive Newton iteration because each step loses regularity. Nash overcame this by interleaving Newton steps with parameterized smoothing operators $S_\theta$ obeying tame estimates ($\|S_\theta u\|_s \le C \theta^{s-r}\|u\|_r$ for $s \ge r$).
3. **Higher-Order Curvature Lecture (Oslo 2015 / Zampino 2015):** In his final Abel Prize week lecture in Oslo (*"An Interesting Equation"*, May 20, 2015; analyzed by Zampino, 2015), Nash explored fourth-order curvature Lagrangians of the form $\int \sqrt{-g}(2R_{\mu\nu}R^{\mu\nu} - R^2)\,d^4x$. Higher-derivative systems famously risk unbounded Ostrogradsky modes unless unstable sectors are filtered or damped.

**Architectural takeaway (`INSPIRED_BY`):** In `KY–Nash`, we combine these two intuitions without conflating game theory with physical gravity. Nash (1950) stabilizes *choice inside a fixed room*; projection and smoothing principles inspire how `KY` stabilizes *the room itself* against high-gain, regularity-destroying moves.

---

## 4. Representation Dependence and Three Time Regimes

Two state descriptions that look equivalent under a coarse local score can differ in provenance, witness chain, or coordinate validity:

$$\mathrm{Repr}(A) \neq \mathrm{Repr}(B) \implies \Pi_{\mathcal{K}}(\mathbf{x}_A) \text{ need not equal } \Pi_{\mathcal{K}}(\mathbf{x}_B)$$

Accordingly, every transition passes through three distinct temporal phases:

1. **Reversible Exploration Time ($\mathcal{D}_1$ — Play / Trial):** Candidate transformations satisfy involution ($F \circ F = \mathrm{Id}$). Trials can be stepped forward and undone cleanly with zero external commitment.
2. **Dissipative Projection Time ($\Delta t_\Pi$ — The Cut):** Unregulated candidates meet an idempotent projection ($\Pi_{\mathcal{K}}^2 = \Pi_{\mathcal{K}}$). Because many raw candidates map to the same projected state, projection is non-invertible ($\det D\Pi_{\mathcal{K}} = 0$ off the subspace) and discards microstate information — incurring at minimum Landauer’s erasure bound $Q \ge k_B T \ln 2 \cdot \Delta I$ in any physical realization (Landauer, 1961).
3. **Monotonic Witness Time ($\mathcal{D}_2$ — Post-Commit History):** Once `OPEN` is granted, the event is appended to the hash chain. Retraction requires a *new* Compensating Entry; past entries are never erased.

---

## 5. Reversible Trial Space and Seven Design Rules

Before reaching the consequence gate, candidate updates can be tested inside a reversible trial buffer ($\mathcal{D}_1$) governed by seven engineering rules:

1. **No Silent Overwrite:** Trial steps permute or shift state coordinates without erasing input provenance.
2. **Symmetric Undo:** Every trial transform $F$ carries an explicit inverse (or involution $F(F(s)) = s$).
3. **Bounded Drift:** Perturbations that break exact round-trip recovery flag `MASK_MUTATED` and abort actuation.
4. **Role Separation:** The generator proposes what to test; an independent checker verifies round-trip consistency.
5. **Zero Actuation Authority:** Passing a reversible trial never grants `OPEN` by itself.
6. **Explicit Residual Reporting:** Any numerical or constraint mismatch is surfaced as a structured deficiency ($\Delta_K$).
7. **Post-Commit Silence:** Once a transition enters $\mathcal{D}_2$, trial scratchpads cannot mutate committed history.

---

## 6. Four-Valued Consequence Gate (`E-TOR`)

The supervisor $\Omega$ maps candidate and diagnostic state into four mutually exclusive verdicts:

$$\Omega : \mathcal{X}_{\mathrm{cand}} \times \mathcal{X}_{\mathrm{phase}} \longrightarrow \{\mathrm{OPEN}, \mathrm{HOLD}, \mathrm{KILL}, \mathrm{TRAP}\}$$

evaluated under strict fail-closed precedence:

$$\mathbf{KILL} \;\succ\; \mathbf{TRAP} \;\succ\; \mathbf{HOLD} \;\succ\; \mathbf{OPEN}$$

No high payoff estimate can override a single invariant violation:

* **`OPEN`:** Candidate satisfies structural invariants and carries an explicit, verifiable evidence ID. Authorized to cross into $\mathcal{D}_2$.
* **`HOLD`:** Candidate lacks complete warrant ($\Delta_K \neq \varnothing$) or sits within the threshold margin. Returned to the workbench under bounded clock supervision ($\tau_{\max}$) so `HOLD` cannot decay into `OPEN` by waiting nor be abused as indefinite administrative stalling.
* **`KILL`:** Candidate breaches invariants, spoofs provenance, or attempts to pass metaphor/bluff as proof. Rejected immediately (`0 V` / disabled actuation).
* **`TRAP` (Shadow Containment):** When coordinated adversarial probing or bypass patterns are detected, execution is routed to an isolated sandbox state ($\mathbf{x}_{\mathrm{mirror}}$) returning only a synthetic local receipt (`local_ACK`) with zero external effect:
  $$\mathrm{local\_ACK}(c) \neq \mathrm{public\_consequence}(c)$$

---

## 7. Realization Separation, Sabotage Detection, and Non-Holomorphy

> **Theorem 1 (Realization Separation):** Let $\mathcal{X}_{\mathrm{safe}} \subseteq \mathcal{X}$ be the set of states satisfying static safety constraints, and let $\mathcal{X}_{\mathrm{realized}}$ be the set of states authorized to actuate. Whenever actuation requires an independent extrinsic evidence token $w \in \mathcal{W}_{\mathrm{valid}}$ in addition to state safety,
> $$\mathcal{X}_{\mathrm{realized}} \subsetneq \mathcal{X}_{\mathrm{safe}}.$$

*Proof:* By definition, $\mathbf{x} \in \mathcal{X}_{\mathrm{realized}} \iff \mathbf{x} \in \mathcal{X}_{\mathrm{safe}} \land \Omega(\mathbf{x}, w) = \mathrm{OPEN}$. Every realized state belongs to $\mathcal{X}_{\mathrm{safe}}$. Conversely, take any safe configuration $\mathbf{x}_0 \in \mathcal{X}_{\mathrm{safe}}$ with missing or empty warrant ($w = \varnothing$). Fail-closed gating assigns $\Omega(\mathbf{x}_0, \varnothing) = \mathrm{HOLD} \neq \mathrm{OPEN}$, so $\mathbf{x}_0 \notin \mathcal{X}_{\mathrm{realized}}$. Thus the inclusion is strict. $\blacksquare$

> **Theorem 2 (Hardware Interlock Bypass Detection):** Suppose the hardware contract enforces the biconditional $\big(\Omega = \mathrm{OPEN}\big) \iff \big(I_{\mathrm{act}} > I_{\mathrm{leak}}\big)$, where $I_{\mathrm{act}}$ is measured actuator current above leakage floor $I_{\mathrm{leak}}$. Any observation satisfying $\Omega \in \{\mathrm{HOLD}, \mathrm{KILL}, \mathrm{TRAP}\} \land I_{\mathrm{act}} > I_{\mathrm{leak}}$ refutes the contract and witnesses a physical bypass or fault.

*Proof:* Substituting $\Omega \neq \mathrm{OPEN}$ (false on the left) and $I_{\mathrm{act}} > I_{\mathrm{leak}}$ (true on the right) falsifies the biconditional $(\text{False} \iff \text{True}) \equiv \text{False}$, providing a deterministic comparator trigger (`SABOTAGE_INTERLOCK_BYPASS`) for upstream cutoff. $\blacksquare$

> **Theorem 3 (Non-Holomorphy of Exact Binary Gates):** Let $\mathcal{D} \subset \mathbb{C}^n$ be a non-empty connected open domain. No non-constant exact binary gate $\chi_{\mathcal{K}} : \mathcal{D} \to \{0, 1\}$ can be holomorphic on $\mathcal{D}$.

*Proof:* Suppose $\chi_{\mathcal{K}} : \mathcal{D} \to \mathbb{C}$ is holomorphic and takes values only in the discrete set $\{0, 1\}$. Because $\chi_{\mathcal{K}}$ is continuous on the connected set $\mathcal{D}$ into a discrete space, $\chi_{\mathcal{K}}$ must be constant ($\chi_{\mathcal{K}} \equiv 0$ or $\chi_{\mathcal{K}} \equiv 1$). Hence no holomorphic function can separate admissible ($1$) from inadmissible ($0$) regions on a connected domain. $\blacksquare$

**Design consequence:** Smooth optimization and gradient methods belong strictly *inside* the candidate generator ($\Phi$), whereas final authorization ($\Omega$) must remain a non-smooth, discrete cut at the boundary.

---

## 8. Integrity-Adjusted Payoffs and Structural Parallels

In `KY–Nash` game theory, raw immediate gain $u_i(s)$ is corrected by three real-world costs incurred when pushing an action through shared institutions or infrastructure:

$$\boxed{U_i(s) = u_i(s) - C_K(s) - S_{\mathrm{irr}}(s) - R_W(s)}$$

| Strategic Cost Term | Meaning in `KY–Nash` Game Theory | Motivating Physical Analogy (`INSPIRED_BY`) |
| :--- | :--- | :--- |
| **$C_K(s)$ (Structure Cost)** | Effort spent bending rules, fighting friction, or straining shared interfaces. | Viscous boundary shear resisting rapid deformation. |
| **$S_{\mathrm{irr}}(s)$ (Irreversibility Cost)** | Loss of future strategic options after burning bridges or locking into rigid paths. | Higher-order curvature damping suppressing runaway Ostrogradsky modes (Nash, 2015; Zampino, 2015). |
| **$R_W(s)$ (Witness Cost)** | Reputational, legal, and trust cost once the move is permanently recorded before witnesses. | Boundary information / decodability load required to reconstruct history within finite propagation bounds (cf. Mozumdar, 2026). |

*(Note: The rightmost column records motivating analogies across physics and information theory, not an identity between tensor fields and scalar utilities.)*

---

## 9. Case Studies: Napoleon in 1812 and Financial Shadow Gates

### 9.1 Napoleon’s 1812 Campaign as Boundary Collapse (*Ghost Win*)

Napoleon optimized raw tactical utility ($\max u_i$) under the cabinet-war convention where occupying an opponent’s capital triggered an `OPEN` transition to peace terms. Russian command under Kutuzov refused that gate rule, preserving army viability ($\mathrm{Viab}(\mathcal{K}_{\mathrm{Russ}})$) over territory:

* **Ghost Win:** Entering Moscow yielded high symbolic score ($u_i \gg 0$) while failing the opponent’s peace gate (`KILL` on treaty expectations).
* **Unbounded `HOLD` Bleed:** Waiting five weeks in Moscow trapped the Grande Armée in an uncompensated `HOLD` state where metabolic and structural losses ($\Delta C_K + \Delta S_{\mathrm{irr}}$) accumulated daily with zero commit.
* **Viability Collapse:** By the time retreat began, supply and weather margins had fallen outside $\mathrm{Viab}(\mathcal{K})$, turning an apparent victory into systemic collapse.

### 9.2 Financial Consequence Control (`Shadow Gate`)

Autonomous trading and credit agents generate fluent, locally persuasive transaction proposals at machine speed. The core safeguard is straightforward:

$$\boxed{\mathbf{Finance\;tolerates\;open\;models,\;but\;never\;open\;consequences.}}$$

Deployed as a pre-execution gate ahead of settlement rails:
* **`OPEN`:** Within risk invariants and signed warrant $\to$ released to settlement.
* **`HOLD`:** Missing warrant or threshold ambiguity $\to$ queued with explicit deficiency list ($\Delta_K \neq \varnothing$) and deadline ($\tau_{\max}$) for human maker-checker review.
* **`KILL`:** Breaches hard exposure or compliance bounds $\to$ blocked at `0` execution, hash-logged.
* **`TRAP`:** Coordinated probing or prompt/API manipulation $\to$ shunted to $\mathbf{x}_{\mathrm{mirror}}$ (`local_ACK` only, zero capital moved).

---

## 10. Pre-Actuation Gating and Step-Sealing (`L1` / `L1.5` Architecture)

In hardware-oriented control chains (`L1` simulation and `L1.5` FPGA synthesis prototypes), gating acts **prior to energy delivery** rather than as a post-hoc audit:

$$\text{Estimator} \longrightarrow \Pi_{\mathcal{K}} \longrightarrow \Omega\text{ Enable} \longrightarrow \text{Actuator Drive}$$

$$\text{Inadmissible Candidate} \implies \Omega \neq \mathrm{OPEN} \implies \text{Enable} = 0 \implies \text{No Actuation}$$

When discrete sequence counters or stochastic step-checks use random Fibonacci recurrences ($F_n = \pm F_{n-1} \pm F_{n-2}$ under unbiased sign noise), asymptotic exponential growth is governed almost surely by **Viswanath’s constant** (Viswanath, 2000):

$$\lim_{n \to \infty} |F_n|^{1/n} = C_{\mathrm{Vis}} \approx 1.13198824\dots$$

providing an exact analytical reference rate when testing stochastic drift monitors in `L1` simulations.

---

## 11. Conclusion

Across game theory, software agents, and fail-closed hardware interfaces, the architectural boundary is the same:

$$\boxed{\mathbf{Reality\;is\;not\;the\;sum\;of\;what\;can\;be\;computed.\;Reality\;is\;that\;which\;survives\;the\;cut.}}$$

* **Inside the generator ($\Phi$):** Exploration remains free, smooth, and reversible.
* **At the gate ($\Pi_{\mathcal{K}}, \Omega$):** Proposals face discrete, fail-closed selection (`KILL > TRAP > HOLD > OPEN`).
* **In history ($\mathcal{D}_2$):** Only authorized transitions enter the witness chain, while final accountability stays with the human operator outside the code.

---

## References

1. Aubin, J.-P. (1991). *Viability Theory*. Birkhäuser, Boston.
2. Gemp, I., Marris, L., & Piliouras, G. (2024). Approximating Nash equilibria in normal-form games via stochastic optimization. *ICLR 2024*.
3. Landauer, R. (1961). Irreversibility and heat generation in the computing process. *IBM Journal of Research and Development*, 5(3):183–191.
4. Mozumdar, J. (2026). Lieb–Robinson bounds and entanglement limits in quantum dynamics with finite-dimensional memory. *arXiv:2604.11209*.
5. Nash, J. F. (1950). Equilibrium points in $n$-person games. *Proceedings of the National Academy of Sciences*, 36(1):48–49.
6. Nash, J. F. (1956). The imbedding problem for Riemannian manifolds. *Annals of Mathematics*, 63(1):20–63.
7. Viswanath, D. (2000). Random Fibonacci sequences and the number $1.13198824\dots$. *Mathematics of Computation*, 69(231):1131–1155.
8. Zampino, E. J. (2015). *A Note on "An Interesting Equation" by John Nash Jr.* (analyzing J. F. Nash’s May 20, 2015 Abel Prize lecture at the University of Oslo).
