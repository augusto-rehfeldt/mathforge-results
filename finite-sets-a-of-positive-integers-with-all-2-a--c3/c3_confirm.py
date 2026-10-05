from itertools import combinations, product


WITNESS = {"n": 4, "A": (1, 2, 4, 8), "C": (3, 5, 6, 7)}


def is_positive_integer(x):
    return type(x) is int and x > 0


def distinct_subset_sums(X):
    elements = tuple(X)
    seen = set()
    for mask in range(1 << len(elements)):
        total = sum(elements[i] for i in range(len(elements))
                    if mask & (1 << i))
        if total in seen:
            return False
        seen.add(total)
    return True


def D(X):
    elements = tuple(X)
    return {
        sum(coefficient * element
            for coefficient, element in zip(coefficients, elements))
        for coefficients in product((-1, 0, 1), repeat=len(elements))
    }


def check_hypotheses(witness):
    n, A, C = witness["n"], witness["A"], witness["C"]
    if type(n) is not int or n < 2:
        return False, "n is not an integer at least 2"
    for name, elements in (("A", A), ("C", C)):
        if not all(is_positive_integer(x) for x in elements):
            return False, name + " contains a nonpositive or noninteger element"
        if len(elements) != n or len(set(elements)) != n:
            return False, name + " is not a set of cardinality n"
        if not distinct_subset_sums(elements):
            return False, name + " does not have distinct subset sums"
    if not max(C) < max(A):
        return False, "max C is not less than max A"
    return True, ""


def brute_force_conclusion(n, A):
    A = set(A)
    maximum = max(A)

    # Any successful T consists of distinct positive integers below maximum.
    # Thus this finite enumeration includes every possible successful T.
    universe = range(1, maximum)
    for size in range(1, n // 2 + 2):
        for removed in combinations(sorted(A), size):
            R = set(removed)
            retained = A - R
            for replacement in combinations(universe, size):
                T = set(replacement)
                # Evaluate every condition of the conclusion literally.
                if not (1 <= len(R) <= n // 2 + 1):
                    continue
                if len(T) != len(R):
                    continue
                if not all(is_positive_integer(x) for x in T):
                    continue
                if not T.isdisjoint(retained):
                    continue
                if not distinct_subset_sums(T):
                    continue
                if D(T).intersection(D(retained)) != {0}:
                    continue
                if not max(retained | T) < maximum:
                    continue
                return True, {"R": sorted(R), "T": sorted(T)}
    return False, None


def main():
    hypotheses, reason = check_hypotheses(WITNESS)
    if not hypotheses:
        print("REFUTATION REJECTED:", reason)
        return

    conclusion, replacement = brute_force_conclusion(
        WITNESS["n"], WITNESS["A"]
    )
    if conclusion:
        print("REFUTATION REJECTED:",
              "the conclusion holds; successful replacement =", replacement)
    else:
        print("REFUTATION CONFIRMED:", WITNESS,
              "hypotheses =", hypotheses, "conclusion =", conclusion)


if __name__ == "__main__":
    main()