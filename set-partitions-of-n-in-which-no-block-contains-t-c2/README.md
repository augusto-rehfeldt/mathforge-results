# Refuted: Odd-length partition counts modulo two reduce to weighted matchings on blocks of half-length partitions

**Verdict: FALSE.** Counterexample: `m=2, exponents=(3, 1, 0); LHS=1 (mod 2=1), RHS=0 (mod 2=0)`

**Models:** gpt-6.1-sol (roles under *Models* below)

*A half-size matching formula for reversal parity*

*Automated run on the seed topic "Set partitions of [n] in which no block contains two elements differing by two, refined by the number of blocks, singleton blocks, and indices i whose consecutive elements i and i+1 lie in the same block; look for insertion recurrences tracking the last two block memberships and reversal-induced coefficient congruences.", 2026-10-01 01:14 UTC. Status: `machine-refuted`.*

## Statement

For every integer m≥2, the following polynomial congruence holds coefficientwise modulo 2: F_{2m+1}(x,y,z) ≡ Σ_Q Σ_{D,I,M} x^{2b−|I|−2δ+1} y^{2u+1−δ} z^{2a(Q)}. The outer sum ranges over all admissible partitions Q of [m]. In each inner sum, D is either absent or a block of Q containing neither m−1 nor m; δ is 0 or 1 according as D is absent or present. The set I is any subset of the blocks other than D that excludes the block containing m. The object M is any matching on the blocks outside I and D. The integer u counts singleton blocks of Q outside I and D that are unmatched in M.

## Notation

[r]={1,…,r}. A partition is admissible if no block contains two integers differing by two. For an admissible partition P, b(P) is its number of blocks, s(P) its number of singleton blocks, and a(P)=|{i∈[r−1]: i and i+1 belong to the same block of P}|. Define F_r(x,y,z)=Σ_P x^{b(P)}y^{s(P)}z^{a(P)}, summing over admissible partitions of [r]; x,y,z are commuting indeterminates. In the displayed congruence, b=b(Q). A matching on a finite set is a collection of pairwise disjoint unordered pairs of distinct members, including the empty collection. An absent D removes no block. Coefficientwise congruence means that every corresponding pair of integer coefficients has even difference.

## Why it is false

`m=2, exponents=(3, 1, 0); LHS=1 (mod 2=1), RHS=0 (mod 2=0)`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies that, for every natural number m ≥ 2 and every triple of natural exponents p,q,t, the number of admissible partitions of [2m+1] with p blocks, q singleton blocks, and t adjacent pairs in a common block has the same parity as the following count: admissible partitions Q of [m], choices of an absent distinguished block or a block D containing neither m−1 nor m, subsets I of the other blocks excluding the block containing m, and matchings M on the remaining blocks, whose exponents are p = 2|Q|−|I|−2δ+1, q = 2u+1−δ, and t = 2a(Q), where u counts unmatched singleton blocks. The statement inside the negation asserts this parity equality universally.

Re-check output (tail):

```
REFUTATION CONFIRMED: m=2, exponents=(3, 1, 0); LHS=1 (mod 2=1), RHS=0 (mod 2=0)
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `set-partitions-of-n-in-which-no-block-contains-t-c2` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
