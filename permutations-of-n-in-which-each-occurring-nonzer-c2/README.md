# Refuted: With exactly three long displacement lengths, every permutation not composed of transpositions has one explicitly shaped six-cycle

**Verdict: FALSE.** Counterexample: `{'n': 6, 'a': 3, 'b': 4, 'c': 5} brute_force_side = 0 claimed_side = 4`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Three long displacement lengths force a unique six-cycle shape*

*Automated run on the seed topic "Permutations π of [n] in which each occurring nonzero absolute displacement |π(i)−i| occurs exactly twice, once with each sign, refined by fixed-point count, cycle count, and total positive displacement; look for cut-and-glue identities tracking unmatched displacement lengths across a cut and structural criteria forcing all nontrivial cycles to be transpositions.", 2026-10-01 19:15 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1 and all integers a, b, c satisfying (n−1)/2 < a < b < c ≤ n−1, let P(n;a,b,c) consist of permutations π of [n] whose nonzero signed displacements are exactly +a, −a, +b, −b, +c, −c, each occurring once. Put s=a+c−b. Exactly 2(n−s) members of P(n;a,b,c) have a nontrivial cycle of length greater than two. More precisely, these members are exactly the permutations fixing every point outside one of the cycles (t+b−a, t+b, t, t+c, t+c−a, t+s), or its inverse, where 1 ≤ t ≤ n−s. Consequently, each such member has n−6 fixed points, n−5 cycles in total, and total positive displacement a+b+c; every remaining member of P(n;a,b,c) consists of three transpositions and n−6 fixed points.

## Notation

[n]={1,…,n}. A permutation is a bijection π:[n]→[n]. Its signed displacement at i is π(i)−i. A fixed point satisfies π(i)=i. A nontrivial cycle has length at least two. Cycle notation (x1,…,x6) means π(xj)=x(j+1) for 1≤j<6 and π(x6)=x1. Its inverse traverses these entries in reverse order. Total positive displacement means the sum of π(i)−i over all i with π(i)>i. The letters a,b,c denote the three distinct absolute displacement lengths, and s=a+c−b.

## Why it is false

`{'n': 6, 'a': 3, 'b': 4, 'c': 5} brute_force_side = 0 claimed_side = 4`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following assertion: For all integers n,a,b,c with n≥1, n−1<2a, a<b<c≤n−1, set s=a+c−b. Among permutations of {1,…,n} with each displacement ±a, ±b, ±c occurring exactly once and all other displacements zero, exactly 2(n−s) are not involutions. Such a permutation is not an involution if and only if it fixes all points outside the six distinct entries (t+b−a,t+b,t,t+c,t+c−a,t+s) and traverses those entries cyclically forward or backward, for some integer 1≤t≤n−s. Each such permutation has n−6 fixed points, n−5 cycles, and positive displacement sum a+b+c. Every admissible involution consists of three transpositions and has n−6 fixed points.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'n': 6, 'a': 3, 'b': 4, 'c': 5} brute_force_side = 0 claimed_side = 4
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

No Palomar bundle: Challenge.lean does not elaborate: C:\Users\Augusto\mathforge-lean\MathForge\c2_Challenge.lean:88:15: error: unsolved goals.
