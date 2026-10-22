# L1_LAW // PWR2 & Power-Law Spin Scrambling vs. Collective Dynamics Gate ($\Pi_K$)

$$\boxed{\text{GENERATION} \neq \text{AUTHORIZATION} \neq \text{WITNESSED CONSEQUENCE}}$$

* **Surface:** `L1_LAW/PWR2_SCRAMBLING_COLLECTIVE_GATE_SPEC.md`
* **Executable Gate Verifier:** [`L2_GATE/verify_pwr2_scrambling_collective_gate.py`](../L2_GATE/verify_pwr2_scrambling_collective_gate.py) (`6/6 PASS`)
* **Epistemic Boundary:** `INSPIRED_BY != IMPLEMENTS != PROVES` · `PHYSICAL_AUTHORITY = NONE` (`L1` deterministic software only)

---

## 1. Fixed Hamiltonian, Tunable Complexity Regime

Inspired by Kuriyattil, Kombe, Daley & Poggi (2026), *"Tuning between collective dynamics and scrambling through initial-state symmetry alignment in long-range spin models"*, consider a translation-invariant 1D XY spin model on $N$ spins with periodic boundary conditions:

$$H = \sum_{i,j} \chi_{ij} \left( S_i^x S_j^x + S_i^y S_j^y \right),$$

where the circulant coupling matrix $\chi_{ij}$ belongs to one of four canonical geometries:
1. **Powers-of-Two (`PWR2`):** $\chi_{ij} = \chi_0$ if $\min(|i-j|, N-|i-j|) = 2^{m-1}$, else $0$ ($\mathcal{O}(\log_2 N)$ degree).
2. **Power-Law (`PL`, $\alpha=1$):** $\chi_{ij} = \min(|i-j|, N-|i-j|)^{-\alpha}$.
3. **All-to-All (`A2A`):** $\chi_{ij} = 1$ for all $i \neq j$ (One-Axis Twisting limit).
4. **Nearest-Neighbor (`NN`):** $\chi_{ij} = 1$ if $\min(|i-j|, N-|i-j|) = 1$.

---

## 2. Circulant Fourier Spectrum & Linearized OTOC Instability ($\Gamma_q^2(K)$)

For any symmetric circulant adjacency matrix with first row $(a_0, a_1, \dots, a_{N-1})$, the exact Fourier eigenvalues are:

$$\lambda_q = \sum_{r=0}^{N-1} a_r \cos\!\left(\frac{2\pi q r}{N}\right), \qquad q \in \{0, 1, \dots, N-1\}.$$

Linearizing the semiclassical Heisenberg equations of motion around an equatorial background configuration with dominant Fourier mode $K \in \{0, 1, N/2\}$ yields the mode evolution equation:

$$\ddot{y}_q = \lambda_K (\lambda_q - \lambda_K) y_q \implies \Gamma_q^2(K) = \lambda_K (\lambda_q - \lambda_K).$$

* **Theorem 1 (`PWR2` Alternating Néel Instability):** At the staggered Néel mode $K = N/2$, **only** the `PWR2` graph has $\lambda_{N/2} > 0$ (for $N=32$, $\lambda_{16} = +5.0$, $\lambda_0 = +9.0 \implies \Gamma_0^2(16) = 20.0 > 0$), whereas `PL` ($\lambda_{16} = -1.3882 < 0$), `A2A` ($\lambda_{16} = -1.0 < 0$), and `NN` ($\lambda_{16} = -2.0 < 0$) all satisfy $\lambda_{N/2} < 0$.
* **Theorem 2 (`PL` Protocol Asymmetry):** In the Power-Law (`PL`, $\alpha=1$) graph, alternating spin flips ($K = N/2$) suppress exponential sensitivity ($\max_q \Gamma_q^2(N/2) \le 0 \implies \text{HOLD}$), whereas one-sided spin flips ($K = 1$, $\lambda_1 = +3.4069 > 0$) yield $\Gamma_0^2(1) > 0 \implies \text{KILL}$.

---

## 3. Signed Graph Laplacian Gap & Critical Scaling $k^*(N) \sim \sqrt{N}$

Initializing $k$ spin flips $|\Psi_k^\alpha(0)\rangle = Z_k^\alpha |+\rangle^{\otimes N}$ induces a similarity transformation $H_k^\alpha = Z_k^\alpha H Z_k^\alpha$ with signed adjacency matrix:

$$A_k^\alpha = D_k^\alpha A D_k^\alpha, \qquad (D_k^\alpha)_{ii} = (-1)^{\mathbb{I}(i \in \alpha)}.$$

The spectral gap $\Delta(\alpha)$ protecting the $\mathcal{O}(N)$ collective Dicke manifold collapses when the number of symmetry-breaking flips exceeds the subextensive critical threshold:

$$k^*(N) \sim \sqrt{N} \quad \Longleftrightarrow \quad \frac{k^*(N)}{N} \propto N^{-1/2}.$$

The consequence gate $\Pi_K$ maps $(N, k, \text{geometry}, \text{protocol})$ to:
- `GATE::OPEN` ($5.00\text{ V DC}$): $k = 0$ (full permutational symmetry, $\Delta > 0$, $F_Q^*/N = N$).
- `GATE::HOLD` ($0.00\text{ V DC}$): $0 < k \le \sqrt{N}$ or $\max_q \Gamma_q^2(K) \le 0$ (requires $Z_k^\alpha$ resymmetrization prior to actuation).
- `GATE::KILL` ($0.00\text{ V DC}$): $k > \sqrt{N}$ and $\max_q \Gamma_q^2(K) > 0$ (fast scrambling across the $2^N$ space in $t^* \propto \log_2 N$).
