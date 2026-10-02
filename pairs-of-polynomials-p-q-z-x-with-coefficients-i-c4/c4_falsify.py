import itertools
import time
import sys

LIMIT = 225.0
MAX_ELEMENT = 14
MAX_SIZE = 6


def plain_counts(A, B):
    counts = {}
    for a in A:
        for b in B:
            s = a + b
            counts[s] = counts.get(s, 0) + 1
    return counts


def mask(S):
    return sum(1 << x for x in S)


def fast_counts(A, bmask):
    """Return support, doubled support, and whether any coefficient exceeds 2."""
    seen = doubled = 0
    for a in A:
        row = bmask << a
        if row & doubled:
            return 0, 0, True
        doubled |= seen & row
        seen |= row
    return seen, doubled, False


def partitions(A):
    # Fix 0 in U, as required, and enumerate every possible nonempty V.
    n = len(A) - 1
    for bits in range(1, 1 << n):
        U = (0,) + tuple(A[k + 1] for k in range(n)
                         if not (bits >> k) & 1)
        V = tuple(A[k + 1] for k in range(n) if (bits >> k) & 1)
        yield U, V


def examine(A, B, plain=False):
    """Compute both alternatives literally, checking every successful split."""
    splits = []
    translation_failures = []
    for X, Y in ((A, B), (B, A)):
        ym = mask(Y)
        for U, V in partitions(X):
            if plain:
                ru, rv = plain_counts(U, Y), plain_counts(V, Y)
                if set(ru) & set(rv):
                    continue
                du = [s for s, c in ru.items() if c == 2]
                dv = [s for s, c in rv.items() if c == 2]
                if len(du) != 1 or len(dv) != 1:
                    continue
                cu, cv = du[0], dv[0]
            else:
                su, du, badu = fast_counts(U, ym)
                sv, dv, badv = fast_counts(V, ym)
                if badu or badv or su & sv:
                    continue
                if du.bit_count() != 1 or dv.bit_count() != 1:
                    continue
                cu, cv = du.bit_length() - 1, dv.bit_length() - 1

            splits.append((X, Y, U, V, cu, cv))
            start = max(X) + max(Y) + 1
            for T in range(start, start + 20):
                XT = tuple(sorted(U + tuple(v + T for v in V)))
                expected = (len(X), len(Y), (cu, cv + T),
                            T + cv - cu, False)
                if plain:
                    r = plain_counts(XT, Y)
                    doubles = tuple(sorted(s for s, c in r.items() if c == 2))
                    bad = any(c > 2 for c in r.values())
                else:
                    _, dm, bad = fast_counts(XT, ym)
                    doubles = tuple(i for i in range(dm.bit_length())
                                    if (dm >> i) & 1)
                separation = (doubles[1] - doubles[0]
                              if len(doubles) == 2 else None)
                actual = (len(set(XT)), len(set(Y)), doubles, separation, bad)
                if actual != expected:
                    translation_failures.append(
                        (X, Y, U, V, T, actual, expected))

    cores = []
    for X, Y in ((A, B), (B, A)):
        r = plain_counts(X, Y)
        participating = {(a, b) for a in X for b in Y if r[a + b] == 2}
        ys = set(Y)
        for u, w in itertools.combinations(X, 2):
            d = w - u
            for v in Y:
                if v + d not in ys or v + 2 * d not in ys:
                    continue
                proposed = {(u, v + d), (u + d, v),
                            (u, v + 2 * d), (u + d, v + d)}
                if participating == proposed:
                    cores.append((X, Y, u, v, d))

    r = plain_counts(A, B)
    doubles = sorted(s for s, c in r.items() if c == 2)
    core_failures = []
    for core in cores:
        d = core[-1]
        actual = (doubles[1] - doubles[0], bool(splits))
        expected = (d, False)
        if actual != expected:
            core_failures.append((core, actual, expected))

    return bool(splits), bool(cores), translation_failures, core_failures


