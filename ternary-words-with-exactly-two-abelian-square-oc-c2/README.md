# Refuted: A ternary word with exactly two crossing abelian squares has length plus overlap at most fifteen

**Verdict: FALSE.** Counterexample: `{"failing_relation": "16 <= 15", "intervals": [[1, 8], [2, 9]], "lhs_n+a+2p-b": 16, "n": 9, "p": 4, "q": 4, "rhs": 15, "t": 7, "word": "010201020"}; left side = 16; right side = 15`

**Models:** gpt-6.1-sol (roles under *Models* below)

*An overlap-sensitive defect bound for ternary words*

*Automated run on the seed topic "Ternary words with exactly two abelian-square occurrences (factors uv with |u|=|v| and equal letter-count vectors) whose intervals overlap but neither contains the other, refined by length, half-lengths, and overlap length; look for overlap-decomposition identities and prefix-extension recurrences tracking letter-count differences and the exclusion of additional abelian squares.", 2026-10-02 06:05 UTC. Status: `machine-refuted`.*

## Statement

For every integer n ≥ 1 and every word w in {0,1,2}^n, suppose w has exactly two abelian-square occurrences, with intervals [a,a+2p−1] and [b,b+2q−1], where a,b,p,q are positive integers satisfying 1 ≤ a < b ≤ a+2p−1 < b+2q−1 ≤ n. Then n + a + 2p − b ≤ 15.

## Notation

Positions are numbered from 1 to n. An interval [i,i+2h−1] is an abelian-square occurrence when h ≥ 1 and, for each letter c in {0,1,2}, c occurs equally often in w[i..i+h−1] and w[i+h..i+2h−1]. Occurrences are distinguished by their intervals. The two displayed intervals overlap without either containing the other. Their overlap length is t = a+2p−b, so the asserted inequality is n+t ≤ 15.

## Why it is false

`{"failing_relation": "16 <= 15", "intervals": [[1, 8], [2, 9]], "lhs_n+a+2p-b": 16, "n": 9, "p": 4, "q": 4, "rhs": 15, "t": 7, "word": "010201020"}; left side = 16; right side = 15`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following universal assertion: For every integer n, function w from integers to the three letters Fin 3, and integers a,b,p,q, if n,a,b,p,q are positive, a < b ≤ a+2p−1 < b+2q−1 ≤ n, and the abelian-square occurrences in positions 1 through n are exactly the start/half-length pairs (a,p) and (b,q), then n+a+2p−b ≤ 15. An abelian-square occurrence has positive start and half-length, ends at most at n, and has equal counts of each letter in its two halves.

Re-check output (tail):

```
REFUTATION CONFIRMED: {"failing_relation": "16 <= 15", "intervals": [[1, 8], [2, 9]], "lhs_n+a+2p-b": 16, "n": 9, "p": 4, "q": 4, "rhs": 15, "t": 7, "word": "010201020"}; left side = 16; right side = 15
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `ternary-words-with-exactly-two-abelian-square-oc-c2` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
