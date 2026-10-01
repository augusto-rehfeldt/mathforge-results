# Refuted: Occupied vertices equal twice enclosed vacancies plus six per cycle, corrected by enclosed squares and four-vertex cycles

**Verdict: FALSE.** Counterexample: `n = 4 A = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (2, 4), (3, 1), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)] v(A) = 12 2h(A)+6c(A)-2s(A)-2q(A) = 10 (v,h,c,s,q) = (12, 2, 1, 0, 0)`

**Models:** gpt-6.1-sol (roles under *Models* below)

*An enclosure-square correction for induced grid cycles*

*Automated run on the seed topic "Vertex subsets of the 4×n rectangular grid whose induced subgraph is 2-regular, refined by occupied-vertex count, cycle count, and the number of unoccupied grid vertices strictly enclosed by cycles; look for column-extension recurrences tracking boundary connectivity and enclosure, and identities from cutting at empty columns.", 2026-10-01 15:00 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1 and every subset A of the vertices of G_n whose induced subgraph is 2-regular, the identity v(A) = 2h(A) + 6c(A) − 2s(A) − 2q(A) holds. The empty subset is allowed.

## Notation

G_n has vertex set {1,2,3,4} × {1,...,n}, with edges between vertices at Euclidean distance one, drawn as straight segments. A graph is 2-regular if every vertex has degree two; the empty graph is included. Each connected component of G_n[A] is consequently a simple polygonal cycle. v(A) = |A|. c(A) is the number of these cycles. h(A) counts vertices of G_n outside A lying strictly inside at least one cycle. s(A) counts unit grid squares whose four corner vertices are outside A and lie strictly inside the same cycle. q(A) counts connected components of G_n[A] having exactly four vertices. All four statistics are zero when A is empty.

## Why it is false

`n = 4 A = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (2, 4), (3, 1), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)] v(A) = 12 2h(A)+6c(A)-2s(A)-2q(A) = 10 (v,h,c,s,q) = (12, 2, 1, 0, 0)`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies that, for every natural number n ≥ 1 and every subset A of the 4-by-n grid vertices, if every vertex in the induced graph on A has exactly two neighbors, then |A| = 2h + 6c − 2s − 2q. Here c counts connected components, h counts unselected grid vertices strictly inside at least one component cycle, s counts unit squares whose four corners are unselected and strictly inside one common component cycle, and q counts components with four vertices. The empty subset is included.

Re-check output (tail):

```
REFUTATION CONFIRMED: n = 4 A = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (2, 4), (3, 1), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)] v(A) = 12 2h(A)+6c(A)-2s(A)-2q(A) = 10 (v,h,c,s,q) = (12, 2, 1, 0, 0)
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `vertex-subsets-of-the-4-n-rectangular-grid-whose-c1` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
