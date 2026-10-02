# Refuted: Period-two words containing consecutive zeros decompose into four block types, yielding an explicit weight-refined necklace gluing formula

**Verdict: FALSE.** Counterexample: `1110100; period-two brute_force=True, claimed=False; blocks=['11101']; M(7,1,4,4,2) brute_force=14, claimed=0`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Zero-gap gluing formula for period-two necklaces*

*Automated run on the seed topic "Binary necklaces of exact temporal period two under the cyclic update T(x)_i=x_i+x_{i-1}x_{i+1} over F₂, refined by length, the unordered pair of Hamming weights of x and T(x), and the number of changed positions; look for cutting-and-gluing identities with explicit boundary bits that preserve T²(x)=x while excluding fixed points.", 2026-10-02 10:42 UTC. Status: `machine-refuted`.*

## Statement

Conjecture: For every integer n≥3, a cyclic binary word x of length n containing consecutive zeros has exact temporal period two if and only if cutting at every maximal zero run of length at least two leaves blocks belonging to {1,11,111,101}, with at least one block belonging to {111,101}. Moreover, for all integers k≥1, a≥0, b≥0 and c≥1, let M(n,k,a,b,c) be the sum of n/s(N) over all binary necklaces N of length n whose representatives x have exact temporal period two, exactly k maximal zero runs of length at least two, unordered weight pair {a,b}, and exactly c changed positions. Then M(n,k,a,b,c) equals (n/k) times the coefficient of t^n u^a v^b q^c in P^k when a=b, and equals (n/k) times the sum of the coefficients of t^n u^a v^b q^c and t^n u^b v^a q^c in P^k when a≠b, where P=(t²/(1−t))(tuv+t²u²v²+t³q(u³v²+u²v³)).

## Notation

Indices of x=(x_0,...,x_{n−1}) are taken modulo n. Arithmetic in T(x)_i=x_i+x_{i−1}x_{i+1} is over F₂. Exact temporal period two means T(T(x))=x and T(x)≠x. The Hamming weight w(x) is the number of entries equal to 1; the unordered weight pair is {w(x),w(T(x))}. The changed-position count is |{i:T(x)_i≠x_i}|. A necklace is an equivalence class under cyclic rotation. Its rotational stabilizer size s(N) is the number of rotations fixing any representative, so n/s(N) counts its distinct representatives. A maximal zero run is a cyclically consecutive string of zeros bounded by ones; an all-zero word has one zero run and no remaining block. Cutting removes all maximal zero runs of length at least two; remaining blocks are read between successive removed runs. The symbols t,u,v,q are formal indeterminates, and coefficient extraction uses the formal expansion 1/(1−t)=Σ_{j≥0}t^j. The notation {a,b} denotes an unordered pair allowing repetition.

## Why it is false

`1110100; period-two brute_force=True, claimed=False; blocks=['11101']; M(7,1,4,4,2) brute_force=14, claimed=0`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following conjunction: (1) For every natural n ≥ 3 and every cyclic Boolean word x of length n containing adjacent zeros, applying the specified Boolean update twice returns x, but applying it once does not, if and only if every block between maximal zero runs of length at least two is one of 1, 11, 111, 101, and at least one block is 111 or 101. (2) For every natural n ≥ 3, k ≥ 1, a,b ≥ 0, and c ≥ 1, the number of indexed words with exact temporal period two, k long zero runs, unordered weight pair {a,b}, and c changed positions equals n/k times the specified coefficient count, using one coefficient when a=b and the sum of the two weight-swapped coefficients otherwise. The coefficient count enumerates ordered choices of k zero runs of length at least two and the four monomial types in P.

Re-check output (tail):

```
REFUTATION CONFIRMED: 1110100; period-two brute_force=True, claimed=False; blocks=['11101']; M(7,1,4,4,2) brute_force=14, claimed=0
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `binary-necklaces-of-exact-temporal-period-two-un-c1` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
