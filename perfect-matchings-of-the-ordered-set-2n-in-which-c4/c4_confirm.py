from math import comb


def perfect_matchings(points):
    if not points:
        yield ()
        return
    a = points[0]
    for i in range(1, len(points)):
        b = points[i]
        remaining = points[1:i] + points[i + 1:]
        for rest in perfect_matchings(remaining):
            yield ((a, b),) + rest


def crosses(first, second):
    a, b = first
    s, t = second
    return a < s < b < t or s < a < t < b


def nested(first, second):
    a, b = first
    s, t = second
    return a < s < t < b or s < a < b < t


def matching_statistics(matching):
    size = len(matching)
    adjacency = [set() for _ in range(size)]
    nested_pairs = 0

    for i in range(size):
        for k in range(i + 1, size):
            if crosses(matching[i], matching[k]):
                adjacency[i].add(k)
                adjacency[k].add(i)
            if nested(matching[i], matching[k]):
                nested_pairs += 1

    all_degrees_two = all(len(neighbors) == 2 for neighbors in adjacency)

    seen = set()
    components = 0
    for vertex in range(size):
        if vertex in seen:
            continue
        components += 1
        stack = [vertex]
        seen.add(vertex)
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

    return all_degrees_two, components, nested_pairs


def main():
    # The reported witness only; no search for other witnesses.
    n, c, j = 4, 1, 1
    witness = f"(n={n}, c={c}, j={j})"

    if any(type(value) is not int for value in (n, c, j)):
        print("REFUTATION REJECTED: witness parameters must be integers")
        return
    if c < 1:
        print("REFUTATION REJECTED: c must be at least 1")
        return
    if n < 3 * c:
        print("REFUTATION REJECTED: n must be at least 3c")
        return

    threshold = n - 3 * c
    if 0 <= j < threshold:
        claimed = 0
    elif j == threshold:
        r, s = n - 2 * c - 1, c - 1
        if not (0 <= s <= r):
            print("REFUTATION REJECTED: binomial arguments outside stated domain")
            return
        claimed = 2 ** (n - 3 * c) * comb(r, s)
    else:
        print("REFUTATION REJECTED: j is outside the asserted conclusions")
        return

    actual = 0
    points = tuple(range(1, 2 * n + 1))
    for matching in perfect_matchings(points):
        degrees_two, component_count, nested_count = matching_statistics(matching)
        if degrees_two and component_count == c and nested_count == j:
            actual += 1

    if actual != claimed:
        print(
            f"REFUTATION CONFIRMED: {witness}; "
            f"A(n,c,j)={actual}; claimed={claimed}"
        )
    else:
        print(
            f"REFUTATION REJECTED: {witness} satisfies the conclusion; "
            f"A(n,c,j)={actual}; claimed={claimed}"
        )


if __name__ == "__main__":
    main()