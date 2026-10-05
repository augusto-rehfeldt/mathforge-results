# Refuted: Every nonoptimal distinct-subset-sum set admits a maximum-reducing replacement of at most half its elements plus one

**Verdict: FALSE.** Counterexample: `{'n': 4, 'A': (1, 2, 4, 8), 'C': (3, 5, 6, 7)} hypotheses = True conclusion = False`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Half-block escape from nonoptimal distinct-subset-sum sets*

*Automated run on the seed topic "Finite sets A of positive integers with all 2^{|A|} subset sums distinct; seek block-replacement lemmas expressed through disjoint signed-sum sets that preserve this property while reducing max A, targeting the open Erdős distinct subset sums conjecture that max A≥c·2^{|A|} for some absolute c>0.", 2026-10-05 02:37 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 2 and every set A of n positive integers having distinct subset sums, suppose there exists a set C of n positive integers having distinct subset sums with max C < max A. Then there exist a subset R of A and a set T of positive integers such that 1 ≤ |R| ≤ floor(n/2)+1, |T| = |R|, T is disjoint from A\R, T has distinct subset sums, D(T) ∩ D(A\R) = {0}, and max((A\R) ∪ T) < max A.

## Notation

A finite set X has distinct subset sums if the map U ↦ sum_{x∈U} x is injective on all subsets U of X, including the empty subset. Define D(X) = {sum_{x∈X} ε_x x : ε_x ∈ {-1,0,1} for every x∈X}, with D(∅) = {0}. The notation |X| denotes cardinality, max X denotes the largest element of a nonempty finite set, X\Y denotes set difference, and floor(t) denotes the greatest integer at most t. The sets A and C are the original and comparison sets; R is the removed block and T its replacement. The signed-sum intersection condition, together with distinct subset sums within both retained and replacement blocks, guarantees distinct subset sums for their union.

## Why it is false

`{'n': 4, 'A': (1, 2, 4, 8), 'C': (3, 5, 6, 7)} hypotheses = True conclusion = False`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following claim: For every natural number n ≥ 2 and every finite set A of natural numbers with cardinality n, all elements positive, and distinct subset sums, if there exists a finite set C of n positive natural numbers with distinct subset sums and maximum less than that of A, then there exist finite sets R and T such that R ⊆ A, T consists of positive numbers, 1 ≤ |R| ≤ n / 2 + 1, |T| = |R|, T is disjoint from A \ R, the maximum of (A \ R) ∪ T is less than that of A, T has distinct subset sums, and the intersection of the signed-sum sets of T and A \ R is exactly {0}. Here division is natural-number division, and signed sums are differences of two subset sums.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'n': 4, 'A': (1, 2, 4, 8), 'C': (3, 5, 6, 7)} hypotheses = True conclusion = False
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `finite-sets-a-of-positive-integers-with-all-2-a--c3` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
