# Refuted: Six-word affine blocks admit shift-invariant compatible outer codes with one information bit per block

**Verdict: FALSE.** Counterexample: `{'m': 2, 'witness': 'exhaustive UNSAT, independently rechecked', 'brute_force_side': 'maximum cardinality < 12', 'claimed_side': 'exists cardinality >= 12'} ; brute_force_side: maximum cardinality=6 < 12 ; claimed_side: exists invariant D with cardinality >= 12 and the stated triple property; literal truth value=False`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Binary-rate outer codes for a six-word affine block*

*Automated run on the seed topic "Ternary trifferent codes C⊆{0,1,2}ⁿ closed under the global shift x↦x+(1,…,1) modulo three, where every three distinct codewords have a coordinate displaying all three symbols; seek block-concatenation constructions with explicit triple-compatibility conditions that improve exponential size bounds, targeting the open problem of determining the trifferent-code capacity limsupₙ(max|C|)^(1/n).", 2026-10-05 06:16 UTC. Status: `machine-refuted`.*

## Statement

For every integer m ≥ 1, there exists a set D ⊆ (F₃ × {0,1})^m of cardinality at least 3·2^m, invariant under the map ((a_j,b_j))_{j=1}^m ↦ ((a_j+1,b_j))_{j=1}^m, with the following property. For every three distinct elements d^(1), d^(2), d^(3) of D, there is an index j ∈ {1,…,m} satisfying one of these two conditions: (i) b_j^(1)=b_j^(2)=b_j^(3) and the three values a_j^(1), a_j^(2), a_j^(3) are pairwise distinct; (ii) exactly two of the three values b_j^(1), b_j^(2), b_j^(3) agree, and the corresponding two values of a are different.

## Notation

F₃ is the field {0,1,2}, with arithmetic modulo three. The set {0,1} in each pair is regarded as a subset of F₃. An element d of D is a sequence of m pairs (a_j,b_j). Its block expansion E(d) is the word of length 3m obtained by concatenating the blocks (a_j,a_j+b_j,a_j+2b_j), in increasing order of j. A ternary code is trifferent if every three distinct words have a coordinate containing all three symbols.

## Why it is false

`{'m': 2, 'witness': 'exhaustive UNSAT, independently rechecked', 'brute_force_side': 'maximum cardinality < 12', 'claimed_side': 'exists cardinality >= 12'} ; brute_force_side: maximum cardinality=6 < 12 ; claimed_side: exists invariant D with cardinality >= 12 and the stated triple property; literal truth value=False`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following assertion: for every natural number m with m ≥ 1, there exists a finite set D of functions from Fin m to ZMod 3 × Fin 2, with at least 3·2^m elements, closed under simultaneously adding 1 to every first component, such that every three pairwise distinct members p, q, r have an index where either their second components all agree and their first components are pairwise distinct, or exactly two second components agree and the first components of that pair differ.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'m': 2, 'witness': 'exhaustive UNSAT, independently rechecked', 'brute_force_side': 'maximum cardinality < 12', 'claimed_side': 'exists cardinality >= 12'} ; brute_force_side: maximum cardinality=6 < 12 ; claimed_side: exists invariant D with cardinality >= 12 and the stated triple property; literal truth value=False
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `ternary-trifferent-codes-c-0-1-2-closed-under-th-c1` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