def failures(result):
    I, II, tf, cf = result
    out = []
    if int(I) + int(II) != 1:
        out.append(("exclusive alternatives", (I, II),
                    "exactly one of (I, II) is true"))
    out.extend(("translation", x[:-2], x[-2], x[-1]) for x in tf)
    out.extend(("arithmetic core conclusion", x[0], x[1], x[2]) for x in cf)
    return out


def sanity():
    small = []
    for size in range(2, 5):
        small.extend((0,) + c for c in
                     itertools.combinations(range(1, 5), size - 1))
    checked = 0
    for A in small:
        for B in small:
            r = plain_counts(A, B)
            s, d, bad = fast_counts(A, mask(B))
            expected_bad = any(c > 2 for c in r.values())
            if bad != expected_bad:
                return False
            if not bad:
                if s != mask(r) or d != mask(s for s, c in r.items() if c == 2):
                    return False
                if sum(c == 2 for c in r.values()) == 2:
                    if examine(A, B) != examine(A, B, plain=True):
                        return False
            checked += 1
    print("SANITY 1 PASS: fast coefficients and classification versus plain "
          "enumeration on", checked, "small ordered pairs")

    examples = [
        ((0, 1), (0, 1, 2), (False, True)),
        ((0, 1, 10, 11), (0, 1), (True, False)),
    ]
    for A, B, expected in examples:
        result = examine(A, B, plain=True)
        if result[:2] != expected or result[2] or result[3]:
            return False
    print("SANITY 2 PASS: known arithmetic-core and splitting examples")
    return True


def main():
    if not sanity():
        print("SANITY FAILED")
        return

    supports = []
    for size in range(2, MAX_SIZE + 1):
        supports.extend((0,) + c for c in
                        itertools.combinations(range(1, MAX_ELEMENT + 1),
                                               size - 1))
    masks = [mask(S) for S in supports]
    n = len(supports)
    started = time.monotonic()
    tested = retained = 0
    last = None
    stopped = False

    # Symmetry permits searching unordered pairs, including equal supports.
    for i, A in enumerate(supports):
        for j in range(i, n):
            if tested % 256 == 0 and time.monotonic() - started >= LIMIT:
                stopped = True
                break
            B = supports[j]
            tested += 1
            last = (i, j)
            _, dm, bad = fast_counts(A, masks[j])
            if bad or dm.bit_count() != 2:
                continue
            retained += 1
            result = examine(A, B)
            if not failures(result):
                continue

            # Independently recompute the hypotheses and every claimed property.
            r = plain_counts(A, B)
            if any(c > 2 for c in r.values()) or \
                    sum(c == 2 for c in r.values()) != 2:
                print("SANITY FAILED")
                return
            confirmed = failures(examine(A, B, plain=True))
            if confirmed:
                print("COUNTEREXAMPLE:", {
                    "A": A,
                    "B": B,
                    "representation_counts": sorted(r.items()),
                    "failing_relations_actual_vs_claimed": confirmed,
                })
                return
            print("SANITY FAILED")
            return
        if stopped:
            break

    print("NO COUNTEREXAMPLE", {
        "universe": "A,B subset of {0,...,14}, both contain 0",
        "sizes": "2 through 6",
        "support_order": "increasing size, then lexicographic tuple order",
        "number_of_supports": n,
        "exact_pairs_checked": (
            "all unordered index pairs 0 <= i <= j < n"
            if not stopped else
            "lexicographic prefix of unordered index pairs "
            "0 <= i <= j < n, ending inclusively at " + repr(last)
        ),
        "pairs_tested": tested,
        "hypothesis_satisfying_cases_tested": retained,
        "partitions": "every partition in both orientations for retained cases",
        "translation_T": "max(A)+max(B)+1 through max(A)+max(B)+20",
        "arithmetic_cores": "all possible cores in both orientations",
    })


if __name__ == "__main__":
    main()
    sys.exit(0)