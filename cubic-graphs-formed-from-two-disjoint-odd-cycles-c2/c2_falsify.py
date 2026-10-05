#!/usr/bin/env python3
import itertools
import time
import sys
from collections import deque

COLORS = 63
SETS = [x for x in range(64) if x.bit_count() == 2]
INDEX = {x: i for i, x in enumerate(SETS)}
ALL = (1 << 15) - 1
TRIPLES = [
    (INDEX[a], INDEX[b], INDEX[COLORS ^ a ^ b])
    for a in SETS for b in SETS if not (a & b)
]
START = time.monotonic()
DEADLINE = START + 210


class Timeout(Exception):
    pass


def clock():
    if time.monotonic() >= DEADLINE:
        raise Timeout


def graph(p):
    m = len(p)
    edges = []
    inc = [[] for _ in range(2 * m)]

    def add(a, b=None):
        e = len(edges)
        edges.append((a, b))
        inc[a].append(e)
        if b is not None:
            inc[b].append(e)
        return e

    for i in range(m - 1):
        add(i, i + 1)
        add(m + i, m + i + 1)
    for i, j in enumerate(p):
        add(i, m + j - 1)
    dangling = [add(x) for x in (0, m, m - 1, 2 * m - 1)]
    return edges, inc, dangling


def fast(p, q, timed=True):
    edges, inc, dangling = graph(p)
    domains = [ALL] * len(edges)
    for e, x in zip(dangling, q):
        domains[e] = 1 << INDEX[x]

    def search(ds):
        if timed:
            clock()
        queue = deque(range(len(inc)))
        queued = set(queue)
        while queue:
            v = queue.popleft()
            queued.remove(v)
            es = inc[v]
            supports = [0, 0, 0]
            for t in TRIPLES:
                if all(ds[es[k]] & (1 << t[k]) for k in range(3)):
                    for k in range(3):
                        supports[k] |= 1 << t[k]
            if not supports[0]:
                return False
            for k, e in enumerate(es):
                new = ds[e] & supports[k]
                if not new:
                    return False
                if new != ds[e]:
                    ds[e] = new
                    for w in edges[e]:
                        if w is not None and w not in queued:
                            queue.append(w)
                            queued.add(w)
        candidates = [e for e, d in enumerate(ds) if d & (d - 1)]
        if not candidates:
            return True
        e = min(candidates, key=lambda x: ds[x].bit_count())
        d = ds[e]
        while d:
            bit = d & -d
            d -= bit
            child = ds[:]
            child[e] = bit
            if search(child):
                return True
        return False

    return search(domains)


def plain(p, q):
    """Independent exhaustive vertex-by-vertex assignment, using color masks."""
    edges, inc, dangling = graph(p)
    values = [0] * len(edges)
    for e, x in zip(dangling, q):
        values[e] = x

    def options(v):
        es = inc[v]
        used = 0
        missing = []
        for e in es:
            x = values[e]
            if x:
                if used & x:
                    return []
                used |= x
            else:
                missing.append(e)
        if not missing:
            return [()] if used == COLORS else []
        available = COLORS ^ used
        out = []

        def generate(k, rem, chosen):
            if k == len(missing):
                if rem == 0:
                    out.append(tuple(zip(missing, chosen)))
                return
            for x in SETS:
                if x & rem == x:
                    generate(k + 1, rem ^ x, chosen + [x])

        generate(0, available, [])
        return out

    def search():
        best = None
        for v, es in enumerate(inc):
            opts = options(v)
            if not opts:
                return False
            if any(values[e] == 0 for e in es):
                if best is None or len(opts) < len(best):
                    best = opts
        if best is None:
            return True
        for assignment in best:
            for e, x in assignment:
                values[e] = x
            if search():
                return True
            for e, x in assignment:
                values[e] = 0
        return False

    return search()


def compatible(q):
    return all(sum(bool(x & (1 << c)) for x in q) % 2 == 0
               for c in range(6))


