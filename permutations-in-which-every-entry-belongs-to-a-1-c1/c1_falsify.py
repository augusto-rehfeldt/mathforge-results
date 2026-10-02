import itertools
import sys
from collections import Counter

MAX_N = 9
cases = 0
deletion_cases = 0


def occurrences(p):
    """Enumerate every 132-occurrence, using zero-based positions."""
    out = []
    n = len(p)
    for i in range(n - 2):
        a = p[i]
        for j in range(i + 1, n - 1):
            b = p[j]
            if a < b:
                for k in range(j + 1, n):
                    if a < p[k] < b:
                        out.append((i, j, k))
    return out


def is_member(p, occ):
    """Coverage plus a connected, acyclic incidence graph."""
    n = len(p)
    covered = set()
    for triple in occ:
        covered.update(triple)
    if len(covered) != n:
        return False

    vertices = n + len(occ)
    if 3 * len(occ) != vertices - 1:
        return False

    parent = list(range(vertices))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for r, triple in enumerate(occ):
        for i in triple:
            a, b = find(i), find(n + r)
            if a == b:
                return False
            parent[a] = b
    return len({find(v) for v in range(vertices)}) == 1


def plain_occurrences(p):
    return [
        (i, j, k)
        for i, j, k in itertools.combinations(range(len(p)), 3)
        if p[i] < p[k] < p[j]
    ]


