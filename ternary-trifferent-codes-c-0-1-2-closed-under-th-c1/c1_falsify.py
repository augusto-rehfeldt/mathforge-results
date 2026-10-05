import itertools
import time
import sys

# Exhaustive orbit-union feasibility searches, in increasing dimension.
# A deadline leaves only completed dimensions in the certified range.
START = time.monotonic()
DEADLINE = START + 225.0
counts = {"orbit_subsets_tested": 0, "constraint_tests": 0, "nodes": 0}
completed = []


class Timeout(Exception):
    pass


def tick():
    if time.monotonic() >= DEADLINE:
        raise Timeout


def words(m):
    return list(itertools.product(tuple(itertools.product(range(3), range(2))),
                                  repeat=m))


def shift(w, t):
    return tuple(((a + t) % 3, b) for a, b in w)


def compatible(x, y, z):
    # Literal conditions from the claim.
    for (a, b), (c, d), (e, f) in zip(x, y, z):
        if b == d == f:
            if len({a, c, e}) == 3:
                return True
        elif b == d:
            if a != c:
                return True
        elif b == f:
            if a != e:
                return True
        elif d == f:
            if c != e:
                return True
    return False


def expansion(w):
    return tuple(v for a, b in w
                 for v in (a, (a + b) % 3, (a + 2 * b) % 3))


def expanded_compatible(x, y, z):
    return any(len(set(t)) == 3
               for t in zip(expansion(x), expansion(y), expansion(z)))


def make_orbits(m):
    # Unique representative: first a-coordinate is zero.
    reps = [w for w in words(m) if w[0][0] == 0]
    return [tuple(shift(w, t) for t in range(3)) for w in reps]


def literal_valid(D):
    return all(compatible(*triple)
               for triple in itertools.combinations(D, 3))


def sanity():
    # Independent check 1: literal pair conditions versus block expansion.
    tested = 0
    for m in (1, 2):
        for t in itertools.combinations(words(m), 3):
            if compatible(*t) != expanded_compatible(*t):
                print("SANITY FAILED")
                sys.exit(0)
            tested += 1
    print("SANITY 1 PASS: literal/block equivalence on", tested, "triples")

    # Independent check 2: orbit partition, invariance, and known m=1 maximum.
    for m in (1, 2, 3):
        O = make_orbits(m)
        flat = [w for o in O for w in o]
        if (len(O) != 6 ** m // 3 or len(set(flat)) != 6 ** m
                or set(flat) != set(words(m))
                or any(set(shift(w, 1) for w in o) != set(o) for o in O)):
            print("SANITY FAILED")
            sys.exit(0)
    if not literal_valid(words(1)) or len(words(1)) != 3 * 2 ** 1:
        print("SANITY FAILED")
        sys.exit(0)
    print("SANITY 2 PASS: orbit partitions m=1..3; m=1 maximum is 6")


def constraints(O):
    n = len(O)
    bad_one = 0
    bad_pair = [0] * n
    bad_triple = {}

    for i, o in enumerate(O):
        if not literal_valid(o):
            bad_one |= 1 << i

    for i in range(n):
        tick()
        for j in range(i + 1, n):
            counts["constraint_tests"] += 1
            if not literal_valid(O[i] + O[j]):
                bad_pair[i] |= 1 << j
                bad_pair[j] |= 1 << i

    for i in range(n):
        tick()
        for j in range(i + 1, n):
            if bad_pair[i] & (1 << j):
                continue
            for k in range(j + 1, n):
                if (bad_pair[i] | bad_pair[j]) & (1 << k):
                    continue
                counts["constraint_tests"] += 1
                # Simultaneous shift normalizes the word from orbit i to phase 0.
                bad = any(not compatible(O[i][0], O[j][s], O[k][t])
                          for s in range(3) for t in range(3))
                if bad:
                    for a, b, c in ((i, j, k), (i, k, j), (j, k, i)):
                        bad_triple[a, b] = bad_triple.get((a, b), 0) | (1 << c)
    return bad_one, bad_pair, bad_triple


