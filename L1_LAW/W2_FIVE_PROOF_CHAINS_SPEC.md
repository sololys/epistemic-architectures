# Formal Specification: Five Mathematical Proof Chains for $W^2$ Pre-Commit Authorization

**Document ID:** `SPEC-W2-FIVE-PROOF-CHAINS-2026-v1.0`  
**Surface:** `/specifications/W2_FIVE_PROOF_CHAINS_SPEC.md`  
**Epistemic Status:** `L1` Formal Contract & Deterministic Verification Specification (`INSPIRED_BY != IMPLEMENTS != PROVES`; `PHYSICAL_AUTHORITY = NONE`)  
**Governing Law:** $\text{GENERATION} \neq \text{AUTHORIZATION} \neq \text{WITNESSED CONSEQUENCE}$

---

## 1. Axiom of Conjunctive Pre-Commit Authorization

No candidate state transition $x'_{t+1} \in \Phi(x_t)$ may enter the `OPEN` ($5.00\,\mathrm{V\ DC}$) state unless all five orthogonal projection residuals satisfy their respective thresholds and a synchronous dual witness $W^2 = \langle W_{\mathrm{machine}}, W_{\mathrm{human}}\rangle$ is sealed prior to actuation:

$$\Omega(\Pi_K(x_t)) = \begin{cases}
\mathrm{OPEN}\;(5.00\,\mathrm{V\ DC}), & \text{if } \prod_{k=1}^{5} \mathbb{I}(\Delta_{K,k} \le \epsilon_k) = 1 \;\land\; W_{\mathrm{machine}} \neq \varnothing \;\land\; W_{\mathrm{human}} \neq \varnothing, \\[6pt]
\mathrm{KILL}\;(0.00\,\mathrm{V\ DC}), & \text{if } \exists\, k \in \{1..5\} : \Delta_{K,k} > \epsilon_k \quad (\text{Cycle-1 cutoff + post-mortem log}), \\[6pt]
\mathrm{HOLD}\;(0.00\,\mathrm{V\ DC}), & \text{otherwise} \quad \left(\text{High-Z quarantine, } \frac{\mathrm{d}}{\mathrm{d}t}\mathrm{HOLD} = 0\right).
\end{cases}$$

---

## 2. The Five Mathematical Proof Chains

### Chain 1 — Involutive Reversibility & Envelope Bound (`Door 25` Digital Twin)
For any proposed transition operator $a$ acting on initial state $S_0 \in \mathbb{R}^d$, the Digital Twin evaluates the forward state $S_f = a(S_0)$ and the inverse pullback $S_r = a^{-1}(S_f)$:
$$\Delta_{K,1} := \|S_0 - S_r\|_2 \le \epsilon_{\mathrm{iso}}, \qquad \|S_f\|_\infty \le E_{\max}.$$
* $\Delta_{K,1} > \epsilon_{\mathrm{iso}} \implies \mathrm{KILL}$ (`TWIN_ASYMMETRY_DETECTED`).
* $\|S_f\|_\infty > E_{\max} \implies \mathrm{HOLD}$ (`TWIN_ENVELOPE_BREACH`).

### Chain 2 — Relational Gram Invariance (`Monolith 4` Kernel Drift)
Given a state configuration matrix $\Psi(t) = [\psi_1(t), \dots, \psi_m(t)]$ and its relational Gram matrix $G_{ij}(t) = \langle \psi_i(t), \psi_j(t)\rangle$:
$$\Delta_{K,2} := \|G(t) - G(0)\|_F \le \tau_G, \qquad \mathrm{Tr}(G(t)) \ge 0, \quad \det(G(t)) \ge 0.$$
Rigid orthogonal transformations $\Psi(t) = U\Psi(0)$ with $U^\top U = I$ satisfy $\Delta_{K,2} = 0$ (`OPEN`), whereas internal metric shear violating relational geometry triggers $\mathrm{KILL}$ (`RELATIONAL_GRAM_SHEAR_KILL`). Missing reference state $G(0)$ triggers $\mathrm{HOLD}$.

### Chain 3 — Exact Rational Conservation & Operator Completeness ($\mathbb{Q}$)
All conserved balances (mass, charge, token flow, and diagonal POVM completeness $\sum_{k=1}^M E_k = I$) are evaluated over exact rational arithmetic ($\mathbb{Q}$ via `fractions.Fraction`):
$$\Delta_{K,3} := \left|\sum_{\mathrm{in}} q_i - \sum_{\mathrm{out}} q_j\right|_{\mathbb{Q}} \equiv \frac{0}{1}, \qquad \sum_{k=1}^M E_k \equiv \frac{1}{1}.$$
* Unsealed transaction window $\implies \mathrm{HOLD}$ (`RATIONAL_WINDOW_PENDING`).
* Any non-zero rational discrepancy $\Delta_{K,3} \neq 0 \implies \mathrm{KILL}$ (`RATIONAL_CONSERVATION_BREACH`).

### Chain 4 — Relativistic Light-Cone & Euclidean Phase-Cone (`Infranett / ISAC`)
Round-trip propagation delay $\Delta t$ in medium with speed $c$ bounds physical distance $d_{\mathrm{ToF}} = c\Delta t / 2$, while multi-antenna phase difference $\Delta\phi$ across baseline $d = \lambda/2$ defines directional sine $s_{\mathrm{obs}} = \Delta\phi / \pi$:
$$ds^2 = d_{\mathrm{ToF}}^2 - \left(\frac{c\Delta t_{\max}}{2}\right)^2 \le 0, \qquad |d_{\mathrm{claimed}} - d_{\mathrm{ToF}}| \le \tau_{\mathrm{spoof}}, \qquad |s_{\mathrm{obs}}| \le 1.0.$$
* $|s_{\mathrm{obs}}| > 1.0 \implies \cos\theta \in i\mathbb{R}_{>0} \implies \mathrm{KILL}$ (`UNPHYSICAL_PHASE_CONE_KILL`).
* $ds^2 > 0$ or $|d_{\mathrm{claimed}} - d_{\mathrm{ToF}}| > \tau_{\mathrm{spoof}} \implies \mathrm{HOLD}$ (`CAUSAL_LIGHTCONE_HOLD`).

### Chain 5 — Cook–Levin Ancestor Hash Chain, Monotone Fuse & Conjunctive $W^2$
Every state transition is bound to an append-only SHA-256 chain and a 64-bit monotone hardware fuse register $F_n \in \{0, 1\}^{64}$:
$$\mathcal{H}_{t+1} = \mathrm{SHA256}(\mathcal{H}_t \parallel \Phi_t \parallel \Delta_K \parallel \Omega_t), \qquad (F_n \mathbin{\&} F_{n+1}) == F_n.$$
* If $(F_n \mathbin{\&} F_{n+1}) \neq F_n$ (bit rollback attempt) or $\mathcal{H}_t \neq \mathcal{H}_{\mathrm{expected}} \implies \mathrm{KILL}$ (`COOK_LEVIN_FUSE_OR_HASH_KILL`).
* If $W_{\mathrm{human}} == \varnothing$ or `zone_occupied == True` $\implies \mathrm{HOLD}$ (`W2_ATTESTATION_OR_ZONE_HOLD`, $\frac{\mathrm{d}}{\mathrm{d}t}\mathrm{HOLD} = 0$).
