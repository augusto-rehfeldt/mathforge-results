# Refuted: Every strongly connected tournament with edge-triangle capacity two admits a connectivity-preserving vertex deletion of weighted triangle cost at most eight

**Verdict: FALSE.** Counterexample: `{'n': 7, 'directed_edges': [(0, 2), (0, 5), (0, 6), (1, 0), (1, 4), (1, 6), (2, 1), (2, 3), (2, 6), (3, 0), (3, 1), (3, 5), (4, 0), (4, 2), (4, 3), (5, 1), (5, 2), (5, 4), (6, 3), (6, 4), (6, 5)]} {'hypotheses': True, 'conclusion_exists_v': False, 'per_vertex': [{'v': 0, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 1, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 2, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 3, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 4, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 5, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 6, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}]}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Low-cost strongly connected vertex deletion*

*Automated run on the seed topic "Tournaments in which every directed edge belongs to at most two directed triangles, refined by vertex count, directed-triangle count, and number of strongly connected components; look for strong-component decomposition identities and vertex-deletion recurrences tracking edges whose triangle capacity is exhausted.", 2026-10-01 21:12 UTC. Status: `machine-refuted`.*

## Statement

For every integer n >= 4 and every strongly connected tournament T on n vertices in which each directed edge belongs to at most two directed triangles, there exists a vertex v such that T-v is strongly connected and a_T(v) + b_T(v) <= 8.

## Notation

A tournament is a finite directed graph having exactly one of x->y and y->x for each pair of distinct vertices. A directed triangle is a three-element vertex set inducing a directed cycle. Strong connectivity means that every ordered pair of vertices is joined by a directed path. T-v is the induced tournament obtained by deleting v. For each directed edge e, c_T(e) is the number of directed triangles containing e; e is exhausted when c_T(e)=2. The integer a_T(v) counts directed triangles containing v. The integer b_T(v) counts edges e of T-v satisfying c_T(e)=2 and c_{T-v}(e)=1: surviving edges whose exhausted capacity is released by deleting v.

## Why it is false

`{'n': 7, 'directed_edges': [(0, 2), (0, 5), (0, 6), (1, 0), (1, 4), (1, 6), (2, 1), (2, 3), (2, 6), (3, 0), (3, 1), (3, 5), (4, 0), (4, 2), (4, 3), (5, 1), (5, 2), (5, 4), (6, 3), (6, 4), (6, 5)]} {'hypotheses': True, 'conclusion_exists_v': False, 'per_vertex': [{'v': 0, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 1, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 2, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 3, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 4, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 5, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 6, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}]}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following assertion: for every natural number n ≥ 4 and every loopless tournament E on Fin n, if E is strongly connected and every directed edge lies in at most two cyclic three-element vertex sets, then there exists a vertex v whose deletion leaves a strongly connected induced tournament and for which a E v + b E v ≤ 8. Here a counts cyclic triples containing v, and b counts surviving directed edges lying in exactly two cyclic triples before deletion and exactly one afterward.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'n': 7, 'directed_edges': [(0, 2), (0, 5), (0, 6), (1, 0), (1, 4), (1, 6), (2, 1), (2, 3), (2, 6), (3, 0), (3, 1), (3, 5), (4, 0), (4, 2), (4, 3), (5, 1), (5, 2), (5, 4), (6, 3), (6, 4), (6, 5)]} {'hypotheses': True, 'conclusion_exists_v': False, 'per_vertex': [{'v': 0, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 1, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 2, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 3, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 4, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 5, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}, {'v': 6, 'T-v_strong': True, 'a_T(v)': 6, 'b_T(v)': 6, 'a_T(v)+b_T(v)': 12}]}
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `tournaments-in-which-every-directed-edge-belongs-c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
