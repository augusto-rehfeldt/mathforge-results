# Refuted: Minimum nesting counts factor into cycle compositions and binary choices within each cycle

**Verdict: FALSE.** Counterexample: `(n=4, c=1, j=1); A(n,c,j)=1; claimed=2`

**Models:** gpt-6.1-sol (roles under *Models* below)

*The lowest-nesting coefficient for cycle matchings*

*Automated run on the seed topic "Perfect matchings of the ordered set [2n] in which every arc crosses exactly two other arcs, refined by the number of components of the arc-crossing graph and the number of nested arc pairs; look for decomposition identities obtained by removing a crossing-graph cycle and tracking how the remaining arcs occupy its endpoint intervals.", 2026-10-01 17:08 UTC. Status: `machine-refuted`.*

## Statement

For every pair of integers c ≥ 1 and n ≥ 3c, let A(n,c,j) count perfect matchings of [2n] whose arc-crossing graph has exactly c connected components, whose every vertex has degree two, and which have exactly j nested arc pairs. Conjecturally, A(n,c,j) = 0 for every integer j with 0 ≤ j < n−3c, and A(n,c,n−3c) = 2^(n−3c) binom(n−2c−1,c−1).

## Notation

[2n] denotes {1,...,2n}. A perfect matching partitions this set into unordered pairs, called arcs. Write each arc as (a,b) with a<b. Two arcs (a,b) and (s,t) cross when a<s<b<t or s<a<t<b. They are nested when a<s<t<b or s<a<b<t; each unordered nested pair is counted once. The arc-crossing graph has the arcs as vertices and crossing pairs as edges. Thus every connected component under consideration is a cycle with at least three vertices. A(n,c,j) is the number defined in the statement, and binom(r,s)=r!/(s!(r−s)!) for integers 0≤s≤r.

## Why it is false

`(n=4, c=1, j=1); A(n,c,j)=1; claimed=2`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal assertion: for all integers c and n with c ≥ 1 and n ≥ 3c, the number of perfect matchings of {1,…,2n} having degree two at every vertex of their arc-crossing graph, exactly c connected components, and exactly j unordered nested arc pairs is zero for every integer j with 0 ≤ j < n−3c; at j = n−3c, that number equals 2^(n−3c) times binom(n−2c−1,c−1).

Re-check output (tail):

```
REFUTATION CONFIRMED: (n=4, c=1, j=1); A(n,c,j)=1; claimed=2
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `perfect-matchings-of-the-ordered-set-2n-in-which-c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
