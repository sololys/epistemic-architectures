# Boundary Counterexamples & Fail-Closed Derivations for $W^2$

**Surface:** `/notes/W2_BOUNDARY_COUNTEREXAMPLES.md`  
**Role:** Non-executable working derivations illustrating why each of the five proof chains in `/specifications/W2_FIVE_PROOF_CHAINS_SPEC.md` is necessary.

---

## 1. Orthogonal Blindness of Pointwise State Norms (Chain 2 Counterexample)
Consider a 2D state basis $\Psi(0) = I_2$. Under a rigid rotation by $\theta = \pi/2$:
$$\Psi(t) = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}.$$
A naive pointwise Euclidean detector measures $\|\Psi(t) - \Psi(0)\|_F = 2 > 0$ and falsely trips an alarm on a harmless coordinate rotation. Conversely, the relational Gram observable $G(t) = \Psi(t)^\top \Psi(t) = I_2$ yields $\Delta_G = \|G(t) - G(0)\|_F = 0$ (`OPEN`), while an internal shear $\Psi_{\mathrm{shear}} = \begin{pmatrix} 1 & 0.2 \\ 0 & 1 \end{pmatrix}$ yields $\Delta_G > 0$ (`KILL`).

## 2. IEEE-754 Floating-Point Drift vs. Exact Rational Ledger (Chain 3 Counterexample)
In binary floating-point arithmetic (`float64`):
$$0.1 + 0.2 - 0.3 = 5.551115123125783 \times 10^{-17} \neq 0.$$
To avoid arbitrary epsilon thresholds that can be exploited via salami-slicing drift, Chain 3 evaluates conserved quantities strictly in $\mathbb{Q}$ (`fractions.Fraction`), enforcing $\Delta R \equiv \frac{0}{1}$.

## 3. Monotone Hardware Fuse Against State Rollback (Chain 5 Counterexample)
If an adversary replays an older valid SHA-256 state receipt from time $t - k$, the 64-bit monotone fuse register $F_n$ detects the cleared fuse bits because $(F_{\mathrm{current}} \mathbin{\&} F_{\mathrm{replayed}}) \neq F_{\mathrm{current}}$, forcing immediate `KILL` ($0.00\,\mathrm{V\ DC}$).
