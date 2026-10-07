# The Non-Expansive Gate

## Computational Complexity as the Boundary Condition of Spacetime and Perception

> **Abstract:** The persistent divide between computational complexity theory, fundamental physics, and cognitive neuroscience stems from an unexamined assumption: that complexity classes describe the difficulty of calculation rather than the physical boundaries of spacetime itself. Through the Cook-Levin reduction, nondeterministic polynomial verification is mapped into a frozen, two-dimensional spatial tableau where time is eliminated in favor of simultaneous geometric relation. Physical reality, however, operates strictly within bounded, deterministic limits where state reduction incurs an unavoidable causal and thermodynamic toll. By analyzing continuous attractor networks on toroidal manifolds ($\mathbb{T}^2$) and their metric projection into motor action, we demonstrate that coherent reality is not generated through additive synthesis, but admitted through non-expansive restriction. Reality is the causal residue of what survives the gate.

---

## 1. The Spatialization of Computation: Cook-Levin and $NP$

The fundamental property of the complexity class $NP$ is often framed combinatorially: problems whose solutions are verifiable in polynomial time by a deterministic Turing machine. The structural significance of this definition was laid bare by the Cook-Levin theorem. By reducing any arbitrary polynomial-time verification problem to the satisfiability of a propositional boolean formula, the theorem performs a coordinate transformation between temporal execution and static spatial topology.

In the Cook-Levin construction, the complete temporal progression of a computational machine—its tape cells, head positions, and internal state transitions over $T$ steps—is flattened into a two-dimensional grid of size $O(T) \times O(T)$. Every temporal step becomes a spatial row. Every causal consequence is reduced to local spatial adjacency constraints:

$$\text{Time} \longrightarrow \text{Space}$$

In the unconstrained phase space of $NP$, time is already space. All state transitions, branches, and verification trajectories exist simultaneously, devoid of temporal friction. No energy is dissipated, no entropy is produced, and no irreversible state collapse is enforced during candidate superposition. It is a frozen geometric expanse where potential configurations coexist without mutual exclusion.

---

## 2. The Physics of Restriction: $P$ as Causal Consequence

Classical physical reality does not inhabit this unconstrained spatial tableau. The physical universe operates strictly within the domain of bounded, deterministic polynomial evolution ($P$), where time is not a spatial dimension that can be traversed arbitrarily, but the thermodynamic and causal cost of state reduction.

1. **The Minkowski Bound:** The speed of light $c$ and the invariant interval $ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2$ are not facilitators of motion, but strict geometric bounds that prevent instantaneous, non-local collapse across the spatial field.
2. **The Thermodynamic Bound:** Under Landauer's principle, the erasure or irreversible reduction of information dissipation requires an unavoidable entropic payment:
   $$\Delta Q \ge k_B T \ln 2$$
3. **The Causal Bound:** Physical time is the metric friction generated when an unbounded, high-dimensional phase space is forced through a finite, deterministic gate. 

$P$ is therefore not a diminished subset of an idealized $NP$ continuum. It is the non-negotiable boundary condition that prevents physical reality from dissolving into instantaneous, white-noise saturation. Without the metric constraint of $P$, the universe would collapse into an undifferentiated superposition where all possible configurations occur simultaneously without consequence.

---

## 3. Neural Realization: The Toroidal Attractor and Metric Projection

This exact architectural division is empirically observed in the biological neural substrates of spatial representation and navigation.

In the medial entorhinal cortex, continuous attractor networks (CANs) maintain a stable representation of the organism's coordinate space. Modern topological data analysis confirms that the collective firing patterns of grid cell populations lie on a two-dimensional toroidal manifold ($\mathbb{T}^2 = S^1 \times S^1$). 

Left unconstrained, this recurrent network is fundamentally **fail-open**. It generates an open-ended, combinatorial phase space capable of sustaining multiple concurrent trajectories and phase ambiguities:

$$\mathcal{M}_{\text{attractor}} \cong \mathbb{T}^2$$

The organism does not achieve physical orientation or purposeful action by generating an internal map from scratch. Instead, it enforces a metric projection $\Pi_A$ from the unconstrained toroidal phase space onto the restricted manifold of physical motor action:

$$\Pi_A : \mathbb{T}^2 \longrightarrow \mathcal{A} \subset \mathbb{R}^n$$

Crucially, this realization operator is **non-expansive**:

$$\|\Pi_A(x) - \Pi_A(y)\| \le \|x - y\| \quad \forall x, y \in \mathbb{T}^2$$

The distance between projected action states cannot exceed the metric distance between the unprojected coordinates. Coherent spatial orientation and motor action exist exclusively because of this non-expansive contraction. 

```text
       UNBOUNDED PHASE SPACE (NP)
      [ Toroidal Manifold T² ]
                 │
                 │   Fail-open candidate field
                 ▼
       ┌──────────────────┐
       │   METRIC GATE    │   Π_A Non-expansive projection
       │   (||Π(x)-Π(y)|| │   ||x - y||)
       │    <= ||x - y||) │
       └────────┬─────────┘
                 │
                 │   Irreversible collapse
                 ▼
       PHYSICAL CONSEQUENCE (P)
      [ Singular Worldline / Action ]
```

---

## 4. The Friston Inversion: Subtractive Realization

The standard framework of predictive processing and the Free Energy Principle (FEP) routinely models perception as an additive simulation: an internal generative engine synthesizing top-down prior beliefs to reconcile sensory error.

The mathematics of the non-expansive gate invert this premise:

* **Additive Model (Conventional):** The brain generates reality by projecting structured hypotheses onto an ambiguous sensory vacuum.
* **Subtractive Model (The Inversion):** The sensory and recurrent neural substrates already harbor an unconstrained, over-complete combinatorial space ($NP$). Perception and action are formed by **subtractive filtration**—the systematic excision of states that violate physical admissibility.

Under this inversion, phenomena such as hallucinations or cognitive decompensation are not caused by the excessive generation of false priors. They represent a structural failure or metabolic fatigue of the gating filter $\Pi_A$. When the non-expansive gate loses confinement, the raw, unpruned geometry of the underlying continuous attractor network spills directly into consciousness. Hallucination is not an overproduction of fiction; it is a loss of restriction.

---

## 5. Epistemic Architecture: The Invariant of Restriction

The synthesis of computational complexity, spacetime geometry, and biological realization converges upon a singular structural law:

> **Restriction is the invisible architecture of clarity.**

Beneath any coherent, deterministic reality operates an unyielding matrix of constraints. This boundary does not merely limit what can occur; it establishes the precise pressure under which structure is forged:

```text
THEORY != DEMONSTRATOR
CANDIDATE != CONSEQUENCE
NP (Tableau) != P (Trajectory)
SUPERPOSITION != REALIZATION
```

Reality does not emerge by adding mechanisms onto a void. Structure arises only when unbounded geometry meets an unyielding boundary, and reality is simply the residue of what survives the restriction.

---

## Citation

```bibtex
@article{torjusen2026nonexpansivegate,
  author    = {Torjusen, Marius Egerhei},
  title     = {The Non-Expansive Gate: Computational Complexity as the Boundary Condition of Spacetime and Perception},
  journal   = {Epistemic Architectures Working Papers},
  year      = {2026},
  url       = {https://github.com/sololys/epistemic-architectures}
}
```
