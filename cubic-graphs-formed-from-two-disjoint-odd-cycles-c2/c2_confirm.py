#!/usr/bin/env python3
import itertools

WITNESS = {
    "m": 2,
    "pi": (2, 1),
    "unrealizable_quadruple": ((3, 4), (3, 4), (5, 6), (5, 6)),
}
COLORS = frozenset(range(1, 7))
PAIRS = tuple(frozenset(p) for p in itertools.combinations(sorted(COLORS), 2))


def reject(reason):
    print("REFUTATION REJECTED:", reason)


def compatible(quadruple):
    return all(sum(color in pair for pair in quadruple) % 2 == 0
               for color in COLORS)


def build_graph(m, pi):
    vertices = [(row, i) for row in ("u", "v") for i in range(1, m + 1)]
    edges = []
    for row in ("u", "v"):
        for i in range(1, m):
            edges.append(((row, i), (row, i + 1)))
    for i in range(1, m + 1):
        edges.append((("u", i), ("v", pi[i - 1])))

    # These singleton endpoint tuples represent dangling edges.
    dangling = [(("u", 1),), (("v", 1),),
                (("u", m),), (("v", m),)]
    all_edges = edges + dangling
    incident = {
        vertex: [index for index, edge in enumerate(all_edges) if vertex in edge]
        for vertex in vertices
    }
    return edges, dangling, incident


def realizable(quadruple, internal_edges, incident):
    # Plain exhaustive enumeration: every internal edge independently receives
    # one of all fifteen two-element subsets. Dangling sets are fixed.
    for internal_sets in itertools.product(PAIRS, repeat=len(internal_edges)):
        assignment = internal_sets + quadruple
        valid = True
        for indices in incident.values():
            sets = [assignment[index] for index in indices]
            if (len(sets) != 3
                    or set().union(*sets) != COLORS
                    or any(sets[i] & sets[j]
                           for i in range(3) for j in range(i + 1, 3))):
                valid = False
                break
        if valid:
            return True
    return False


def main():
    m = WITNESS["m"]
    pi = WITNESS["pi"]
    raw_quadruple = WITNESS["unrealizable_quadruple"]

    if type(m) is not int or m < 2 or m % 2:
        reject("m is not an even integer at least 2")
        return
    if (len(pi) != m or any(type(i) is not int for i in pi)
            or sorted(pi) != list(range(1, m + 1))):
        reject("pi is not a permutation of {1,...,m}")
        return
    if len(raw_quadruple) != 4:
        reject("the reported boundary prescription is not an ordered quadruple")
        return
    for pair in raw_quadruple:
        if (len(pair) != 2 or any(type(c) is not int for c in pair)
                or len(set(pair)) != 2 or not set(pair) <= COLORS):
            reject("a reported boundary set is not a two-element color subset")
            return

    quadruple = tuple(frozenset(pair) for pair in raw_quadruple)
    if not compatible(quadruple):
        reject("the reported quadruple is not parity-compatible")
        return

    internal, dangling, incident = build_graph(m, pi)
    if len(dangling) != 4 or any(len(indices) != 3
                                for indices in incident.values()):
        reject("the constructed graph does not have the specified incidences")
        return

    side_i = any(i % 2 != pi[i - 1] % 2 for i in range(1, m + 1))

    # Evaluate the universal statement literally, with ordinary short-circuiting.
    # Test the reported prescription first; no new witness is sought.
    def all_prescriptions():
        yield quadruple
        for q in itertools.product(PAIRS, repeat=4):
            if q != quadruple and compatible(q):
                yield q

    side_ii = True
    reported_realizable = None
    for q in all_prescriptions():
        exists = realizable(q, internal, incident)
        if q == quadruple:
            reported_realizable = exists
        if not exists:
            side_ii = False
            break

    if reported_realizable:
        reject("the reported unrealizable quadruple has a realization")
    elif side_i == side_ii:
        reject("the two sides of the claimed equivalence agree")
    else:
        print("REFUTATION CONFIRMED:", WITNESS,
              {"(i)": side_i, "(ii)": side_ii})


if __name__ == "__main__":
    main()