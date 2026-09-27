# Refuted: Every self-complementary Sidon family with given sum and maximum has even cardinality

**Verdict: FALSE.** Counterexample: `n=7 k=3 s=12 m=7 2*s=24 k*(m+1)=24 N=1 N_even=False sets=[(2, 3, 7)]`

**Models:** muse-spark-1.3-contributor-free (roles under *Models* below)

*Even parity of self-mirror Sidon counts with fixed sum and maximum*

*Automated run on the seed topic "Sidon (B_2) subsets of {1,...,n} and of cyclic groups Z_n, with all pairwise sums distinct, refined by cardinality, element sum, and maximal element, looking for enumerative identities, recurrences across n, modular counting congruences, and translation, reflection, and dilation equinumerosity relations together with interval-to-cyclic lifting identities.", 2026-09-27 15:51 UTC. Status: `machine-refuted`.*

## Statement

For all integers n >= 1, k >= 3, m >= 1, and s >= 1 with m <= n, if 2*s = k*(m+1) then N(n,k,s,m) is even, where N(n,k,s,m) is the number of subsets A of {1,...,n} with |A| = k, sum(A) = s, max(A) = m, and all sums a+b with a,b in A and a <= b pairwise distinct.

## Notation

n is the interval bound; {1,...,n} is the ground set; k is cardinality; s = sum of elements of A; m = largest element of A; Sidon means the k*(k+1)/2 sums a+b with a <= b are all distinct; N(n,k,s,m) counts such sets A.

## Why it is false

`n=7 k=3 s=12 m=7 2*s=24 k*(m+1)=24 N=1 N_even=False sets=[(2, 3, 7)]`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. For all natural numbers n, k, s, m with n >= 1, k >= 3, m >= 1, s >= 1 and m <= n, if 2*s = k*(m+1) then N(n,k,s,m) is even, where N(n,k,s,m) is the number of k-element subsets A of {1,...,n} such that the sum of A equals s, the supremum of A equals m, and A satisfies IsSidon, meaning the sums a+b for pairs (a,b) in A x A with a <= b are all pairwise distinct.

Re-check output (tail):

```
REFUTATION CONFIRMED: n=7 k=3 s=12 m=7 2*s=24 k*(m+1)=24 N=1 N_even=False sets=[(2, 3, 7)]
```

## Models

- Proposed the claim: muse-spark-1.3-contributor-free
- Counterexample search: muse-spark-1.3-contributor-free
- Independent re-check of the witness: muse-spark-1.3-contributor-free
- Lean formalization: muse-spark-1.3-contributor-free
- Faithfulness judge: muse-spark-1.3-contributor-free

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

This folder is a Lake project for the [Palomar registry](https://palomar-registry.org/). To submit it, use the [form](https://submit.palomar-registry.org/) with this repository, the commit, and `sidon-b-2-subsets-of-1-n-and-of-cyclic-groups-z--c4` as the project path. Read `Challenge.lean` against the statement first: Palomar asks for human review, and none has been done.