def solve(O, target, C):
    bad_one, bad_pair, bad_triple = C
    n = len(O)

    def dfs(chosen, candidates):
        counts["nodes"] += 1
        if counts["nodes"] % 1024 == 0:
            tick()
        if len(chosen) == target:
            counts["orbit_subsets_tested"] += 1
            return chosen
        need = target - len(chosen)
        while candidates.bit_count() >= need:
            bit = candidates & -candidates
            candidates ^= bit
            v = bit.bit_length() - 1
            remaining = candidates & ~bad_pair[v]
            for u in chosen:
                remaining &= ~bad_triple.get((min(u, v), max(u, v)), 0)
            result = dfs(chosen + [v], remaining)
            if result is not None:
                return result
        return None

    return dfs([], ((1 << n) - 1) & ~bad_one)


def plain_second_search(O, target):
    # Independent exhaustive combination enumeration with only literal
    # triple checks. Invalid prefixes cannot have valid extensions.
    def dfs(start, indices, D):
        counts["nodes"] += 1
        if counts["nodes"] % 128 == 0:
            tick()
        if len(indices) == target:
            counts["orbit_subsets_tested"] += 1
            return indices
        need = target - len(indices)
        for i in range(start, len(O) - need + 1):
            new = D + list(O[i])
            if literal_valid(new):
                ans = dfs(i + 1, indices + [i], new)
                if ans is not None:
                    return ans
        return None
    return dfs(0, [], [])


def crosscheck_constraints(O, C):
    one, pair, triple = C
    tested = 0
    for size in range(1, 4):
        for ids in itertools.combinations(range(len(O)), size):
            predicted = not any(one & (1 << i) for i in ids)
            predicted &= not any(pair[i] & (1 << j)
                                 for i, j in itertools.combinations(ids, 2))
            if size == 3:
                i, j, k = ids
                predicted &= not bool(triple.get((i, j), 0) & (1 << k))
            actual = literal_valid([w for i in ids for w in O[i]])
            if predicted != actual:
                print("SANITY FAILED")
                sys.exit(0)
            tested += 1
    print("SANITY 3 PASS: compressed constraints versus brute force on",
          tested, "orbit subsets")


def main():
    sanity()
    interrupted = None
    try:
        for m in range(1, 5):
            tick()
            interrupted = m
            O = make_orbits(m)
            target = 2 ** m
            C = constraints(O)
            if m <= 2:
                crosscheck_constraints(O, C)
            answer = solve(O, target, C)
            if answer is not None:
                D = [w for i in answer for w in O[i]]
                # Recheck the actual statement, not merely the encoding.
                if (len(set(D)) < 3 * 2 ** m
                        or set(map(lambda w: shift(w, 1), D)) != set(D)
                        or not literal_valid(D)):
                    print("SANITY FAILED")
                    return
                completed.append(m)
                print("m =", m, ": feasible; cardinality =", len(D))
                continue

            # UNSAT is only reported after an independent literal search.
            second = plain_second_search(O, target)
            if second is not None:
                print("SANITY FAILED")
                return
            # Both exhaustive searches establish that no admissible union
            # reaches the literal claimed threshold.
            print("COUNTEREXAMPLE:",
                  {"m": m,
                   "witness": "exhaustive UNSAT, independently rechecked",
                   "brute_force_side": "maximum cardinality < " + str(3 * 2 ** m),
                   "claimed_side": "exists cardinality >= " + str(3 * 2 ** m)})
            return
        interrupted = None
    except Timeout:
        pass

    print("NO COUNTEREXAMPLE",
          "exact completed ranges: m=" + repr(completed),
          "cases tested=" + repr(counts),
          "unfinished dimension=" + repr(interrupted),
          "(unfinished dimension is not certified)")


if __name__ == "__main__":
    main()