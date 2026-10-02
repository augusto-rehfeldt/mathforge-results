# Refuted: The rightmost square determines exactly how many further letters preserve the two overlapping square occurrences

**Verdict: FALSE.** Counterexample: `{"b": 5, "brute_force_side": 0, "claimed_side": 1, "computed_occurrences": [[1, 2], [4, 1]], "computed_r": 1, "computed_t": 0, "k": 2, "n": 5, "occurrences": [[1, 2], [4, 1]], "r": 1, "relation": "continuation count", "structural_conclusion": true, "t": 0, "valid_extensions": [], "w": "10100"}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Exact continuation budget for overlapping binary squares*

*Automated run on the seed topic "Binary words having exactly two occurrences of square factors uu, with nonempty u, whose occurrence intervals overlap but neither contains the other, refined by word length, the two root lengths, and overlap length; look for overlap-forced periodicity identities and prefix-extension recurrences tracking suffixes that would create a third square occurrence.", 2026-10-02 00:32 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1 and every binary word w of length n having exactly two square occurrences whose intervals overlap and neither contains the other, let b be the final position of the occurrence that starts later, let r be its root length, and put t = n − b. Then r belongs to {1,2}. If r = 1, then 0 ≤ t ≤ 2 and, for every integer k ≥ 0, exactly one binary word x of length k makes wx have exactly two square occurrences when k ≤ 2 − t, and no such x exists when k > 2 − t. If r = 2, then t = 0 and no nonempty binary word x makes wx have exactly two square occurrences.

## Notation

A binary word is a finite sequence over {0,1}; its positions are numbered from 1. A square occurrence is a pair (i,r) of integers with r ≥ 1 and 1 ≤ i ≤ n − 2r + 1 such that w[i+j] = w[i+r+j] for every integer j with 0 ≤ j < r. Its interval is [i,i+2r−1], and its root length is r. Occurrences are counted separately even when their factors are identical. Two intervals overlap when their intersection is nonempty. Neither contains the other when neither interval is a subset of the other. The occurrence starting later is uniquely defined under these conditions. The notation wx denotes concatenation; the unique word of length zero is the empty word.

## Why it is false

`{"b": 5, "brute_force_side": 0, "claimed_side": 1, "computed_occurrences": [[1, 2], [4, 1]], "computed_r": 1, "computed_t": 0, "k": 2, "n": 5, "occurrences": [[1, 2], [4, 1]], "r": 1, "relation": "continuation count", "structural_conclusion": true, "t": 0, "valid_extensions": [], "w": "10100"}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following universal claim: For every natural n ≥ 1, every Boolean word w of length n, and every pair of square occurrences a,c, if w has exactly two square occurrences, a starts strictly before c, c starts before the exclusive end of a, and a ends strictly before c, then the root length of c is 1 or 2. Put t = n minus the exclusive zero-based end of c. If c has root length 1, then t ≤ 2, and for every natural k there is exactly one Boolean word x of length k whose concatenation with w has exactly two square occurrences when k ≤ 2 − t, and no such word when k > 2 − t. If c has root length 2, then t = 0 and no positive-length Boolean word can be appended while retaining exactly two square occurrences.

Re-check output (tail):

```
REFUTATION CONFIRMED: {"b": 5, "brute_force_side": 0, "claimed_side": 1, "computed_occurrences": [[1, 2], [4, 1]], "computed_r": 1, "computed_t": 0, "k": 2, "n": 5, "occurrences": [[1, 2], [4, 1]], "r": 1, "relation": "continuation count", "structural_conclusion": true, "t": 0, "valid_extensions": [], "w": "10100"}
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `binary-words-having-exactly-two-occurrences-of-s-c2` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
