# Refuted: Nonreflection homometric sets differing in only two points each occupy at most half their ambient interval

**Verdict: FALSE.** Counterexample: `n=11, k=9, A=[0, 1, 4, 5, 6, 7, 8, 9, 11], B=[0, 1, 2, 3, 4, 6, 7, 8, 11]; left side n=11, right side 2k-1=17 (11 >= 17 is false)`

**Models:** gpt-6.1-sol (roles under *Models* below)

*A density obstruction for two-point homometric trades*

*Automated run on the seed topic "Pairs of subsets A,B of {0,…,n}, each containing 0 and n, with identical multisets of positive pairwise differences but not related by reflection, refined by cardinality and |A∩B|; look for polynomial factor-switching constructions and structural identities using P_A(x)P_A(x⁻¹)=P_B(x)P_B(x⁻¹), where P_A(x)=∑_{a∈A}xᵃ.", 2026-10-01 14:13 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1 and every pair of distinct subsets A,B of {0,…,n}, suppose that 0,n belong to both sets, that |A|=|B|=k, that |A∩B|=k−2, and that for every integer t with 1≤t≤n the numbers of pairs (a,a′)∈A×A and (b,b′)∈B×B satisfying a′−a=t and b′−b=t are equal. If B≠{n−a:a∈A}, then n≥2k−1.

## Notation

The symbol |S| denotes the cardinality of a finite set S; A∩B is their intersection; k is their common cardinality. The set {n−a:a∈A} is the reflection of A in the midpoint of {0,…,n}.

## Why it is false

`n=11, k=9, A=[0, 1, 4, 5, 6, 7, 8, 9, 11], B=[0, 1, 2, 3, 4, 6, 7, 8, 11]; left side n=11, right side 2k-1=17 (11 >= 17 is false)`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following assertion: For every integer n ≥ 1, all distinct finite sets A and B of integers contained in [0,n] and both containing 0 and n, and every natural number k, if A and B each have cardinality k, their intersection has cardinality k−2 (using natural-number subtraction), and for every integer t with 1 ≤ t ≤ n they have equal numbers of ordered pairs whose second entry minus their first entry is t, then, provided B is not the image of A under a ↦ n−a, n ≥ 2k−1, with the conclusion computed in integers.

Re-check output (tail):

```
REFUTATION CONFIRMED: n=11, k=9, A=[0, 1, 4, 5, 6, 7, 8, 9, 11], B=[0, 1, 2, 3, 4, 6, 7, 8, 11]; left side n=11, right side 2k-1=17 (11 >= 17 is false)
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `pairs-of-subsets-a-b-of-0-n-each-containing-0-an-c2` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
