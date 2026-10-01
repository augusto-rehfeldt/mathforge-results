from itertools import combinations

WITNESS = (3, 2, 1, 1, 4)


def partitions(n):
    """Generate each partition of [n] exactly once."""
    blocks = []

    def generate(x):
        if x > n:
            yield tuple(tuple(block) for block in blocks)
            return
        for block in blocks:
            block.append(x)
            yield from generate(x + 1)
            block.pop()
        blocks.append([x])
        yield from generate(x + 1)
        blocks.pop()

    yield from generate(1)


def check():
    n, k, s, t, m = WITNESS
    if any(type(x) is not int for x in WITNESS):
        return False, "all parameters must be integers"
    if n < 1:
        return False, "n must be at least 1"
    if any(x < 0 for x in (k, s, t, m)):
        return False, "k, s, t, and m must be nonnegative"

    count = 0
    for partition in partitions(n):
        # Independently enforce the definition of a partition of [n].
        if any(not block for block in partition):
            continue
        elements = [x for block in partition for x in block]
        if sorted(elements) != list(range(1, n + 1)):
            continue

        gaps = []
        for block in partition:
            ordered = sorted(block)
            gaps.extend(
                ordered[j + 1] - ordered[j]
                for j in range(len(ordered) - 1)
            )
        if len(gaps) != len(set(gaps)):
            continue

        statistics = (
            len(partition),
            sum(len(block) == 1 for block in partition),
            sum(gaps),
            sum(max(block) for block in partition),
        )
        if statistics == (k, s, t, m):
            count += 1

    # The two equalities are conditions defining the claimed side,
    # not additional hypotheses restricting the universal claim.
    subset_count = 0
    r = n - k
    if s == 2 * k - n and 2 * m == k * (n + 1) + t:
        universe = tuple(range(1, n // 2 + 1))
        # Enumerate every subset literally, including the empty subset.
        for size in range(len(universe) + 1):
            for subset in combinations(universe, size):
                if len(subset) == r and sum(
                    n + 1 - 2 * i for i in subset
                ) == t:
                    subset_count += 1

    actual_parity = count % 2
    claimed_parity = subset_count % 2
    if actual_parity != claimed_parity:
        return True, (
            f"n={n}, k={k}, s={s}, t={t}, m={m}; "
            f"A={count}, A mod 2={actual_parity}; "
            f"claimed side={subset_count}, claimed parity={claimed_parity}"
        )
    return False, (
        f"the conclusion holds at witness {WITNESS}: "
        f"A={count}, A mod 2={actual_parity}, "
        f"claimed side={subset_count}, claimed parity={claimed_parity}"
    )


if __name__ == "__main__":
    confirmed, details = check()
    print(
        ("REFUTATION CONFIRMED:" if confirmed else "REFUTATION REJECTED:")
        + " "
        + details
    )