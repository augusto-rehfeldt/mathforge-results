import heapq
import math
import sys


def minimal(gens):
    # Test each generator using only the other three.
    for target in gens:
        reachable = [False] * (target + 1)
        reachable[0] = True
        others = [g for g in gens if g != target and g <= target]
        for n in range(1, target + 1):
            reachable[n] = any(n >= g and reachable[n - g] for g in others)
        if reachable[target]:
            return False
    return True


def apery(m, a, b, d):
    inf = float("inf")
    dist = [inf] * m
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        value, residue = heapq.heappop(heap)
        if value != dist[residue]:
            continue
        for g in (a, b, d):
            nxt = (residue + g) % m
            candidate = value + g
            if candidate < dist[nxt]:
                dist[nxt] = candidate
                heapq.heappush(heap, (candidate, nxt))
    return dist


def ambiguous(w, a, b, d):
    solutions = 0
    for x in range(w // a + 1):
        remainder = w - x * a
        for y in range(remainder // b + 1):
            if (remainder - y * b) % d == 0:
                solutions += 1
                if solutions == 2:
                    return True
    return False


def evaluate(gens):
    m, a, b, d = gens
    A = apery(m, a, b, d)
    c = max(A) - m + 1
    L = sum(s >= A[s % m] for s in range(c))
    q = sum(ambiguous(w, a, b, d) for w in A)
    return A, c, L, q, 4 * L - c, m - 4 + q


def brute(gens):
    # Build S directly until m consecutive members establish the conductor.
    m, a, b, d = gens
    member = [True]
    run = 1
    n = 0
    while run < m:
        n += 1
        present = any(n >= g and member[n - g] for g in gens)
        member.append(present)
        run = run + 1 if present else 0
    c = n - m + 1

    # Extend far enough to find every Apéry element directly.
    end = c + m - 1
    for n in range(len(member), end + 1):
        member.append(any(n >= g and member[n - g] for g in gens))

    A = [s for s in range(end + 1)
         if member[s] and (s < m or not member[s - m])]
    L = sum(member[:c])

    # Literal exhaustive triple enumeration, with no early stopping.
    q = 0
    for w in A:
        count = 0
        for x in range(w // a + 1):
            for y in range(w // b + 1):
                for z in range(w // d + 1):
                    if x * a + y * b + z * d == w:
                        count += 1
        q += count >= 2

    return sorted(A), c, L, q, 4 * L - c, m - 4 + q


def sanity_failure(message):
    print("SANITY FAILED", message)
    sys.exit(0)


def main():
    known = evaluate((4, 5, 6, 7))
    if known != ([0, 5, 6, 7], 4, 1, 0, 0, 0):
        sanity_failure("known semigroup <4,5,6,7>")
    print("SANITY 1 PASSED: <4,5,6,7>, A={0,5,6,7}, c=4, |L|=1, q=0")

    checks = 0
    for m in range(4, 9):
        for a in range(m + 1, 25):
            for b in range(a + 1, 26):
                d = a + b - m
                gens = (m, a, b, d)
                if d > 30 or math.gcd(*gens) != 1 or not minimal(gens):
                    continue
                fast = evaluate(gens)
                fast = (sorted(fast[0]),) + fast[1:]
                if fast != brute(gens):
                    sanity_failure("shortest paths versus direct membership/triples: "
                                   + repr(gens))
                checks += 1
    if not checks:
        sanity_failure("empty cross-check")
    print("SANITY 2 PASSED:", checks,
          "valid tuples cross-checked by direct membership and triple enumeration")

    # Independent minimality examples.
    if not minimal((4, 5, 6, 7)) or minimal((4, 5, 6, 8)):
        sanity_failure("minimality examples")
    print("SANITY 3 PASSED: minimality accepts <4,5,6,7> and rejects <4,5,6,8>")

    tested = 0
    for m in range(4, 26):
        for a in range(m + 1, 121):
            for b in range(a + 1, 121):
                d = a + b - m
                if d > 120:
                    break
                gens = (m, a, b, d)
                if not (4 <= m < a < b < d <= 120):
                    continue
                if math.gcd(*gens) != 1 or not minimal(gens):
                    continue
                tested += 1
                result = evaluate(gens)
                lhs, rhs = result[-2:]
                if lhs < rhs:
                    confirmation = brute(gens)
                    normalized = (sorted(result[0]),) + result[1:]
                    if normalized != confirmation:
                        sanity_failure("witness recomputation mismatch: " + repr(gens))
                    if confirmation[-2] < confirmation[-1]:
                        print("COUNTEREXAMPLE:",
                              "m,a,b,d=" + repr(gens),
                              "4|L|-c=" + str(confirmation[-2]),
                              "m-4+q=" + str(confirmation[-1]))
                        return

    print("NO COUNTEREXAMPLE",
          "ranges: 4<=m<=25, m<a<b<d<=120, d=a+b-m;",
          "gcd=1 and minimal generating set;",
          "cases tested=" + str(tested))


if __name__ == "__main__":
    main()