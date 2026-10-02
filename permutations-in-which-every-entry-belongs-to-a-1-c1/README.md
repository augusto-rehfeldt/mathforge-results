# Refuted: A permutation whose 132-incidence graph is a tree consists of an initial minimum followed by increasing reversed pairs

**Verdict: FALSE.** Counterexample: `{'relation': 'membership in T_n', 'n': 5, 'permutation': (1, 3, 2, 5, 4), '132_occurrences': [(0, 1, 2), (0, 3, 4), (1, 3, 4), (2, 3, 4)]} brute_force_side: False claimed_side: True`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Rigidity of tree-incidence 132 permutations*

*Automated run on the seed topic "Permutations in which every entry belongs to a 132-pattern occurrence and the bipartite incidence graph between entries and 132-occurrences is a tree, refined by length, inversion number, and descent number; look for leaf-occurrence deletion and reinsertion identities tracking relative-order constraints that prevent additional 132-occurrences.", 2026-10-02 02:44 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1, let T_n be the set of permutations of {1,…,n} in which every entry belongs to a 132-occurrence and the entry–occurrence incidence graph is a tree. Conjecturally, T_n is empty unless n = 2m+1 for an integer m ≥ 1, and T_{2m+1} consists exactly of the permutation (1,3,2,5,4,…,2m+1,2m). Consequently, for every m ≥ 1, the polynomial sum over π in T_{2m+1} of q^{inv(π)}t^{des(π)} equals q^m t^m. For m ≥ 2, deleting the two entries belonging exclusively to any one occurrence and then standardizing gives the unique member of T_{2m−1}, decreasing both inversion number and descent number by exactly one.

## Notation

A permutation π is written as (π_1,…,π_n). A 132-occurrence is a triple of positions i<j<k satisfying π_i<π_k<π_j. The incidence graph has one vertex for each position and one vertex for each occurrence; an occurrence vertex is adjacent exactly to its three positions. A tree is a connected graph with no cycle. The inversion number inv(π) counts pairs i<j with π_i>π_j. The descent number des(π) counts positions i<n with π_i>π_{i+1}. The symbols q and t are commuting formal indeterminates. Standardization replaces the smallest retained entry by 1, the next smallest by 2, and so on, preserving positions. The displayed permutation begins with 1 and then appends (2r+1,2r) for r=1,…,m.

## Why it is false

`{'relation': 'membership in T_n', 'n': 5, 'permutation': (1, 3, 2, 5, 4), '132_occurrences': [(0, 1, 2), (0, 3, 4), (1, 3, 4), (2, 3, 4)]} brute_force_side: False claimed_side: True`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem refutes the following conjunction: (1) For every natural n ≥ 1 and permutation p of Fin n, every position belongs to a 132-occurrence and the incidence graph is a tree if and only if n = 2m+1 for some natural m ≥ 1 and p is the zero-based permutation (0,2,1,4,3,…,2m,2m−1). (2) For every m ≥ 1, the sum of X₀^inv(p) X₁^des(p) over such tree-incidence permutations of size 2m+1 equals X₀^m X₁^m. (3) For every m ≥ 2, every such permutation, and every 132-occurrence, exactly two positions belong exclusively to that occurrence; deleting them and standardizing yields a tree-incidence permutation of size 2m−1 having the canonical form, with inversion and descent numbers each reduced by one.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'relation': 'membership in T_n', 'n': 5, 'permutation': (1, 3, 2, 5, 4), '132_occurrences': [(0, 1, 2), (0, 3, 4), (1, 3, 4), (2, 3, 4)]} brute_force_side: False claimed_side: True
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `permutations-in-which-every-entry-belongs-to-a-1-c1` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
