#!/usr/bin/env python3
from collections import Counter
from itertools import combinations
import sys


def partitions(n):
    """Plain enumeration of every set partition, without gap pruning."""
    blocks = []

    def visit(x):
        if x > n:
            yield tuple(tuple(b) for b in blocks)
            return
        for j in range(len(blocks)):
            blocks[j].append(x)
            yield from visit(x + 1)
            blocks[j].pop()
        blocks.append([x])
        yield from visit(x + 1)
        blocks.pop()

    yield from visit(1)


def statistics(partition):
    """Return the defining tuple, or None when gaps are not distinct."""
    gaps = []
    for block in partition:
        gaps.extend(b - a for a, b in zip(block, block[1:]))
    if len(gaps) != len(set(gaps)):
        return None
    return (
        len(partition),
        sum(len(b) == 1 for b in partition),
        sum(gaps),
        sum(b[-1] for b in partition),
    )


def plain_counts(n):
    result = Counter()
    for partition in partitions(n):
        key = statistics(partition)
        if key is not None:
            result[key] += 1
    return result


def pruned_counts(n):
    """Restricted-growth enumeration, pruning only repeated gaps."""
    result = Counter()
    blocks = []

    def visit(x, used, gap_sum):
        if x > n:
            key = (
                len(blocks),
                sum(len(b) == 1 for b in blocks),
                gap_sum,
                sum(b[-1] for b in blocks),
            )
            result[key] += 1
            return

        for j in range(len(blocks)):
            gap = x - blocks[j][-1]
            bit = 1 << gap
            if used & bit:
                continue
            blocks[j].append(x)
            visit(x + 1, used | bit, gap_sum + gap)
            blocks[j].pop()

        blocks.append([x])
        visit(x + 1, used, gap_sum)
        blocks.pop()

    visit(1, 0, 0)
    return result


def claimed_parity(n, key):
    """Evaluate precisely the stated side conditions and subset formula."""
    k, s, t, m = key
    if s != 2 * k - n or 2 * m != k * (n + 1) + t:
        return 0
    r = n - k
    h = n // 2
    if r < 0 or r > h:
        return 0
    count = sum(
        sum(n + 1 - 2 * i for i in subset) == t
        for subset in combinations(range(1, h + 1), r)
    )
    return count % 2


def formula_keys(n):
    """Include every tuple that the subset formula could predict as odd."""
    keys = set()
    h = n // 2
    for mask in range(1 << h):
        subset = [i for i in range(1, h + 1) if mask & (1 << (i - 1))]
        r = len(subset)
        k = n - r
        s = 2 * k - n
        t = sum(n + 1 - 2 * i for i in subset)
        twice_m = k * (n + 1) + t
        if s >= 0 and twice_m % 2 == 0:
            keys.add((k, s, t, twice_m // 2))
    return keys


def verify_witness(n, key):
    """Second computation: unpruned partitions and exhaustive subset masks."""
    actual = 0
    for partition in partitions(n):
        if statistics(partition) == key:
            actual += 1

    k, s, t, m = key
    predicted_count = 0
    if s == 2 * k - n and 2 * m == k * (n + 1) + t:
        for mask in range(1 << (n // 2)):
            subset = [
                i for i in range(1, n // 2 + 1)
                if mask & (1 << (i - 1))
            ]
            if (len(subset) == n - k
                    and sum(n + 1 - 2 * i for i in subset) == t):
                predicted_count += 1
    return actual, predicted_count % 2


def fail_sanity(message):
    print("SANITY FAILED:", message)
    sys.exit(0)


def main():
    # Independent check 1: unpruned enumeration against known Bell numbers.
    bells = [1, 2, 5, 15, 52, 203, 877]
    observed = [sum(1 for _ in partitions(n)) for n in range(1, 8)]
    print("Sanity 1: Bell numbers n=1..7:", observed,
          "PASS" if observed == bells else "FAIL")
    if observed != bells:
        fail_sanity("partition enumeration")

    # Independent check 2: gap-pruned enumeration versus plain gap validation.
    for n in range(1, 7):
        if pruned_counts(n) != plain_counts(n):
            fail_sanity("pruned/plain cross-check at n=" + str(n))
    print("Sanity 2: full tuple-count cross-check n=1..6: PASS")

    # Known small valid counts provide an additional definition check.
    small = [sum(plain_counts(n).values()) for n in range(1, 4)]
    print("Sanity 3: valid partition totals n=1..3:", small,
          "PASS" if small == [1, 2, 4] else "FAIL")
    if small != [1, 2, 4]:
        fail_sanity("known small valid counts")

    cases = 0
    for n in range(1, 12):
        counts = pruned_counts(n)
        keys = set(counts) | formula_keys(n)
        for key in sorted(keys):
            cases += 1
            actual = counts.get(key, 0)
            predicted = claimed_parity(n, key)
            if actual % 2 != predicted:
                checked_actual, checked_predicted = verify_witness(n, key)
                if checked_actual != actual or checked_predicted != predicted:
                    fail_sanity("independent witness recomputation disagreed")
                if checked_actual % 2 != checked_predicted:
                    k, s, t, m = key
                    print(
                        "COUNTEREXAMPLE:",
                        f"n={n}, k={k}, s={s}, t={t}, m={m}; "
                        f"A={checked_actual}, A mod 2={checked_actual % 2}; "
                        f"claimed parity={checked_predicted}"
                    )
                    return

    print(
        "NO COUNTEREXAMPLE",
        "ranges checked: 1<=n<=11; all set partitions, all resulting "
        "nonnegative (k,s,t,m), and all subset-formula predicted-odd tuples; "
        f"cases tested={cases}"
    )


if __name__ == "__main__":
    main()