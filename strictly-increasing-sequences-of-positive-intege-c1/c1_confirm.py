from itertools import combinations

def main():
    witness = (1, 2, 3, 6)
    reported_pairs = [
        ({1, 2}, {3}),
        ({1, 2, 3}, {4}),
    ]

    def reject(reason):
        print("REFUTATION REJECTED:", reason)

    n = len(witness)
    if n < 1:
        reject("n must be at least 1")
        return
    if any(type(a) is not int or a <= 0 for a in witness):
        reject("all entries must be positive integers")
        return
    if any(witness[i] >= witness[i + 1] for i in range(n - 1)):
        reject("the sequence is not strictly increasing")
        return

    # Enumerate every subset of the 1-based index set, including the empty set.
    indices = tuple(range(1, n + 1))
    subsets = [
        frozenset(c)
        for size in range(n + 1)
        for c in combinations(indices, size)
    ]
    subset_sums = {
        subset: sum(witness[i - 1] for i in subset)
        for subset in subsets
    }

    # Each unordered pair of distinct nonempty subsets is considered once.
    nonempty = [subset for subset in subsets if subset]
    equal_sum_pairs = []
    for I, J in combinations(nonempty, 2):
        if I.isdisjoint(J) and subset_sums[I] == subset_sums[J]:
            equal_sum_pairs.append((I, J))

    if len(equal_sum_pairs) != 2:
        reject("there are {} qualifying unordered pairs, not exactly two"
               .format(len(equal_sum_pairs)))
        return

    # Independently check that the search output named those same two pairs.
    actual = {frozenset((I, J)) for I, J in equal_sum_pairs}
    reported = {
        frozenset((frozenset(I), frozenset(J)))
        for I, J in reported_pairs
    }
    if actual != reported:
        reject("the reported equal-sum pairs do not match brute-force enumeration")
        return

    S = sum(witness)
    attainable = set(subset_sums.values())
    missing = [value for value in range(S + 1) if value not in attainable]
    if missing:
        reject("not every integer from 0 through S is attainable; missing {}"
               .format(missing))
        return

    (I1, J1), (I2, J2) = equal_sum_pairs
    R1 = I1.union(J1)
    R2 = I2.union(J2)
    left_side = len(R1.intersection(R2))
    right_side = 2

    if left_side == right_side:
        reject("the conclusion holds: |R1 intersection R2| = 2")
        return

    print(
        "REFUTATION CONFIRMED:",
        "witness = {}; |R1 intersection R2| = {}; claimed right side = {}"
        .format(witness, left_side, right_side)
    )

if __name__ == "__main__":
    main()