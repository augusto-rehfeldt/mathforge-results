#!/usr/bin/env python3
import itertools
import math
import time
import sys

try:
    import numpy as np
except ImportError:
    print("SANITY FAILED: numpy is required")
    sys.exit(0)

START = time.monotonic()
DEADLINE = START + 225.0
BATCH = 16384
SEARCH = (3, 5, 7, 11, 13, 15)


def squarefree(n):
    return all(n % (p * p) for p in range(2, math.isqrt(n) + 1))


def literal(x, u):
    """The statement's formulas, evaluated using plain Python integers."""
    n = 4 * u
    if len(x) != n:
        return False, None
    correlations = [
        sum(x[i] * x[(i + t) % n] for i in range(n))
        for t in range(n)
    ]
    valid = (
        u > 1 and u % 2 == 1 and squarefree(u)
        and all(isinstance(v, int) and v % 2 and abs(v) <= u for v in x)
        and sum(x) == 2 * u
        and correlations == [4 * u * u] + [0] * (n - 1)
    )
    return valid, correlations


def batch_vectors(magnitudes, lo, hi):
    n = len(magnitudes)
    masks = np.arange(lo, hi, dtype=np.uint64)
    bits = ((masks[:, None] >> np.arange(n, dtype=np.uint64)) & 1)
    signs = 1 - 2 * bits.astype(np.int16)
    return signs * np.asarray(magnitudes, dtype=np.int16)


def survivors(vectors, u):
    x = vectors[vectors.sum(axis=1, dtype=np.int64) == 2 * u]
    x = x[(x.astype(np.int64) ** 2).sum(axis=1) == 4 * u * u]
    for t in range(1, 2 * u + 1):
        if len(x) == 0:
            break
        c = (x.astype(np.int64) * np.roll(x, -t, axis=1)).sum(axis=1)
        x = x[c == 0]
    return x


def sanity():
    # Known small periodic perfect sequence; u=1 is used ONLY as a unit test.
    x = [1, 1, 1, -1]
    c = [sum(x[i] * x[(i + t) % 4] for i in range(4))
         for t in range(4)]
    ok1 = sum(x) == 2 and c == [4, 0, 0, 0]
    print("Sanity 1:", "PASS" if ok1 else "FAIL", flush=True)

    # Independent full-sign brute-force check of the vectorized routine.
    m = [3, 3, 3] + [1] * 9
    fast = {
        tuple(map(int, row))
        for row in survivors(batch_vectors(m, 0, 1 << 12), 3)
    }
    slow = set()
    for signs in itertools.product((-1, 1), repeat=12):
        v = [a * s for a, s in zip(m, signs)]
        if literal(v, 3)[0]:
            slow.add(tuple(v))
    ok2 = fast == slow
    print("Sanity 2:", "PASS" if ok2 else "FAIL",
          "(4096 independent literal evaluations)", flush=True)
    if not (ok1 and ok2):
        print("SANITY FAILED")
        sys.exit(0)


def multiplicities(u):
    """All absolute-value multiplicities satisfying the literal energy."""
    values = list(range(u, 0, -2))
    n = 4 * u

    def rec(j, left, energy, counts):
        if j == len(values) - 1:
            if energy == left:
                yield tuple(counts + [left])
            return
        a = values[j]
        # Descending order deliberately tries the largest magnitudes first.
        for count in range(left, -1, -1):
            remaining = energy - count * a * a
            slots = left - count
            if slots <= remaining <= slots * values[j + 1] ** 2:
                yield from rec(j + 1, slots, remaining, counts + [count])

    yield from rec(0, n, 4 * u * u, [])


def arrangements(u, counts):
    """Unique magnitude arrangements in explicitly defined nested order."""
    values = list(range(u, 0, -2))
    n = 4 * u
    work = [1] * n

    def rec(j, free):
        if j == len(values) - 1:
            yield tuple(work)
            return
        count = counts[j]
        for chosen in itertools.combinations(free, count):
            chosen_set = set(chosen)
            for i in chosen:
                work[i] = values[j]
            rest = tuple(i for i in free if i not in chosen_set)
            yield from rec(j + 1, rest)
            for i in chosen:
                work[i] = 1

    yield from rec(0, tuple(range(n)))


def report_witness(row, u):
    v = [int(a) for a in row]
    # Recompute independently from scratch before reporting anything.
    valid, correlations = literal(v, u)
    if not valid:
        print("SANITY FAILED: optimized candidate failed literal verification")
        sys.exit(0)
    print("COUNTEREXAMPLE:",
          {"u": u, "x": v, "sum": sum(v),
           "correlations": correlations,
           "required_correlations": [4 * u * u] + [0] * (4 * u - 1),
           "failing_relation": "a satisfying vector exists",
           "computed_side": True, "claim_side": False})
    sys.exit(0)


sanity()
assert all(u > 1 and u % 2 and squarefree(u) for u in SEARCH)

tested = 0
records = []
stopped = False

for u in SEARCH:
    for counts in multiplicities(u):
        full_supports = 0
        partial_masks = 0
        for rank, magnitudes in enumerate(arrangements(u, counts)):
            partial_masks = 0
            for lo in range(0, 1 << (4 * u), BATCH):
                if time.monotonic() >= DEADLINE:
                    stopped = True
                    break
                hi = min(lo + BATCH, 1 << (4 * u))
                rows = batch_vectors(magnitudes, lo, hi)
                found = survivors(rows, u)
                tested += hi - lo
                partial_masks = hi
                if len(found):
                    report_witness(found[0], u)
            if stopped:
                break
            full_supports += 1
            partial_masks = 0
        records.append({
            "u": u,
            "magnitudes_descending": list(range(u, 0, -2)),
            "multiplicities": counts,
            "fully_checked_support_ranks": [0, full_supports],
            "masks_for_each_full_support": [0, 1 << (4 * u)],
            "partial_support_rank": full_supports if partial_masks else None,
            "partial_mask_range": [0, partial_masks],
            "entire_multiplicity_class_completed": not stopped,
        })
        if stopped:
            break
    if stopped:
        break

print("NO COUNTEREXAMPLE",
      {"cases_tested": tested,
       "ranges_checked": records,
       "range_convention": "All intervals are half-open.",
       "support_order":
           "arrangements(): nested itertools.combinations in ascending "
           "position order, magnitudes descending.",
       "mask_order":
           "Integer masks ascending; bit i=0 means positive coordinate i, "
           "bit i=1 means negative coordinate i.",
       "excluded_without_sign_enumeration":
           "Magnitude multiplicities failing sum of squares = 4*u*u.",
       "search_space_requested": SEARCH,
       "time_limited": stopped})
sys.exit(0)