def plain_member(p, occ):
    """Independent adjacency-list traversal and edge count."""
    n = len(p)
    graph = [[] for _ in range(n + len(occ))]
    for r, triple in enumerate(occ):
        for i in triple:
            graph[i].append(n + r)
            graph[n + r].append(i)
    if any(not graph[i] for i in range(n)):
        return False
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for w in graph[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    edges = sum(map(len, graph)) // 2
    return len(seen) == len(graph) and edges == len(graph) - 1


def statistics(p):
    inv = sum(p[i] > p[j]
              for i in range(len(p))
              for j in range(i + 1, len(p)))
    des = sum(p[i] > p[i + 1] for i in range(len(p) - 1))
    return inv, des


def plain_statistics(p):
    inversions = list(itertools.combinations(p, 2))
    return (
        len([pair for pair in inversions if pair[0] > pair[1]]),
        len([i for i in range(1, len(p)) if p[i - 1] > p[i]]),
    )


def claimed_permutation(n):
    if n < 3 or n % 2 == 0:
        return None
    return (1,) + tuple(
        x for r in range(1, (n - 1) // 2 + 1)
        for x in (2 * r + 1, 2 * r)
    )


def standardize(values):
    rank = {x: i + 1 for i, x in enumerate(sorted(values))}
    return tuple(rank[x] for x in values)


def fail_sanity(message):
    print("SANITY FAILED", message)
    sys.exit(0)


def report(witness, actual, claimed, verified_actual, verified_claimed):
    if (actual, claimed) != (verified_actual, verified_claimed):
        fail_sanity("counterexample did not survive independent recomputation")
    if verified_actual == verified_claimed:
        fail_sanity("purported counterexample is not a discrepancy")
    print("COUNTEREXAMPLE:", {
        "witness": witness,
        "brute_force_side": verified_actual,
        "claimed_side": verified_claimed,
    })
    sys.exit(0)


# Sanity check 1: known small cases and independently computed statistics.
small_survivors = {}
for n in range(1, 4):
    small_survivors[n] = [
        p for p in itertools.permutations(range(1, n + 1))
        if is_member(p, occurrences(p))
    ]
if small_survivors != {1: [], 2: [], 3: [(1, 3, 2)]}:
    fail_sanity(("known small cases", small_survivors))
if statistics((3, 2, 1)) != (3, 2):
    fail_sanity("descending length-three statistics")
print("SANITY 1 PASSED: T_1=T_2=empty; T_3={(1,3,2)}; inv(321)=3, des(321)=2")

# Sanity check 2: exhaustive independent implementations through length five.
cross_checks = 0
for n in range(1, 6):
    for p in itertools.permutations(range(1, n + 1)):
        a, b = occurrences(p), plain_occurrences(p)
        if a != b or is_member(p, a) != plain_member(p, b):
            fail_sanity(("occurrence/graph cross-check", p))
        if statistics(p) != plain_statistics(p):
            fail_sanity(("statistics cross-check", p))
        cross_checks += 1
print("SANITY 2 PASSED: independent occurrence, graph, and statistic checks;",
      cross_checks, "permutations of lengths 1..5")

for n in range(1, MAX_N + 1):
    expected = claimed_permutation(n)
    polynomial = Counter()

    for p in itertools.permutations(range(1, n + 1)):
        cases += 1
        occ = occurrences(p)
        actual_member = is_member(p, occ)
        claimed_member = p == expected

        if actual_member != claimed_member:
            fresh = plain_occurrences(p)
            report(
                {"relation": "membership in T_n", "n": n, "permutation": p,
                 "132_occurrences": fresh},
                actual_member, claimed_member,
                plain_member(p, fresh),
                p == claimed_permutation(n),
            )

        if not actual_member:
            continue

        inv, des = statistics(p)
        polynomial[(inv, des)] += 1
        m = (n - 1) // 2

        if (inv, des) != (m, m):
            report(
                {"relation": "monomial q^inv t^des = q^m t^m",
                 "n": n, "permutation": p,
                 "132_occurrences": plain_occurrences(p)},
                (inv, des), (m, m),
                plain_statistics(p), ((n - 1) // 2,) * 2,
            )

        if n < 5:
            continue

        degrees = Counter(i for triple in occ for i in triple)
        for triple in occ:
            deletion_cases += 1
            exclusive = tuple(i for i in triple if degrees[i] == 1)
            retained = [x for i, x in enumerate(p) if i not in exclusive]
            reduced = standardize(retained)
            reduced_stats = statistics(reduced)
            actual = (
                len(exclusive),
                reduced,
                inv - reduced_stats[0],
                des - reduced_stats[1],
            )
            claimed = (2, claimed_permutation(n - 2), 1, 1)

            if actual != claimed:
                fresh = plain_occurrences(p)
                fresh_exclusive = tuple(
                    i for i in triple
                    if sum(i in other for other in fresh) == 1
                )
                kept = tuple(
                    p[i] for i in range(n) if i not in fresh_exclusive
                )
                # Independent standardization by counting smaller entries.
                fresh_reduced = tuple(
                    1 + sum(y < x for y in kept) for x in kept
                )
                old_stats = plain_statistics(p)
                new_stats = plain_statistics(fresh_reduced)
                verified = (
                    len(fresh_exclusive),
                    fresh_reduced,
                    old_stats[0] - new_stats[0],
                    old_stats[1] - new_stats[1],
                )
                report(
                    {"relation": "exclusive-entry deletion",
                     "n": n, "permutation": p,
                     "occurrence": triple, "132_occurrences": fresh,
                     "deleted_positions": fresh_exclusive},
                    actual, claimed, verified,
                    (2, claimed_permutation(n - 2), 1, 1),
                )

    # Explicit literal polynomial comparison, with fresh brute-force
    # recomputation if it ever disagrees.
    if n >= 3 and n % 2:
        m = (n - 1) // 2
        expected_polynomial = Counter({(m, m): 1})
        if polynomial != expected_polynomial:
            fresh_polynomial = Counter()
            for p in itertools.permutations(range(1, n + 1)):
                fresh = plain_occurrences(p)
                if plain_member(p, fresh):
                    fresh_polynomial[plain_statistics(p)] += 1
            report(
                {"relation": "polynomial sum", "n": n,
                 "representation": "(q exponent, t exponent) -> coefficient"},
                dict(polynomial), dict(expected_polynomial),
                dict(fresh_polynomial),
                {(m, m): 1},
            )

print("NO COUNTEREXAMPLE",
      f"ranges: all permutations for 1 <= n <= {MAX_N}; "
      f"all occurrence deletions in survivors for 5 <= n <= {MAX_N}; "
      f"cases tested: {cases} permutations, {deletion_cases} deletions; "
      f"sanity cross-check cases: {cross_checks}")