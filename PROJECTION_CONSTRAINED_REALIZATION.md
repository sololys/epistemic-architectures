# Projection-Constrained Realization and Nash-Type Fixed Points in Physical Systems

> **Abstract:** Standard physical formulations identify reality with the full solution space of dynamical equations ($\dot{x} = f(x)$). In physical, biological, and engineered control systems, however, not all mathematical solutions are realized: causality, thermodynamic irreversibility, stability, and fail-closed admissibility eliminate candidates before physical actuation. We formalize this selection principle:
> 
> $$\boxed{\mathbf{Reality} = \operatorname{Fix}(\Pi \circ \Phi) = \ker(E)}$$
> 
> where $\Phi$ generates candidate dynamics and $\Pi$ is an idempotent admissibility projection ($\Pi^2 = \Pi$). We prove that: (i) realized dynamics is generically non-involutive ($M \circ M \neq \mathrm{Id}$) even when the pre-selection consistency layer is involutive ($F \circ F = \mathrm{Id}$), (ii) physical existence is structurally equivalent to a Nash equilibrium under an induced best-response operator $BR = \Pi \circ \Phi$, and (iii) General Relativity's field equations emerge as an equilibrium limit ($\Phi_\perp = 0$) of a broader projection-constrained dynamics. We outline falsifiable experimental predictions separating state-determined statistics from history-dependent kernel admissibility. Finally, we show that decentralized local-first survivability architectures (Infranett) constitute physical engineering instantiations of this fixed-point selection law.

---

## 1. Introduction: From Solution to Selection

Classical mechanics, field theory, and dynamical systems routinely identify physical reality with the unrestricted trajectory of a generator:

$$x_{t+1} = \Phi(x_t)$$

In physical implementation, however, unconstrained generation is an idealization. Physical systems do not realize all mathematically possible solutions; invalid, unstable, ungrounded, or non-admissible candidate states are eliminated prior to irreversible commitment.

We define physical existence through an explicit selection principle:

$$\boxed{x \text{ exists} \iff x = \Pi(\Phi(x)) \iff x \in \operatorname{Fix}(\Pi \circ \Phi)}$$

where:
* $\Phi : \mathcal{X} \to \mathcal{X}$ generates candidate dynamics,
* $\Pi : \mathcal{X} \to \mathcal{K} \subseteq \mathcal{X}$ is an idempotent admissibility projection ($\Pi^2 = \Pi$),
* $\mathcal{K} = \operatorname{Im}(\Pi) = \{x \in \mathcal{X} \mid \Pi(x) = x\}$ is the admissible constraint manifold.

$$\boxed{\mathbf{Dynamical\;laws\;generate\;possibilities;\;admissibility\;selects\;realizable\;states.}}$$

---

## 2. Mathematical Framework and Elimination Operator

Let $\mathcal{X}$ be a complete metric state space.

* **Realized Dynamics Operator:**
  $$M := \Pi \circ \Phi, \qquad x_{t+1} = M(x_t)$$

* **The Elimination Operator:**
  We define the defect or elimination operator $E : \mathcal{X} \to \mathcal{X}$:
  $$E(x) := x - \Pi(\Phi(x))$$

  $$\boxed{\mathbf{Reality} = \operatorname{Fix}(M) = \ker(E)}$$

  *Ontological shift:* Reality is not what is merely generated; **reality is that which cannot be eliminated.**

* **Orthogonal Decomposition:**
  For any candidate transition $\Phi(x)$, the state decomposes into admissible and inadmissible components:
  $$\Phi(x) = \Phi_{\mathcal{K}}(x) + \Phi_\perp(x)$$
  satisfying:
  $$\Pi(\Phi_{\mathcal{K}}) = \Phi_{\mathcal{K}}, \qquad \Pi(\Phi_\perp) = 0$$

* **Fail-Closed Realization:**
  In physical control and hardware architectures, realization is strictly fail-closed:
  $$x_{t+1} = \begin{cases} \Phi(x_t), & \Phi(x_t) \in \mathcal{K} \\ \bot, & \Phi(x_t) \notin \mathcal{K} \end{cases}$$
  Invalid states are completely eliminated ($0.00\,\text{V}$ stasis), never permitted to degrade gracefully into corrupted reality.

