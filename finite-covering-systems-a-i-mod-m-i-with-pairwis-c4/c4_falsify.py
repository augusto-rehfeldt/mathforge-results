import itertools
import math
import random
import time
import sys

LIMIT = 230.0
LS = (105, 225, 315, 525, 1225)
START = time.monotonic()
rng = random.Random(20260401)


def factor(n):
    result = []
    p = 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            result.append((p, e))
        p += 1
    if n > 1:
        result.append((n, 1))
    return result


def divisors(n):
    return tuple(d for d in range(2, n + 1) if n % d == 0)


def valid(ms, aa):
    return (
        bool(ms)
        and len(ms) == len(set(ms))
        and len(ms) == len(aa)
        and all(m > 1 and m % 2 and all(e <= 2 for _, e in factor(m))
                for m in ms)
        and all(0 <= a < m for m, a in zip(ms, aa))
    )


def box_exists(ms, aa):
    """Exact search assigning each forbidden congruence a blocking prime.

    At a prime, forbidden lifts can be avoided unless more than two
    first-digit classes have every possible lift forbidden.
    """
    L = math.lcm(*ms)
    fs = factor(L)
    clauses = []
    for m, a in zip(ms, aa):
        clause = []
        for j, (p, e) in enumerate(fs):
            if m % p:
                continue
            if m % (p * p) == 0:
                mask = 1 << (a % (p * p))
            else:
                mask = sum(1 << r for r in range(a % p, p ** e, p))
            clause.append((j, mask))
        clauses.append(tuple(clause))

    groups = [
        tuple(sum(1 << r for r in range(b, p ** e, p)) for b in range(p))
        for p, e in fs
    ]

    def feasible(j, mask):
        return sum(mask & g == g for g in groups[j]) <= 2

    memo = set()

    def visit(state):
        if state in memo:
            return False
        best = None
        for clause in clauses:
            if any(state[j] & mask == mask for j, mask in clause):
                continue
            choices = [
                (j, state[j] | mask)
                for j, mask in clause
                if feasible(j, state[j] | mask)
            ]
            if not choices:
                memo.add(state)
                return False
            if best is None or len(choices) < len(best):
                best = choices
        if best is None:
            return True
        for j, mask in best:
            nxt = list(state)
            nxt[j] = mask
            if visit(tuple(nxt)):
                return True
        memo.add(state)
        return False

    return visit((0,) * len(fs))


def literal_box_exists(ms, aa):
    """Independent enumeration of actual sets and lifts, with exact pruning."""
    L = math.lcm(*ms)
    fs = factor(L)

    def options(p, e):
        for B in itertools.combinations(range(p), p - 2):
            for lifts in itertools.product(
                *(range(b, p ** e, p) for b in B)):
                yield lifts

    def visit(j, remaining):
        if not remaining:
            return True
        if j == len(fs):
            return False
        p, e = fs[j]
        for selected in options(p, e):
            survivors = []
            for i in remaining:
                m, a = ms[i], aa[i]
                if m % p:
                    survivors.append(i)
                else:
                    q = p * p if m % (p * p) == 0 else p
                    if any(r % q == a % q for r in selected):
                        survivors.append(i)
            if visit(j + 1, survivors):
                return True
        return False

    return visit(0, tuple(range(len(ms))))


def sanity():
    # Known values, including a fully covered composite-modulus system.
    known = [
        ((3,), (0,), True),
        ((9,), (0,), True),
        ((3, 5, 15), (0, 0, 1), True),
        ((3, 5, 15), (0, 0, 0), True),
    ]
    ok = all(box_exists(m, a) == expected
             and literal_box_exists(m, a) == expected
             for m, a, expected in known)
    print("Sanity 1: known small values:", "PASS" if ok else "FAIL",
          flush=True)
    if not ok:
        return False

    checked = 0
    for L in (9, 15):
        ds = divisors(L)
        for size in range(1, len(ds) + 1):
            for ms in itertools.combinations(ds, size):
                if math.lcm(*ms) != L:
                    continue
                for aa in itertools.product(*(range(m) for m in ms)):
                    checked += 1
                    if box_exists(ms, aa) != literal_box_exists(ms, aa):
                        print("Sanity 2: FAIL", ms, aa, flush=True)
                        return False
    print("Sanity 2: independent literal-box exhaustive cross-check:",
          checked, "cases PASS", flush=True)
    return True


if not sanity():
    print("SANITY FAILED")
    sys.exit(0)

counts = {L: 0 for L in LS}
random_counts = {L: 0 for L in LS}
exhaustive_counts = {L: 0 for L in LS}
completed_subsets = {L: [] for L in LS}
partial = None


def test(L, ms, aa):
    if not valid(ms, aa) or math.lcm(*ms) != L:
        print("SANITY FAILED")
        sys.exit(0)
    actual = box_exists(ms, aa)
    counts[L] += 1
    if not actual:
        # Recompute the claimed value and independently enumerate literal boxes.
        claimed_again = valid(ms, aa) and math.lcm(*ms) == L
        actual_again = literal_box_exists(ms, aa)
        if claimed_again and not actual_again:
            witness = {
                "L": L,
                "m": ms,
                "a": aa,
                "claimed_box_exists": True,
                "brute_force_box_exists": False,
            }
            print("COUNTEREXAMPLE:", witness, flush=True)
            sys.exit(0)
        print("SANITY FAILED")
        sys.exit(0)


# Round-robin random sampling: attempt 100000 assignments for each listed L.
# The wall-clock budget may stop this phase early.
eligible = {L: divisors(L) for L in LS}
timed_out = False
for iteration in range(100000):
    for L in LS:
        if time.monotonic() - START >= LIMIT:
            timed_out = True
            break
        ms = eligible[L]
        aa = tuple(rng.randrange(m) for m in ms)
        test(L, ms, aa)
        random_counts[L] += 1
    if timed_out:
        break

# If sampling finishes, exhaustively enumerate subsets and residue products.
if not timed_out:
    for L in LS:
        ds = eligible[L]
        for size in range(1, len(ds) + 1):
            for ms in itertools.combinations(ds, size):
                if math.lcm(*ms) != L:
                    continue
                done = 0
                for aa in itertools.product(*(range(m) for m in ms)):
                    if time.monotonic() - START >= LIMIT:
                        partial = {
                            "L": L,
                            "subset": ms,
                            "lexicographic_product_prefix_length": done,
                            "coordinate_ranges": tuple((0, m - 1) for m in ms),
                        }
                        timed_out = True
                        break
                    test(L, ms, aa)
                    exhaustive_counts[L] += 1
                    done += 1
                if timed_out:
                    break
                completed_subsets[L].append(ms)
            if timed_out:
                break
        if timed_out:
            break

print("NO COUNTEREXAMPLE", {
    "search_cases_tested": sum(counts.values()),
    "cases_by_L": counts,
    "random_sampling": {
        "seed": 20260401,
        "generator": "random.Random; round-robin L order",
        "eligible_divisors": eligible,
        "assignments_tested_by_L": random_counts,
        "residue_ranges": "0 <= a_i < m_i",
    },
    "exhaustive_cases_by_L": exhaustive_counts,
    "fully_exhausted_subsets": completed_subsets,
    "partial_exhaustive_slice": partial,
    "stopped_at_time_budget": timed_out,
}, flush=True)
sys.exit(0)