# Refuted: Every distinct odd cube-free congruence family leaves an uncovered CRT box with two exclusions per prime

**Verdict: FALSE.** Counterexample: `{'L': 315, 'm': (3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315), 'a': (2, 2, 2, 7, 10, 19, 18, 9, 24, 36, 255), 'claimed_box_exists': True, 'brute_force_box_exists': False} claimed_side = True literal_brute_force_side = False`

**Models:** gpt-6.1-sol (roles under *Models* below)

*A CRT first-digit box conjecture for cube-free odd moduli*

*Automated run on the seed topic "Finite covering systems {a_i mod m_i} with pairwise distinct odd moduli m_i>1 and no prime cube dividing any m_i; seek Chinese-remainder fiber inequalities and residue-class replacement lemmas that force an uncovered residue modulo lcm(m_i), targeting this restricted case of the open odd covering systems conjecture.", 2026-10-06 21:08 UTC. Status: `machine-refuted`.*

## Statement

For every integer k ≥ 1, every collection of pairwise distinct odd integers m_1,...,m_k > 1 such that no prime cube divides any m_i, and every choice of integers a_1,...,a_k, put L = lcm(m_1,...,m_k). For each prime p dividing L, let e_p be its exponent in L. There exist sets B_p ⊆ Z/pZ with |B_p| ≥ p−2 and functions f_p: B_p → Z/p^{e_p}Z satisfying f_p(b) ≡ b modulo p, such that every residue x ∈ Z/LZ whose coordinate modulo p^{e_p} belongs to f_p(B_p) for every prime p dividing L satisfies x ≠ a_i modulo m_i for every i ∈ {1,...,k}.

## Notation

Z/nZ denotes the residues modulo the positive integer n. The least common multiple L has factorization L = ∏_{p|L} p^{e_p}, with e_p ∈ {1,2}. Chinese remainder coordinates identify Z/LZ with ∏_{p|L} Z/p^{e_p}Z. The image f_p(B_p) contains one selected lift of each first-digit residue in B_p. Their Cartesian product is the asserted uncovered CRT box.

## Why it is false

`{'L': 315, 'm': (3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315), 'a': (2, 2, 2, 7, 10, 19, 18, 9, 24, 36, 255), 'claimed_box_exists': True, 'brute_force_box_exists': False} claimed_side = True literal_brute_force_side = False`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following assertion: For every natural k ≥ 1, every injective family m of k natural numbers, and every family a of k integers, suppose each m_i is odd, greater than 1, and divisible by no prime cube. For every positive natural L divisible by all m_i and dividing every common multiple of them, and every assignment e to natural numbers p ≤ L such that, for prime divisors p of L, p^{e_p} divides L but p^{e_p+1} does not, there exist finite sets B_p of residues modulo p and functions f_p from residues modulo p to residues modulo p^{e_p}. For each prime divisor p of L, B_p has at least p−2 elements and f_p(b) reduces to b modulo p for every b in B_p. Every residue x modulo L whose remainder modulo each p^{e_p} is f_p(b) for some b in B_p avoids a_i modulo m_i for every i.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'L': 315, 'm': (3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315), 'a': (2, 2, 2, 7, 10, 19, 18, 9, 24, 36, 255), 'claimed_box_exists': True, 'brute_force_box_exists': False} claimed_side = True literal_brute_force_side = False
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `finite-covering-systems-a-i-mod-m-i-with-pairwis-c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
