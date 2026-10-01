#!/usr/bin/env python3
import sys
from collections import Counter


def elements(mask, n):
    return [i for i in range(n + 1) if mask & (1 << i)]


def signature(mask, n):
    # Each surviving bit represents one pair separated by d.
    return bytes((mask & (mask >> d)).bit_count()
                 for d in range(1, n + 1))


def brute_differences(values):
    return Counter(values[j] - values[i]
                   for i in range(len(values))
                   for j in range(i + 1, len(values)))


def reflect(mask, n):
    result = 0
    for a in elements(mask, n):
        result |= 1 << (n - a)
    return result


def fail():
    print("SANITY FAILED")
    sys.exit(0)


def sanity_checks():
    # Check 1: independently calculated small multiplicities.
    values = [0, 1, 3, 4]
    mask = sum(1 << a for a in values)
    expected = (2, 1, 2, 1)
    if tuple(signature(mask, 4)) != expected:
        fail()
    if brute_differences(values) != Counter({1: 2, 2: 1, 3: 2, 4: 1}):
        fail()
    print("SANITY 1 PASSED: known difference multiplicities")

    # Check 2: cross-check all optimized operations with plain set/pair loops.
    checked_sets = checked_pairs = 0
    for n in range(1, 7):
        masks = [(middle << 1) | 1 | (1 << n)
                 for middle in range(1 << (n - 1))]
        for mask in masks:
            values = elements(mask, n)
            counts = brute_differences(values)
            if tuple(signature(mask, n)) != tuple(
                    counts[d] for d in range(1, n + 1)):
                fail()
            if set(elements(reflect(mask, n), n)) != {
                    n - a for a in values}:
                fail()
            checked_sets += 1

        for i, a in enumerate(masks):
            sa = set(elements(a, n))
            for b in masks[i + 1:]:
                sb = set(elements(b, n))
                if (a & ~b).bit_count() != len(sa - sb):
                    fail()
                if (signature(a, n) == signature(b, n)) != (
                        brute_differences(sorted(sa)) ==
                        brute_differences(sorted(sb))):
                    fail()
                checked_pairs += 1
    print("SANITY 2 PASSED:", checked_sets, "sets and",
          checked_pairs, "pairs cross-checked")


def verify_and_report(a, b, n):
    # Fresh, plain brute-force verification of every hypothesis and conclusion.
    A = elements(a, n)
    B = elements(b, n)
    sa, sb = set(A), set(B)
    da = brute_differences(A)
    db = brute_differences(B)
    hypotheses = (
        n >= 1
        and sa <= set(range(n + 1))
        and sb <= set(range(n + 1))
        and {0, n} <= sa
        and {0, n} <= sb
        and da == db
        and len(sa - sb) <= 2
    )
    actual = (sa == sb or sb == {n - x for x in sa})
    claimed = True
    if not hypotheses or actual == claimed:
        fail()
    print("COUNTEREXAMPLE:", {
        "n": n,
        "A": A,
        "B": B,
        "A_minus_B": sorted(sa - sb),
        "difference_multiplicities_A": dict(sorted(da.items())),
        "difference_multiplicities_B": dict(sorted(db.items())),
        "claimed_conclusion": claimed,
        "actual_A_equals_B_or_B_equals_reflection_of_A": actual,
    })
    sys.exit(0)


def main():
    sanity_checks()
    total_sets = bucket_pairs = hypothesis_pairs = 0

    for n in range(1, 19):
        buckets = {}
        for middle in range(1 << (n - 1)):
            mask = (middle << 1) | 1 | (1 << n)
            key = signature(mask, n)
            buckets.setdefault(key, []).append(mask)
            total_sets += 1

        for bucket in buckets.values():
            for i, a in enumerate(bucket):
                reflected_a = reflect(a, n)
                for b in bucket[i + 1:]:
                    bucket_pairs += 1
                    if (a & ~b).bit_count() > 2:
                        continue
                    hypothesis_pairs += 1
                    # Literal conclusion: A=B or B={n-a : a in A}.
                    actual = (a == b or b == reflected_a)
                    if not actual:
                        verify_and_report(a, b, n)

    print("NO COUNTEREXAMPLE",
          "ranges: n=1..18; all subsets of {0,...,n} containing 0 and n;",
          "cases tested:", total_sets, "sets;",
          bucket_pairs, "distinct equal-difference pairs;",
          hypothesis_pairs, "distinct pairs satisfying every hypothesis")
    sys.exit(0)


if __name__ == "__main__":
    main()