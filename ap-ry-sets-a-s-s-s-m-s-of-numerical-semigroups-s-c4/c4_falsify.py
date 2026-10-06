#!/usr/bin/env python3
import heapq
import math
import time

# Exhaustive lexicographic search, with a hard time budget. A stopped search
# reports its exact lexicographic prefix, not an unsearched rectangular range.
START = time.monotonic()
DEADLINE = START + 220.0
INF = 10**30


def apery(m, generators):
    """Shortest paths on residues; the generator m supplies redundant loops."""
    dist = [INF] * m
    dist[0] = 0
    heap = [(0, 0)]
    edges = [(x % m, x) for x in generators if x % m]
    while heap:
        value, r = heapq.heappop(heap)
        if value != dist[r]:
            continue
        for shift, weight in edges:
            s = (r + shift) % m
            candidate = value + weight
            if candidate < dist[s]:
                dist[s] = candidate
                heapq.heappush(heap, (candidate, s))
    return dist


def invariants(w, m):
    assert max(w) < INF
    c = max(w) - m + 1
    numerator = 2 * sum(w) - m * (m - 1)
    assert numerator % (2 * m) == 0
    return c, numerator // (2 * m)


def membership_table(generators, limit):
    reachable = bytearray(limit + 1)
    reachable[0] = 1
    for n in range(1, limit + 1):
        reachable[n] = any(n >= x and reachable[n - x]
                           for x in generators)
    return reachable


def minimal_brute(generators):
    if len(set(generators)) != len(generators):
        return False
    for i, x in enumerate(generators):
        others = generators[:i] + generators[i + 1:]
        if membership_table(others, x)[x]:
            return False
    return True


def brute_invariants(generators):
    """Plain integer-by-integer membership, stopping at m consecutive members."""
    m = min(generators)
    reachable = [True]
    run = 0
    gaps = 0
    n = 0
    while True:
        n += 1
        present = any(n >= x and reachable[n - x] for x in generators)
        reachable.append(present)
        if present:
            run += 1
            if run == m:
                c = n - m + 1
                return c, gaps
        else:
            run = 0
            gaps += 1


def sanity():
    try:
        known = [
            ((4, 5, 6, 7), (4, 3)),
            ((4, 6, 9), (12, 6)),
            ((3, 5), (8, 4)),
        ]
        for gens, expected in known:
            assert invariants(apery(min(gens), gens), min(gens)) == expected
            assert brute_invariants(gens) == expected
        print("SANITY 1: known conductor/genus values passed", flush=True)

        checks = 0
        for m in range(4, 9):
            for a in range(m + 1, 2 * m):
                for b in range(a + 1, 2 * m):
                    base = apery(m, (m, a, b))
                    table = membership_table((m, a, b), 8 * m)
                    for d in range(2 * m, 8 * m + 1):
                        e = d - m
                        fast_minimal = (
                            e not in (m, a, b)
                            and d < base[d % m]
                            and e < base[e % m]
                        )
                        assert fast_minimal == (
                            minimal_brute((m, a, b, d))
                            and minimal_brute((m, a, b, e))
                        )
                        assert bool(table[d]) == (d >= base[d % m])
                        if math.gcd(math.gcd(m, a), math.gcd(b, d)) == 1:
                            for gens in ((m, a, b, d), (m, a, b, e)):
                                assert invariants(apery(m, gens), m) == \
                                       brute_invariants(gens)
                            checks += 1
        print("SANITY 2: independent membership/minimality and "
              f"brute-force invariant cross-checks passed ({checks} pairs)",
              flush=True)
    except Exception as exc:
        print("SANITY FAILED", repr(exc), flush=True)
        return False
    return True


def report_clean(last, tested, examined, complete):
    description = (
        "4<=m<=80, m<a<b<2m, 2m<=d<=8m"
        if complete else
        "lexicographic prefix of [4<=m<=80, m<a<b<2m, "
        f"2m<=d<=8m], through {last!r} inclusive"
    )
    print(f"NO COUNTEREXAMPLE; ranges checked: {description}; "
          f"cases tested: {tested}; raw quadruples examined: {examined}")


def main():
    if not sanity():
        return

    tested = 0
    examined = 0
    last = None

    for m in range(4, 81):
        for a in range(m + 1, 2 * m):
            for b in range(a + 1, 2 * m):
                base = apery(m, (m, a, b))
                cache = {}
                common_gcd = math.gcd(math.gcd(m, a), b)

                def get_invariants(x):
                    if x not in cache:
                        cache[x] = invariants(apery(m, (m, a, b, x)), m)
                    return cache[x]

                for d in range(2 * m, 8 * m + 1):
                    if time.monotonic() >= DEADLINE:
                        report_clean(last, tested, examined, False)
                        return

                    last = (m, a, b, d)
                    examined += 1
                    e = d - m

                    if math.gcd(common_gcd, d) != 1:
                        continue
                    # Since a,b<2m and every generator is >=m, neither
                    # a nor b can be a sum of two positive generators.
                    # The only additional issue is a duplicate generator.
                    if e in (m, a, b):
                        continue
                    if d >= base[d % m] or e >= base[e % m]:
                        continue

                    cs, gs = get_invariants(d)
                    ct, gt = get_invariants(e)
                    if cs - ct < m:
                        continue

                    tested += 1
                    left = 4 * (gs - gt)
                    right = 3 * (cs - ct)
                    if left <= right:
                        continue

                    # Recheck every hypothesis and both sides independently.
                    sg = (m, a, b, d)
                    tg = (m, a, b, e)
                    if not (4 <= m < a < b < 2 * m <= d <= 8 * m
                            and math.gcd(common_gcd, d) == 1
                            and minimal_brute(sg)
                            and minimal_brute(tg)):
                        print("SANITY FAILED: candidate hypotheses")
                        return
                    bcs, bgs = brute_invariants(sg)
                    bct, bgt = brute_invariants(tg)
                    brute_left = 4 * (bgs - bgt)
                    brute_right = 3 * (bcs - bct)
                    if ((bcs, bgs, bct, bgt) != (cs, gs, ct, gt)
                            or bcs - bct < m
                            or brute_left <= brute_right):
                        print("SANITY FAILED: candidate recomputation")
                        return

                    print(f"COUNTEREXAMPLE: (m,a,b,d)={last}; "
                          f"4(g(S)-g(T))={brute_left}; "
                          f"3(c(S)-c(T))={brute_right}")
                    return

    report_clean(last, tested, examined, True)


if __name__ == "__main__":
    main()