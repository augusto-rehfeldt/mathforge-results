#!/usr/bin/env python3
import itertools
import time

LIMIT_SECONDS = 220.0


def kunz(a):
    m = len(a) + 1
    for i in range(1, m):
        for j in range(1, m):
            s = i + j
            if s < m and a[i - 1] + a[j - 1] < a[s - 1]:
                return False
            if s > m and a[i - 1] + a[j - 1] + 1 < a[s - m - 1]:
                return False
    return True


def member(x, a):
    if x < 0:
        return False
    m = len(a) + 1
    r = x % m
    return r == 0 or x >= r + m * a[r - 1]


def maximal(a):
    m = len(a) + 1
    w = [0] + [i + m * a[i - 1] for i in range(1, m)]
    return {
        i for i in range(1, m)
        if not any(i != j and member(w[j] - w[i], a)
                   for j in range(1, m))
    }


def generator(x, a):
    return member(x, a) and x > 0 and not any(
        member(y, a) and member(x - y, a) for y in range(1, x)
    )


def literal_formula(a, p, r):
    m = len(a) + 1
    w = [0] + [i + m * a[i - 1] for i in range(1, m)]
    C = set()
    for j in range(1, m):
        if j in (p, r):
            continue
        k = (r - j) % m
        epsilon = int(j > r)
        if (a[j - 1] + a[k - 1] + epsilon == 3
                and generator(w[k], a)
                and not member(w[p] - w[j], a)):
            C.add(j)
    R = {r} if not member(w[p] - (w[r] - m), a) else set()
    return C, R


# Independent finite-set implementation: explicitly enumerate S up to a bound.
def brute_data(a):
    m = len(a) + 1
    w = {i: i + m * a[i - 1] for i in range(1, m)}
    bound = max(w.values())
    S = set(range(0, bound + 1, m))
    for x in w.values():
        S.update(range(x, bound + 1, m))
    maxima = {
        i for i in w
        if not any(i != j and w[j] - w[i] in S for j in w)
    }
    generators = {
        i for i, x in w.items()
        if not any(y in S and x - y in S for y in range(1, x))
    }
    valid = True
    for i, x in w.items():
        for j, y in w.items():
            residue = (i + j) % m
            if residue and x + y < w[residue]:
                valid = False
    return w, S, maxima, generators, valid


def comparison(a, p, r, brute=False):
    m = len(a) + 1
    b = list(a)
    b[r - 1] = 2
    b = tuple(b)

    if brute:
        w, S, old_max, generators, old_valid = brute_data(a)
        assert old_valid and old_max == {p, r} and a[r - 1] == 3
        C = set()
        for j in range(1, m):
            if j in (p, r):
                continue
            k = (r - j) % m
            epsilon = 0 if j < r else 1
            if (a[j - 1] + a[k - 1] + epsilon == 3
                    and k in generators
                    and w[p] - w[j] not in S):
                C.add(j)
        R = {r} if w[p] - (w[r] - m) not in S else set()
        _, _, new_max, _, new_valid = brute_data(b)
    else:
        C, R = literal_formula(a, p, r)
        new_max = maximal(b)
        new_valid = kunz(b)

    D = C | R
    expected = {
        "Kunz(b)": True,
        "maximal_indices(b)": sorted({p} | D),
        "exactly_two_maximal_indices": len(D) == 1,
    }
    actual = {
        "Kunz(b)": new_valid,
        "maximal_indices(b)": sorted(new_max),
        "exactly_two_maximal_indices": len(new_max) == 2,
    }
    if len(D) == 1:
        q = next(iter(D))
        expected["genus(b)"] = sum(a) - 1
        expected["maximal_residue_gap(b)"] = abs(p - q)
        actual["genus(b)"] = sum(b)
        actual["maximal_residue_gap(b)"] = (
            abs(max(new_max) - min(new_max)) if len(new_max) == 2 else None
        )
    return expected, actual, C, R, b


def sanity():
    known_ok = (
        kunz((1, 1, 1))
        and maximal((1, 1, 1)) == {1, 2, 3}
        and all(generator(x, (1, 1, 1)) for x in (4, 5, 6, 7))
        and kunz((1, 2))
        and maximal((1, 2)) == {2}
        and generator(4, (1, 2))
        and not generator(8, (1, 2))
    )
    print("Sanity 1: known small semigroups:", "PASS" if known_ok else "FAIL")
    if not known_ok:
        print("SANITY FAILED")
        return False

    checked = 0
    for m in range(3, 6):
        for a in itertools.product((1, 2, 3), repeat=m - 1):
            w, S, maxima, generators, valid = brute_data(a)
            ok = kunz(a) == valid
            if valid:
                ok = ok and maximal(a) == maxima
                ok = ok and all(
                    member(x, a) == (x in S)
                    for x in range(max(w.values()) + 1)
                )
                ok = ok and {
                    i for i in w if generator(w[i], a)
                } == generators
                if len(maxima) == 2:
                    for r in sorted(maxima):
                        if a[r - 1] == 3:
                            p = next(iter(maxima - {r}))
                            ok = ok and comparison(a, p, r) == comparison(
                                a, p, r, brute=True
                            )
            checked += 1
            if not ok:
                print("Sanity 2: finite-set cross-check: FAIL", m, a)
                print("SANITY FAILED")
                return False
    print("Sanity 2: finite-set cross-check: PASS;", checked, "vectors")
    return True


def main():
    if not sanity():
        return
    start = time.monotonic()
    vectors = 0
    cases = 0
    completed = []
    for m in range(3, 12):
        count_m = 0
        last = None
        for a in itertools.product((1, 2, 3), repeat=m - 1):
            if vectors % 1024 == 0 and time.monotonic() - start >= LIMIT_SECONDS:
                print("NO COUNTEREXAMPLE")
                print("Fully checked m:", completed)
                if count_m:
                    print("Partially checked m:", m,
                          "; lexicographic prefix ending at:", last,
                          "; vectors in prefix:", count_m)
                print("Coordinates: {1,2,3}; all eligible choices of r and p.")
                print("Vectors checked:", vectors, "; cases tested:", cases)
                return
            vectors += 1
            count_m += 1
            last = a
            if not kunz(a):
                continue
            maxima = maximal(a)
            if len(maxima) != 2:
                continue
            for r in sorted(maxima):
                if a[r - 1] != 3:
                    continue
                p = next(iter(maxima - {r}))
                cases += 1
                expected, actual, C, R, b = comparison(a, p, r)
                if expected != actual:
                    expected2, actual2, C2, R2, b2 = comparison(
                        a, p, r, brute=True
                    )
                    if expected2 != actual2:
                        print("COUNTEREXAMPLE:")
                        print({"m": m, "a": a, "p": p, "r": r,
                               "b": b2, "C": sorted(C2), "R": sorted(R2)})
                        print("Claimed side:", expected2)
                        print("Brute-force side:", actual2)
                        return
                    print("SANITY FAILED")
                    return
        completed.append(m)
    print("NO COUNTEREXAMPLE")
    print("Exact range: 3 <= m <= 11; every a in {1,2,3}^{m-1}; "
          "all eligible choices of r and p.")
    print("Vectors checked:", vectors, "; cases tested:", cases)


if __name__ == "__main__":
    main()