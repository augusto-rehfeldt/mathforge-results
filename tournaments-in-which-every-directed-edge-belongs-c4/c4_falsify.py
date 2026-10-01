#!/usr/bin/env python3
import itertools
import time

# Exhaustive isomorph-free augmentation, retaining also non-strong parents:
# the edge-triangle bound is hereditary, whereas strong connectivity is not.
LIMIT_SECONDS = 220
START = time.monotonic()
DEADLINE = START + LIMIT_SECONDS


class TimeUp(Exception):
    pass


def tick():
    if time.monotonic() >= DEADLINE:
        raise TimeUp


def triangles(A):
    n = len(A)
    counts = [[0] * n for _ in range(n)]
    ts = []
    for x, y, z in itertools.combinations(range(n), 3):
        if ((A[x][y] and A[y][z] and A[z][x]) or
                (A[y][x] and A[z][y] and A[x][z])):
            ts.append((x, y, z))
            for u, v in ((x, y), (x, z), (y, z)):
                counts[u][v] += 1
                counts[v][u] += 1
    return ts, counts


def strong(A, omitted=None):
    vertices = [i for i in range(len(A)) if i != omitted]
    if not vertices:
        return False
    root = vertices[0]
    for reverse in (False, True):
        reached = {root}
        stack = [root]
        while stack:
            u = stack.pop()
            for v in vertices:
                if v not in reached and (A[v][u] if reverse else A[u][v]):
                    reached.add(v)
                    stack.append(v)
        if len(reached) != len(vertices):
            return False
    return True


def canonical(A):
    """Canonical adjacency string via invariant refinement and all cell orders."""
    n = len(A)
    cells = [list(range(n))]
    while True:
        new = []
        for cell in cells:
            groups = {}
            for v in cell:
                signature = tuple(sum(A[v][w] for w in c) for c in cells)
                groups.setdefault(signature, []).append(v)
            for signature in sorted(groups):
                new.append(groups[signature])
        if len(new) == len(cells):
            break
        cells = new
    best = None
    orders = [tuple(itertools.permutations(c)) for c in cells]
    for k, parts in enumerate(itertools.product(*orders)):
        if k % 1024 == 0:
            tick()
        p = tuple(v for part in parts for v in part)
        key = bytes(A[p[i]][p[j]] for i in range(n) for j in range(i + 1, n))
        if best is None or key < best:
            best = key
    return best


def from_key(key, n):
    A = [[0] * n for _ in range(n)]
    for bit, (i, j) in zip(key, itertools.combinations(range(n), 2)):
        A[i][j] = bit
        A[j][i] = 1 - bit
    return A


def fast_values(A):
    ts, counts = triangles(A)
    n = len(A)
    result = []
    for v in range(n):
        a = sum(v in t for t in ts)
        # A surviving exhausted edge releases exactly one unit iff its
        # triangle through v existed.
        b = 0
        for x, y in itertools.combinations(
                [u for u in range(n) if u != v], 2):
            if counts[x][y] == 2:
                cycle = ((A[x][y] and A[y][v] and A[v][x]) or
                         (A[y][x] and A[v][y] and A[x][v]))
                b += bool(cycle)
        result.append((strong(A, v), a, b))
    return result


def plain_verification(A):
    """Independent cycle test, Floyd-Warshall, and literal deletion counts."""
    n = len(A)

    def census(vertices):
        ts = []
        c = {}
        for x, y in itertools.combinations(vertices, 2):
            edge = (x, y) if A[x][y] else (y, x)
            c[edge] = 0
        for triple in itertools.combinations(vertices, 3):
            if all(sum(A[u][w] for w in triple if w != u) == 1
                   for u in triple):
                ts.append(triple)
                for x, y in itertools.combinations(triple, 2):
                    edge = (x, y) if A[x][y] else (y, x)
                    c[edge] += 1
        return ts, c

    def connected(vertices):
        if not vertices:
            return False
        reach = {(u, v): u == v or bool(A[u][v])
                 for u in vertices for v in vertices}
        for k in vertices:
            for u in vertices:
                for v in vertices:
                    reach[u, v] |= reach[u, k] and reach[k, v]
        return all(reach.values())

    vertices = list(range(n))
    ts, c = census(vertices)
    hypotheses = n >= 4 and connected(vertices) and all(x <= 2 for x in c.values())
    values = []
    for v in vertices:
        remaining = [u for u in vertices if u != v]
        _, deleted_counts = census(remaining)
        a = sum(v in t for t in ts)
        b = sum(c[e] == 2 and deleted_counts[e] == 1
                for e in deleted_counts)
        values.append((connected(remaining), a, b))
    return hypotheses, values


