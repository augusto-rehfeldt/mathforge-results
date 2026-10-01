def main():
    n = 11
    A = [0, 1, 4, 5, 6, 7, 8, 9, 11]
    B = [0, 1, 2, 3, 4, 6, 7, 8, 11]

    def reject(reason):
        print("REFUTATION REJECTED: " + reason)

    if type(n) is not int or n < 1:
        reject("n is not an integer at least 1")
        return

    for name, values in (("A", A), ("B", B)):
        if any(type(x) is not int or x < 0 or x > n for x in values):
            reject(name + " is not a subset of {0,...,n}")
            return
        if len(set(values)) != len(values):
            reject(name + " contains duplicate entries")
            return

    SA, SB = set(A), set(B)
    if SA == SB:
        reject("A and B are not distinct")
        return
    if not all(x in SA and x in SB for x in (0, n)):
        reject("0 and n do not belong to both sets")
        return

    k = len(SA)
    if len(SB) != k:
        reject("A and B do not have equal cardinalities")
        return
    if len(SA.intersection(SB)) != k - 2:
        reject("|A intersection B| is not k-2")
        return

    for t in range(1, n + 1):
        count_A = 0
        count_B = 0
        for a in SA:
            for a_prime in SA:
                if a_prime - a == t:
                    count_A += 1
        for b in SB:
            for b_prime in SB:
                if b_prime - b == t:
                    count_B += 1
        if count_A != count_B:
            reject(
                "difference counts disagree at t={}: A={}, B={}".format(
                    t, count_A, count_B
                )
            )
            return

    reflected_A = set()
    for a in SA:
        reflected_A.add(n - a)
    if SB == reflected_A:
        reject("B is the reflection of A")
        return

    left_side = n
    right_side = 2 * k - 1
    if left_side >= right_side:
        reject(
            "the conclusion holds: {} >= {}".format(left_side, right_side)
        )
        return

    print(
        "REFUTATION CONFIRMED: n={}, k={}, A={}, B={}; "
        "left side n={}, right side 2k-1={} ({} >= {} is false)".format(
            n, k, sorted(SA), sorted(SB),
            left_side, right_side, left_side, right_side
        )
    )


if __name__ == "__main__":
    main()