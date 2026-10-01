from itertools import combinations

WITNESS = {
    "n": 7,
    "directed_edges": [
        (0, 2), (0, 5), (0, 6), (1, 0), (1, 4), (1, 6),
        (2, 1), (2, 3), (2, 6), (3, 0), (3, 1), (3, 5),
        (4, 0), (4, 2), (4, 3), (5, 1), (5, 2), (5, 4),
        (6, 3), (6, 4), (6, 5),
    ],
}


def strongly_connected(vertices, edges):
    """Check directed reachability for every ordered pair."""
    vertices = set(vertices)
    for source in vertices:
        reached = {source}
        pending = [source]
        while pending:
            x = pending.pop()
            for y in vertices:
                if (x, y) in edges and y not in reached:
                    reached.add(y)
                    pending.append(y)
        if reached != vertices:
            return False
    return True


def directed_triangles(vertices, edges):
    """Enumerate three-element sets inducing a directed cycle."""
    result = []
    for x, y, z in combinations(sorted(vertices), 3):
        if (
            ((x, y) in edges and (y, z) in edges and (z, x) in edges)
            or
            ((y, x) in edges and (x, z) in edges and (z, y) in edges)
        ):
            result.append(frozenset((x, y, z)))
    return result


def triangle_counts(edges, triangles):
    return {
        edge: sum(
            edge[0] in triangle and edge[1] in triangle
            for triangle in triangles
        )
        for edge in edges
    }


def check():
    n = WITNESS["n"]
    listed_edges = WITNESS["directed_edges"]

    if type(n) is not int or n < 4:
        return False, "n is not an integer at least 4"

    vertices = set(range(n))
    for edge in listed_edges:
        if not isinstance(edge, tuple) or len(edge) != 2:
            return False, "malformed directed edge"
        x, y = edge
        if type(x) is not int or type(y) is not int:
            return False, "noninteger vertex label"
        if x not in vertices or y not in vertices or x == y:
            return False, "edge has an invalid endpoint or is a loop"

    edges = set(listed_edges)
    if len(edges) != len(listed_edges):
        return False, "duplicate directed edges"

    for x, y in combinations(sorted(vertices), 2):
        if int((x, y) in edges) + int((y, x) in edges) != 1:
            return False, "not exactly one directed edge for pair %r" % ((x, y),)

    if not strongly_connected(vertices, edges):
        return False, "T is not strongly connected"

    triangles = directed_triangles(vertices, edges)
    counts = triangle_counts(edges, triangles)
    over_capacity = {e: c for e, c in counts.items() if c > 2}
    if over_capacity:
        return False, "edges belong to more than two directed triangles: %r" % over_capacity

    per_vertex = []
    for v in sorted(vertices):
        remaining = vertices - {v}
        surviving_edges = {
            (x, y) for x, y in edges if x in remaining and y in remaining
        }
        remaining_triangles = directed_triangles(remaining, surviving_edges)
        remaining_counts = triangle_counts(surviving_edges, remaining_triangles)

        strong = strongly_connected(remaining, surviving_edges)
        a = sum(v in triangle for triangle in triangles)
        b = sum(
            counts[e] == 2 and remaining_counts[e] == 1
            for e in surviving_edges
        )
        per_vertex.append({
            "v": v, "T-v_strong": strong, "a_T(v)": a,
            "b_T(v)": b, "a_T(v)+b_T(v)": a + b,
        })

    conclusion = any(
        row["T-v_strong"] and row["a_T(v)+b_T(v)"] <= 8
        for row in per_vertex
    )
    if conclusion:
        return False, "the conclusion holds: %r" % per_vertex

    return True, {
        "hypotheses": True,
        "conclusion_exists_v": conclusion,
        "per_vertex": per_vertex,
    }


def main():
    try:
        confirmed, details = check()
        if confirmed:
            print("REFUTATION CONFIRMED:", WITNESS, details)
        else:
            print("REFUTATION REJECTED:", details)
    except Exception as exc:
        print("REFUTATION REJECTED:", "verification error: %s" % exc)


if __name__ == "__main__":
    main()