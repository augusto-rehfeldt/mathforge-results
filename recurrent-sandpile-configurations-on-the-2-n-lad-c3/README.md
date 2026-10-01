# Refuted: Configurations two chips below maximum have an explicit avalanche polynomial with only one odd intermediate avalanche size

**Verdict: FALSE.** Counterexample: `n=2; LHS coefficients={0: 4, 1: 1, 2: 2, 3: 3}; RHS coefficients={0: 4, 1: 1, 2: 1, 3: 3, 4: 1}; stable configurations with |eta|=6 tested=10`

**Models:** gpt-6.1-sol (roles under *Models* below)

*The two-chip-deficit avalanche polynomial*

*Automated run on the seed topic "Recurrent sandpile configurations on the 2×n ladder with each vertex joined to a sink by enough edges to make its degree three, refined by total chip count and the number of distinct vertices toppled after adding one chip at the upper-left corner; look for column-deletion recurrences tracking the burning condition and avalanche propagation.", 2026-10-01 15:48 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 2, let R_n be the recurrent stable configurations on the ladder defined below. Then Σ_{η∈R_n: |η|=4n−2} z^{A(η)} = 2n + z + Σ_{j=1}^{n−1} z^{2j} + 3z^{2n−1} + (2n²−2n−3)z^{2n}, as an identity of polynomials in the indeterminate z.

## Notation

The nonsink vertices are u_i and v_i for 1 ≤ i ≤ n. Edges are u_i v_i for every i, and u_i u_{i+1} and v_i v_{i+1} for 1 ≤ i < n. Each vertex receives enough edges to a single sink s to make its degree three. A stable configuration η assigns each nonsink vertex a height in {0,1,2}; |η| is the sum of these heights. A toppling removes three chips from its vertex and sends one chip along each incident edge, with chips reaching s discarded. R_n consists of stable configurations passing the burning test: starting with s burned, repeatedly burn any unburned vertex whose height is at least its number of unburned nonsink neighbors; every nonsink vertex must eventually burn. A(η) is the number of distinct nonsink vertices that topple during stabilization after adding one chip at u_1. The summation index j is an integer.

## Why it is false

`n=2; LHS coefficients={0: 4, 1: 1, 2: 2, 3: 3}; RHS coefficients={0: 4, 1: 1, 2: 1, 3: 3, 4: 1}; stable configurations with |eta|=6 tested=10`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies that, for every integer n ≥ 2, the following polynomial identity holds: the sum of X raised to the number of distinct vertices toppled after adding a chip at vertex 0, over all burning-test recurrent height configurations on the 2n-vertex ladder with total height 4n−2, equals 2n + X + ∑_{j=1}^{n−1} X^(2j) + 3X^(2n−1) + (2n²−2n−3)X^(2n). Stabilization uses legal topplings with fuel (4n+1)n².

Re-check output (tail):

```
REFUTATION CONFIRMED: n=2; LHS coefficients={0: 4, 1: 1, 2: 2, 3: 3}; RHS coefficients={0: 4, 1: 1, 2: 1, 3: 3, 4: 1}; stable configurations with |eta|=6 tested=10
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `recurrent-sandpile-configurations-on-the-2-n-lad-c3` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
