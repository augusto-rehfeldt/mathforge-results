def main():
    w = "0101212"
    reported_occurrences = [(0, 2), (3, 2)]
    n = len(w)

    def reject(reason):
        print("REFUTATION REJECTED:", reason)

    if n < 1:
        reject("n is not at least 1")
        return
    if any(c not in "012" for c in w):
        reject("w is not a word over {0,1,2}")
        return

    occurrences = []
    for k in range(1, n // 2 + 1):
        for a in range(n - 2 * k + 1):
            equal = True
            for c in "012":
                left_count = 0
                right_count = 0
                for position in range(a, a + k):
                    if w[position] == c:
                        left_count += 1
                for position in range(a + k, a + 2 * k):
                    if w[position] == c:
                        right_count += 1
                if left_count != right_count:
                    equal = False
            if equal:
                occurrences.append((a, k))

    if len(occurrences) != 2:
        reject(f"expected exactly two occurrences; found {occurrences}")
        return
    if sorted(occurrences) != sorted(reported_occurrences):
        reject(f"reported occurrences disagree with brute force: {occurrences}")
        return

    (i, h), (j, other_h) = sorted(occurrences)
    if h != other_h:
        reject("the two occurrences do not have a common half-length")
        return
    if not (h >= 1 and 0 <= i < j < i + 2 * h <= n
            and j + 2 * h <= n):
        reject("the required interval and overlap inequalities fail")
        return

    # Evaluate the conclusion literally: j = i + 1.
    left_side = j
    right_side = i + 1
    if left_side == right_side:
        reject(f"the conclusion holds: j={left_side}, i+1={right_side}")
        return

    print(
        f"REFUTATION CONFIRMED: w={w} "
        f"j={left_side} i+1={right_side}"
    )


if __name__ == "__main__":
    main()