---

## 3. Involutive Pre-Selection vs. Non-Involutive Realization

### 3.1 The Dual-Layer Architecture

A consistent system contains two structurally incompatible operational layers:

1. **The Involutive Consistency Layer ($F$):**
   An internal verification operator $F : \mathcal{X} \to \mathcal{X}$ satisfying the involution identity:
   $$F \circ F = \mathrm{Id} \implies F^{-1} = F$$
   *Lemma 3.1:* $F$ is strictly information-preserving and reversible ($\Delta S_{\mathrm{irr}} = 0$). This constitutes a zero-dissipation test space.

2. **The Non-Involutive Realization Layer ($M$):**
   The realization operator $M = \Pi \circ \Phi$.

### 3.2 The Irreversibility Theorem

> **Theorem 3.2 (Non-Involutivity of Realization):** If $\Pi(\Phi(x)) \neq \Phi(x)$ (i.e., $\Phi_\perp(x) \neq 0$), then the realized dynamics $M$ is strictly non-involutive:
> 
> $$M(M(x)) \neq x$$

*Proof:*  
$M(x) = \Pi(\Phi(x)) = \Phi_{\mathcal{K}}(x)$.  
Applying $M$ again yields $M(M(x)) = \Pi(\Phi(\Phi_{\mathcal{K}}(x)))$.  
Because the orthogonal component $\Phi_\perp(x)$ was discarded by the idempotent projection $\Pi$ ($\Pi(\Phi_\perp) = 0$), the original state $x$ cannot be reconstructed by any composition of $M$. Hence $M(M(x)) \neq x$. $\blacksquare$

> **Corollary 3.3 (Projection Induces Physical Irreversibility):**  
> An idempotent projection ($\Pi^2 = \Pi \neq \mathrm{Id}$) is non-invertible. Therefore, realization $M = \Pi \circ \Phi$ is intrinsically irreversible, even when the underlying generator $\Phi$ is strictly unitary or Hamiltonian.

$$\boxed{\mathbf{Involusjon\;bestemmer\;konsistens.\;Projeksjon\;bestemmer\;eksistens.}}$$

---

## 4. Nash–Admissibility Equivalence

Let $BR : \mathcal{X} \to \mathcal{X}$ be a response operator in game-theoretic decision space.

* **Definition 4.1 (Nash Equilibrium):** A state $x^*$ is a Nash equilibrium if and only if:
  $$x^* = BR(x^*)$$

* **Theorem 4.2 (Structural Equivalence):** Let the response operator be defined by the projection-constrained generator $BR := \Pi \circ \Phi$. Then:
  $$\boxed{x \text{ physically exists} \iff x \text{ is a Nash equilibrium}}$$

*Proof:* Immediate from $x = \Pi(\Phi(x)) \iff x = BR(x) \iff x \in \operatorname{Fix}(BR)$. $\blacksquare$

### Refusal of Ghost Wins

Standard optimization seeks to maximize immediate local payoff:

$$\max_{\pi} \mathbb{E}[R_t]$$

This frequently precipitates a **Ghost Win**—capturing a localized round while destroying the global viability boundary $\mathcal{K}$. 

KY-Nash defines true strategic admissibility as persistent forward invariance:

$$\mathrm{Viab}(\mathcal{K}) = \left\{ x_0 \in \mathcal{X} \mid (\Pi \circ \Phi)^t(x_0) \in \mathcal{K}, \; \forall t \ge 0 \right\}$$

Physical survival and strategic coherence require refusing local optimization whenever it drives the state outside the viable kernel.

---

## 5. Physical Instantiations

### 5.1 Quantum Measurement
* Generator $\Phi$: Unitary time evolution $U_t = e^{-i\hat{H}t/\hbar}$ (reversible, unitary).
* Projection $\Pi$: Measurement / decoherence boundary onto eigenbasis.
* Realized State:
  $$|\psi_{t+1}\rangle = \Pi(U |\psi_t\rangle)$$
  The measurement operator is non-unitary because selection discards the unselected branches of the candidate superposition.

