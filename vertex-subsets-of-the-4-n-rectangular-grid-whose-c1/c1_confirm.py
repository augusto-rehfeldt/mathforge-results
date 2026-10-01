def strictly_inside(point, polygon):
    """Boundary exclusion followed by the even-odd ray test."""
    x, y = point
    inside = False
    for i, (ax, ay) in enumerate(polygon):
        bx, by = polygon[(i + 1) % len(polygon)]

        cross = (x - ax) * (by - ay) - (y - ay) * (bx - ax)
        if (cross == 0 and min(ax, bx) <= x <= max(ax, bx)
                and min(ay, by) <= y <= max(ay, by)):
            return False

        if (ay > y) != (by > y):
            # Every nonhorizontal edge here is vertical, so its
            # intersection with the horizontal ray has x-coordinate ax.
            if ax > x:
                inside = not inside
    return inside


def check():
    n = 4
    witness = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 3), (2, 4),
        (3, 1), (3, 2), (3, 4),
        (4, 2), (4, 3), (4, 4),
    ]

    def reject(reason):
        print("REFUTATION REJECTED:", reason)

    if type(n) is not int or n < 1:
        reject("n is not an integer at least 1")
        return

    vertices = {(x, y) for x in range(1, 5) for y in range(1, n + 1)}
    for p in witness:
        if (not isinstance(p, tuple) or len(p) != 2
                or any(type(t) is not int for t in p)):
            reject("a reported vertex is not an integer coordinate pair")
            return
        if p not in vertices:
            reject("a reported vertex lies outside G_n")
            return

    A = set(witness)
    if len(A) != len(witness):
        reject("the reported witness contains duplicate vertices")
        return

    # Build G_n from the stated Euclidean-distance definition.
    graph = {p: set() for p in vertices}
    for p in vertices:
        for r in vertices:
            if (p[0] - r[0]) ** 2 + (p[1] - r[1]) ** 2 == 1:
                graph[p].add(r)

    induced = {p: graph[p] & A for p in A}
    for p in sorted(A):
        if len(induced[p]) != 2:
            reject("induced degree at {} is {}, not 2".format(
                p, len(induced[p])))
            return

    # Find connected components by brute-force traversal.
    components = []
    unseen = set(A)
    while unseen:
        start = min(unseen)
        component = set()
        pending = [start]
        while pending:
            p = pending.pop()
            if p not in component:
                component.add(p)
                pending.extend(induced[p] - component)
        unseen -= component
        components.append(component)

    # Recover each cycle in edge order, checking the entire component.
    polygons = []
    for component in components:
        start = min(component)
        polygon = []
        visited = set()
        previous = None
        current = start
        while True:
            if current in visited:
                reject("cycle traversal repeats a vertex before closing")
                return
            visited.add(current)
            polygon.append(current)
            choices = sorted(induced[current] - (
                {previous} if previous is not None else set()))
            if not choices:
                reject("cycle traversal cannot continue")
                return
            following = choices[0]
            if following == start:
                break
            previous, current = current, following

        if visited != component or len(polygon) < 4:
            reject("a component is not a simple polygonal cycle")
            return

        # Unit axis-aligned grid edges cannot intersect except at shared
        # endpoints. Distinct cycle vertices therefore ensure simplicity.
        polygons.append(polygon)

    outside = vertices - A
    interiors = [
        {p for p in outside if strictly_inside(p, polygon)}
        for polygon in polygons
    ]

    v = len(A)
    c = len(components)
    h = sum(any(p in interior for interior in interiors) for p in outside)

    s = 0
    for x in range(1, 4):
        for y in range(1, n):
            corners = {(x, y), (x + 1, y),
                       (x, y + 1), (x + 1, y + 1)}
            if corners <= outside and any(
                    corners <= interior for interior in interiors):
                s += 1

    q = sum(len(component) == 4 for component in components)
    left = v
    right = 2 * h + 6 * c - 2 * s - 2 * q

    if left != right:
        print("REFUTATION CONFIRMED:",
              "n =", n, "A =", witness,
              "v(A) =", left,
              "2h(A)+6c(A)-2s(A)-2q(A) =", right,
              "(v,h,c,s,q) =", (v, h, c, s, q))
    else:
        reject("the witness satisfies the identity: both sides equal {}".format(left))


if __name__ == "__main__":
    try:
        check()
    except Exception as error:
        print("REFUTATION REJECTED:",
              "verification failed: {}: {}".format(type(error).__name__, error))