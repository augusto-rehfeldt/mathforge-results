#!/usr/bin/env python3
import itertools
import math
import sys
import time
from collections import Counter, deque

DEADLINE = time.monotonic() + 225.0


def graph(n):
    vertices = [(r, c) for r in range(1, 4) for c in range(1, n + 1)]
    index = {v: i for i, v in enumerate(vertices)}
    edges = []
    for r, c in vertices:
        for w in ((r + 1, c), (r, c + 1)):
            if w in index:
                edges.append((index[r, c], index[w]))
    return vertices, edges


def plain_check(n, selected):
    """Independent connectivity, acyclicity, and full BFS verification."""
    vertices, edges = graph(n)
    N = len(vertices)
    selected = set(selected)
    if len(selected) != N - 1:
        return None
    adj = [[] for _ in vertices]
    for i in selected:
        if not 0 <= i < len(edges):
            return None
        a, b = edges[i]
        adj[a].append(b)
        adj[b].append(a)

    seen = {0}
    q = deque([0])
    while q:
        a = q.popleft()
        for b in adj[a]:
            if b not in seen:
                seen.add(b)
                q.append(b)
    # A connected simple graph on N vertices with N-1 edges is a tree.
    if len(seen) != N:
        return None

    distances = []
    for i, (a, b) in enumerate(edges):
        if i in selected:
            continue
        d = [-1] * N
        d[a] = 0
        q = deque([a])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if d[y] == -1:
                    d[y] = d[x] + 1
                    q.append(y)
        distances.append(d[b])
    if any(d not in (3, 5) for d in distances):
        return None
    L = sum(len(a) == 1 for a in adj)
    S = sum(d == 5 for d in distances)
    return L, S


class Timeout(Exception):
    pass


def enumerate_trees(n, callback, timed=False):
    """Combination enumeration with rollback-DSU pruning of cyclic prefixes.

    Each pruned prefix accounts for every candidate subset extending it.
    Enumeration order is the ordinary lexicographic combination order.
    """
    vertices, edges = graph(n)
    N, m = len(vertices), len(edges)
    parent = list(range(N))
    size = [1] * N
    chosen = []
    accounted = 0
    trees = 0
    calls = 0

    def root(a):
        while parent[a] != a:
            a = parent[a]
        return a

    def visit(start, need):
        nonlocal accounted, trees, calls
        calls += 1
        if timed and calls % 4096 == 0 and time.monotonic() >= DEADLINE:
            raise Timeout
        if need == 0:
            # N-1 acyclic edges necessarily form a spanning tree.
            accounted += 1
            trees += 1
            callback(tuple(chosen), edges, N)
            return
        for i in range(start, m - need + 1):
            a, b = edges[i]
            a, b = root(a), root(b)
            if a == b:
                accounted += math.comb(m - i - 1, need - 1)
                continue
            if size[a] < size[b]:
                a, b = b, a
            old_size = size[a]
            parent[b] = a
            size[a] += size[b]
            chosen.append(i)
            visit(i + 1, need - 1)
            chosen.pop()
            parent[b] = b
            size[a] = old_size

    complete = True
    try:
        visit(0, N - 1)
    except Timeout:
        complete = False
    return complete, accounted, trees


def fast_check(selected, edges, N):
    adj = [[] for _ in range(N)]
    mask = 0
    for i in selected:
        mask |= 1 << i
        a, b = edges[i]
        adj[a].append(b)
        adj[b].append(a)
    S = 0
    for i, (a, b) in enumerate(edges):
        if mask & (1 << i):
            continue
        # Tree paths are unique; search only through depth five.
        stack = [(a, -1, 0)]
        distance = -1
        while stack:
            x, previous, d = stack.pop()
            if x == b:
                distance = d
                break
            if d < 5:
                for y in adj[x]:
                    if y != previous:
                        stack.append((y, x, d + 1))
        if distance not in (3, 5):
            return None
        S += distance == 5
    return sum(len(a) == 1 for a in adj), S


def sanity_failed(message):
    print("SANITY FAILED", message)
    sys.exit(0)


# Sanity check 1: independently known tree counts for a path and a ladder.
known_counts = {1: 1, 2: 15}
for n, expected in known_counts.items():
    complete, accounted, trees = enumerate_trees(n, lambda *args: None)
    _, edges = graph(n)
    if not complete or trees != expected or accounted != math.comb(len(edges), 3*n - 1):
        sanity_failed(("known tree count", n, trees, expected))
print("SANITY 1 PASSED: tree counts G_1=1, G_2=15")


# Sanity check 2: unpruned subsets, independent BFS, and exact witness sets.
for n in range(1, 4):
    vertices, edges = graph(n)
    brute = {}
    for selected in itertools.combinations(range(len(edges)), 3*n - 1):
        result = plain_check(n, selected)
        if result is not None:
            brute[selected] = result
    clever = {}

    def collect(selected, es, N):
        result = fast_check(selected, es, N)
        if result is not None:
            clever[selected] = result

    complete, accounted, trees = enumerate_trees(n, collect)
    if (not complete or clever != brute
            or accounted != math.comb(len(edges), 3*n - 1)):
        sanity_failed(("independent subset/BFS cross-check", n))
print("SANITY 2 PASSED: exact retained trees and (L,S) agree for n=1..3")


total_candidates = 0
total_trees = 0
total_retained = 0
completed_n = 0

for n in range(1, 7):
    retained_here = [0]

    def inspect(selected, edges, N):
        result = fast_check(selected, edges, N)
        if result is None:
            return
        retained_here[0] += 1
        L, S = result
        if L + S < n + 1:
            # Recompute the hypotheses and both literal sides independently.
            checked = plain_check(n, selected)
            if checked is None or checked != result:
                sanity_failed(("witness recheck", n, selected))
            L2, S2 = checked
            left, right = L2 + S2, n + 1
            if left >= right:
                sanity_failed(("witness inequality recheck", n, selected))
            vertices, es = graph(n)
            witness = [(vertices[es[i][0]], vertices[es[i][1]])
                       for i in selected]
            print("COUNTEREXAMPLE:",
                  {"n": n, "tree_edges": witness, "L": L2, "S": S2,
                   "L(T)+S(T)": left, "n+1": right})
            sys.exit(0)

    complete, accounted, trees = enumerate_trees(n, inspect, timed=True)
    total_candidates += accounted
    total_trees += trees
    total_retained += retained_here[0]
    if not complete:
        print("NO COUNTEREXAMPLE",
              f"exact ranges: all subsets for 1<=n<={completed_n}; "
              f"first {accounted} lexicographic candidate subsets at n={n}; "
              f"cases tested/accounted={total_candidates}; "
              f"trees tested={total_trees}; retained={total_retained}")
        sys.exit(0)
    _, edges = graph(n)
    if accounted != math.comb(len(edges), 3*n - 1):
        sanity_failed(("exhaustive accounting", n, accounted))
    completed_n = n

print("NO COUNTEREXAMPLE",
      f"exact ranges: 1<=n<=6, all subsets of size 3n-1; "
      f"cases tested/accounted={total_candidates}; "
      f"trees tested={total_trees}; retained={total_retained}")