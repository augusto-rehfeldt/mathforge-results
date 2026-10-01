#!/usr/bin/env python3
import itertools
import sys


def cycle_displacements(vertices):
    """Displacements of the directed cycle; all other points are fixed."""
    return tuple(
        vertices[(i + 1) % len(vertices)] - vertices[i]
        for i in range(len(vertices))
    )


def valid_cycle(vertices, n, a, b, c):
    return (
        len(vertices) == 6
        and len(set(vertices)) == 6
        and all(1 <= v <= n for v in vertices)
        and sorted(cycle_displacements(vertices)) == [-c, -b, -a, a, b, c]
    )


def displacement_search(a, b, c):
    """
    Exhaust every possible cycle up to translation and rotation.

    Each eligible cycle has exactly one +a edge, so rotate it to put that
    edge first. Enumerating the remaining five steps covers every cycle.
    The minimum number of consecutive integer positions needed is its
    maximum vertex minus its minimum vertex plus one.
    """
    best_width = None
    best_vertices = None
    for tail in itertools.permutations((-a, b, -b, c, -c)):
        steps = (a,) + tail
        position = 0
        vertices = []
        for step in steps:
            vertices.append(position)
            position += step
        if position != 0 or len(set(vertices)) != 6:
            continue
        low, high = min(vertices), max(vertices)
        width = high - low + 1
        if best_width is None or width < best_width:
            best_width = width
            best_vertices = tuple(v - low + 1 for v in vertices)
    return best_width, best_vertices


def plain_brute_exists(n, a, b, c):
    """Enumerate every subset and every directed cycle, without step tricks."""
    target = [-c, -b, -a, a, b, c]
    for subset in itertools.combinations(range(1, n + 1), 6):
        # Fixing the smallest vertex first removes only cyclic rotations.
        for tail in itertools.permutations(subset[1:]):
            vertices = (subset[0],) + tail
            if sorted(cycle_displacements(vertices)) == target:
                return True, vertices
    return False, None


def plain_brute_records(n):
    """Record all eligible displacement triples from all directed six-cycles."""
    records = set()
    cycles = 0
    for subset in itertools.combinations(range(1, n + 1), 6):
        for tail in itertools.permutations(subset[1:]):
            vertices = (subset[0],) + tail
            cycles += 1
            ds = cycle_displacements(vertices)
            positive = sorted(d for d in ds if d > 0)
            negative = sorted(-d for d in ds if d < 0)
            if (
                len(positive) == 3
                and positive == negative
                and len(set(positive)) == 3
            ):
                a, b, c = positive
                if c != a + b:
                    records.add((a, b, c))
    return records, cycles


def sanity_failure(message):
    print("SANITY FAILED:", message)
    sys.exit(0)


# Independent sanity check 1: explicit permutation and known absence.
known_cycle = (1, 2, 6, 4, 3, 5)
if not valid_cycle(known_cycle, 6, 1, 2, 4):
    sanity_failure("explicit six-cycle")
exists, _ = plain_brute_exists(6, 1, 2, 5)
if exists:
    sanity_failure("unexpected cycle for n=6, (a,b,c)=(1,2,5)")
print("Sanity 1 passed: explicit (1,2,4) cycle; brute-force (1,2,5) absence.")

# Independent sanity check 2: exhaustive subset/cycle enumeration versus
# the displacement-order routine, including expected cycle enumeration counts.
for n, expected_cycles in ((6, 120), (7, 840)):
    records, cycle_count = plain_brute_records(n)
    if cycle_count != expected_cycles:
        sanity_failure("directed-cycle enumeration count")
    for a, b, c in itertools.combinations(range(1, n), 3):
        if c == a + b:
            continue
        width, vertices = displacement_search(a, b, c)
        computed = width is not None and width <= n
        if computed != ((a, b, c) in records):
            sanity_failure(f"routine disagreement at {(n, a, b, c)}")
        if computed and not valid_cycle(vertices, n, a, b, c):
            sanity_failure("invalid displacement-search cycle")
    print(f"Sanity 2 passed for n={n}: all {cycle_count} directed cycles checked.")

# Exhaust the entire requested space. Translation is accounted for by width;
# rotation is accounted for by anchoring the unique +a edge.
cache = {}
cases = 0
for n in range(6, 17):
    for a, b, c in itertools.combinations(range(1, n), 3):
        if c == a + b:
            continue
        cases += 1
        key = (a, b, c)
        if key not in cache:
            cache[key] = displacement_search(a, b, c)
        width, vertices = cache[key]
        actual = width is not None and width <= n
        claimed = n >= b + c - a + 1

        if actual != claimed:
            # Independently recompute existence by the plain subset/cycle
            # enumeration, and recompute the statement's literal inequality.
            verified_actual, verified_cycle = plain_brute_exists(n, a, b, c)
            verified_claimed = n >= b + c - a + 1
            if verified_actual != actual:
                sanity_failure("candidate failed independent verification")
            if verified_actual != verified_claimed:
                if verified_actual and not valid_cycle(
                    verified_cycle, n, a, b, c
                ):
                    sanity_failure("invalid independently verified witness")
                print(
                    "COUNTEREXAMPLE:",
                    f"n={n}, a={a}, b={b}, c={c}; "
                    f"brute_force_exists={verified_actual}; "
                    f"(n >= b+c-a+1)={verified_claimed}; "
                    f"threshold={b + c - a + 1}; "
                    f"cycle={verified_cycle}"
                )
                sys.exit(0)

print(
    "NO COUNTEREXAMPLE",
    "ranges: 6<=n<=16, 1<=a<b<c<=n-1, c!=a+b;",
    f"cases tested={cases}"
)
sys.exit(0)