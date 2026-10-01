from collections import Counter
from itertools import combinations

# Reported witness; no other witnesses are tested.
m = 2
exponents = (3, 1, 0)
reported_lhs = 1
reported_rhs = 0


def partitions(n):
    """Generate every partition of [n] exactly once."""
    blocks = []

    def visit(i):
        if i > n:
            yield tuple(tuple(block) for block in blocks)
            return
        for j in range(len(blocks)):
            blocks[j].append(i)
            yield from visit(i + 1)
            blocks[j].pop()
        blocks.append([i])
        yield from visit(i + 1)
        blocks.pop()

    yield from visit(1)


def admissible(partition):
    return all(abs(i - j) != 2
               for block in partition
               for i, j in combinations(block, 2))


def statistics(partition, n):
    owner = {}
    for index, block in enumerate(partition):
        for element in block:
            owner[element] = index
    b = len(partition)
    s = sum(len(block) == 1 for block in partition)
    a = sum(owner[i] == owner[i + 1] for i in range(1, n))
    return b, s, a


def subsets(items):
    for size in range(len(items) + 1):
        yield from combinations(items, size)


def matchings(items):
    """Brute force all subsets of possible edges, retaining matchings."""
    edges = tuple(combinations(items, 2))
    for chosen in subsets(edges):
        endpoints = [v for edge in chosen for v in edge]
        if len(endpoints) == len(set(endpoints)):
            yield chosen


def check():
    if type(m) is not int or m < 2:
        return "REFUTATION REJECTED: m must be an integer at least 2"
    if (not isinstance(exponents, tuple) or len(exponents) != 3
            or any(type(e) is not int or e < 0 for e in exponents)):
        return "REFUTATION REJECTED: witness must specify three nonnegative integer exponents"

    # The witness is a coefficient index, not a particular Q, D, I, or M.
    # All admissibility and inner-sum restrictions are enforced below.
    lhs = Counter()
    for p in partitions(2 * m + 1):
        if admissible(p):
            lhs[statistics(p, 2 * m + 1)] += 1

    rhs = Counter()
    for q in partitions(m):
        if not admissible(q):
            continue
        b, _, a = statistics(q, m)
        block_of_m = next(j for j, block in enumerate(q) if m in block)
        d_choices = [None] + [
            j for j, block in enumerate(q)
            if m - 1 not in block and m not in block
        ]
        for d in d_choices:
            delta = int(d is not None)
            eligible_i = tuple(
                j for j in range(b) if j != d and j != block_of_m
            )
            for i_tuple in subsets(eligible_i):
                i_set = set(i_tuple)
                remaining = tuple(
                    j for j in range(b) if j != d and j not in i_set
                )
                for matching in matchings(remaining):
                    matched = {j for edge in matching for j in edge}
                    u = sum(len(q[j]) == 1 and j not in matched
                            for j in remaining)
                    powers = (
                        2 * b - len(i_set) - 2 * delta + 1,
                        2 * u + 1 - delta,
                        2 * a,
                    )
                    rhs[powers] += 1

    left = lhs[exponents]
    right = rhs[exponents]
    if left % 2 == right % 2:
        return (
            f"REFUTATION REJECTED: witness m={m}, exponents={exponents} "
            f"has equal coefficient parities; LHS={left}, RHS={right}"
        )
    return (
        f"REFUTATION CONFIRMED: m={m}, exponents={exponents}; "
        f"LHS={left} (mod 2={left % 2}), "
        f"RHS={right} (mod 2={right % 2})"
    )


if __name__ == "__main__":
    print(check())