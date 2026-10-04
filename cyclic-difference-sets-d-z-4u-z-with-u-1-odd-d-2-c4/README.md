# Refuted: Squarefree parameters admit no bounded odd integral perfect sequence of the length forced by a Hadamard quotient

**Verdict: FALSE.** Counterexample: `{'witness': {'u': 3, 'x': [-3, 1, 1, 1, -3, 1, 1, 1, 3, 1, 1, 1]}, 'sum': 6, 'correlations': [36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'required_correlations': [36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'computed_side': True, 'claim_side': False}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Squarefree obstruction for odd integral quotient sequences*

*Automated run on the seed topic "Cyclic difference sets D⊆Z/(4u²)Z with u>1 odd, |D|=2u²−u, and exactly u²−u representations of every nonzero residue as d−d′; seek quotient-projection identities and integral lifting obstructions that rule out infinite families of u, targeting Ryser’s open circulant Hadamard conjecture.", 2026-10-04 20:29 UTC. Status: `machine-refuted`.*

## Statement

For every odd squarefree integer u > 1, there is no vector (x_0,...,x_{4u-1}) of odd integers satisfying |x_i| ≤ u for every i, sum_{i=0}^{4u-1} x_i = 2u, and sum_{i=0}^{4u-1} x_i x_{i+t} = 4u² when t = 0 and 0 when 1 ≤ t < 4u.

## Notation

An integer is squarefree if no prime square divides it. All vector indices are reduced modulo 4u. The parameter t is an integer in {0,...,4u-1}. The displayed correlation sums are periodic, not aperiodic.

## Why it is false

`{'witness': {'u': 3, 'x': [-3, 1, 1, 1, -3, 1, 1, 1, 3, 1, 1, 1]}, 'sum': 6, 'correlations': [36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'required_correlations': [36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'computed_side': True, 'claim_side': False}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following assertion: For every integer u that is odd, whose absolute value is squarefree, and that satisfies u > 1, there is no function x from Fin (4 * u.toNat) to the integers such that every x_i is odd and has absolute value at most u, the sum of its entries is 2u, and for every shift t in Fin (4 * u.toNat), the sum of x_i times x_{i+t}, with indices added modulo 4 * u.toNat, is 4u² if t is zero and is zero otherwise.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'witness': {'u': 3, 'x': [-3, 1, 1, 1, -3, 1, 1, 1, 3, 1, 1, 1]}, 'sum': 6, 'correlations': [36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'required_correlations': [36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'computed_side': True, 'claim_side': False}
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `cyclic-difference-sets-d-z-4u-z-with-u-1-odd-d-2-c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