def canonical(q):
    # A color's four-position incidence signature determines its orbit.
    signatures = sorted(
        sum(((x >> c) & 1) << k for k, x in enumerate(q))
        for c in range(6)
    )
    return tuple(sum(1 << c for c, s in enumerate(signatures) if s & (1 << k))
                 for k in range(4))


raw = [q for q in itertools.product(SETS, repeat=4) if compatible(q)]
QUADS = sorted({canonical(q) for q in raw})


def sanity_fail(message):
    print("SANITY FAILED", message)
    sys.exit(0)


# Independent parity enumeration: choose three sets; XOR determines the fourth.
raw2 = set()
for a, b, c in itertools.product(SETS, repeat=3):
    d = a ^ b ^ c
    if d.bit_count() == 2:
        raw2.add((a, b, c, d))
if set(raw) != raw2:
    sanity_fail("parity enumeration disagreement")
print("Sanity 1: direct color counts agree with XOR enumeration;",
      len(raw), "compatible quadruples;", len(QUADS), "color orbits.")

# Cross-check orbit reduction against literal simultaneous color permutations.
for q in QUADS:
    for perm in itertools.permutations(range(6)):
        transformed = tuple(
            sum(1 << perm[c] for c in range(6) if x & (1 << c)) for x in q
        )
        if canonical(transformed) != q:
            sanity_fail("color-orbit canonicalization")
print("Sanity 2: canonicalization invariant under all 720 color permutations.")

for p in itertools.permutations((1, 2)):
    for q in QUADS:
        if fast(p, q, timed=False) != plain(p, q):
            sanity_fail("independent solvers disagree at m=2")
print("Sanity 3: domain solver agrees with plain exhaustive solver for all m=2 orbits.")


def literal_left(p):
    return any((i % 2) != (j % 2) for i, j in enumerate(p, 1))


def display(q):
    return tuple(tuple(c + 1 for c in range(6) if x & (1 << c)) for x in q)


tested = 0
completed = []
current = None
last_completed = None
blocks_this_m = 0


def report_candidate(p, bad):
    # Recompute the literal first side and the universal second side independently.
    left = literal_left(p)
    if bad is not None:
        if plain(p, bad):
            sanity_fail("candidate rejection failed plain recomputation")
        right = False
    else:
        right = all(plain(p, q) for q in QUADS)
    if left == right:
        sanity_fail("candidate equivalence did not survive recomputation")
    witness = {
        "m": len(p), "pi": p,
        "(i)": left, "(ii)": right,
        "unrealizable_quadruple": None if bad is None else display(bad),
    }
    print("COUNTEREXAMPLE:", witness)
    sys.exit(0)


try:
    for m in (2, 4, 6, 8):
        blocks_this_m = 0
        last_completed = None
        for p in itertools.permutations(range(1, m + 1)):
            current = (m, p, 0)
            left = literal_left(p)
            bad = None
            for k, q in enumerate(QUADS):
                clock()
                result = fast(p, q)
                tested += 1
                current = (m, p, k + 1)
                if not result:
                    bad = q
                    break
            right = bad is None
            if left != right:
                report_candidate(p, bad)
            blocks_this_m += 1
            last_completed = p
            current = None
        completed.append((m, blocks_this_m))
except Timeout:
    pass

print("NO COUNTEREXAMPLE",
      {
          "m_values": (2, 4, 6, 8),
          "permutation_order": "lexicographic",
          "fully_completed_m": completed,
          "additional_complete_permutation_prefix": {
              "m": current[0] if current else None,
              "count": blocks_this_m if current else 0,
              "last": last_completed if current else None,
          },
          "partial_block": current,
          "quadruple_order": "sorted canonical mask tuples",
          "quadruple_representatives": QUADS,
          "cases_tested": tested,
          "note": "Universal conditions stop at their first failed quadruple; "
                  "color-orbit representatives cover all compatible quadruples.",
      })
sys.exit(0)