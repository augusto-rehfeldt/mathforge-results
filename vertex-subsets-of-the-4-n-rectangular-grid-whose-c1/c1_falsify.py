#!/usr/bin/env python3
import itertools
import sys

WIDTH = 4
MAX_N = 6


def vertices(n):
    return [(x, y) for y in range(1, n + 1)
            for x in range(1, WIDTH + 1)]


def neighbors(p, n):
    x, y = p
    return [(a, b) for a, b in
            ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
            if 1 <= a <= WIDTH and 1 <= b <= n]


def valid(A, n):
    return all(sum(p in A for p in neighbors(v, n)) == 2 for v in A)


# A column is accepted only when every occupied vertex has degree two,
# counting its vertical neighbors and its left and right neighbors.
TRANSITIONS = {}
for left in range(16):
    for current in range(16):
        allowed = []
        for right in range(16):
            good = True
            for row in range(4):
                if current & (1 << row):
                    degree = (
                        int(row > 0 and bool(current & (1 << (row - 1))))
                        + int(row < 3 and bool(current & (1 << (row + 1))))
                        + ((left >> row) & 1)
                        + ((right >> row) & 1)
                    )
                    if degree != 2:
                        good = False
                        break
            if good:
                allowed.append(right)
        TRANSITIONS[left, current] = tuple(allowed)


def candidates(n):
    """Enumerate all subsets satisfying the degree condition, exactly once."""
    def extend(columns):
        left = columns[-2] if len(columns) > 1 else 0
        current = columns[-1]
        if len(columns) == n:
            if 0 in TRANSITIONS[left, current]:
                yield frozenset(
                    (row + 1, col + 1)
                    for col, mask in enumerate(columns)
                    for row in range(4) if mask & (1 << row)
                )
            return
        for right in TRANSITIONS[left, current]:
            yield from extend(columns + [right])

    for first in range(16):
        yield from extend([first])


def extract_cycles(A, n):
    remaining = set(A)
    cycles = []
    while remaining:
        start = min(remaining)
        cycle = [start]
        previous = None
        current = start
        while True:
            adjacent = sorted(p for p in neighbors(current, n) if p in A)
            if len(adjacent) != 2:
                raise ValueError("Not 2-regular")
            nxt = adjacent[0] if adjacent[0] != previous else adjacent[1]
            if nxt == start:
                break
            if nxt in cycle:
                raise ValueError("Invalid cycle traversal")
            cycle.append(nxt)
            previous, current = current, nxt
        remaining.difference_update(cycle)
        cycles.append(cycle)
    return cycles


def cross(a, b, p):
    return ((b[0] - a[0]) * (p[1] - a[1])
            - (b[1] - a[1]) * (p[0] - a[0]))


def on_segment(p, a, b):
    return (cross(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def inside_ray(p, cycle):
    """Strict containment by horizontal ray casting, using exact arithmetic."""
    parity = False
    for a, b in zip(cycle, cycle[1:] + cycle[:1]):
        if on_segment(p, a, b):
            return False
        # Grid edges are axis-aligned; only vertical edges cross the ray.
        if (a[1] > p[1]) != (b[1] > p[1]):
            if a[0] > p[0]:
                parity = not parity
    return parity


def inside_winding(p, cycle):
    """Independent strict point-in-polygon test by winding number."""
    winding = 0
    for a, b in zip(cycle, cycle[1:] + cycle[:1]):
        if on_segment(p, a, b):
            return False
        if a[1] <= p[1] < b[1] and cross(a, b, p) > 0:
            winding += 1
        elif b[1] <= p[1] < a[1] and cross(a, b, p) < 0:
            winding -= 1
    return winding != 0


def statistics(A, n, containment=inside_ray):
    cycles = extract_cycles(A, n)
    interiors = [
        {p for p in vertices(n) if p not in A and containment(p, cycle)}
        for cycle in cycles
    ]
    h = len(set().union(*interiors)) if interiors else 0
    s = 0
    for x in range(1, WIDTH):
        for y in range(1, n):
            corners = {(x, y), (x + 1, y),
                       (x, y + 1), (x + 1, y + 1)}
            if any(corners <= interior for interior in interiors):
                s += 1
    q = sum(len(cycle) == 4 for cycle in cycles)
    return len(A), h, len(cycles), s, q


def literal_sides(stats):
    v, h, c, s, q = stats
    return v, 2 * h + 6 * c - 2 * s - 2 * q


def brute_recompute(A, n):
    # Recheck every occupied vertex against every other occupied vertex.
    for p in A:
        degree = sum(abs(p[0] - r[0]) + abs(p[1] - r[1]) == 1
                     for r in A)
        if degree != 2:
            raise ValueError("Witness is outside the hypotheses")
    return statistics(A, n, inside_winding)


def fail(message):
    print("SANITY FAILED:", message)
    sys.exit(0)


def sanity_checks():
    examples = [
        (1, frozenset(), (0, 0, 0, 0, 0)),
        (2, frozenset({(1, 1), (2, 1), (1, 2), (2, 2)}),
         (4, 0, 1, 0, 1)),
        (4, frozenset((x, y) for x in range(1, 5)
                      for y in range(1, 5)
                      if x in (1, 4) or y in (1, 4)),
         (12, 4, 1, 1, 0)),
    ]
    for n, A, expected in examples:
        if not valid(A, n):
            fail("Known example failed degree check")
        if statistics(A, n) != expected or brute_recompute(A, n) != expected:
            fail("Known geometric statistics disagree")
    print("SANITY 1 PASS: empty set, unit square, and 4-by-4 boundary")

    total = 0
    for n in range(1, 4):
        points = vertices(n)
        brute = set()
        for bits in itertools.product((0, 1), repeat=len(points)):
            A = frozenset(p for p, bit in zip(points, bits) if bit)
            if valid(A, n):
                brute.add(A)
        generated_list = list(candidates(n))
        if len(generated_list) != len(set(generated_list)):
            fail("Duplicate generated subset")
        if set(generated_list) != brute:
            fail("Pruned enumeration differs from full subset enumeration")
        for A in brute:
            if statistics(A, n) != brute_recompute(A, n):
                fail("Ray casting and winding statistics disagree")
        total += len(brute)
    print("SANITY 2 PASS: full subset cross-check for n=1..3;",
          total, "admissible subsets")


def main():
    sanity_checks()
    tested = 0
    for n in range(1, MAX_N + 1):
        for A in candidates(n):
            if not valid(A, n):
                fail("Generator produced an inadmissible subset")
            stats = statistics(A, n)
            lhs, rhs = literal_sides(stats)
            tested += 1
            if lhs != rhs:
                second_stats = brute_recompute(A, n)
                second_lhs, second_rhs = literal_sides(second_stats)
                if second_stats != stats or second_lhs == second_rhs:
                    fail("Candidate counterexample failed independent recomputation")
                print("COUNTEREXAMPLE:",
                      "n =", n, "A =", sorted(A),
                      "v(A) =", second_lhs,
                      "2h(A)+6c(A)-2s(A)-2q(A) =", second_rhs,
                      "(v,h,c,s,q) =", second_stats)
                return
    covered = sum(1 << (WIDTH * n) for n in range(1, MAX_N + 1))
    print("NO COUNTEREXAMPLE",
          "n=1..6, all A subsets of {1,2,3,4} x {1,...,n};",
          tested, "admissible cases tested;",
          covered, "subsets exhaustively covered by degree pruning")


if __name__ == "__main__":
    main()