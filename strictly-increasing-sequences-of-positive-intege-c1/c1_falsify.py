#!/usr/bin/env python3
import itertools
import time
import sys

MAX_N = 9
MAX_S = 100
TIME_LIMIT = 220.0


def extend(buckets, relations, value, index):
    """Add one value; cancel common indices in colliding subset sums."""
    bit = 1 << index
    found = set(relations)
    for total, masks in buckets.items():
        for old_mask in buckets.get(total + value, ()):
            for low_mask in masks:
                left = old_mask & ~low_mask
                right = (low_mask | bit) & ~old_mask
                pair = (min(left, right), max(left, right))
                found.add(pair)
                if len(found) > 2:
                    return None, found

    updated = {total: list(masks) for total, masks in buckets.items()}
    for total, masks in buckets.items():
        updated.setdefault(total + value, []).extend(
            mask | bit for mask in masks
        )
    return updated, found


def clever(a):
    buckets = {0: [0]}
    relations = set()
    for index, value in enumerate(a):
        buckets, relations = extend(buckets, relations, value, index)
        if buckets is None:
            return None, relations
    return buckets, relations


def plain(a):
    """Independent exhaustive enumeration of all disjoint ordered assignments."""
    relations = set()
    n = len(a)
    for assignment in itertools.product((-1, 0, 1), repeat=n):
        left = right = difference = 0
        for i, sign in enumerate(assignment):
            difference += sign * a[i]
            if sign == 1:
                left |= 1 << i
            elif sign == -1:
                right |= 1 << i
        if difference == 0 and left and right:
            relations.add((min(left, right), max(left, right)))

    sums = set()
    for mask in range(1 << n):
        sums.add(sum(a[i] for i in range(n) if mask & (1 << i)))
    return relations, sums == set(range(sum(a) + 1))


def coverage_rule(a):
    covered = 0
    for value in a:
        if value > covered + 1:
            return False
        covered += value
    return True


def sanity():
    known = [
        ((1,), 0, True),
        ((1, 2, 3), 1, True),
        ((1, 2, 3, 5), 2, True),
        ((2, 3), 0, False),
    ]
    for a, count, covered in known:
        pairs, coverage = plain(a)
        if len(pairs) != count or coverage != covered:
            return False
    print("Sanity 1: known small cases PASS", flush=True)

    checked = 0
    for n in range(1, 6):
        for a in itertools.combinations(range(1, 10), n):
            brute_pairs, brute_coverage = plain(a)
            buckets, fast_pairs = clever(a)
            if buckets is None:
                if len(brute_pairs) <= 2:
                    return False
            elif fast_pairs != brute_pairs:
                return False
            if coverage_rule(a) != brute_coverage:
                return False
            checked += 1
    print(
        "Sanity 2: independent ternary brute-force cross-check PASS "
        f"({checked} sequences)",
        flush=True,
    )
    return True


def indices(mask, n):
    return [i + 1 for i in range(n) if mask & (1 << i)]


class TimeExpired(Exception):
    pass


def main():
    started = time.monotonic()
    if not sanity():
        print("SANITY FAILED")
        return 0

    deadline = started + TIME_LIMIT
    completed_sum = 0
    completed_cases = 0
    calls = 0

    for target in range(1, MAX_S + 1):
        target_cases = 0

        def visit(a, total, buckets, relations):
            nonlocal calls, target_cases
            calls += 1
            if calls % 256 == 0 and time.monotonic() >= deadline:
                raise TimeExpired

            if total == target:
                if len(relations) != 2:
                    return
                # Literal coverage and literal support-intersection formula.
                if set(buckets) != set(range(target + 1)):
                    return
                target_cases += 1
                p, q = sorted(relations)
                actual = ((p[0] | p[1]) & (q[0] | q[1])).bit_count()
                expected = 2
                if actual != expected:
                    verified_pairs, verified_coverage = plain(a)
                    if (
                        not verified_coverage
                        or len(verified_pairs) != 2
                        or not (1 <= len(a) <= MAX_N and sum(a) <= MAX_S)
                        or any(x <= 0 for x in a)
                        or any(x >= y for x, y in zip(a, a[1:]))
                    ):
                        print("SANITY FAILED")
                        sys.exit(0)
                    vp, vq = sorted(verified_pairs)
                    second_actual = (
                        (vp[0] | vp[1]) & (vq[0] | vq[1])
                    ).bit_count()
                    if second_actual != actual:
                        print("SANITY FAILED")
                        sys.exit(0)
                    if second_actual != expected:
                        witness = {
                            "a": a,
                            "equal_sum_pairs": [
                                (indices(x, len(a)), indices(y, len(a)))
                                for x, y in sorted(verified_pairs)
                            ],
                            "|R1 intersection R2|": second_actual,
                            "claimed_value": expected,
                        }
                        print("COUNTEREXAMPLE:", witness)
                        sys.exit(0)
                return

            if len(a) == MAX_N:
                return

            first = a[-1] + 1 if a else 1
            # For sorted positive integers, a gap above total+1 cannot
            # be filled by any later value. This is a coverage-only prune.
            last = min(total + 1, target - total)
            for value in range(first, last + 1):
                new_buckets, new_relations = extend(
                    buckets, relations, value, len(a)
                )
                # Existing disjoint relations persist under extension.
                if new_buckets is None:
                    continue
                visit(
                    a + (value,),
                    total + value,
                    new_buckets,
                    new_relations,
                )

        try:
            visit((), 0, {0: [0]}, set())
        except TimeExpired:
            break
        completed_sum = target
        completed_cases += target_cases

    print(
        "NO COUNTEREXAMPLE "
        f"exact exhaustive ranges: 1 <= n <= {MAX_N}, "
        f"1 <= S <= {completed_sum}; strictly increasing positive integers; "
        "complete subset-sum coverage; exactly two disjoint nonempty "
        f"equal-sum pairs; cases tested={completed_cases}. "
        "Any unfinished next-total slice is excluded from these counts."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())