# Refuted: Equal-height triple contacts permit middle-block reversal, preserving areas while exchanging pair-only shared peaks and valleys

**Verdict: FALSE.** Counterexample: `{'n': 2, 'a': 1, 'b': 3, 'H': 1, 'A': 0, 'B': 1, 'L': [2], 'U': [], 'p12': 0, 'v12': 1, 'p23': 0, 'v23': 0} first cardinality = 1 second cardinality = 0`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Middle-block reciprocity for pair-only contacts*

*Automated run on the seed topic "Ordered triples of Dyck paths of the same semilength such that the first lies weakly below the second, the second lies weakly below the third, and exactly two internal vertices are shared by all three, refined by the two contact positions and the areas between adjacent paths; look for contact-cutting convolution identities and segment-reversal symmetries that track contacts shared by only two paths.", 2026-10-02 02:32 UTC. Status: `machine-refuted`.*

## Statement

Conjecture: For every integer n≥2, integers 1≤a<b≤2n−1, integer H≥0, nonnegative integers A and B, subsets L and U of {1,…,2n−1}\{a,b}, and nonnegative integers p12,v12,p23,v23, the following two finite sets have equal cardinality. The first consists of ordered Dyck triples with exactly two internal triple contacts, at a and b, both at height H; adjacent areas A and B; pair-only contact sets L and U; and middle-block shared-peak and shared-valley counts (p12,v12,p23,v23). The second has the same requirements except that its pair-only contact sets are R(L) and R(U), and its four counts are (v12,p12,v23,p23).

## Notation

A Dyck path of semilength n is a function h:{0,…,2n}→Z≥0 with h(0)=h(2n)=0 and h(t+1)−h(t)∈{−1,1}. An ordered Dyck triple is (h1,h2,h3) with h1(t)≤h2(t)≤h3(t) for every t. An internal triple contact is an integer t with 1≤t≤2n−1 and h1(t)=h2(t)=h3(t). The adjacent areas are A=∑_{t=0}^{2n}(h2(t)−h1(t))/2 and B=∑_{t=0}^{2n}(h3(t)−h2(t))/2; these are integers because all three heights have parity t. The pair-only contact sets are L={t:1≤t≤2n−1, h1(t)=h2(t)<h3(t)} and U={t:1≤t≤2n−1, h1(t)<h2(t)=h3(t)}. For any subset S of the internal times, R(S)={r(t):t∈S}, where r(t)=a+b−t if a<t<b and r(t)=t otherwise. A path has a peak at t if h(t−1)=h(t+1)=h(t)−1, and a valley if h(t−1)=h(t+1)=h(t)+1. The integer p12 counts times t∈L with a<t<b at which both h1 and h2 have peaks; v12 counts such times with both having valleys. Define p23 and v23 identically using U and paths h2,h3. All counts refer only to these strictly interior middle-block times.

## Why it is false

`{'n': 2, 'a': 1, 'b': 3, 'H': 1, 'A': 0, 'B': 1, 'L': [2], 'U': [], 'p12': 0, 'v12': 1, 'p23': 0, 'v23': 0} first cardinality = 1 second cardinality = 0`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following universal assertion: For all integers n,a,b,H, natural numbers A,B,p12,v12,p23,v23, and finite sets L,U of natural-number times, if n≥2, 1≤a<b≤2n−1, H≥0, and L,U contain only internal times other than a,b, then two families of ordered triples of nonnegative, balanced up/down paths of length 2n have equal cardinality. The first family has exactly the internal triple contacts a,b, with common height H at both; adjacent areas A,B; pair-only contact sets L,U; and shared peak/valley counts p12,v12,p23,v23 strictly between a and b. The second has the same conditions, but reflects both contact sets by t↦a+b−t strictly between a and b, fixes their other times, and swaps each pair’s peak and valley counts.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'n': 2, 'a': 1, 'b': 3, 'H': 1, 'A': 0, 'B': 1, 'L': [2], 'U': [], 'p12': 0, 'v12': 1, 'p23': 0, 'v23': 0} first cardinality = 1 second cardinality = 0
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `ordered-triples-of-dyck-paths-of-the-same-semile-c2` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
