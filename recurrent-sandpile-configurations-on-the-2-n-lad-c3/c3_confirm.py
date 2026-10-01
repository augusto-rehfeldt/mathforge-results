from itertools import product


def check_witness():
    # The reported witness is n=2, not an individual configuration.
    n = 2
    if type(n) is not int or n < 2:
        return False, "the reported n is not an integer at least 2"

    vertices = [(row, i) for i in range(1, n + 1)
                for row in ("u", "v")]
    neighbors = {vertex: [] for vertex in vertices}

    def add_edge(a, b):
        neighbors[a].append(b)
        neighbors[b].append(a)

    for i in range(1, n + 1):
        add_edge(("u", i), ("v", i))
    for i in range(1, n):
        add_edge(("u", i), ("u", i + 1))
        add_edge(("v", i), ("v", i + 1))

    # Each of these edges goes to the same sink.
    sink_edges = {v: 3 - len(neighbors[v]) for v in vertices}
    for v in vertices:
        if sink_edges[v] < 0 or len(neighbors[v]) + sink_edges[v] != 3:
            return False, "constructed graph does not have degree three"

    def recurrent(heights):
        # Sink is already burned; only nonsink vertices remain here.
        unburned = set(vertices)
        while unburned:
            burnable = [
                v for v in unburned
                if heights[v] >= sum(w in unburned for w in neighbors[v])
            ]
            if not burnable:
                return False
            unburned.difference_update(burnable)
        return True

    def avalanche_area(heights):
        chips = heights.copy()
        chips[("u", 1)] += 1
        toppled = set()
        while True:
            unstable = next((v for v in vertices if chips[v] >= 3), None)
            if unstable is None:
                return len(toppled)
            chips[unstable] -= 3
            toppled.add(unstable)
            for w in neighbors[unstable]:
                chips[w] += 1
            # The remaining sink_edges[unstable] chips are discarded.

    lhs = {}
    eligible_count = 0
    for values in product((0, 1, 2), repeat=len(vertices)):
        heights = dict(zip(vertices, values))
        if sum(values) != 4 * n - 2:
            continue
        eligible_count += 1
        if not recurrent(heights):
            continue
        area = avalanche_area(heights)
        lhs[area] = lhs.get(area, 0) + 1

    # Compute the stated polynomial literally, adding overlapping terms.
    rhs = {}

    def add_term(exponent, coefficient):
        rhs[exponent] = rhs.get(exponent, 0) + coefficient

    add_term(0, 2 * n)
    add_term(1, 1)
    for j in range(1, n):
        add_term(2 * j, 1)
    add_term(2 * n - 1, 3)
    add_term(2 * n, 2 * n * n - 2 * n - 3)

    lhs = dict(sorted((k, v) for k, v in lhs.items() if v != 0))
    rhs = dict(sorted((k, v) for k, v in rhs.items() if v != 0))

    if lhs == rhs:
        return False, f"n={n} satisfies the hypotheses, but both sides equal {lhs}"

    return True, (
        f"n={n}; LHS coefficients={lhs}; RHS coefficients={rhs}; "
        f"stable configurations with |eta|={4 * n - 2} tested={eligible_count}"
    )


def main():
    try:
        confirmed, detail = check_witness()
    except Exception as exc:
        confirmed = False
        detail = f"verification failed: {type(exc).__name__}: {exc}"
    prefix = "REFUTATION CONFIRMED:" if confirmed else "REFUTATION REJECTED:"
    print(prefix, detail)


if __name__ == "__main__":
    main()