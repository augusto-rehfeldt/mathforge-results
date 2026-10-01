# Refuted: A six-cycle using three nonresonant displacement lengths fits exactly when its available span reaches largest plus middle minus smallest

**Verdict: FALSE.** Counterexample: `witness=(7, 1, 3, 5, (1, 2, 7, 4, 3, 6)) exists=True (n >= b+c-a+1)=False`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Minimum span of a three-length displacement hexagon*

*Automated run on the seed topic "Permutations π of [n] in which each occurring nonzero absolute displacement |π(i)−i| occurs exactly twice, once with each sign, refined by fixed-point count, cycle count, and total positive displacement; look for cut-and-glue identities tracking unmatched displacement lengths across a cut and structural criteria forcing all nontrivial cycles to be transpositions.", 2026-10-01 19:16 UTC. Status: `machine-refuted`.*

## Statement

For every choice of integers 1 ≤ a < b < c with c ≠ a+b, and every integer n ≥ 6, there exists a permutation π of {1,…,n} having exactly one cycle of length six and n−6 fixed points, whose nonzero signed displacements consist exactly of +a, −a, +b, −b, +c, −c, if and only if n ≥ b+c−a+1.

## Notation

A permutation is a bijection π:{1,…,n}→{1,…,n}. Its signed displacement at i is π(i)−i. A fixed point satisfies π(i)=i. A cycle of length six consists of six distinct integers v₁,…,v₆ with π(vⱼ)=vⱼ₊₁ for 1≤j<6 and π(v₆)=v₁. The integers a,b,c are the three distinct positive displacement lengths. Such a permutation has n−5 cycles in total and total positive displacement a+b+c.

## Why it is false

`witness=(7, 1, 3, 5, (1, 2, 7, 4, 3, 6)) exists=True (n >= b+c-a+1)=False`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal statement: for all integers a, b, c, n satisfying 1 ≤ a < b < c, c ≠ a+b, and n ≥ 6, there exists a permutation of the indices 0 through n−1 with six distinct vertices forming one six-cycle, every other vertex fixed, exactly n−6 fixed points, and nonzero displacement multiset {a, −a, b, −b, c, −c}, if and only if n ≥ b+c−a+1.

Re-check output (tail):

```
REFUTATION CONFIRMED: witness=(7, 1, 3, 5, (1, 2, 7, 4, 3, 6)) exists=True (n >= b+c-a+1)=False
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `permutations-of-n-in-which-each-occurring-nonzer-c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