def sanity():
    # Known counts of unlabeled tournaments, including disconnected ones.
    expected = {1: 1, 2: 1, 3: 2, 4: 4}
    observed = {}
    for n in expected:
        keys = set()
        for bits in itertools.product((0, 1), repeat=n * (n - 1) // 2):
            keys.add(canonical(from_key(bits, n)))
        observed[n] = len(keys)
    print("Sanity 1: unlabeled counts", observed, flush=True)
    if observed != expected:
        return False

    # Independently check all 1,024 labeled tournaments of order five.
    checked = 0
    for bits in itertools.product((0, 1), repeat=10):
        A = from_key(bits, 5)
        ts, c = triangles(A)
        hypothesis, literal = plain_verification(A)
        expected_hypothesis = strong(A) and all(
            c[x][y] <= 2 for x, y in itertools.combinations(range(5), 2))
        if hypothesis != expected_hypothesis or fast_values(A) != literal:
            print("Sanity 2: mismatch", bits, flush=True)
            return False
        checked += 1
    print("Sanity 2: independent literal/Floyd cross-check:",
          checked, "labeled tournaments passed", flush=True)
    return True


def main():
    if not sanity():
        print("SANITY FAILED")
        return

    parents = [b""]
    completed = {}
    retained_counts = {}
    tested_counts = {}
    interrupted = None

    try:
        for n in range(2, 10):
            children = {}
            tested = 0
            for parent_key in parents:
                tick()
                A = from_key(parent_key, n - 1)
                _, old_counts = triangles(A)
                for mask in range(1 << (n - 1)):
                    tick()
                    B = [row + [0] for row in A] + [[0] * n]
                    for u in range(n - 1):
                        B[u][n - 1] = (mask >> u) & 1
                        B[n - 1][u] = 1 - B[u][n - 1]

                    # Exact incremental capacity test: only new triples matter.
                    new_counts = [0] * (n - 1)
                    valid = True
                    for x, y in itertools.combinations(range(n - 1), 2):
                        z = n - 1
                        if ((B[x][y] and B[y][z] and B[z][x]) or
                                (B[y][x] and B[z][y] and B[x][z])):
                            if old_counts[x][y] == 2:
                                valid = False
                                break
                            new_counts[x] += 1
                            new_counts[y] += 1
                            if new_counts[x] > 2 or new_counts[y] > 2:
                                valid = False
                                break
                    if not valid:
                        continue
                    key = canonical(B)
                    if key in children:
                        continue
                    children[key] = None
                    if n < 4 or not strong(B):
                        continue
                    tested += 1
                    values = fast_values(B)
                    if not any(s and a + b <= 8 for s, a, b in values):
                        hypotheses, literal = plain_verification(B)
                        if hypotheses and not any(
                                s and a + b <= 8 for s, a, b in literal):
                            edges = [(u, v) for u in range(n)
                                     for v in range(n) if B[u][v]]
                            print("COUNTEREXAMPLE:", {
                                "n": n, "directed_edges": edges,
                                "per_vertex_(T-v_strong,a,b)": literal,
                                "left_side": "exists v: T-v strong and a+b<=8",
                                "computed_left_side": False,
                                "claimed_right_side": True,
                            })
                            return
            parents = list(children)
            completed[n] = len(parents)
            if n >= 4:
                retained_counts[n] = len(parents)
                tested_counts[n] = tested
    except TimeUp:
        interrupted = n

    # An interrupted order is deliberately excluded from all reported totals.
    checked_orders = sorted(tested_counts)
    print("NO COUNTEREXAMPLE",
          "exact complete orders =", checked_orders,
          "; strongly connected hypothesis cases tested =", tested_counts,
          "; total =", sum(tested_counts.values()),
          "; all capacity-valid isomorphism classes =", retained_counts,
          "; incomplete order (excluded) =", interrupted)


if __name__ == "__main__":
    main()