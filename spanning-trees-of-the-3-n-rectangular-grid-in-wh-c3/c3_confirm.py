from collections import deque

witness = {
    "n": 2,
    "tree_edges": [
        ((1, 1), (2, 1)),
        ((1, 1), (1, 2)),
        ((2, 1), (2, 2)),
        ((2, 2), (3, 2)),
        ((3, 1), (3, 2)),
    ],
}

def check(w):
    n = w["n"]
    if type(n) is not int or n < 1:
        return False, "n is not an integer at least 1"

    vertices = {(r, c) for r in (1, 2, 3) for c in range(1, n + 1)}
    graph_edges = set()
    for u in vertices:
        for v in vertices:
            if u < v and abs(u[0] - v[0]) + abs(u[1] - v[1]) == 1:
                graph_edges.add((u, v))

    tree_edges = set()
    adjacency = {v: set() for v in vertices}
    for u, v in w["tree_edges"]:
        if u not in vertices or v not in vertices:
            return False, "a tree edge has an endpoint outside G_n"
        edge = tuple(sorted((u, v)))
        if edge not in graph_edges:
            return False, "a reported tree edge is not an edge of G_n"
        if edge in tree_edges:
            return False, "the reported tree contains a duplicate edge"
        tree_edges.add(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)

    # Check connectivity and acyclicity directly, including every vertex.
    visited = set()
    def traverse(u, parent):
        visited.add(u)
        for v in adjacency[u]:
            if v == parent:
                continue
            if v in visited:
                return False
            if not traverse(v, u):
                return False
        return True

    if not traverse(min(vertices), None):
        return False, "the reported subgraph contains a cycle"
    if visited != vertices:
        return False, "the reported subgraph is not connected and spanning"

    L = sum(len(adjacency[v]) == 1 for v in vertices)
    S = 0
    for u, v in sorted(graph_edges - tree_edges):
        # Enumerate all simple tree paths between the edge's endpoints.
        paths = []
        queue = deque([(u, (u,))])
        while queue:
            current, path = queue.popleft()
            if current == v:
                paths.append(path)
                continue
            for neighbor in adjacency[current]:
                if neighbor not in path:
                    queue.append((neighbor, path + (neighbor,)))
        if len(paths) != 1:
            return False, "a missing edge does not have a unique tree path"
        # A path with k vertices has k-1 edges; adding the edge gives k.
        cycle_length = len(paths[0])
        if cycle_length not in (4, 6):
            return False, (
                f"adding missing edge {(u, v)} creates a cycle "
                f"of length {cycle_length}, not four or six"
            )
        if cycle_length == 6:
            S += 1

    left = L + S
    right = n + 1
    if left >= right:
        return False, f"the conclusion holds: L={L}, S={S}, {left} >= {right}"
    return True, f"{w!r}; L={L}, S={S}; L(T)+S(T)={left}; n+1={right}"

def main():
    try:
        confirmed, detail = check(witness)
    except Exception as exc:
        confirmed, detail = False, f"witness validation failed: {exc}"
    prefix = "REFUTATION CONFIRMED:" if confirmed else "REFUTATION REJECTED:"
    print(prefix, detail)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())