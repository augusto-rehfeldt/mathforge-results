# Refuted: Every skew-symmetric Littlewood sequence stable under parity-block flips has asymptotic merit factor at least four

**Verdict: FALSE.** Counterexample: `{'m': 24, 'a': [1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1]} E(a)=424; (2m+1)^2/8 + 2(2m+1)=3185/8`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Parity-block stability forces merit factor four*

*Automated run on the seed topic "Skew-symmetric Littlewood polynomials P(z)=∑_{j=0}^{2m}a_jz^j with a_j∈{−1,1} and a_{m+j}=(-1)^j a_{m-j}; seek signed block-interleaving identities controlling the aperiodic autocorrelation energy ∑_{r=1}^{2m}(∑_{j=0}^{2m-r}a_ja_{j+r})² and constructions improving asymptotic merit-factor lower bounds, targeting the open Littlewood merit-factor problem.", 2026-10-05 08:55 UTC. Status: `machine-refuted`.*

## Statement

For every integer m ≥ 1, let a = (a_0,…,a_{2m}) be a sequence with entries in {−1,1} satisfying a_{m+j} = (−1)^j a_{m−j} for every integer j with 0 ≤ j ≤ m. Suppose E(a) ≤ E(T_{u,v,d}a) for every d ∈ {1,2} and every pair of integers 0 ≤ u ≤ v ≤ m with d dividing v−u. Then E(a) ≤ (2m+1)^2/8 + 2(2m+1).

## Notation

Set N = 2m+1. For 1 ≤ r ≤ 2m, define C_r(a) = ∑_{j=0}^{2m−r} a_j a_{j+r}, and define E(a) = ∑_{r=1}^{2m} C_r(a)^2. For admissible u,v,d, let S_{u,v,d} = {u,u+d,…,v}. The transformation T_{u,v,d} negates precisely those coordinates a_i with i ∈ S_{u,v,d} or 2m−i ∈ S_{u,v,d}; every other coordinate remains unchanged. Each coordinate is negated once, even when both conditions hold. Thus T preserves skew symmetry. The merit factor is F(a) = N^2/(2E(a)); the proposed bound implies F(a) ≥ 4N/(N+16).

## Why it is false

`{'m': 24, 'a': [1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1]} E(a)=424; (2m+1)^2/8 + 2(2m+1)=3185/8`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal statement: For every natural number m ≥ 1 and every integer-valued function a on the natural numbers, if a_i is −1 or 1 for 0 ≤ i ≤ 2m, if a_{m+j} = (−1)^j a_{m−j} for 0 ≤ j ≤ m, and if E(a) ≤ E(T_{u,v,d}a) for every 0 ≤ u ≤ v ≤ m and d ∈ {1,2} dividing v−u, then 8E(a) ≤ (2m+1)^2 + 16(2m+1). Here E is the sum of squared correlations at lags 1 through 2m, and T negates a coordinate once when it or its reflection about m belongs to the progression from u to v with step d.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'m': 24, 'a': [1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1]} E(a)=424; (2m+1)^2/8 + 2(2m+1)=3185/8
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `skew-symmetric-littlewood-polynomials-p-z-j-0-2m-c3` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
