# Refuted: Every third-order-equivalent binary pair admits a balanced constant-run encoding amplifying its fourth-order discrepancy by at least six

**Verdict: FALSE.** Counterexample: `{'witness': {'n': 7, 'u': '0110001', 'v': '1000110', 'U': '001011011001001001011001011011001001001011', 'V': '011001001001011011001011001001001011011001'}, 'violations': [{'relation': 'U 0 count', 'actual_side': 22, 'claimed_side': 21}, {'relation': 'U 1 count', 'actual_side': 20, 'claimed_side': 21}, {'relation': 'V 0 count', 'actual_side': 22, 'claimed_side': 21}, {'relation': 'V 1 count', 'actual_side': 20, 'claimed_side': 21}]}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Balanced constant-run amplification of fourth-order discrepancies*

*Automated run on the seed topic "Pairs of binary words with identical counts of every scattered subsequence of length at most three but different counts at length four, refined by letter counts, run counts, and the vector of length-four count differences; look for concatenation and reversal identities that preserve the lower-order equalities and explicitly transform the length-four differences.", 2026-10-02 07:57 UTC. Status: `machine-refuted`.*

## Statement

For every integer n >= 1 and every pair u,v of binary words of length n satisfying C_s(u)=C_s(v) for every binary word s with 1 <= |s| <= 3, define U=E(u rev(v)) and V=E(v rev(u)), where E replaces each 0 by 001 and each 1 by 011. Then U and V each have length 6n, exactly 3n occurrences of each letter, and exactly 4n runs; they satisfy C_s(U)=C_s(V) for every s with 1 <= |s| <= 3. Moreover, for every t=t_1t_2t_3t_4 in {0,1}^4, their fourth-order difference satisfies Δ_t(U,V)=2 sum_{s in {0,1}^4} Δ_s(u,v) product_{i=1}^4 M_{t_i,s_i}, and 6||Δ(u,v)||_2 <= ||Δ(U,V)||_2 <= 54||Δ(u,v)||_2, where M=[[2,1],[1,2]] with rows and columns ordered 0,1.

## Notation

A binary word is a finite sequence of letters from {0,1}; |w| is its length. C_s(w) counts strictly increasing index sequences in w whose selected letters spell s. Juxtaposition denotes concatenation, and rev(w) reverses the letters of w. E acts by concatenating the indicated replacement blocks. A run is a maximal nonempty consecutive block of equal letters. For words x,y and t in {0,1}^4, Δ_t(x,y)=C_t(x)-C_t(y). Δ(x,y) is the vector of these sixteen coordinates, and ||Δ(x,y)||_2=(sum_{t in {0,1}^4} Δ_t(x,y)^2)^(1/2). M_{a,b} denotes the entry indexed by a,b in {0,1}.

## Why it is false

`{'witness': {'n': 7, 'u': '0110001', 'v': '1000110', 'U': '001011011001001001011001011011001001001011', 'V': '011001001001011011001011001001001011011001'}, 'violations': [{'relation': 'U 0 count', 'actual_side': 22, 'claimed_side': 21}, {'relation': 'U 1 count', 'actual_side': 20, 'claimed_side': 21}, {'relation': 'V 0 count', 'actual_side': 22, 'claimed_side': 21}, {'relation': 'V 1 count', 'actual_side': 20, 'claimed_side': 21}]}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem denies the following universal statement: For every natural number n ≥ 1 and binary lists x,y of length n whose scattered-subword counts agree for every pattern of lengths 1, 2, and 3, let U = E(x concatenated with reverse(y)) and V = E(y concatenated with reverse(x)), where E replaces 0 by 001 and 1 by 011. Both U and V have length 6n, have 3n copies of each letter, and have 4n runs. Their scattered-subword counts agree through order three. For each binary pattern t of length four, delta_t(U,V) equals twice the sum over all length-four binary patterns s of delta_s(x,y) times the product of M(t_i,s_i), where M has diagonal entries 2 and off-diagonal entries 1. Their fourth-order Euclidean difference norms satisfy 6 norm(delta(x,y)) ≤ norm(delta(U,V)) ≤ 54 norm(delta(x,y)).

Re-check output (tail):

```
REFUTATION CONFIRMED: {'witness': {'n': 7, 'u': '0110001', 'v': '1000110', 'U': '001011011001001001011001011011001001001011', 'V': '011001001001011011001011001001001011011001'}, 'violations': [{'relation': 'U 0 count', 'actual_side': 22, 'claimed_side': 21}, {'relation': 'U 1 count', 'actual_side': 20, 'claimed_side': 21}, {'relation': 'V 0 count', 'actual_side': 22, 'claimed_side': 21}, {'relation': 'V 1 count', 'actual_side': 20, 'claimed_side': 21}]}
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

No Palomar bundle: Challenge.lean does not elaborate: C:\Users\Augusto\mathforge-lean\MathForge\c2_Challenge.lean:72:15: error: unsolved goals.
