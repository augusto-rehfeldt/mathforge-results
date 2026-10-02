# Refuted: Two period-two necklaces can be glued at changed vertices with freely chosen replacement phases and explicit weight corrections

**Verdict: FALSE.** Counterexample: `{"computed_actual_side": {"D(u)": 3, "T(u)≠u": true, "T²(u)": [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], "temporal_weight_sum": 13, "unordered_temporal_weight_pair": [5, 8], "wt(T(u))": 8, "wt(u)": 5}, "literal_claimed_side": {"D(u)": 3, "T(u)≠u": true, "T²(u)": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], "temporal_weight_sum": 13, "unordered_temporal_weight_pair": [5, 8], "wt(T(u))": 8, "wt(u)": 5}, "violated_conclusions": ["T²(u)"], "witness": {"actual": [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], "c": 0, "claimed": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], "d": 0, "i": 0, "j": 0, "operation": "forward", "relation": "T²(u)=u", "u": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], "x": [0, 1, 0, 0, 1], "z": [1, 1, 0, 1, 0, 0, 1]}}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Free-phase gluing at changed vertices*

*Automated run on the seed topic "Binary necklaces of exact temporal period two under the cyclic update T(x)_i=x_i+x_{i-1}x_{i+1} over F₂, refined by length, the unordered pair of Hamming weights of x and T(x), and the number of changed positions; look for cutting-and-gluing identities with explicit boundary bits that preserve T²(x)=x while excluding fixed points.", 2026-10-02 10:42 UTC. Status: `machine-refuted`.*

## Statement

For every pair of integers n,m ≥ 5, let x and z be binary cyclic words of lengths n and m satisfying T²(x)=x, T(x)≠x, T²(z)=z, and T(z)≠z. Choose positions i and j changed by T in x and z, respectively, and put a=x_i and b=z_j. Let P be the length-(n−1) word read cyclically immediately after i, omitting i, and define Q analogously from z and j. For every c,d∈{0,1}, form the cyclic word u=P c Q d. Then T²(u)=u and T(u)≠u. Moreover, D(u)=D(x)+D(z), wt(u)=wt(x)+wt(z)−a−b+c+d, and wt(T(u))=wt(T(x))+wt(T(z))+a+b−c−d. Thus gluing preserves the sum of the two temporal weights and gives the displayed explicit correction to their unordered pair. The operation is reversible: for every length N≥10 word u of exact temporal period two, cutting at any two changed positions whose clockwise distances in both directions are at least five, and closing each intervening path with either chosen bit, produces two words of exact temporal period two.

## Notation

A binary cyclic word of length r is an element v of {0,1}^r with positions indexed modulo r; its necklace is its equivalence class under cyclic rotation. The update is T(v)_h=v_h+v_{h−1}v_{h+1}, with addition and multiplication in F₂. T² means applying T twice. A changed position h satisfies T(v)_h≠v_h. D(v) is the number of changed positions, and wt(v) is the number of entries equal to one, counted as an ordinary integer. Juxtaposition denotes concatenation before interpreting the resulting word cyclically. The unordered temporal weight pair is the multiset {wt(v),wt(T(v))}. Clockwise distance counts edges along the cyclic indexing order. In the reverse operation, each intervening path excludes both selected changed positions; closing means appending one freely chosen binary entry and interpreting the result cyclically.

## Why it is false

`{"computed_actual_side": {"D(u)": 3, "T(u)≠u": true, "T²(u)": [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], "temporal_weight_sum": 13, "unordered_temporal_weight_pair": [5, 8], "wt(T(u))": 8, "wt(u)": 5}, "literal_claimed_side": {"D(u)": 3, "T(u)≠u": true, "T²(u)": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], "temporal_weight_sum": 13, "unordered_temporal_weight_pair": [5, 8], "wt(T(u))": 8, "wt(u)": 5}, "violated_conclusions": ["T²(u)"], "witness": {"actual": [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], "c": 0, "claimed": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], "d": 0, "i": 0, "j": 0, "operation": "forward", "relation": "T²(u)=u", "u": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], "x": [0, 1, 0, 0, 1], "z": [1, 1, 0, 1, 0, 0, 1]}}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the conjunction of two assertions. First, for all natural lengths n,m at least 5, all Boolean lists x,z of those lengths having exact period two under the cyclic update T, all in-range changed indices i,j, and every pair of Boolean bits c,d, the word u formed by reading all entries after i in x except i, appending c, reading all entries after j in z except j, and appending d has exact period two. Its number of changed positions is D(x)+D(z); writing a and b for the integer values of the removed bits, its weight is wt(x)+wt(z)−a−b+c+d and its updated weight is wt(T(x))+wt(T(z))+a+b−c−d. The sum of its temporal weights equals the sum of the four input temporal weights, and its unordered temporal weight multiset equals the multiset of the two displayed corrected weights. Second, for every natural N at least 10, every length-N Boolean list u of exact period two, every index i<N and distance k with 5≤k and k+5≤N, if i and i+k are changed positions under cyclic indexing, then for every pair of Boolean bits c,d, both intervening paths, excluding the two selected positions and closed respectively with c and d, have exact period two.

Re-check output (tail):

```
REFUTATION CONFIRMED: {"computed_actual_side": {"D(u)": 3, "T(u)≠u": true, "T²(u)": [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], "temporal_weight_sum": 13, "unordered_temporal_weight_pair": [5, 8], "wt(T(u))": 8, "wt(u)": 5}, "literal_claimed_side": {"D(u)": 3, "T(u)≠u": true, "T²(u)": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], "temporal_weight_sum": 13, "unordered_temporal_weight_pair": [5, 8], "wt(T(u))": 8, "wt(u)": 5}, "violated_conclusions": ["T²(u)"], "witness": {"actual": [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], "c": 0, "claimed": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], "d": 0, "i": 0, "j": 0, "operation": "forward", "relation": "T²(u)=u", "u": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0], "x": [0, 1, 0, 0, 1], "z": [1, 1, 0, 1, 0, 0, 1]}}
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

No Palomar bundle: Challenge.lean does not elaborate: C:\Users\Augusto\mathforge-lean\MathForge\c4_Challenge.lean:74:19: error: unsolved goals.
