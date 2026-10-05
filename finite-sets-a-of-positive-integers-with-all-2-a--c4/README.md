# Refuted: Every two-element extension of a superincreasing core can be compressed using one of its first two signed-sum holes

**Verdict: FALSE.** Counterexample: `R=(1, 6), x=4, y=8, h1=2, h2=3; hypotheses=True; given four subset-sum translates pairwise disjoint=True; exists positive u<v<=y with u in {h1,h2} and four subset-sum translates pairwise disjoint=False`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Two-hole compression for superincreasing cores*

*Automated run on the seed topic "Finite sets A of positive integers with all 2^{|A|} subset sums distinct; seek block-replacement lemmas expressed through disjoint signed-sum sets that preserve this property while reducing max A, targeting the open Erdős distinct subset sums conjecture that max A≥c·2^{|A|} for some absolute c>0.", 2026-10-05 02:39 UTC. Status: `machine-refuted`.*

## Statement

For every integer m≥1 and every sequence of positive integers r₁<⋯<rₘ satisfying rᵢ>∑_{j<i}rⱼ for each 2≤i≤m, put R={r₁,…,rₘ}. Let h₁<h₂ be the two smallest positive integers outside D(R). For every pair of positive integers x<y such that the four sets D(R), x+D(R), y+D(R), and x+y+D(R) are pairwise disjoint, there exist positive integers u<v≤y with u∈{h₁,h₂} such that D(R), u+D(R), v+D(R), and u+v+D(R) are pairwise disjoint.

## Notation

D(R)={∑_{r∈R}εᵣr : εᵣ∈{−1,0,1} for every r∈R} is the signed-sum set. For an integer t, t+D(R)={t+d:d∈D(R)}. In the statement, replace every occurrence of D(R) in the four-set disjointness conditions by S(R)={∑_{r∈T}r:T⊆R}; equivalently, those conditions mean that x, y, y−x, x+y all lie outside D(R), and likewise for u, v, v−u, u+v. The intended conjecture uses this equivalent signed-sum formulation.

## Why it is false

`R=(1, 6), x=4, y=8, h1=2, h2=3; hypotheses=True; given four subset-sum translates pairwise disjoint=True; exists positive u<v<=y with u in {h1,h2} and four subset-sum translates pairwise disjoint=False`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal claim: For every natural number m ≥ 1 and every strictly increasing sequence r indexed by Fin m of positive integers, with each entry after the first greater than the sum of all earlier entries, let D be the set of sums obtained by assigning each entry a coefficient −1, 0, or 1. For any integers h₁ and h₂ with 0 < h₁ < h₂ that are outside D, such that every positive integer below h₁ and every integer strictly between h₁ and h₂ belongs to D, and any integers 0 < x < y for which x, y, y−x, and x+y are outside D, there exist integers 0 < u < v ≤ y with u equal to h₁ or h₂ and with u, v, v−u, and u+v outside D.

Re-check output (tail):

```
REFUTATION CONFIRMED: R=(1, 6), x=4, y=8, h1=2, h2=3; hypotheses=True; given four subset-sum translates pairwise disjoint=True; exists positive u<v<=y with u in {h1,h2} and four subset-sum translates pairwise disjoint=False
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `finite-sets-a-of-positive-integers-with-all-2-a--c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