### 5.2 General Relativity as an Equilibrium Limit
Let $g_{\mu\nu}$ be the spacetime metric and $\Phi$ a geometric flow. Admissibility requires causal stability:

$$\mathcal{A} = \left\{ g \mid \mathrm{Re}(\lambda_i(\mathcal{L}_g)) \le 0 \right\}, \qquad g_{t+1} = \Pi_{\mathcal{A}}(\Phi(g_t))$$

When decomposing candidate geometry $\Phi(g) = \Phi_{\mathcal{K}} + \Phi_\perp$, the discarded component $\Phi_\perp$ induces an effective non-equilibrium selection stress tensor $\Sigma_{\mu\nu}^{\mathrm{irr}}$:

$$G_{\mu\nu} = 8\pi G \left( T_{\mu\nu} + \Sigma_{\mu\nu}^{\mathrm{irr}} \right)$$

At the **equilibrium limit** where projection stress vanishes ($\Phi_\perp = 0$):

$$\boxed{G_{\mu\nu} = 8\pi G \, T_{\mu\nu}}$$

Einstein's field equations emerge as the zero-selection-stress equilibrium of a broader projection-constrained manifold.

---

## 6. The Kernel as Verifiable History ($K_\gamma$)

Standard physics models the state solely via instantaneous variables $x_t$. We extend the description to include the verifiable state chain:

$$K_\gamma = \{ q_0 \xrightarrow{\;\Pi\;} q_1 \xrightarrow{\;\Pi\;} \dots \xrightarrow{\;\Pi\;} q_T \}$$

where each transition satisfies verified admissibility:

$$\mathcal{V}(q_t, q_{t+1}) = 1 \iff q_{t+1} = \mathcal{E}(\Pi(\Phi(x_t)))$$

### Falsifiable Experimental Prediction

Standard quantum mechanics asserts that outcome probability depends solely on the density matrix: $p = \mathrm{Tr}(E\rho)$.

Our selection framework yields an operational, falsifiable hypothesis:

$$\boxed{\rho_A \approx \rho_B, \quad K_A \neq K_B \implies p_A \neq p_B}$$

* **Null Hypothesis ($H_0$):** $p_A = p_B$ (Standard QM; history has no selection effect).
* **Alternative Hypothesis ($H_1$):** $p_A \neq p_B$ (Kernel-constrained realization; prior admissible history deforms measurement projection).

---

## 7. Infranett as the Physical Fixed Point

The profound engineering consequence of this law is realized in **Infranett**:

In an adversarial, degraded, or sabotaged operating environment (severed fiber, electromagnetic warfare, satellite denial), the unconstrained environmental generator $\Phi_{\text{env}}$ introduces catastrophic divergence ($\Phi_\perp \gg 0$).

Ordinary centralized systems collapse because they lack an internal idempotent projection operator $\Pi$; they attempt to maintain state across an invalid path ($K \to \emptyset$), resulting in systemic failure.

Infranett, by contrast, enforces:

1. **Idempotent Local Projection ($\Pi_{\text{local}}^2 = \Pi_{\text{local}}$):** Every node evaluates admissibility exclusively against its local boundary.
2. **Fail-Closed Hardware Gating ($x \notin \mathcal{K} \implies 0.00\,\text{V}$):** Undefined states are mechanically locked out via analog crowbars.
3. **Verifiable State Chain ($K_\gamma$):** Append-only write-ahead logs (WAL) physically transported via courier capsules ensure that the causal history remains unbroken.

Therefore:

$$\boxed{\mathbf{Infranett} \equiv \operatorname{Fix}(\Pi \circ \Phi)}$$

**Infranett is the physical fixed point.** It is the state that remains invariant when the external world is forced through the boundary of physical survival.

---

## Citation

```bibtex
@article{torjusen2026projectionconstrained,
  author    = {Torjusen, Marius Egerhei},
  title     = {Projection-Constrained Realization and Nash-Type Fixed Points in Physical Systems},
  journal   = {Epistemic Architectures Working Papers},
  year      = {2026},
  url       = {https://github.com/sololys/epistemic-architectures}
}
```
