#!/usr/bin/env python3
import itertools
import time
from collections import Counter

START = time.monotonic()
TIME_LIMIT = 220.0
MAX_ORDER = 9


def positions(n):
    return [(i, j) for i in range(n)
            for j in range(i + 1, min(n, i + 4))]


def matrix_from_mask(n, mask):
    A = [[0] * n for _ in range(n)]
    for k, (i, j) in enumerate(positions(n)):
        A[i][j] = (mask >> k) & 1
    return A


def square_zero(A):
    n = len(A)
    return all(
        sum(A[i][k] * A[k][j] for k in range(n)) % 2 == 0
        for i in range(n) for j in range(n)
    )


def image(A):
    """Plain enumeration of every input vector, not Gaussian elimination."""
    n = len(A)
    return {
        tuple(sum(A[i][j] * ((z >> j) & 1)
                  for j in range(n)) % 2 for i in range(n))
        for z in range(1 << n)
    }


def rank_elimination(A):
    rows = [sum(bit << j for j, bit in enumerate(row)) for row in A]
    rank = 0
    for j in range(len(A)):
        pivot = next((i for i in range(rank, len(rows))
                      if (rows[i] >> j) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> j) & 1):
                rows[i] ^= rows[rank]
        rank += 1
    return rank


VECTORS = list(itertools.product((0, 1), repeat=3))


def boundary(A):
    n = len(A)
    H = tuple(
        tuple(A[i][j] if 0 <= i < n and 0 <= j < n else 0
              for j in range(n - 3, n))
        for i in range(n - 6, n)
    )
    im = image(A)
    I = []
    for u in VECTORS:
        if any(u[c] and n - 3 + c < 0 for c in range(3)):
            continue
        e = [0] * n
        for c in range(3):
            if 0 <= n - 3 + c < n:
                e[n - 3 + c] = u[c]
        if tuple(e) in im:
            I.append(u)
    return H, tuple(sorted(I))


def monomial(A, plain=False):
    n = len(A)
    rank = (len(image(A)).bit_length() - 1
            if plain else rank_elimination(A))
    return (rank,) + tuple(
        sum(A[i][i + k] for i in range(n - k))
        for k in (1, 2, 3)
    )


def claimed_transition(H, I, v):
    if any(sum(H[r][c] * v[c] for c in range(3)) % 2
           for r in range(6)):
        return None
    third = (0, 0, v[0], v[1], v[2], 0)
    Hp = tuple(
        (H[r + 1][1] if r < 5 else 0,
         H[r + 1][2] if r < 5 else 0,
         third[r])
        for r in range(6)
    )
    summed = {
        tuple(u[c] ^ (b * v[c]) for c in range(3))
        for u in I for b in (0, 1)
    }
    Ip = tuple(sorted((a, b, 0)
                      for a, b in itertools.product((0, 1), repeat=2)
                      if (0, a, b) in summed))
    return (Hp, Ip), (int(v not in I), v[2], v[1], v[0])


def enumerate_order(n, plain=False):
    result = Counter()
    retained = 0
    for mask in range(1 << len(positions(n))):
        A = matrix_from_mask(n, mask)
        if square_zero(A):
            retained += 1
            result[(boundary(A), monomial(A, plain))] += 1
    return result, retained


def claimed_polynomial(F):
    result = Counter()
    cases = 0
    for (state, powers), coefficient in F.items():
        H, I = state
        for v in VECTORS:
            cases += 1
            transition = claimed_transition(H, I, v)
            if transition is not None:
                target, increment = transition
                exponent = tuple(a + b for a, b in zip(powers, increment))
                result[(target, exponent)] += coefficient
    return result, cases


def sanity():
    # Independent known enumeration counts.
    counts = [enumerate_order(n)[1] for n in range(4)]
    ok1 = counts == [1, 1, 2, 6]
    print("Sanity 1: orders 0..3 counts =", counts,
          "PASS" if ok1 else "FAIL")

    # Gaussian rank versus exhaustive image enumeration, including matrices
    # that do not satisfy A^2=0.
    tested = 0
    ok2 = True
    for n in range(5):
        for mask in range(1 << len(positions(n))):
            A = matrix_from_mask(n, mask)
            tested += 1
            if rank_elimination(A) != len(image(A)).bit_length() - 1:
                ok2 = False
    print("Sanity 2: rank versus exhaustive image on",
          tested, "matrices:", "PASS" if ok2 else "FAIL")
    if not (ok1 and ok2):
        print("SANITY FAILED")
        raise SystemExit(0)


def plain_claim_coefficient(n, wanted):
    """Recompute one recurrence coefficient directly from individual matrices."""
    total = 0
    for mask in range(1 << len(positions(n))):
        A = matrix_from_mask(n, mask)
        if not square_zero(A):
            continue
        H, I = boundary(A)
        powers = monomial(A, plain=True)
        for v in VECTORS:
            transition = claimed_transition(H, I, v)
            if transition is None:
                continue
            target, increment = transition
            key = (target, tuple(a + b for a, b in zip(powers, increment)))
            if key == wanted:
                total += 1
    return total


def plain_actual_coefficient(n, wanted):
    total = 0
    for mask in range(1 << len(positions(n))):
        A = matrix_from_mask(n, mask)
        if square_zero(A):
            if (boundary(A), monomial(A, plain=True)) == wanted:
                total += 1
    return total


def main():
    sanity()
    F, retained = enumerate_order(0)
    cases = 0
    checked = []
    for n in range(MAX_ORDER):
        if time.monotonic() - START > TIME_LIMIT:
            break
        predicted, tested = claimed_polynomial(F)
        cases += tested
        actual, retained_next = enumerate_order(n + 1)
        checked.append((n, n + 1))
        for key in sorted(set(actual) | set(predicted)):
            if actual[key] == predicted[key]:
                continue
            direct_again = plain_actual_coefficient(n + 1, key)
            claim_again = plain_claim_coefficient(n, key)
            if (direct_again != claim_again
                    and direct_again == actual[key]
                    and claim_again == predicted[key]):
                state, powers = key
                print("COUNTEREXAMPLE:",
                      {"source_order": n,
                       "target_order": n + 1,
                       "H": state[0],
                       "I": state[1],
                       "monomial_exponents_(t,x1,x2,x3)": powers,
                       "defined_F_coefficient": direct_again,
                       "claimed_recurrence_coefficient": claim_again,
                       "recomputed_by_exhaustive_matrix_and_image_enumeration": True})
                return
            print("SANITY FAILED")
            return
        F = actual
        retained += retained_next
    print("NO COUNTEREXAMPLE",
          {"orders_checked": list(range(len(checked) + 1)),
           "transitions_checked": checked,
           "retained_matrices": retained,
           "state_monomial_vector_cases_tested": cases})


if __name__ == "__main__":
    main()