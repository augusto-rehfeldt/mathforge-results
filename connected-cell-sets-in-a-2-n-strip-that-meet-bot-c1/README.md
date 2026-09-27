# Refuted: Opposite-end strip animals occur in even numbers unless their area and perimeter match two parity conditions

**Verdict: FALSE.** Counterexample: `n=3, a=4, p=10; C(n,a,p)=1, actual parity=1, claimed parity=0`

**Models:** gpt-6-sol (roles under *Models* below)

*A parity congruence for opposite-end strip animals*

*Automated run on the seed topic "Connected cell sets in a 2×n strip that meet both end columns, refined by area, perimeter, and the occupancy of each end column; look for column-extension recurrences and reflection-based parity congruences.", 2026-09-27 15:49 UTC. Status: `machine-refuted`.*

## Statement

For every integer n≥2 and all integers a,p≥0, let C(n,a,p) count connected cell sets in a 2×n strip whose first column contains only its top cell, whose last column contains only its bottom cell, and whose area and perimeter are a and p. Then C(n,a,p) is even whenever a is odd or p is not congruent to 2(n−1) modulo 4.

## Notation

Cells sharing an edge are adjacent; connected means connected under this adjacency. Area is the number of cells, and perimeter is the number of cell edges bordering an unoccupied cell or the exterior. A column contains only its top or bottom cell when exactly that cell is occupied.

## Why it is false

`n=3, a=4, p=10; C(n,a,p)=1, actual parity=1, claimed parity=0`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem says it is false that, for every integer n ≥ 2 and nonnegative integers a and p, the number of connected occupied subsets of a 2×n strip with a top-only first column, a bottom-only last column, area a, and perimeter p is even whenever a is odd or p is not congruent to 2(n−1) modulo 4.

Re-check output (tail):

```
REFUTATION CONFIRMED: n=3, a=4, p=10; C(n,a,p)=1, actual parity=1, claimed parity=0
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `connected-cell-sets-in-a-2-n-strip-that-meet-bot-c1` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
