#!/usr/bin/env python3
from collections import Counter
from itertools import combinations
import sys


def fast_partitions(n):
    """Generate admissible partitions, represented by nonempty bit masks."""
    blocks = []

    def visit(i):
        if i == n:
            yield tuple(blocks)
            return
        bit = 1 << i
        forbidden = (1 << (i - 2)) if i >= 2 else 0
        for j in range(len(blocks)):
            if not blocks[j] & forbidden:
                blocks[j] |= bit
                yield from visit(i + 1)
                blocks[j] ^= bit
        blocks.append(bit)
        yield from visit(i + 1)
        blocks.pop()

    yield from visit(0)


def plain_partitions(n):
    """Generate ALL set partitions without admissibility pruning."""
    blocks = []

    def visit(v):
        if v > n:
            yield tuple(tuple(block) for block in blocks)
            return
        for j in range(len(blocks)):
            blocks[j].append(v)
            yield from visit(v + 1)
            blocks[j].pop()
        blocks.append([v])
        yield from visit(v + 1)
        blocks.pop()

    yield from visit(1)


def plain_admissible(p):
    return all(
        abs(v - w) != 2
        for block in p
        for v, w in combinations(block, 2)
    )


def fast_left(n):
    result = Counter()
    for p in fast_partitions(n):
        b = len(p)
        s = sum(mask.bit_count() == 1 for mask in p)
        a = sum((mask & (mask >> 1)).bit_count() for mask in p)
        result[b, s, a] += 1
    return result


def plain_left(n):
    result = Counter()
    for p in plain_partitions(n):
        if not plain_admissible(p):
            continue
        owner = {}
        for j, block in enumerate(p):
            for v in block:
                owner[v] = j
        triple = (
            len(p),
            sum(len(block) == 1 for block in p),
            sum(owner[v] == owner[v + 1] for v in range(1, n)),
        )
        result[triple] += 1
    return result


def matchings(vertices):
    """Enumerate every matching exactly once, including the empty one."""
    if not vertices:
        yield ()
        return
    first, rest = vertices[0], vertices[1:]
    yield from matchings(rest)  # first is unmatched
    for j, partner in enumerate(rest):
        remaining = rest[:j] + rest[j + 1:]
        for matching in matchings(remaining):
            yield ((first, partner),) + matching


def fast_right(m):
    result = Counter()
    for q in fast_partitions(m):
        b = len(q)
        a = sum((mask & (mask >> 1)).bit_count() for mask in q)
        last_bit = 1 << (m - 1)
        last_two_bits = last_bit | (1 << (m - 2))
        ds = [None] + [
            j for j, block in enumerate(q)
            if not block & last_two_bits
        ]
        for d in ds:
            delta = int(d is not None)
            eligible = [
                j for j in range(b)
                if j != d and not q[j] & last_bit
            ]
            for subset in range(1 << len(eligible)):
                chosen = {
                    eligible[k] for k in range(len(eligible))
                    if subset & (1 << k)
                }
                outside = tuple(
                    j for j in range(b) if j != d and j not in chosen
                )
                for matching in matchings(outside):
                    matched = {v for edge in matching for v in edge}
                    u = sum(
                        q[j].bit_count() == 1 and j not in matched
                        for j in outside
                    )
                    result[
                        2 * b - len(chosen) - 2 * delta + 1,
                        2 * u + 1 - delta,
                        2 * a,
                    ] += 1
    return result


def plain_right(m):
    """Literal independent enumeration, using subsets of all possible edges."""
    result = Counter()
    for q in plain_partitions(m):
        if not plain_admissible(q):
            continue
        b = len(q)
        owner = {}
        for j, block in enumerate(q):
            for v in block:
                owner[v] = j
        a = sum(owner[v] == owner[v + 1] for v in range(1, m))
        ds = [None] + [
            j for j, block in enumerate(q)
            if m - 1 not in block and m not in block
        ]
        for d in ds:
            delta = int(d is not None)
            for mask in range(1 << b):
                chosen = {j for j in range(b) if mask & (1 << j)}
                if owner[m] in chosen or (d is not None and d in chosen):
                    continue
                outside = [
                    j for j in range(b) if j != d and j not in chosen
                ]
                edges = list(combinations(outside, 2))
                for edge_mask in range(1 << len(edges)):
                    used = set()
                    valid = True
                    for k, (v, w) in enumerate(edges):
                        if edge_mask & (1 << k):
                            if v in used or w in used:
                                valid = False
                                break
                            used.add(v)
                            used.add(w)
                    if not valid:
                        continue
                    u = sum(
                        len(q[j]) == 1 and j not in used for j in outside
                    )
                    result[
                        2 * b - len(chosen) - 2 * delta + 1,
                        2 * u + 1 - delta,
                        2 * a,
                    ] += 1
    return result


def sanity(label, condition):
    print("SANITY:", label, "PASS" if condition else "FAIL", flush=True)
    if not condition:
        print("SANITY FAILED", flush=True)
        sys.exit(0)


def main():
    bell = [1, 1, 2, 5, 15, 52, 203]
    sanity(
        "unrestricted partition counts equal Bell numbers for n=0..6",
        all(sum(1 for _ in plain_partitions(n)) == bell[n]
            for n in range(7)),
    )
    sanity(
        "known F_3 = x^3*y^3 + 2*x^2*y*z",
        fast_left(3) == Counter({(3, 3, 0): 1, (2, 1, 1): 2}),
    )
    sanity(
        "pruned enumeration agrees with unpruned brute force for n=0..6",
        all(fast_left(n) == plain_left(n) for n in range(7)),
    )
    sanity(
        "recursive matchings agree with edge-subset brute force for m=2..5",
        all(fast_right(m) == plain_right(m) for m in range(2, 6)),
    )

    cases = 0
    for m in range(2, 6):
        left = fast_left(2 * m + 1)
        right = fast_right(m)
        keys = sorted(set(left) | set(right))
        for triple in keys:
            cases += 1
            if (left[triple] - right[triple]) % 2:
                # Recompute BOTH entire sides by unpruned/plain enumeration.
                checked_left = plain_left(2 * m + 1)
                checked_right = plain_right(m)
                if (checked_left[triple] - checked_right[triple]) % 2:
                    print(
                        "COUNTEREXAMPLE:",
                        f"m={m}, (x,y,z) exponents={triple}; "
                        f"LHS coefficient={checked_left[triple]} "
                        f"(mod 2={checked_left[triple] % 2}); "
                        f"RHS coefficient={checked_right[triple]} "
                        f"(mod 2={checked_right[triple] % 2})",
                        flush=True,
                    )
                    return
                print("SANITY FAILED", flush=True)
                return

    print(
        "NO COUNTEREXAMPLE "
        f"m=2..5; lengths=5,7,9,11; "
        f"all coefficient triples in either support checked; "
        f"cases tested={cases}",
        flush=True,
    )


if __name__ == "__main__":
    main()