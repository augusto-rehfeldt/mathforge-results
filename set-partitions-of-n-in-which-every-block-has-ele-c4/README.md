# Refuted: Compressing two prime-sized residue classes preserves partition counts modulo prime squares, apart from an explicit paired-block correction

**Verdict: FALSE.** Counterexample: `p=5, n=14, coefficient x^2 y^0, left=2731, right=11, residues modulo 25: 6, 11`

**Models:** gpt-6.1-sol (roles under *Models* below)

*A prime-square congruence with a paired-block correction*

*Automated run on the seed topic "Set partitions of [n] in which every block has element sum divisible by three, refined by the numbers of blocks and singleton blocks; look for residue-class deletion recurrences and coefficient congruences induced by cyclically permuting labels within each residue class.", 2026-10-01 00:23 UTC. Status: `machine-refuted`.*

## Statement

For every prime p ≥ 5 and every integer n ≥ 3p−1, let A consist of the p smallest elements of [n] congruent to 1 modulo 3, let B consist of the p smallest elements congruent to 2 modulo 3, and put R = [n] \ (A ∪ B). Then, coefficientwise in the integer polynomial ring Z[x,y], F_[n](x,y) ≡ H_R,p(x,y) + p! x^p F_R(x,y) modulo p².

## Notation

[n] = {1,…,n}. For any finite set S of positive integers, F_S(x,y) is the sum of x^k y^s over all set partitions of S whose every block has element sum divisible by 3, where k is the number of blocks and s is the number of singleton blocks. The empty partition contributes 1. Introduce two distinct formal objects a and b, not belonging to R, with weights w(a)=p and w(b)=2p; set w(r)=r for r∈R. H_R,p(x,y) is the sum of x^k y^t over all partitions of R∪{a,b} whose every block has total weight divisible by 3, where k counts all blocks and t counts only singleton blocks {r} with r∈R. Thus singleton blocks containing a or b receive no factor y. The symbols x and y are commuting indeterminates, and p! = 1·2·…·p. Coefficientwise congruence means that every coefficient of the difference is divisible by p².

## Why it is false

`p=5, n=14, coefficient x^2 y^0, left=2731, right=11, residues modulo 25: 6, 11`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal assertion: for all natural numbers p and n, if p is prime, p ≥ 5, and n ≥ 3p−1, then for every pair of natural numbers k,t, p² divides the difference between two integer coefficients. The first counts partitions of {1,…,n} into k nonempty blocks with each block’s sum divisible by 3 and exactly t singleton blocks. The second counts such weighted partitions of the remaining elements together with two distinct added items of weights p and 2p, counting only ordinary singleton blocks toward t, and adds p! times the remaining-set partition count with k−p blocks and t singletons when k ≥ p. The remaining elements exclude residue-1 elements at most 3p−2 and residue-2 elements at most 3p−1.

Re-check output (tail):

```
REFUTATION CONFIRMED: p=5, n=14, coefficient x^2 y^0, left=2731, right=11, residues modulo 25: 6, 11
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `set-partitions-of-n-in-which-every-block-has-ele-c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
