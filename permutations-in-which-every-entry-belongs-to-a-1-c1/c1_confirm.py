from itertools import combinations

# The reported witness; its reported occurrences and verdicts are not trusted.
witness = {
    "relation": "membership in T_n",
    "n": 5,
    "permutation": (1, 3, 2, 5, 4),
    "132_occurrences": [(0, 1, 2), (0, 3, 4),
                        (1, 3, 4), (2, 3, 4)],
}


def occurrences(pi):
    return [
        (i, j, k)
        for i, j, k in combinations(range(len(pi)), 3)
        if pi[i] < pi[k] < pi[j]
    ]


def incidence_graph(pi, triples):
    graph = {("position", i): set() for i in range(len(pi))}
    for r, triple in enumerate(triples):
        vertex = ("occurrence", r)
        graph[vertex] = set()
        for i in triple:
            position = ("position", i)
            graph[vertex].add(position)
            graph[position].add(vertex)
    return graph


def is_tree(graph):
    if not graph:
        return False

    visited = set()

    def visit(vertex, parent):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor == parent:
                continue
            if neighbor in visited or not visit(neighbor, vertex):
                return False
        return True

    return visit(next(iter(graph)), None) and len(visited) == len(graph)


def in_T(pi):
    triples = occurrences(pi)
    graph = incidence_graph(pi, triples)
    every_entry_covered = all(
        graph[("position", i)] for i in range(len(pi))
    )
    return every_entry_covered and is_tree(graph)


def inversions(pi):
    return sum(
        pi[i] > pi[j]
        for i, j in combinations(range(len(pi)), 2)
    )


def descents(pi):
    return sum(pi[i] > pi[i + 1] for i in range(len(pi) - 1))


def standardize(entries):
    ranks = {value: rank for rank, value in enumerate(sorted(entries), 1)}
    return tuple(ranks[value] for value in entries)


def exclusive_positions(pi, triple):
    triples = occurrences(pi)
    counts = [
        sum(i in occurrence for occurrence in triples)
        for i in range(len(pi))
    ]
    return tuple(i for i in triple if counts[i] == 1)


def delete_and_standardize(pi, positions):
    removed = set(positions)
    return standardize(
        tuple(value for i, value in enumerate(pi) if i not in removed)
    )


def polynomial(qualified_permutations):
    # Dictionary representation of a formal polynomial:
    # (exponent of q, exponent of t) -> integer coefficient.
    result = {}
    for pi in qualified_permutations:
        exponent = (inversions(pi), descents(pi))
        result[exponent] = result.get(exponent, 0) + 1
    return result


def claimed_membership(n, pi):
    # Literally: empty unless n = 2m+1 with integer m >= 1;
    # otherwise exactly (1,3,2,5,4,...,2m+1,2m).
    if n < 3 or n % 2 == 0:
        return False
    m = (n - 1) // 2
    displayed = (1,) + tuple(
        value for r in range(1, m + 1) for value in (2 * r + 1, 2 * r)
    )
    return pi == displayed


def main():
    n = witness["n"]
    pi = witness["permutation"]

    if type(n) is not int or n < 1:
        print("REFUTATION REJECTED: n is not an integer >= 1")
        return
    if (
        len(pi) != n
        or any(type(value) is not int for value in pi)
        or sorted(pi) != list(range(1, n + 1))
    ):
        print("REFUTATION REJECTED: witness is not a permutation of {1,...,n}")
        return

    # For the claimed set equality, the hypotheses are n >= 1 and
    # an ambient permutation. Membership in T_n is the conclusion being
    # compared, not an additional hypothesis imposed on the witness.
    actual = in_T(pi)
    claimed = claimed_membership(n, pi)

    if actual != claimed:
        checked_witness = {
            "relation": witness["relation"],
            "n": n,
            "permutation": pi,
            "132_occurrences": occurrences(pi),
        }
        print(
            "REFUTATION CONFIRMED:",
            checked_witness,
            "brute_force_side:", actual,
            "claimed_side:", claimed,
        )
    else:
        print("REFUTATION REJECTED: brute-force and claimed membership agree")


if __name__ == "__main__":
    main()