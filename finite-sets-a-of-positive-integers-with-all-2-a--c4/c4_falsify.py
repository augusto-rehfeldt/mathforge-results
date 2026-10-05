#!/usr/bin/env python3
import itertools
import time

MAX_R = 40
MAX_Y = 160
DEADLINE_SECONDS = 220


def signed_sums(core):
    d = {0}
    for r in core:
        d = {s + e * r for s in d for e in (-1, 0, 1)}
    return d


def subset_sums(core):
    return {
        sum(r for r, take in zip(core, mask) if take)
        for mask in itertools.product((0, 1), repeat=len(core))
    }


def holes(d):
    result = []
    n = 1
    while len(result) < 2:
        if n not in d:
            result.append(n)
        n += 1
    return tuple(result)


def cores_of_length(m, bound, prefix=(), total=0):
    if len(prefix) == m:
        yield prefix
        return
    start = max(total + 1, prefix[-1] + 1 if prefix else 1)
    for r in range(start, bound + 1):
        yield from cores_of_length(m, bound, prefix + (r,), total + r)


def fast_minima(core, bound):
    """Return minimum unrestricted y and minimum claimed-side v."""
    d = signed_sums(core)
    hs = holes(d)
    width = 2 * bound
    allowed = 0
    reflected = 0
    for n in range(1, width + 1):
        if n not in d:
            allowed |= 1 << n
            reflected |= 1 << (width - n)

    claimed_min = None
    claimed_pair = None
    limit_mask = (1 << (bound + 1)) - 1
    for u in hs:
        if u >= bound:
            continue
        candidates = (
            allowed
            & (allowed << u)
            & (allowed >> u)
            & limit_mask
            & ~((1 << (u + 1)) - 1)
        )
        if candidates:
            v = (candidates & -candidates).bit_length() - 1
            if claimed_min is None or v < claimed_min:
                claimed_min, claimed_pair = v, (u, v)

    tested_pairs = 0
    unrestricted_pair = None
    for y in range(2, bound + 1):
        tested_pairs += y - 1
        if not ((allowed >> y) & 1):
            continue
        candidates = (
            allowed
            & (allowed >> y)
            & (reflected >> (width - y))
            & ((1 << y) - 1)
        )
        if candidates:
            x = (candidates & -candidates).bit_length() - 1
            unrestricted_pair = (x, y)
            break
    return unrestricted_pair, claimed_min, claimed_pair, tested_pairs


def literal_disjoint(s, x, y):
    sets = [
        s,
        {x + a for a in s},
        {y + a for a in s},
        {x + y + a for a in s},
    ]
    return all(
        sets[i].isdisjoint(sets[j])
        for i in range(4)
        for j in range(i + 1, 4)
    )


def plain_minima(core, bound):
    s = subset_sums(core)
    # Independent construction of D as the difference set of S.
    d = {a - b for a in s for b in s}
    hs = holes(d)
    first = None
    for y in range(2, bound + 1):
        for x in range(1, y):
            if literal_disjoint(s, x, y):
                first = (x, y)
                break
        if first is not None:
            break

    claimed = None
    for v in range(2, bound + 1):
        for u in hs:
            if 0 < u < v and literal_disjoint(s, u, v):
                claimed = (u, v)
                break
        if claimed is not None:
            break
    return first, None if claimed is None else claimed[1]


def sanity_checks():
    known = (
        signed_sums((1, 3)) == set(range(-4, 5))
        and holes(signed_sums((1, 3))) == (5, 6)
        and signed_sums((2,)) == {-2, 0, 2}
        and holes(signed_sums((2,))) == (1, 3)
    )
    print("Sanity 1: known signed sums and holes:", "PASS" if known else "FAIL")
    if not known:
        return False

    checked = 0
    for m in range(1, 4):
        for core in cores_of_length(m, 9):
            fast_pair, fast_claimed, _, _ = fast_minima(core, 20)
            plain_pair, plain_claimed = plain_minima(core, 20)
            if fast_pair != plain_pair or fast_claimed != plain_claimed:
                print("Sanity 2: bitset versus literal subset-set brute force: FAIL",
                      core, fast_pair, plain_pair, fast_claimed, plain_claimed)
                return False
            checked += 1
    print("Sanity 2: bitset versus literal subset-set brute force: PASS",
          f"({checked} cores)")
    return True


def main():
    if not sanity_checks():
        print("SANITY FAILED")
        return

    start = time.monotonic()
    core_count = 0
    pair_count = 0
    last_completed = None

    for m in range(1, 7):
        for core in cores_of_length(m, MAX_R):
            if time.monotonic() - start >= DEADLINE_SECONDS:
                print(
                    "NO COUNTEREXAMPLE",
                    "exact ranges checked: m=1..6, r_m<=40, "
                    "positive strictly increasing superincreasing cores, "
                    f"prefix of ordering (m, lexicographic core) through "
                    f"{last_completed!r}; 1<=x<y<=160, stopping each core "
                    "at its minimum feasible y (or y=160 if none);",
                    f"cases tested: {core_count} cores, {pair_count} pair positions"
                )
                return

            assert all(r > 0 for r in core)
            assert all(core[i] > sum(core[:i]) for i in range(1, m))
            pair, claimed_min, _, positions = fast_minima(core, MAX_Y)

            if pair is not None and (
                claimed_min is None or pair[1] < claimed_min
            ):
                # Recompute from scratch using literal subset-set intersections.
                x, y = pair
                s = subset_sums(core)
                independent_d = {a - b for a in s for b in s}
                hs = holes(independent_d)
                lhs = literal_disjoint(s, x, y)
                rhs = any(
                    literal_disjoint(s, u, v)
                    for u in hs
                    for v in range(u + 1, y + 1)
                )
                if lhs and not rhs:
                    print(
                        "COUNTEREXAMPLE:",
                        f"R={core}, x={x}, y={y}, h1={hs[0]}, h2={hs[1]};",
                        "given four subset-sum translates pairwise disjoint=True;",
                        "exists positive u<v<=y with u in {h1,h2} and "
                        "four subset-sum translates pairwise disjoint=False"
                    )
                    return
                print("SANITY FAILED")
                return

            core_count += 1
            pair_count += positions
            last_completed = (m, core)

    print(
        "NO COUNTEREXAMPLE",
        "exact ranges checked: 1<=m<=6, r_m<=40, all positive strictly "
        "increasing superincreasing cores; 1<=x<y<=160, stopping each "
        "core at its minimum feasible y (or y=160 if none);",
        f"cases tested: {core_count} cores, {pair_count} pair positions"
    )


if __name__ == "__main__":
    main()