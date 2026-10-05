# Refuted: Reciprocal cross-cycle defects synchronize exactly when their combined offset is coprime to the cycle lengths, within Černý’s bound

**Verdict: FALSE.** Counterexample: `(3, 3, 1, 1); actual: reset_exists=False, minimum_length=None; claimed: reset_exists=True, length_at_most=25`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Arithmetic cycle-splicing for reciprocal two-defect automata*

*Automated run on the seed topic "Synchronizing deterministic automata on n states with two letters, one acting as a permutation with exactly two cycles and the other as an idempotent map of rank n−2; seek cycle-splicing and subset-compression lemmas yielding reset words of length at most (n−1)², targeting this restricted case of the open Černý conjecture.", 2026-10-05 00:43 UTC. Status: `machine-refuted`.*

## Statement

For every pair of integers p,q ≥ 2 and every pair of integers r,s with 1 ≤ r < q and 1 ≤ s < p, consider the deterministic automaton with state set Q = {C_0,…,C_{p−1},D_0,…,D_{q−1}} and alphabet {a,b}. Define a(C_i)=C_{(i+1) mod p} and a(D_j)=D_{(j+1) mod q}. Define b(C_0)=D_r and b(D_0)=C_s, and let b fix every other state. This automaton admits a reset word if and only if gcd(p,q,r+s)=1. Whenever this greatest common divisor equals 1, it admits a reset word of length at most (p+q−1)².

## Notation

The symbols C_i and D_j denote distinct states, with 0 ≤ i < p and 0 ≤ j < q. The expression x mod m denotes the residue in {0,…,m−1}. The map b is idempotent and has image size p+q−2. A word is a finite sequence of letters from {a,b}, acting on states from left to right; its length is its number of letters. A reset word maps all states to one state. The expression gcd(p,q,r+s) denotes the greatest positive integer dividing all three arguments.

## Why it is false

`(3, 3, 1, 1); actual: reset_exists=False, minimum_length=None; claimed: reset_exists=True, length_at_most=25`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal assertion: for all integers p,q,r,s with p,q ≥ 2, 1 ≤ r < q, and 1 ≤ s < p, the automaton on the disjoint union of residues modulo p and modulo q, with a incrementing each residue and b sending the first cycle's zero to the second cycle's r and the second cycle's zero to the first cycle's s while fixing other states, has a reset word if and only if gcd(gcd(p,q), |r+s|) = 1; moreover, if this gcd is 1, there is a reset word of length at most (p+q−1)². Words act from left to right.

Re-check output (tail):

```
REFUTATION CONFIRMED: (3, 3, 1, 1); actual: reset_exists=False, minimum_length=None; claimed: reset_exists=True, length_at_most=25
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `synchronizing-deterministic-automata-on-n-states-c2` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
