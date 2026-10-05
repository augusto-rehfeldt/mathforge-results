from itertools import product, combinations


def signed_sums(R):
    return {
        sum(e * r for e, r in zip(coefficients, R))
        for coefficients in product((-1, 0, 1), repeat=len(R))
    }


def subset_sums(R):
    return {
        sum(e * r for e, r in zip(coefficients, R))
        for coefficients in product((0, 1), repeat=len(R))
    }


def translates_are_disjoint(S, a, b):
    sets = [S, {a + s for s in S}, {b + s for s in S},
            {a + b + s for s in S}]
    return all(A.isdisjoint(B) for A, B in combinations(sets, 2))


def main():
    R = (1, 6)
    x, y = 4, 8
    reported_holes = (2, 3)
    m = len(R)

    def reject(reason):
        print("REFUTATION REJECTED: " + reason)

    if m < 1:
        reject("m must be at least 1")
        return
    if any(type(r) is not int or r <= 0 for r in R):
        reject("R must consist of positive integers")
        return
    if any(R[i - 1] >= R[i] for i in range(1, m)):
        reject("R is not strictly increasing")
        return
    if any(R[i] <= sum(R[:i]) for i in range(1, m)):
        reject("R does not satisfy the superincreasing hypothesis")
        return
    if type(x) is not int or type(y) is not int or not (0 < x < y):
        reject("x and y must be positive integers with x < y")
        return

    D = signed_sums(R)
    S = subset_sums(R)
    holes = []
    t = 1
    while len(holes) < 2:
        if t not in D:
            holes.append(t)
        t += 1
    h1, h2 = holes

    if (h1, h2) != reported_holes:
        reject("reported holes differ from the two smallest positive holes: "
               + repr((h1, h2)))
        return

    # Use the explicitly corrected statement: literal subset-sum translates.
    premise = translates_are_disjoint(S, x, y)
    if not premise:
        reject("the given four subset-sum translates are not pairwise disjoint")
        return

    # Enumerate every positive u < v <= y, rather than using a shortcut
    # involving signed-sum membership.
    successful_pairs = []
    for u in range(1, y):
        for v in range(u + 1, y + 1):
            if u in (h1, h2) and translates_are_disjoint(S, u, v):
                successful_pairs.append((u, v))
    conclusion = bool(successful_pairs)

    if conclusion:
        reject("the conclusion holds; qualifying pairs=" + repr(successful_pairs))
        return

    print(
        "REFUTATION CONFIRMED: "
        f"R={R}, x={x}, y={y}, h1={h1}, h2={h2}; "
        f"hypotheses=True; given four subset-sum translates pairwise disjoint="
        f"{premise}; exists positive u<v<=y with u in {{h1,h2}} and "
        f"four subset-sum translates pairwise disjoint={conclusion}"
    )


if __name__ == "__main__":
    main()