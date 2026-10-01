# Refuted: Odd refined partition counts lie on one diagonal, with parity determined by subsets of centered pairs

**Verdict: FALSE.** Counterexample: `n=3, k=2, s=1, t=1, m=4; A=1, A mod 2=1; claimed side=0, claimed parity=0`

**Models:** gpt-6.1-sol (roles under *Models* below)

*A block-maximum parity diagonal for globally distinct gaps*

*Automated run on the seed topic "Set partitions of [n] in which all gaps between successive elements of blocks are globally distinct, refined by block count, singleton count, and total gap sum; look for largest-label insertion recurrences tracking used gaps and block maxima, and reflection congruences obtained by classifying reversal-fixed partitions.", 2026-10-01 15:27 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1 and all nonnegative integers k, s, t, m, let A(n,k,s,t,m) count partitions of [n] having globally distinct successive-element gaps, k blocks, s singleton blocks, total gap sum t, and sum of block maxima m. Set r=n−k. Conjecture: A(n,k,s,t,m) is congruent modulo 2 to the number of subsets I of {1,…,⌊n/2⌋} satisfying |I|=r and ∑_{i∈I}(n+1−2i)=t, provided s=2k−n and 2m=k(n+1)+t; otherwise A(n,k,s,t,m) is even.

## Notation

[n]={1,…,n}. A partition is a collection of nonempty, disjoint blocks whose union is [n]. If a block is written b₁<⋯<bℓ, its successive-element gaps are bⱼ₊₁−bⱼ for 1≤j<ℓ. Globally distinct means that no two such gaps anywhere in the partition are equal. A singleton block has one element. The total gap sum is the sum of all successive-element gaps; the sum of block maxima is ∑_B max(B), over all blocks B. The symbol ⌊x⌋ denotes the greatest integer at most x. Empty sums are zero, and no subset has negative cardinality.

## Why it is false

`n=3, k=2, s=1, t=1, m=4; A=1, A mod 2=1; claimed side=0, claimed parity=0`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following universal assertion: For every integer n ≥ 1 and natural numbers k, s, t, m, count the partitions of {1,…,n} into k nonempty blocks with s singleton blocks, globally distinct successive-element gaps, total gap sum t, and sum of block maxima m. This count modulo 2 equals the number modulo 2 of subsets I of {1,…,⌊n/2⌋} with integer cardinality n−k and sum ∑_{i∈I}(n+1−2i)=t, if s=2k−n and 2m=k(n+1)+t; otherwise it equals zero.

Re-check output (tail):

```
REFUTATION CONFIRMED: n=3, k=2, s=1, t=1, m=4; A=1, A mod 2=1; claimed side=0, claimed parity=0
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `set-partitions-of-n-in-which-all-gaps-between-su-c1` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
