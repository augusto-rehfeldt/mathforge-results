# Refuted: Exactly two equal-sum relations in a gapless sequence must have supports intersecting in exactly two indices

**Verdict: FALSE.** Counterexample: `witness = (1, 2, 3, 6); |R1 intersection R2| = 3; claimed right side = 2`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Gapless subset sums force minimal overlap*

*Automated run on the seed topic "Strictly increasing sequences of positive integers having exactly two unordered pairs of disjoint nonempty index subsets with equal sums, refined by total sum, length, and intersection size of the two relation supports; look for largest-term deletion recurrences and structural identities distinguishing overlapping from disjoint relation supports.", 2026-10-01 22:18 UTC. Status: `machine-refuted`.*

## Statement

For every integer n >= 1 and every strictly increasing sequence of positive integers a_1 < ... < a_n, suppose there are exactly two unordered pairs {I,J} of disjoint nonempty subsets of {1,...,n} satisfying sum_{i in I} a_i = sum_{j in J} a_j. Denote these pairs by {I_1,J_1} and {I_2,J_2}, and put R_1 = I_1 union J_1 and R_2 = I_2 union J_2. If every integer from 0 through S = sum_{i=1}^n a_i is the sum of some subset of the sequence, then |R_1 intersection R_2| = 2.

## Notation

A subset sum uses each index at most once; the empty subset has sum zero. An unordered pair {I,J} is counted once, without distinguishing {I,J} from {J,I}. The support of such a pair is I union J. The notation |X| denotes the number of elements of a finite set X.

## Why it is false

`witness = (1, 2, 3, 6); |R1 intersection R2| = 3; claimed right side = 2`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal assertion: for every natural number n ≥ 1 and every strictly increasing function a : Fin n → ℕ with positive values, and for any two distinct ordered pairs (I₁,J₁) and (I₂,J₂) of disjoint nonempty index subsets with equal sums and increasing binary subset codes, if these are exactly all pairs satisfying those conditions and every natural number from zero through the total sum is a subset sum, then the intersection of their supports I₁ ∪ J₁ and I₂ ∪ J₂ has cardinality two.

Re-check output (tail):

```
REFUTATION CONFIRMED: witness = (1, 2, 3, 6); |R1 intersection R2| = 3; claimed right side = 2
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `strictly-increasing-sequences-of-positive-intege-c1` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
