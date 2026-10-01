# Refuted: Two opposite correlation defects force even length and tightly constrain coefficientwise Hamming distance

**Verdict: FALSE.** Counterexample: `{'witness': {'n': 5, 'A': (1, -1, 1, 1, 1), 'B': (1, -1, -1, 1, 1), 'd': 2, 'e': 4, 'c': -2, 'h': 1}, 'identity_left_side': {-4: 2, -3: 0, -2: -2, -1: 0, 0: 10, 1: 0, 2: -2, 3: 0, 4: 2}, 'identity_right_side': {-4: 2, -3: 0, -2: -2, -1: 0, 0: 10, 1: 0, 2: -2, 3: 0, 4: 2}, 'conclusion_actual_side': {'n_even': False, 'c_even': True, 'h': 1, '2*h': 2, 'd+e': 6}, 'conclusion_claimed_side': {'n_even': True, 'c_even': True, 'd+e': 5, '2*h_in': (1, 5, 9)}}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Hamming rigidity from two opposite correlation defects*

*Automated run on the seed topic "Pairs of polynomials A(x),B(x) of degree n−1 with all coefficients in {−1,1} satisfying A(x)A(x⁻¹)+B(x)B(x⁻¹)=2n+c(xᵈ+x⁻ᵈ−xᵉ−x⁻ᵉ) for integers c≠0 and 1≤d<e<n, refined by d, e, c, and coefficientwise Hamming distance; look for even–odd coefficient splitting identities and extension recurrences tracking cancellation of correlation coefficients.", 2026-10-01 19:07 UTC. Status: `machine-refuted`.*

## Statement

For every integer n≥3, every pair of integers 1≤d<e<n, every nonzero integer c, and every pair A(x)=∑_{i=0}^{n−1}a_i x^i and B(x)=∑_{i=0}^{n−1}b_i x^i with a_i,b_i∈{−1,1}, suppose the Laurent-polynomial identity A(x)A(x⁻¹)+B(x)B(x⁻¹)=2n+c(x^d+x⁻ᵈ−x^e−x⁻ᵉ) holds. Then n and c are even. Moreover, writing h for the coefficientwise Hamming distance, if c is divisible by 4 then h=n/2; otherwise d+e=n and h belongs to {n/2−2,n/2,n/2+2}.

## Notation

The variable x is a formal indeterminate. A Laurent polynomial permits integer exponents, including negative ones. The integers a_i and b_i are the coefficients at index i. The coefficientwise Hamming distance is h=|{i∈{0,…,n−1}:a_i≠b_i}|. Divisibility and congruences concern ordinary integers.

## Why it is false

`{'witness': {'n': 5, 'A': (1, -1, 1, 1, 1), 'B': (1, -1, -1, 1, 1), 'd': 2, 'e': 4, 'c': -2, 'h': 1}, 'identity_left_side': {-4: 2, -3: 0, -2: -2, -1: 0, 0: 10, 1: 0, 2: -2, 3: 0, 4: 2}, 'identity_right_side': {-4: 2, -3: 0, -2: -2, -1: 0, 0: 10, 1: 0, 2: -2, 3: 0, 4: 2}, 'conclusion_actual_side': {'n_even': False, 'c_even': True, 'h': 1, '2*h': 2, 'd+e': 6}, 'conclusion_claimed_side': {'n_even': True, 'c_even': True, 'd+e': 5, '2*h_in': (1, 5, 9)}}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following universal statement: For all natural numbers n,d,e, integers c, and integer-valued sequences a,b, if n≥3, 1≤d<e<n, c≠0, all entries of a and b below n are ±1, and at every integer exponent k the sum of their autocorrelation coefficients equals the coefficient of 2n+c(x^d+x^(-d)−x^e−x^(-e)), then n and c are even. Furthermore, if 4 divides c, twice the number of differing entries below n equals n; otherwise d+e=n and twice that number equals n−4, n, or n+4.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'witness': {'n': 5, 'A': (1, -1, 1, 1, 1), 'B': (1, -1, -1, 1, 1), 'd': 2, 'e': 4, 'c': -2, 'h': 1}, 'identity_left_side': {-4: 2, -3: 0, -2: -2, -1: 0, 0: 10, 1: 0, 2: -2, 3: 0, 4: 2}, 'identity_right_side': {-4: 2, -3: 0, -2: -2, -1: 0, 0: 10, 1: 0, 2: -2, 3: 0, 4: 2}, 'conclusion_actual_side': {'n_even': False, 'c_even': True, 'h': 1, '2*h': 2, 'd+e': 6}, 'conclusion_claimed_side': {'n_even': True, 'c_even': True, 'd+e': 5, '2*h_in': (1, 5, 9)}}
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `pairs-of-polynomials-a-x-b-x-of-degree-n-1-with--c1` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
