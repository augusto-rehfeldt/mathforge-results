# Refuted: Lowering a height-three maximum replaces it by reflected minimal generators not dominated by the other maximum

**Verdict: FALSE.** Counterexample: `{'witness': {'m': 5, 'a': (3, 1, 3, 1), 'p': 3, 'r': 1, 'b': (2, 1, 3, 1), 'C': [2], 'R': []}, 'claimed_side': {'Kunz(b)': True, 'maximal_indices(b)': [2, 3], 'exactly_two_maximal_indices': True, 'genus(b)': 7, 'maximal_residue_gap(b)': 1}, 'brute_force_side': {'Kunz(b)': True, 'maximal_indices(b)': [3], 'exactly_two_maximal_indices': False, 'genus(b)': 7, 'maximal_residue_gap(b)': None}}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Reflected-generator rule for lowering a height-three maximum*

*Automated run on the seed topic "Numerical semigroups of multiplicity m whose Apéry representatives w_i=i+ma_i have a_i∈{1,2,3} and exactly two maximal elements under u≼v iff v−u belongs to the semigroup, refined by genus and the residue gap between those maximal elements; look for coordinate-lowering identities tracking the Kunz inequalities and changes in the two maximal representatives.", 2026-10-02 07:37 UTC. Status: `machine-refuted`.*

## Statement

For every integer m≥3 and every vector a∈{1,2,3}^{m−1} satisfying the Kunz inequalities, suppose its Apéry order has exactly two maximal indices p and r, with a_r=3. Replace a_r by 2, leaving every other coordinate unchanged, to obtain b. Conjecturally, b satisfies the Kunz inequalities and its maximal-index set is exactly {p}∪D, where D=C∪R and C and R are defined below. Consequently, b has exactly two maximal indices if and only if D has exactly one element q; in that case its genus is g−1 and its maximal-residue gap is |p−q|.

## Notation

All indices belong to I={1,…,m−1}. The Kunz inequalities are a_i+a_j≥a_{i+j} when i+j<m, and a_i+a_j+1≥a_{i+j−m} when i+j>m; pairs with i+j=m impose no condition. Put w_i=i+ma_i and S={tm:t≥0}∪{w_i+tm:i∈I,t≥0}. For integers u,v in S, write u≼v when v−u∈S. A maximal index is an index whose representative is maximal among {w_i:i∈I} under this order. A positive element x∈S is a minimal generator when there are no positive y,z∈S with x=y+z. Put g=Σ_{i∈I}a_i. For j∈I\{r}, let k(j) be the unique element of I congruent to r−j modulo m, and let ε(j)=0 if j<r and ε(j)=1 if j>r. Define C={j∈I\{p,r}: a_j+a_{k(j)}+ε(j)=3, w_{k(j)} is a minimal generator of S, and w_p−w_j∉S}. Define R={r} if w_p−(w_r−m)∉S, and R=∅ otherwise. The maximal-residue gap between indices x and y is |x−y|.

## Why it is false

`{'witness': {'m': 5, 'a': (3, 1, 3, 1), 'p': 3, 'r': 1, 'b': (2, 1, 3, 1), 'C': [2], 'R': []}, 'claimed_side': {'Kunz(b)': True, 'maximal_indices(b)': [2, 3], 'exactly_two_maximal_indices': True, 'genus(b)': 7, 'maximal_residue_gap(b)': 1}, 'brute_force_side': {'Kunz(b)': True, 'maximal_indices(b)': [3], 'exactly_two_maximal_indices': False, 'genus(b)': 7, 'maximal_residue_gap(b)': None}}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal assertion: For every natural number m≥3, every function a on Fin m whose nonzero coordinates belong to {1,2,3} and satisfy the Kunz inequalities, and distinct nonzero indices p,r with maximal-index set {p,r} and a(r)=3, let b replace coordinate r by 2. Define C using the complementary residue r−j modulo m, the indicated carry, minimal-generator membership in S(a), and exclusion of w_p−w_j from S(a); define R to contain r exactly when w_p−(w_r−m) is not in S(a), and put D=C∪R. Then b satisfies the Kunz inequalities, its maximal-index set is {p}∪D, and it has exactly two maximal indices if and only if D is a singleton. For every singleton witness q, its genus is the genus of a minus one, its maximal-index set is {p,q}, and the residue gap is |p−q|.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'witness': {'m': 5, 'a': (3, 1, 3, 1), 'p': 3, 'r': 1, 'b': (2, 1, 3, 1), 'C': [2], 'R': []}, 'claimed_side': {'Kunz(b)': True, 'maximal_indices(b)': [2, 3], 'exactly_two_maximal_indices': True, 'genus(b)': 7, 'maximal_residue_gap(b)': 1}, 'brute_force_side': {'Kunz(b)': True, 'maximal_indices(b)': [3], 'exactly_two_maximal_indices': False, 'genus(b)': 7, 'maximal_residue_gap(b)': None}}
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

No Palomar bundle: Challenge.lean does not elaborate: C:\Users\Augusto\mathforge-lean\MathForge\c4_Challenge.lean:107:15: error: unsolved goal.
