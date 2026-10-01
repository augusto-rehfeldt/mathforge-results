# Refuted: Every qualifying spanning tree of the three-row grid has at least n+1 leaves and six-cycle omissions combined

**Verdict: FALSE.** Counterexample: `{'n': 2, 'tree_edges': [((1, 1), (2, 1)), ((1, 1), (1, 2)), ((2, 1), (2, 2)), ((2, 2), (3, 2)), ((3, 1), (3, 2))]}; L=2, S=0; L(T)+S(T)=2; n+1=3`

**Models:** gpt-6.1-sol (roles under *Models* below)

*A leaf–six-cycle compensation bound*

*Automated run on the seed topic "Spanning trees of the 3×n rectangular grid in which adding any omitted grid edge creates a cycle of length four or six, refined by leaf count and the number of omitted edges creating six-cycles; look for column-gluing recurrences tracking boundary connectivity, tree distances, and unresolved cycle-length constraints.", 2026-10-01 22:34 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1 and every spanning tree T of G_n such that adding any edge of G_n absent from T creates a cycle of length either four or six, the inequality L(T) + S(T) ≥ n + 1 holds.

## Notation

G_n is the simple graph with vertex set {1,2,3} × {1,…,n}, in which distinct vertices (r,c) and (r′,c′) are adjacent exactly when |r−r′| + |c−c′| = 1. A spanning tree is a connected, acyclic subgraph containing every vertex. L(T) is the number of vertices having degree one in T. S(T) is the number of edges e in E(G_n) \ E(T) for which the unique cycle in T together with e has six edges. E(H) denotes the edge set of a graph H.

## Why it is false

`{'n': 2, 'tree_edges': [((1, 1), (2, 1)), ((1, 1), (1, 2)), ((2, 1), (2, 2)), ((2, 2), (3, 2)), ((3, 1), (3, 2))]}; L=2, S=0; L(T)+S(T)=2; n+1=3`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal statement: for every natural number n ≥ 1 and every set T of grid edges on Fin 3 × Fin n, if T connects all vertices and has 3n−1 edges, and every grid edge absent from T has endpoints at tree distance 3 or 5, then the number of degree-one vertices of T plus the number of absent grid edges whose endpoints have tree distance 5 is at least n+1.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'n': 2, 'tree_edges': [((1, 1), (2, 1)), ((1, 1), (1, 2)), ((2, 1), (2, 2)), ((2, 2), (3, 2)), ((3, 1), (3, 2))]}; L=2, S=0; L(T)+S(T)=2; n+1=3
```

## Models

- Proposed the claim: gpt-6.1-sol
- Counterexample search: gpt-6.1-sol
- Independent re-check of the witness: gpt-6.1-sol
- Lean formalization: gpt-6.1-sol
- Faithfulness judge: gpt-6.1-sol

## How this was produced

Fully automated: every statement, script, proof and formalization here was
written by language models in a pipeline (mathforge), with no human in the loop.
Read it as a machine-checked artifact, not as a reviewed paper.

Only two outcomes are published, both resting on Lean 4 + Mathlib rather than on
a model's opinion of its own work:

- **machine-refuted** — an adversarial script found a witness, a separate
  model call's script re-checked it against the statement from scratch, and Lean elaborated a
  sorry-free proof of the negation of the claim.
- **machine-verified** — Lean elaborated the proof with no `sorry`.

In both cases a separate model call back-translated the Lean statement and judged it
faithful to the informal one. Lean certifies the Lean statement; the
back-translation is a screening filter, not an oracle, so read the attached
`.lean` file against the statement above.

Novelty screening is a bounded automated search over arXiv, Crossref and
OpenAlex with model-written queries. It is blind to books, to journals outside
those indexes, and to anything phrased differently: a result here may well be a
rediscovery. Corrections welcome as GitHub issues.

## Palomar

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `spanning-trees-of-the-3-n-rectangular-grid-in-wh-c3` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
