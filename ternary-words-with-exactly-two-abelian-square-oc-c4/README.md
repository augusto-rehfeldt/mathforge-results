# Refuted: Exactly two crossing abelian squares of equal half-length must start at consecutive positions

**Verdict: FALSE.** Counterexample: `w=0101212 j=3 i+1=1`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Unit displacement for equal-scale crossing squares*

*Automated run on the seed topic "Ternary words with exactly two abelian-square occurrences (factors uv with |u|=|v| and equal letter-count vectors) whose intervals overlap but neither contains the other, refined by length, half-lengths, and overlap length; look for overlap-decomposition identities and prefix-extension recurrences tracking letter-count differences and the exclusion of additional abelian squares.", 2026-10-02 06:06 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1 and every word w of length n over {0,1,2}, suppose w has exactly two abelian-square occurrences. Write their intervals as [i,i+2h) and [j,j+2h), where h ≥ 1 and 0 ≤ i < j < i+2h ≤ n and j+2h ≤ n. Then j=i+1. Equivalently, their overlap has length 2h−1.

## Notation

Positions are indexed from 0. The interval [a,b) denotes positions a through b−1. An abelian-square occurrence is a pair (a,k) of integers with k ≥ 1 and 0 ≤ a ≤ n−2k such that, for each letter c in {0,1,2}, c occurs equally often in positions [a,a+k) and [a+k,a+2k). Distinct pairs count as distinct occurrences. The integer k is the half-length. In the statement, i and j are the two starting positions and h is their common half-length.

## Why it is false

`w=0101212 j=3 i+1=1`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following claim: For every natural number n ≥ 1, every list w of length n with entries in Fin 3, and all natural numbers i, j, h, if h ≥ 1, i < j < i + 2h ≤ n, j + 2h ≤ n, and for every a,k in {0,…,n}, (a,k) is an abelian-square occurrence in w exactly when it equals (i,h) or (j,h), then j = i + 1. An abelian-square occurrence has positive half-length, lies entirely within the length-n word, and has equal counts of each letter in its two halves.

Re-check output (tail):

```
REFUTATION CONFIRMED: w=0101212 j=3 i+1=1
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `ternary-words-with-exactly-two-abelian-square-oc-c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
