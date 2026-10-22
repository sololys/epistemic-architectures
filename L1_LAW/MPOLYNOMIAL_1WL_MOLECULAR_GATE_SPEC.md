# L1_LAW // M-Polynomial & 1-Weisfeiler-Lehman (1-WL) Molecular Consequence Gate ($\Pi_K$)

$$\boxed{\text{GENERATION} \neq \text{AUTHORIZATION} \neq \text{WITNESSED CONSEQUENCE}}$$

* **Surface:** `L1_LAW/MPOLYNOMIAL_1WL_MOLECULAR_GATE_SPEC.md`
* **Executable Gate Verifier:** [`L2_GATE/verify_mpolynomial_1wl_molecular_gate.py`](../L2_GATE/verify_mpolynomial_1wl_molecular_gate.py) (`6/6 PASS`)
* **Epistemic Boundary:** `INSPIRED_BY != IMPLEMENTS != PROVES` · `PHYSICAL_AUTHORITY = NONE` (`L1` deterministic software only)

---

## 1. Exact Edge-Degree Partitioning & Generating M-Polynomial

Let $G = (V, E)$ be a molecular graph with vertex degrees $d_v = \deg(v)$. Decompose the edge set $E(G)$ into exact degree-ordered partitions:

$$E_{\{i,j\}} = \{uv \in E(G) \mid \{d_u, d_v\} = \{i, j\}\}, \qquad m_{ij}(G) = |E_{\{i,j\}}| \quad (1 \le i \le j).$$

The **M-polynomial** (Deutsch & Klavžar, 2015) is the two-variable generating polynomial:

$$M(G; x, y) = \sum_{i \le j} m_{ij}(G)\, x^i y^j.$$

### Closed-Form Differential & Integral Operators at $x = y = 1$

Define the linear operators on $f(x, y) = M(G; x, y)$:

$$D_x = x\frac{\partial}{\partial x}, \quad D_y = y\frac{\partial}{\partial y}, \quad S_x f = \int_0^x \frac{f(t, y)}{t}\,\mathrm{d}t, \quad S_y f = \int_0^y \frac{f(x, t)}{t}\,\mathrm{d}t, \quad J f(x, y) = f(x, x).$$

Evaluating at $x = y = 1$ yields the classical degree-based topological descriptors as exact operator projections:

| Topological Invariant | Operator Projection on $M(G; x, y)$ | Closed Sum over $m_{ij}(G)$ |
| :--- | :--- | :--- |
| **First Zagreb Index $M_1(G)$** | $(D_x + D_y) M(G; x, y)\big|_{x=y=1}$ | $\sum_{i \le j} m_{ij}(i + j) \equiv \sum_{v \in V} d_v^2$ |
| **Second Zagreb Index $M_2(G)$** | $(D_x D_y) M(G; x, y)\big|_{x=y=1}$ | $\sum_{i \le j} m_{ij}(i \cdot j)$ |
| **Randić Connectivity $R(G)$** | $(D_x^{-1/2} D_y^{-1/2}) M(G; x, y)\big|_{x=y=1}$ | $\sum_{i \le j} \frac{m_{ij}}{\sqrt{i \cdot j}}$ |
| **Harmonic Index $H(G)$** | $2 S_x J M(G; x, y)\big|_{x=1}$ | $\sum_{i \le j} \frac{2 m_{ij}}{i + j}$ |
| **Symmetric Division $SDD(G)$** | $(D_x S_y + S_x D_y) M(G; x, y)\big|_{x=y=1}$ | $\sum_{i \le j} m_{ij}\frac{i^2 + j^2}{i \cdot j}$ |

---

## 2. Canonical Bio-Inorganic Cluster: `[Fe7MoS9C]` FeMo-Cofactor ($|V|=18, |E|=30$)

For the 18-atom bio-inorganic `[Fe7MoS9C]` core of nitrogenase containing the central hexacoordinate interstitial carbide ($\mu_6\text{-C}^{4-}$):
- $3$ belt sulfides ($\mu_2\text{-S}$, $d = 2$), $6$ cubane sulfides ($\mu_3\text{-S}$, $d = 3$), $2$ terminal metals ($\text{Fe}_1, \text{Mo}$, $d = 3$), $6$ trigonal-prismatic belt irons ($\text{Fe}_{2..7}$, $d = 4$), and $1$ central interstitial carbide ($\mu_6\text{-C}$, $d = 6$).
- The $30$ coordination bonds partition into $m_{2,4} = 6$, $m_{3,3} = 6$, $m_{3,4} = 12$, and $m_{4,6} = 6$:

$$M(\text{FeMo-co}; x, y) = 6x^2y^4 + 6x^3y^3 + 12x^3y^4 + 6x^4y^6, \qquad M_1 = 216.0, \quad M_2 = 390.0.$$

---

## 3. Why Soft GNN Feature Concatenation Cannot Replace the Consequence Gate $\Pi_K$

Standard Message Passing Neural Networks (MPNNs) are bounded in expressive power by the **1-Weisfeiler-Lehman (1-WL)** color refinement test. Concatenating M-polynomial scalars into the initial node embedding vector

$$h_v^{(0)} \gets \big[\, x_v \;\|\; M_1(G) \;\|\; M_2(G) \;\|\; R(G) \;\|\; H(G) \,\big]$$

does **not** establish a fail-closed consequence gate, for three mathematical reasons verified in [`L2_GATE/verify_mpolynomial_1wl_molecular_gate.py`](../L2_GATE/verify_mpolynomial_1wl_molecular_gate.py):

1. **Co-Polynomial 1-WL Collisions (Decalin vs. Bicyclopentyl, $\text{C}_{10}\text{H}_{18}$):**  
   Both bicyclic isomers have identical 1-WL color refinement signatures **and** identical first-order edge partitions:
   $$M(\text{Decalin}; x, y) = M(\text{Bicyclopentyl}; x, y) = 6x^2y^2 + 4x^2y^3 + x^3y^3.$$
   Hence $M_1 = 46$, $M_2 = 57$, $R = 4.6330$, $H = 4.9333$, and $SDD = 20.6667$ are $100\%$ identical. Without an explicit cycle-motif witness ($2 \times C_6$ vs. $2 \times C_5$), $\Pi_K$ forces `HOLD` ($0.00\text{ V DC}$).
2. **Disconnected Ghost Graphs ($\text{Benzene } C_6$ vs. $2 \times C_3$):**  
   Both graphs are 2-regular on 6 vertices with $M(G; x, y) = 6x^2y^2$ and identical 1-WL multisets. $\Pi_K$ severs $2 \times C_3$ to `KILL` ($0.00\text{ V DC}$) via the Betti connectivity invariant $\beta_0(G) = 2 \neq 1$.
3. **Chemical Valence Breach (Pentavalent "Texas Carbon" vs. Interstitial $\mu_6\text{-C}$):**  
   A soft GNN matrix multiplication $W^{(1)} h_v^{(0)}$ maps an illegal pentavalent organic carbon ($d_{\text{C}} = 5$) to a finite floating-point prediction (`soft_gnn_would_pass = True`). In contrast, $\Pi_K$ enforces strict coordination rules: organic carbon with $d_{\text{C}} > 4$ triggers immediate `KILL` ($0.00\text{ V DC}$), whereas bio-inorganic $\mu_6\text{-C}$ is admitted to `OPEN` ($5.00\text{ V DC}$) if and only if all $6$ neighbors are transition metals ($\text{Fe}/\text{Mo}$).
