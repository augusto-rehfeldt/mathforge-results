#!/usr/bin/env python3
import itertools

WITNESS = {
    "source_order": 0,
    "target_order": 1,
    "H": (
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 1),
        (0, 0, 0),
    ),
    "I": ((0, 0, 0), (0, 1, 0)),
    "monomial_exponents_(t,x1,x2,x3)": (1, 1, 0, 0),
    "defined_F_coefficient": 0,
    "claimed_recurrence_coefficient": 1,
    "recomputed_by_exhaustive_matrix_and_image_enumeration": True,
}

VECTORS = tuple(itertools.product((0, 1), repeat=3))


def xor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def image(A):
    """Enumerate the image directly, using every possible input vector."""
    n = len(A)
    return frozenset(
        tuple(sum(A[i][j] * z[j] for j in range(n)) % 2
              for i in range(n))
        for z in itertools.product((0, 1), repeat=n)
    )


def matrices(n):
    """Enumerate exactly M_n, testing A^2 = 0 directly."""
    positions = [
        (i, j) for i in range(n) for j in range(n)
        if 1 <= j - i <= 3
    ]
    for bits in itertools.product((0, 1), repeat=len(positions)):
        A = [[0] * n for _ in range(n)]
        for (i, j), bit in zip(positions, bits):
            A[i][j] = bit
        if all(
            sum(A[i][k] * A[k][j] for k in range(n)) % 2 == 0
            for i in range(n) for j in range(n)
        ):
            yield tuple(tuple(row) for row in A)


def state_and_exponents(A):
    n = len(A)

    def entry(i, j):
        # Here i and j are the statement's one-based indices.
        return A[i - 1][j - 1] if 1 <= i <= n and 1 <= j <= n else 0

    H = tuple(
        tuple(entry(n - 6 + r, n - 3 + c) for c in range(1, 4))
        for r in range(1, 7)
    )
    im = image(A)
    I = set()
    for u in VECTORS:
        if any(u[c - 1] != 0 and n - 3 + c <= 0
               for c in range(1, 4)):
            continue
        E = [0] * n
        for c in range(1, 4):
            index = n - 3 + c
            if 1 <= index <= n:
                E[index - 1] = u[c - 1]
        if tuple(E) in im:
            I.add(u)

    # An F_2 image of dimension r has exactly 2^r elements.
    rank = len(im).bit_length() - 1
    if len(im) != 2 ** rank:
        raise ValueError("Computed image size is not a power of two")
    degrees = tuple(
        sum(entry(i, i + k) for i in range(1, n + 1))
        for k in (1, 2, 3)
    )
    return (H, frozenset(I)), (rank,) + degrees


def defined_F(n):
    """Store every nonzero coefficient, indexed by state and monomial."""
    coefficients = {}
    for A in matrices(n):
        state, exponents = state_and_exponents(A)
        key = (state, exponents)
        coefficients[key] = coefficients.get(key, 0) + 1
    return coefficients


def literal_recurrence(F):
    result = {}
    for ((H, I), exponents), coefficient in F.items():
        for v in VECTORS:
            if any(sum(row[c] * v[c] for c in range(3)) % 2
                   for row in H):
                continue
            epsilon = 0 if v in I else 1
            first = tuple(H[r][1] for r in range(1, 6)) + (0,)
            second = tuple(H[r][2] for r in range(1, 6)) + (0,)
            third = (0, 0, v[0], v[1], v[2], 0)
            Hp = tuple(zip(first, second, third))

            # I + span(v), computed literally over F_2.
            summed = set(I)
            summed.update(xor(u, v) for u in I)
            Ip = frozenset(
                (a, b, 0)
                for a, b in itertools.product((0, 1), repeat=2)
                if (0, a, b) in summed
            )
            increment = (epsilon, v[2], v[1], v[0])
            ep = tuple(a + b for a, b in zip(exponents, increment))
            key = ((Hp, Ip), ep)
            result[key] = result.get(key, 0) + coefficient
    return result


def reject(reason):
    print("REFUTATION REJECTED:", reason)


def main():
    w = WITNESS
    n, target = w["source_order"], w["target_order"]
    H, raw_I = w["H"], w["I"]
    exponents = w["monomial_exponents_(t,x1,x2,x3)"]

    if type(n) is not int or n < 0:
        reject("Source order is not an integer n >= 0.")
        return
    if type(target) is not int or target != n + 1:
        reject("Target order is not n + 1.")
        return
    if (len(H) != 6 or any(len(row) != 3 for row in H)
            or any(type(b) is not int or b not in (0, 1)
                   for row in H for b in row)):
        reject("H is not a 6-by-3 binary matrix.")
        return
    if any(u not in VECTORS for u in raw_I):
        reject("I contains a vector outside F_2^3.")
        return
    I = frozenset(raw_I)
    if ((0, 0, 0) not in I
            or any(xor(a, b) not in I for a in I for b in I)):
        reject("I is not a subspace of F_2^3.")
        return
    if (len(exponents) != 4
            or any(type(e) is not int or e < 0 for e in exponents)):
        reject("The reported monomial is invalid.")
        return

    # The claim ranges over ALL binary H and subspaces I, including
    # unreachable states. No target-state reachability hypothesis exists.
    F0 = defined_F(0)
    zero_H = tuple((0, 0, 0) for _ in range(6))
    expected_initial = {
        ((zero_H, frozenset({(0, 0, 0)})), (0, 0, 0, 0)): 1
    }
    if F0 != expected_initial:
        reject("Direct definitions do not reproduce the initialization.")
        return

    source = defined_F(n)
    actual = defined_F(target)
    claimed = literal_recurrence(source)
    key = ((H, I), exponents)
    left = actual.get(key, 0)
    right = claimed.get(key, 0)

    if (left != w["defined_F_coefficient"]
            or right != w["claimed_recurrence_coefficient"]):
        reject("Reported coefficients do not match brute force: "
               f"defined side={left}, claimed side={right}.")
    elif left == right:
        reject("The conclusion holds at the reported witness.")
    else:
        print("REFUTATION CONFIRMED:", w,
              "defined side =", left, "claimed side =", right)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        reject(f"Verification failed: {type(exc).__name__}: {exc}")