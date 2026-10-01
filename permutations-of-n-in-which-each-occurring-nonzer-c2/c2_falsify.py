import itertools
import time
import sys

def hypotheses(n, a, b, c):
    return n >= 1 and n - 1 < 2 * a and a < b < c <= n - 1

def assemble(n, edges):
    p = list(range(1, n + 1))
    for x, y in edges:
        p[x - 1] = y
    return tuple(p)

def cycle_lengths(p):
    seen = set()
    lengths = []
    for x in range(1, len(p) + 1):
        if x not in seen:
            y, length = x, 0
            while y not in seen:
                seen.add(y)
                length += 1
                y = p[y - 1]
            lengths.append(length)
    return sorted(lengths)

def fast_enumerate(n, a, b, c):
    """Enumerate disjoint directed cycles using each displacement label once."""
    ds = (a, -a, b, -b, c, -c)
    cache = {}

    def available_cycles(mask):
        if mask in cache:
            return cache[mask]
        anchor = (mask & -mask).bit_length() - 1
        result = []
        for start in range(1, n + 1):
            end = start + ds[anchor]
            if not 1 <= end <= n:
                continue
            vertices = {start, end}
            edges = [(start, end)]

            def extend(current, used):
                remaining = mask & ~used
                for j in range(6):
                    bit = 1 << j
                    if not remaining & bit:
                        continue
                    target = current + ds[j]
                    if not 1 <= target <= n:
                        continue
                    if target == start:
                        result.append((used | bit, frozenset(vertices),
                                       tuple(edges + [(current, target)])))
                    elif target not in vertices:
                        vertices.add(target)
                        edges.append((current, target))
                        extend(target, used | bit)
                        edges.pop()
                        vertices.remove(target)

            extend(end, 1 << anchor)
        cache[mask] = result
        return result

    answers = set()

    def cover(mask, occupied, edges):
        if not mask:
            answers.add(assemble(n, edges))
            return
        for used, vertices, cycle_edges in available_cycles(mask):
            if not occupied.intersection(vertices):
                cover(mask ^ used, occupied | vertices, edges + cycle_edges)

    cover(63, frozenset(), ())
    return answers

def plain_enumerate(n, a, b, c):
    """Literal injection search, with no cycle-based assumptions."""
    ds = (a, -a, b, -b, c, -c)
    domains = [
        tuple(x for x in range(1, n + 1) if 1 <= x + d <= n)
        for d in ds
    ]
    answers = set()
    for sources in itertools.product(*domains):
        if len(set(sources)) != 6:
            continue
        p = assemble(n, zip(sources, (x + d for x, d in zip(sources, ds))))
        if len(set(p)) == n:
            answers.add(p)
    return answers

def claimed_side(n, a, b, c):
    s = a + c - b
    expected = set()
    invalid = []
    for t in range(1, n - s + 1):
        cycle = (t + b - a, t + b, t, t + c, t + c - a, t + s)
        if len(set(cycle)) != 6 or any(not 1 <= x <= n for x in cycle):
            invalid.append(cycle)
            continue
        for order in (cycle, tuple(reversed(cycle))):
            expected.add(assemble(n, zip(order, order[1:] + order[:1])))
    return 2 * (n - s), expected, invalid

def compare(n, a, b, c, actual):
    count, expected, invalid = claimed_side(n, a, b, c)
    long_cycles = {p for p in actual if max(cycle_lengths(p)) > 2}
    if len(long_cycles) != count:
        return ("number with a cycle longer than two", len(long_cycles), count)
    if invalid or long_cycles != expected:
        return ("literal cycle list",
                sorted(long_cycles), {"permutations": sorted(expected),
                                      "invalid_cycles": invalid})
    for p in sorted(actual):
        lengths = cycle_lengths(p)
        fixed = lengths.count(1)
        positive = sum(y - x for x, y in enumerate(p, 1) if y > x)
        if p in long_cycles:
            got = (fixed, len(lengths), positive)
            want = (n - 6, n - 5, a + b + c)
        else:
            got = lengths
            want = sorted([1] * (n - 6) + [2, 2, 2])
        if got != want:
            return ("consequent for permutation " + repr(p), got, want)
    return None

def sanity():
    # Independent check 1: enumerate every permutation, not displacement injections.
    n, a, b, c = 7, 4, 5, 6
    assert hypotheses(n, a, b, c)
    wanted = sorted((a, -a, b, -b, c, -c))
    exhaustive = set()
    for p in itertools.permutations(range(1, n + 1)):
        displacements = sorted(y - x for x, y in enumerate(p, 1) if y != x)
        if displacements == wanted:
            exhaustive.add(p)
    got = fast_enumerate(n, a, b, c)
    if got != exhaustive:
        print("SANITY FAILED")
        sys.exit(0)
    print("SANITY 1 PASSED: all 7! permutations cross-check; count =", len(got))

    # Independent check 2: literal injection enumeration for every admissible
    # triple at n=8.
    checked = 0
    for a, b, c in itertools.combinations(range(1, 8), 3):
        if hypotheses(8, a, b, c):
            if fast_enumerate(8, a, b, c) != plain_enumerate(8, a, b, c):
                print("SANITY FAILED")
                sys.exit(0)
            checked += 1
    print("SANITY 2 PASSED: literal injection cross-check;", checked, "triples")

def main():
    start = time.monotonic()
    sanity()
    tested = []
    completed_n = 0
    for n in range(1, 21):
        triples = [abc for abc in itertools.combinations(range(1, n), 3)
                   if hypotheses(n, *abc)]
        for a, b, c in triples:
            # Leave time for verification if a discrepancy occurs.
            if time.monotonic() - start > 215:
                print("NO COUNTEREXAMPLE",
                      "exact checked (n,a,b,c) cases =", tested,
                      "cases tested =", len(tested),
                      "fully completed n range = 1.." + str(completed_n))
                return
            actual = fast_enumerate(n, a, b, c)
            failure = compare(n, a, b, c, actual)
            if failure is not None:
                # Recompute the enumerated side and the literal claimed side
                # independently of the optimized cycle-cover search.
                verified = plain_enumerate(n, a, b, c)
                second = compare(n, a, b, c, verified)
                if second is None or verified != actual:
                    print("SANITY FAILED")
                    return
                relation, brute_side, claim_side = second
                print("COUNTEREXAMPLE:",
                      {"n": n, "a": a, "b": b, "c": c,
                       "relation": relation,
                       "brute_force_side": brute_side,
                       "claimed_side": claim_side})
                return
            tested.append((n, a, b, c))
        completed_n = n
    print("NO COUNTEREXAMPLE",
          "exact ranges: 1 <= n <= 20; (n-1)/2 < a < b < c <= n-1;",
          "cases tested =", len(tested))

if __name__ == "__main__":
    main()