# Refuted: For matrices of order at least six, only two inverse weights sit closest below the maximum

**Verdict: FALSE.** Counterexample: `n=6, second superdiagonal=[1, 1, 0, 0]; inverse weight=11, claimed bound=11`

**Models:** gpt-6-sol (roles under *Models* below)

*A gap below the maximum inverse weight*

*Automated run on the seed topic "Upper unitriangular matrices over F₂ whose first superdiagonal is all ones and whose second superdiagonal is arbitrary, refined by the number of nonzero entries in their inverses; look for end-extension recurrences and reversal-symmetry congruences.", 2026-09-27 15:54 UTC. Status: `machine-refuted`.*

## Statement

For every integer n≥6, let A range over the n×n upper unitriangular matrices over F₂ whose first superdiagonal is all ones and whose entries outside the diagonal and first two superdiagonals are zero. If A is not the matrix with zero second superdiagonal, then its inverse has at most n(n−1)/2−(n−2) nonzero entries above the diagonal. Equality holds exactly when the second superdiagonal has a single one, at its first or last position.

## Notation

F₂ is the field with two elements. The second superdiagonal consists of entries A_{i,i+2} for 1≤i≤n−2; its first and last positions have i=1 and i=n−2, respectively. Inverse weight counts nonzero entries (A⁻¹)_{i,j} with i<j.

## Why it is false

`n=6, second superdiagonal=[1, 1, 0, 0]; inverse weight=11, claimed bound=11`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. It is false that, for every natural number n ≥ 6, every admissible n×n matrix over ZMod 2 with a nonzero entry on its second superdiagonal, and every right inverse B of that matrix, the number of nonzero entries of B above the diagonal is at most n(n−1)/2−(n−2), with equality exactly when the matrix has a single nonzero second-superdiagonal entry at its first or last position.

Re-check output (tail):

```
REFUTATION CONFIRMED: n=6, second superdiagonal=[1, 1, 0, 0]; inverse weight=11, claimed bound=11
```

## Models

- Proposed the claim: gpt-6-sol
- Counterexample search: gpt-6-sol
- Independent re-check of the witness: gpt-6-sol
- Lean formalization: gpt-6-sol
- Faithfulness judge: gpt-6-sol

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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `upper-unitriangular-matrices-over-f-whose-first--c2` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
