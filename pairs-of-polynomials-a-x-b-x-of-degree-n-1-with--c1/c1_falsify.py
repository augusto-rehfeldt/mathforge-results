#!/usr/bin/env python3
import sys
from collections import defaultdict

MIN_N, MAX_N = 3, 12


def signs(n, mask):
    # Bit i means coefficient i is -1. Bit 0 is always zero.
    return tuple(-1 if (mask >> i) & 1 else 1 for i in range(n))


def direct_correlations(a, b):
    n = len(a)
    return tuple(
        sum(a[i] * a[i + k] + b[i] * b[i + k]
            for i in range(n - k))
        for k in range(1, n)
    )


def fast_single_correlations(n, mask):
    return tuple(
        n - k - 2 * (
            ((mask ^ (mask >> k)) & ((1 << (n - k)) - 1)).bit_count()
        )
        for k in range(1, n)
    )


def retain_pair(ra, rb):
    d = e = c = 0
    for k, (u, v) in enumerate(zip(ra, rb), 1):
        r = u + v
        if not r:
            continue
        if d == 0:
            d, c = k, r
        elif e == 0:
            e = k
            if r != -c:
                return None
        else:
            return None
    return (d, e, c) if e else None


def direct_retention(r):
    nonzero = [(k, value) for k, value in enumerate(r, 1) if value]
    if len(nonzero) != 2:
        return None
    (d, c), (e, other) = nonzero
    return (d, e, c) if other == -c else None


def failures(n, d, e, c, h):
    result = []
    if n % 2:
        result.append(("n % 2", n % 2, 0))
    if c % 2:
        result.append(("c % 2", c % 2, 0))
    # Use integer-scaled relations to express n/2 exactly.
    if c % 4 == 0:
        if 2 * h != n:
            result.append(("2*h = n", 2 * h, n))
    else:
        if d + e != n:
            result.append(("d+e = n", d + e, n))
        allowed = (n - 4, n, n + 4)
        if 2 * h not in allowed:
            result.append(("2*h in {n-4,n,n+4}", 2 * h, allowed))
    return result


def plain_laurent_product(a, b):
    coefficients = defaultdict(int)
    for vector in (a, b):
        for i in range(len(vector)):
            for j in range(len(vector)):
                coefficients[i - j] += vector[i] * vector[j]
    return {k: v for k, v in coefficients.items() if v}


def sanity():
    a = (1, 1, 1, -1)
    b = (1, 1, -1, 1)
    ok = (
        direct_correlations(a, b) == (0, 0, 0)
        and plain_laurent_product(a, b) == {0: 8}
        and sum(u != v for u, v in zip(a, b)) == 2
        and direct_correlations((1, 1, 1), (1, -1, 1)) == (0, 2)
    )
    print("Sanity 1: known small correlations:", "PASS" if ok else "FAIL")
    if not ok:
        print("SANITY FAILED")
        sys.exit(0)

    checked = 0
    for n in range(3, 6):
        masks = range(0, 1 << n, 2)
        vectors = [(m, signs(n, m), fast_single_correlations(n, m))
                   for m in masks]
        for ma, a, ra in vectors:
            for mb, b, rb in vectors:
                direct = direct_correlations(a, b)
                fast = tuple(u + v for u, v in zip(ra, rb))
                if (direct != fast
                        or direct_retention(direct) != retain_pair(ra, rb)
                        or (ma ^ mb).bit_count()
                        != sum(u != v for u, v in zip(a, b))):
                    print("Sanity 2: exhaustive independent cross-check: FAIL")
                    print("SANITY FAILED")
                    sys.exit(0)
                checked += 1
    print("Sanity 2: exhaustive independent cross-check: PASS;",
          checked, "ordered pairs")


def main():
    sanity()
    tested = retained = 0

    for n in range(MIN_N, MAX_N + 1):
        records = [
            (mask, fast_single_correlations(n, mask))
            for mask in range(0, 1 << n, 2)
        ]
        for ma, ra in records:
            for mb, rb in records:
                tested += 1
                candidate = retain_pair(ra, rb)
                if candidate is None:
                    continue

                retained += 1
                d, e, c = candidate
                h = (ma ^ mb).bit_count()
                bad = failures(n, d, e, c, h)
                if not bad:
                    continue

                # Independent, plain recomputation before reporting.
                a, b = signs(n, ma), signs(n, mb)
                direct = direct_correlations(a, b)
                verified = direct_retention(direct)
                h2 = sum(a[i] != b[i] for i in range(n))
                expected = {0: 2 * n, d: c, -d: c, e: -c, -e: -c}
                valid = (
                    3 <= n and 1 <= d < e < n and c != 0
                    and verified == candidate
                    and plain_laurent_product(a, b) == expected
                    and h2 == h
                )
                bad2 = failures(n, d, e, c, h2)
                if not valid or bad2 != bad:
                    print("SANITY FAILED")
                    sys.exit(0)

                print("COUNTEREXAMPLE:",
                      {"n": n, "A": a, "B": b,
                       "d": d, "e": e, "c": c, "h": h2,
                       "failures (relation, actual, claimed)": bad2})
                return

    print(
        "NO COUNTEREXAMPLE",
        f"n={MIN_N}..{MAX_N}; all ordered sign-vector pairs with a_0=b_0=1;",
        "1<=d<e<n; c!=0; exactly two opposite nonzero correlations;",
        f"cases tested={tested}; hypothesis-satisfying cases={retained}"
    )


if __name__ == "__main__":
    main()