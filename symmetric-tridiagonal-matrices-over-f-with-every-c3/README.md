# Refuted: Exactly nine boundary types determine both generalized kernel dimensions of every mirrored concatenation

**Verdict: FALSE.** Counterexample: `{'relation': 'identity', 'u': (0,), 'v': (0, 1), 'matrix_dimension': 4} direct = (0, 0) claimed = (0, 1)`

**Models:** gpt-6.1-sol (roles under *Models* below)

*Nine boundary types for mirrored concatenation*

*Automated run on the seed topic "Symmetric tridiagonal matrices over F₂ with every superdiagonal and subdiagonal entry equal to one, refined by dimension and the pair (dim ker M², dim ker (M+I)²); look for concatenation identities for their diagonal words that track both generalized kernels through explicit boundary data.", 2026-10-02 10:27 UTC. Status: `machine-refuted`.*

## Statement

For every nonempty binary word u, define B(u)=(p_u(0),q_u(0),p_u(1),q_u(1)). Conjecturally, B assumes exactly the nine values in ({(0,1),(1,0),(1,1)})², and the following identity and completeness assertion hold. For every pair of nonempty binary words u,v and every a in {0,1}, put f_a(x)=p_u(a)p_v(x)+q_u(a)r_v(x), with arithmetic in F₂[x]. Then dim ker((M(uv rev(u))+aI)²) equals 0 if f_a(a)=1, equals 1 if f_a(a)=0 and f_a'(a)=1, and equals 2 otherwise. Consequently, for every two nonempty binary words u,w, B(u)=B(w) if and only if, for every nonempty binary word v, the ordered pairs of generalized kernel dimensions of M(uv rev(u)) and M(wv rev(w)) agree. The dimension of the first matrix is exactly 2|u|+|v|.

## Notation

F₂ is the field with two elements. A binary word t=t₁…tₙ is a finite sequence with each tᵢ in F₂; |t|=n. M(t) is the n-by-n matrix over F₂ whose diagonal is t, whose entries immediately above and below the diagonal are 1, and whose other entries are 0. I is the identity matrix of the appropriate size. Concatenation is juxtaposition, and rev(t) reverses t. Set p_t(x)=det(xI+M(t)), with p_empty(x)=1. For nonempty t, q_t(x) is p evaluated on the word obtained by deleting t's last letter. For |t|≥2, r_t(x) is p evaluated on the word obtained by deleting both its first and last letters; for |t|=1, set r_t(x)=0. A prime denotes formal polynomial differentiation. Kernel dimensions are over F₂. The ordered pair associated with a matrix A is (dim ker A², dim ker(A+I)²). The displayed Cartesian square lists the pairs (p_u(0),q_u(0)) and (p_u(1),q_u(1)) in that order.

## Why it is false

`{'relation': 'identity', 'u': (0,), 'v': (0, 1), 'matrix_dimension': 4} direct = (0, 0) claimed = (0, 1)`

## Machine verification

- Adversarial search (`*_falsify.py`) reported the witness.
- Independent re-check (`*_confirm.py`, a separate model call, definitions re-implemented from the statement): confirmed.
- Lean 4 + Mathlib: compiled, sorry-free (`0` occurrences of the token in the source, none reported by the elaborator).
- Back-translation of the Lean statement: **FAITHFUL**. The theorem states that Claim is false. Claim asserts three things: (1) the values of B on nonempty lists over ZMod 2 are exactly all ordered pairs of pairs whose components are each (0,1), (1,0), or (1,1); (2) for all nonempty words u and v, the word u ++ v ++ reverse(u) has length 2|u|+|v|, and for every a in ZMod 2, the dimension of the kernel of the squared action of M+aI is 0 when f(a)=1, 1 when f(a)=0 and f'(a)=1, and 2 otherwise, where f=p_u(a)p_v+q_u(a)r_v; (3) for all nonempty u and w, B(u)=B(w) exactly when their sandwiches with every nonempty v have equal ordered kernel dimensions at shifts 0 and 1. Here p is defined by the continuant recurrence, q deletes the last letter, r deletes both endpoints for length at least two and is zero otherwise, and kernel dimension is computed as the base-two logarithm of the kernel's cardinality.

Re-check output (tail):

```
REFUTATION CONFIRMED: {'relation': 'identity', 'u': (0,), 'v': (0, 1), 'matrix_dimension': 4} direct = (0, 0) claimed = (0, 1)
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

No Palomar bundle: Challenge.lean does not elaborate: C:\Users\Augusto\mathforge-lean\MathForge\c3_Challenge.lean:85:0: error: Unexpected name.
