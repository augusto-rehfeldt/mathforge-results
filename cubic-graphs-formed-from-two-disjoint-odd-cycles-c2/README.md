# Refuted: An even permutation block realizes every parity-compatible boundary state exactly when its matching breaks positional parity

**Verdict: FALSE.** Counterexample: `{'m': 2, 'pi': (2, 1), 'unrealizable_quadruple': ((3, 4), (3, 4), (5, 6), (5, 6))} {'(i)': True, '(ii)': False}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Parity-breaking permutation blocks are universally spliceable*

*Automated run on the seed topic "Cubic graphs formed from two disjoint odd cycles of equal length by adding a perfect matching between their vertices; seek permutation-block splicing lemmas with explicit boundary states that construct six perfect matchings covering every edge exactly twice, targeting this restricted case of the open Berge–Fulkerson conjecture.", 2026-10-05 01:26 UTC. Status: `machine-refuted`.*

## Statement

For every even integer m ≥ 2 and every permutation π of {1,…,m}, form a graph with vertices u₁,…,uₘ,v₁,…,vₘ, path edges uᵢuᵢ₊₁ and vᵢvᵢ₊₁ for 1 ≤ i < m, matching edges uᵢvπ(i) for 1 ≤ i ≤ m, and four dangling edges incident respectively with u₁,v₁,uₘ,vₘ. The following are equivalent: (i) there exists i such that π(i) and i have different parity; (ii) for every ordered quadruple (A,B,C,D) of two-element subsets of {1,2,3,4,5,6} such that each color belongs to an even number of A,B,C,D, there is an assignment of a two-element color set to every edge, including every dangling edge, whose prescribed dangling-edge sets are respectively A,B,C,D and whose three incident edge sets at every vertex partition {1,2,3,4,5,6}.

## Notation

A dangling edge has exactly one endpoint in the graph and counts as an incident edge at that endpoint. A color is an element of {1,2,3,4,5,6}. Positional parity means parity of an index in {1,…,m}. An ordered quadruple is parity-compatible when, for each color, its number of occurrences among its four sets is even. A realization is the edge-set assignment specified in condition (ii). After dangling edges are joined in pairs with equal color sets, each color selects a perfect matching, and every edge belongs to exactly two of the six selected perfect matchings.

## Why it is false

`{'m': 2, 'pi': (2, 1), 'unrealizable_quadruple': ((3, 4), (3, 4), (5, 6), (5, 6))} {'(i)': True, '(ii)': False}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal assertion: for every natural number m ≥ 2 that is even and every permutation π of the zero-based positions Fin m, there is a position i whose parity differs from that of π(i) if and only if every ordered quadruple of two-element subsets of six colors, with each color occurring an even number of times, admits color-set labels on the two paths and permutation matching. The boundary labels occur in order at the first upper, first lower, last upper, and last lower vertices, and at each vertex the three incident labels partition the six colors.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'m': 2, 'pi': (2, 1), 'unrealizable_quadruple': ((3, 4), (3, 4), (5, 6), (5, 6))} {'(i)': True, '(ii)': False}
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `cubic-graphs-formed-from-two-disjoint-odd-cycles-c2` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
