# Refuted: Every two-collision polynomial pair splits into independently movable collision blocks unless its collisions form a two-by-three arithmetic core

**Verdict: FALSE.** Counterexample: `{'A': (0, 1, 3), 'B': (0, 1, 4)} {'representation_counts': [(0, 1), (1, 2), (2, 1), (3, 1), (4, 2), (5, 1), (7, 1)], 'actual_side': {'I': False, 'II': False, 'exactly_one': False}, 'claimed_side': {'exactly_one': True}}`

**Models:** gpt-6.1-sol (roles under *Models* below)

*The two-collision splitting dichotomy*

*Automated run on the seed topic "Pairs of polynomials P,Q∈Z[x] with coefficients in {0,1}, constant term one, and product coefficients at most two, with exactly two coefficients equal to two; refine by support sizes and the separation of the doubled exponents, and seek support-splitting and translation-gluing identities that track both collisions while excluding new ones.", 2026-10-02 11:21 UTC. Status: `machine-refuted`.*

## Statement

For every pair of finite sets A,B of nonnegative integers containing 0, suppose the number r(s) of pairs (a,b) in A×B with a+b=s is at most 2 for every nonnegative integer s, and equals 2 at exactly two integers. Then exactly one of the following alternatives holds. (I) After possibly exchanging A and B, there is a partition A=U∪V into disjoint nonempty sets with 0 in U such that U+B and V+B are disjoint and each of the two restricted representation functions has exactly one coefficient equal to 2. Write their doubled exponents as c_U and c_V. For every integer T>max(A)+max(B), the supports A_T=U∪{v+T:v in V} and B have sizes |A| and |B|, their product has exactly two doubled exponents c_U and c_V+T, and the separation of these exponents is T+c_V−c_U. (II) After possibly exchanging A and B, there exist nonnegative integers u,v and a positive integer d such that {u,u+d}⊆A and {v,v+d,v+2d}⊆B, and the complete set of pairs participating in doubled coefficients is {(u,v+d),(u+d,v),(u,v+2d),(u+d,v+d)}. In alternative (II), the doubled exponents have separation d and no partition of either support satisfies the splitting conditions in alternative (I).

## Notation

For a finite set S of nonnegative integers, P_S(x)=∑_{s∈S}x^s. Thus P_A and P_B have coefficients in {0,1} and constant term 1. The coefficient of x^s in P_A(x)P_B(x) is r(s)=|{(a,b)∈A×B:a+b=s}|. For sets S,R, S+R={s+r:s∈S,r∈R}. A restricted representation function counts pairs in U×B or V×B. A pair participates in a doubled coefficient when its sum s satisfies r(s)=2. The symbols |S| and max(S) denote cardinality and maximum. The variables U,V,c_U,c_V,T,A_T,u,v,d are quantified in the statement.

## Why it is false

`{'A': (0, 1, 3), 'B': (0, 1, 4)} {'representation_counts': [(0, 1), (1, 2), (2, 1), (3, 1), (4, 2), (5, 1), (7, 1)], 'actual_side': {'I': False, 'II': False, 'exactly_one': False}, 'claimed_side': {'exactly_one': True}}`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem negates the following assertion: For all finite subsets A and B of the natural numbers containing 0, if every sum represented by A×B has at most two representations and exactly two sums have two representations, then exactly one of Alternative I and Alternative II holds. Alternative I permits exchanging A and B and requires a disjoint nonempty partition A=U∪V with 0∈U, disjoint sumsets U+B and V+B, and precisely one doubled sum cU and cV in each part. For every natural T greater than max(A)+max(B), shifting V by T preserves the support sizes, gives precisely the doubled sums cU and cV+T, and gives distance T+cV−cU. Alternative II permits exchanging A and B and requires natural u,v and positive d with {u,u+d}⊆A and {v,v+d,v+2d}⊆B, exactly the four specified participating pairs, doubled-sum distance d, and failure of Alternative I.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'A': (0, 1, 3), 'B': (0, 1, 4)} {'representation_counts': [(0, 1), (1, 2), (2, 1), (3, 1), (4, 2), (5, 1), (7, 1)], 'actual_side': {'I': False, 'II': False, 'exactly_one': False}, 'claimed_side': {'exactly_one': True}}
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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `pairs-of-polynomials-p-q-z-x-with-coefficients-i-c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
