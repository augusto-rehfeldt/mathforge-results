# Refuted: Non-reflected sets with identical difference multisets must each contain at least three points absent from the other

**Verdict: FALSE.** Counterexample: `{'n': 11, 'A': [0, 1, 2, 6, 8, 11], 'B': [0, 1, 6, 7, 9, 11]} {'hypotheses': True, 'conclusion_A_equals_B_or_B_equals_reflection_of_A': False, 'A_equals_B': False, 'B_equals_reflection_of_A': False, 'reflection_of_A': [0, 3, 5, 9, 10, 11], 'A_minus_B': [2, 8], 'difference_multiplicities_A': {1: 2, 2: 2, 3: 1, 4: 1, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}, 'difference_multiplicities_B': {1: 2, 2: 2, 3: 1, 4: 1, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Two-deletion rigidity for homometric sets*

*Automated run on the seed topic "Pairs of subsets A,B of {0,…,n}, each containing 0 and n, with identical multisets of positive pairwise differences but not related by reflection, refined by cardinality and |A∩B|; look for polynomial factor-switching constructions and structural identities using P_A(x)P_A(x⁻¹)=P_B(x)P_B(x⁻¹), where P_A(x)=∑_{a∈A}xᵃ.", 2026-10-01 14:14 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1 and every pair of subsets A,B of {0,…,n} containing both 0 and n, suppose A and B have identical multisets of positive pairwise differences. If |A\B| ≤ 2, then either A=B or B={n−a : a∈A}.

## Notation

For a finite set S of integers, its multiset of positive pairwise differences contains one occurrence of t−s for each pair s,t∈S with s<t. Equality of multisets means equality of every difference's multiplicity. A\B={a∈A : a∉B}, and |S| denotes cardinality. Reflection in {0,…,n} sends a to n−a. Define P_S(x)=∑_{s∈S}x^s; equality of difference multisets is equivalent to P_A(x)P_A(x⁻¹)=P_B(x)P_B(x⁻¹) when |A|=|B|. The hypotheses imply |A|=|B|, so the overlap condition is equivalently |A∩B|≥|A|−2.

## Why it is false

`{'n': 11, 'A': [0, 1, 2, 6, 8, 11], 'B': [0, 1, 6, 7, 9, 11]} {'hypotheses': True, 'conclusion_A_equals_B_or_B_equals_reflection_of_A': False, 'A_equals_B': False, 'B_equals_reflection_of_A': False, 'reflection_of_A': [0, 3, 5, 9, 10, 11], 'A_minus_B': [2, 8], 'difference_multiplicities_A': {1: 2, 2: 2, 3: 1, 4: 1, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}, 'difference_multiplicities_B': {1: 2, 2: 2, 3: 1, 4: 1, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal assertion: for every integer n ≥ 1 and all finite sets A and B of integers whose elements lie between 0 and n inclusive, with both 0 and n in each set, if the multisets containing one occurrence of t−s for every pair s<t in each set are equal and A\B has at most two elements, then A=B or B is the image of A under a↦n−a.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'n': 11, 'A': [0, 1, 2, 6, 8, 11], 'B': [0, 1, 6, 7, 9, 11]} {'hypotheses': True, 'conclusion_A_equals_B_or_B_equals_reflection_of_A': False, 'A_equals_B': False, 'B_equals_reflection_of_A': False, 'reflection_of_A': [0, 3, 5, 9, 10, 11], 'A_minus_B': [2, 8], 'difference_multiplicities_A': {1: 2, 2: 2, 3: 1, 4: 1, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}, 'difference_multiplicities_B': {1: 2, 2: 2, 3: 1, 4: 1, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}}
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `pairs-of-subsets-a-b-of-0-n-each-containing-0-an-c3` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
