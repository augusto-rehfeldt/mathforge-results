#!/usr/bin/env python3
import itertools
import sys
from collections import defaultdict

BOUND = 28
NS = (4, 5, 6)


def distinct_fast(xs):
    """Bit i records whether i is a subset sum."""
    bits = 1
    for x in xs:
        shifted = bits << x
        if bits & shifted:
            return False
        bits |= shifted
    return True


def distinct_plain(xs):
    sums = [
        sum(xs[i] for i in range(len(xs)) if mask & (1 << i))
        for mask in range(1 << len(xs))
    ]
    return len(set(sums)) == len(sums)


def differences(xs):
    result = {0}
    for x in xs:
        result = result | {v + x for v in result} | {v - x for v in result}
    return result


def differences_plain(xs):
    return {
        sum(e * x for e, x in zip(es, xs))
        for es in itertools.product((-1, 0, 1), repeat=len(xs))
    }


def literal_replacement(A, R, T):
    retained = set(A) - set(R)
    return (
        1 <= len(R) <= len(A) // 2 + 1
        and len(T) == len(R)
        and len(set(T)) == len(T)
        and all(x > 0 for x in T)
        and not (set(T) & retained)
        and distinct_fast(T)
        and differences(T).intersection(differences(retained)) == {0}
        and max(retained | set(T)) < max(A)
    )


def all_valid(n, bound):
    """Enumerate every combination, pruning only irreversible sum collisions."""
    out = []

    def visit(prefix, start, bits):
        remaining = n - len(prefix)
        if remaining == 0:
            out.append(prefix)
            return
        for x in range(start, bound - remaining + 2):
            shifted = bits << x
            if not bits & shifted:
                visit(prefix + (x,), x + 1, bits | shifted)

    visit((), 1, 1)
    return out


def sanity():
    # Check 1: independently known small optimal maximum values.
    expected = {2: 2, 3: 4, 4: 7}
    actual = {
        n: min(max(A) for A in all_valid(n, 8))
        for n in expected
    }
    ok = actual == expected
    print("Sanity 1: small minimum maxima:", actual, "PASS" if ok else "FAIL")
    if not ok:
        return False

    # Check 2: compare both accelerated definitions to direct enumeration.
    count = 0
    for size in range(7):
        for X in itertools.combinations(range(1, 9), size):
            if (distinct_fast(X) != distinct_plain(X)
                    or differences(X) != differences_plain(X)):
                print("Sanity 2: FAIL", X)
                return False
            count += 1
    print("Sanity 2: direct subset/signed-sum cross-check:",
          count, "PASS")

    # Check 3: verify the block-intersection characterization independently.
    count = 0
    universe = tuple(range(1, 8))
    for labels in itertools.product((0, 1, 2), repeat=len(universe)):
        X = tuple(x for x, label in zip(universe, labels) if label == 1)
        Y = tuple(x for x, label in zip(universe, labels) if label == 2)
        block_property = (
            distinct_fast(X)
            and distinct_fast(Y)
            and differences(X).intersection(differences(Y)) == {0}
        )
        if block_property != distinct_plain(X + Y):
            print("Sanity 3: FAIL", X, Y)
            return False
        count += 1
    print("Sanity 3: block characterization:", count, "PASS")
    return True


def plain_verify_failure(A, C):
    """Second verification: literally enumerate all R and T, without pruning."""
    n = len(A)
    M = max(A)
    if not (
        n >= 2
        and len(set(A)) == n
        and len(set(C)) == n
        and all(x > 0 for x in A + C)
        and distinct_plain(A)
        and distinct_plain(C)
        and max(C) < M
    ):
        raise RuntimeError("Proposed witness does not satisfy the hypotheses")

    checked = 0
    successful = 0
    for r in range(1, n // 2 + 2):
        for R in itertools.combinations(A, r):
            # Without removing M the strict maximum condition is impossible.
            if M not in R:
                continue
            retained = tuple(x for x in A if x not in R)
            pool = tuple(x for x in range(1, M) if x not in retained)
            retained_D = differences_plain(retained)
            for T in itertools.combinations(pool, r):
                checked += 1
                if (
                    distinct_plain(T)
                    and differences_plain(T).intersection(retained_D) == {0}
                    and max(retained + T) < M
                ):
                    successful += 1
    return checked, successful


def main():
    if not sanity():
        print("SANITY FAILED")
        return 0

    tested = 0
    totals = {}
    minima = {}

    for n in NS:
        valid = sorted(all_valid(n, BOUND), key=lambda A: (max(A), A))
        totals[n] = len(valid)
        minimum = min(max(A) for A in valid)
        minima[n] = minimum
        C = next(A for A in valid if max(A) == minimum)
        print("Enumeration:", "n =", n, "valid sets =", len(valid),
              "minimum maximum =", minimum, "comparison set =", C)

        k = n // 2 + 1
        retained_size = n - k
        index = {}

        # Exact exhaustive replacement search, compressed by retained blocks:
        # a successful union B is one of the enumerated valid n-element sets.
        # |A \ B| <= k iff A and B share at least n-k elements.
        # Index only smaller-maximum B, so all maximum side conditions hold.
        groups = defaultdict(list)
        for B in valid:
            groups[max(B)].append(B)

        for M in sorted(groups):
            for A in groups[M]:
                if M == minimum:
                    continue
                tested += 1
                found = False
                for retained_block in itertools.combinations(A, retained_size):
                    B = index.get(retained_block)
                    if B is None:
                        continue
                    R = tuple(x for x in A if x not in B)
                    T = tuple(x for x in B if x not in A)
                    # Evaluate the statement's conditions literally.
                    if not literal_replacement(A, R, T):
                        raise RuntimeError("Indexed replacement failed literal check")
                    found = True
                    break

                if not found:
                    checked, successes = plain_verify_failure(A, C)
                    if successes:
                        raise RuntimeError("Independent brute force disagreed")
                    print(
                        "COUNTEREXAMPLE:",
                        {
                            "n": n,
                            "A": A,
                            "C": C,
                            "hypotheses": True,
                            "claimed_replacement_exists": True,
                            "brute_force_replacement_exists": False,
                            "successful_replacements": successes,
                            "replacement_candidates_rechecked": checked,
                        },
                    )
                    return 0

            # Insert only after the entire equal-maximum group was tested.
            for B in groups[M]:
                for block in itertools.combinations(B, retained_size):
                    index.setdefault(block, B)

    print(
        "NO COUNTEREXAMPLE",
        "ranges: n in {4,5,6}, A subset of {1,...,28}, |A|=n, "
        "distinct subset sums, max(A)>minimum[n];",
        "minimum[n] =", minima,
        "valid-set counts =", totals,
        "hypothesis-qualified cases tested =", tested,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())