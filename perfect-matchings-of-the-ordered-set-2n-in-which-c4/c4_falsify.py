#!/usr/bin/env python3
import itertools
import math
from collections import Counter


def matchings(points):
    """Enumerate each perfect matching exactly once, pairing the first point."""
    if not points:
        yield ()
        return
    a = points[0]
    for k in range(1, len(points)):
        b = points[k]
        rest = points[1:k] + points[k + 1:]
        for tail in matchings(rest):
            yield ((a, b),) + tail


def classify(arcs):
    """Return (component count, nested-pair count), or None if not 2-regular."""
    n = len(arcs)
    adjacency = [0] * n
    degrees = [0] * n
    nested = 0
    for i in range(n):
        a, b = arcs[i]
        for k in range(i + 1, n):
            s, t = arcs[k]
            if a < s < b < t or s < a < t < b:
                degrees[i] += 1
                degrees[k] += 1
                if degrees[i] > 2 or degrees[k] > 2:
                    return None
                adjacency[i] |= 1 << k
                adjacency[k] |= 1 << i
            elif a < s < t < b or s < a < b < t:
                nested += 1
    if any(d != 2 for d in degrees):
        return None

    unseen = (1 << n) - 1
    components = 0
    while unseen:
        components += 1
        frontier = unseen & -unseen
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            if not unseen & bit:
                continue
            unseen ^= bit
            frontier |= adjacency[bit.bit_length() - 1] & unseen
    return components, nested


def plain_classify(arcs):
    """Independent implementation using sorted endpoints and set-valued graphs."""
    graph = [set() for _ in arcs]
    nested = 0
    for i, first in enumerate(arcs):
        for k in range(i + 1, len(arcs)):
            second = arcs[k]
            order = sorted([(x, 0) for x in first] +
                           [(x, 1) for x in second])
            labels = tuple(label for _, label in order)
            if labels in ((0, 1, 0, 1), (1, 0, 1, 0)):
                graph[i].add(k)
                graph[k].add(i)
            elif labels in ((0, 1, 1, 0), (1, 0, 0, 1)):
                nested += 1
    if any(len(neighbors) != 2 for neighbors in graph):
        return None
    unseen = set(range(len(arcs)))
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            v = stack.pop()
            new = graph[v] & unseen
            unseen.difference_update(new)
            stack.extend(new)
    return components, nested


def reverse_matchings(points):
    """Independent exhaustive generator, pairing the last point."""
    if not points:
        yield ()
        return
    b = points[-1]
    for k, a in enumerate(points[:-1]):
        rest = points[:k] + points[k + 1:-1]
        for tail in reverse_matchings(rest):
            yield tail + ((a, b),)


def plain_counts(n):
    counts = Counter()
    total = 0
    for arcs in reverse_matchings(tuple(range(1, 2 * n + 1))):
        total += 1
        result = plain_classify(arcs)
        if result is not None:
            counts[result] += 1
    return counts, total


def expected(n, c, j):
    threshold = n - 3 * c
    if j < threshold:
        return 0
    assert j == threshold
    return 2 ** (n - 3 * c) * math.comb(n - 2 * c - 1, c - 1)


def sanity():
    # Enumeration cardinalities, independently known as (2n-1)!!.
    observed = []
    wanted = []
    for n in range(1, 6):
        observed.append(sum(1 for _ in matchings(tuple(range(1, 2 * n + 1)))))
        wanted.append(math.prod(range(1, 2 * n, 2)))
    ok = observed == wanted
    print("SANITY enumeration cardinalities:", observed, "expected:", wanted,
          "PASS" if ok else "FAIL", flush=True)
    if not ok:
        return False

    # Independent permutation construction, independent graph classifier,
    # and direct per-matching comparison on n=3,4.
    for n in (3, 4):
        independent = set()
        for perm in itertools.permutations(range(1, 2 * n + 1)):
            arcs = tuple(sorted(tuple(sorted(perm[k:k + 2]))
                                for k in range(0, 2 * n, 2)))
            independent.add(arcs)
        generated = set(matchings(tuple(range(1, 2 * n + 1))))
        ok = generated == independent
        counts = Counter()
        for arcs in independent:
            fast = classify(arcs)
            plain = plain_classify(arcs)
            if fast != plain:
                ok = False
            if plain is not None:
                counts[plain] += 1
        if n == 3:
            # Three mutually crossing arcs: uniquely (1,4),(2,5),(3,6).
            ok = ok and counts == Counter({(1, 0): 1})
        print("SANITY independent permutation/graph check:",
              "n =", n, "matchings =", len(independent),
              "retained counts =", dict(sorted(counts.items())),
              "PASS" if ok else "FAIL", flush=True)
        if not ok:
            return False
    return True


def main():
    if not sanity():
        print("SANITY FAILED")
        return

    total_matchings = 0
    relations_tested = 0
    for n in range(3, 9):
        counts = Counter()
        layer_total = 0
        for arcs in matchings(tuple(range(1, 2 * n + 1))):
            layer_total += 1
            result = classify(arcs)
            if result is not None:
                counts[result] += 1
        total_matchings += layer_total

        for c in range(1, n // 3 + 1):
            for j in range(n - 3 * c + 1):
                relations_tested += 1
                actual = counts[c, j]
                claimed = expected(n, c, j)
                if actual != claimed:
                    # Re-enumerate the entire layer using the independent,
                    # plain generator and classifier before reporting.
                    verified, verification_total = plain_counts(n)
                    verified_actual = verified[c, j]
                    verified_claimed = expected(n, c, j)
                    if (verification_total != layer_total or
                            verified_actual != actual):
                        print("SANITY FAILED")
                        return
                    if verified_actual != verified_claimed:
                        print(
                            "COUNTEREXAMPLE:",
                            f"(n={n}, c={c}, j={j}); "
                            f"brute-force A(n,c,j)={verified_actual}; "
                            f"claimed A(n,c,j)={verified_claimed}"
                        )
                        return

    print(
        "NO COUNTEREXAMPLE",
        "ranges: 3 <= n <= 8, 1 <= c <= floor(n/3), "
        "0 <= j <= n-3c; every retained arc has degree 2;",
        f"cases tested: {relations_tested} asserted relations, "
        f"{total_matchings} perfect matchings"
    )


if __name__ == "__main__":
    main()