from collections import Counter
from math import factorial


def is_prime(p):
    if not isinstance(p, int) or p < 2:
        return False
    d = 2
    while d * d <= p:
        if p % d == 0:
            return False
        d += 1
    return True


def partition_polynomial(objects, weights, singleton_y_objects):
    """Brute-force enumeration of all admissible labeled set partitions."""
    size = len(objects)
    limit = 1 << size
    sums = [0] * limit
    singleton_factors = [0] * limit

    for mask in range(1, limit):
        bit = mask & -mask
        index = bit.bit_length() - 1
        sums[mask] = sums[mask ^ bit] + weights[objects[index]]
        if mask == bit and objects[index] in singleton_y_objects:
            singleton_factors[mask] = 1

    polynomial = Counter()

    def enumerate_partitions(remaining, blocks, singletons):
        if remaining == 0:
            polynomial[(blocks, singletons)] += 1
            return

        # The next block contains the least remaining labeled object.
        # This enumerates each unordered set partition exactly once.
        anchor = remaining & -remaining
        others = remaining ^ anchor
        subset = others
        while True:
            block = subset | anchor
            if sums[block] % 3 == 0:
                enumerate_partitions(
                    remaining ^ block,
                    blocks + 1,
                    singletons + singleton_factors[block],
                )
            if subset == 0:
                break
            subset = (subset - 1) & others

    enumerate_partitions(limit - 1, 0, 0)
    return polynomial


def main():
    # The sole reported witness; no search is performed.
    p, n = 5, 14
    exponent = (2, 0)
    reported_left, reported_right = 2731, 11

    reasons = []
    if not is_prime(p):
        reasons.append("p is not prime")
    if p < 5:
        reasons.append("p < 5")
    if not isinstance(n, int):
        reasons.append("n is not an integer")
    elif n < 3 * p - 1:
        reasons.append("n < 3p - 1")

    if reasons:
        print("REFUTATION REJECTED: " + "; ".join(reasons))
        return

    universe = list(range(1, n + 1))
    A = [r for r in universe if r % 3 == 1][:p]
    B = [r for r in universe if r % 3 == 2][:p]
    if len(A) != p or len(B) != p:
        print("REFUTATION REJECTED: the prescribed A or B has fewer than p elements")
        return

    R = [r for r in universe if r not in set(A + B)]
    a, b = object(), object()  # Distinct formal objects, neither in R.

    integer_weights = {r: r for r in universe}
    left_polynomial = partition_polynomial(
        universe, integer_weights, set(universe)
    )
    r_polynomial = partition_polynomial(R, integer_weights, set(R))

    special_weights = {r: r for r in R}
    special_weights[a] = p
    special_weights[b] = 2 * p
    h_polynomial = partition_polynomial(
        R + [a, b], special_weights, set(R)
    )

    # Literally form H_R,p + p! x^p F_R in Z[x,y].
    right_polynomial = Counter(h_polynomial)
    for (k, s), coefficient in r_polynomial.items():
        right_polynomial[(k + p, s)] += factorial(p) * coefficient

    left = left_polynomial[exponent]
    right = right_polynomial[exponent]
    modulus = p * p

    if (left - right) % modulus != 0:
        print(
            f"REFUTATION CONFIRMED: p={p}, n={n}, coefficient x^2 y^0, "
            f"left={left}, right={right}, residues modulo {modulus}: "
            f"{left % modulus}, {right % modulus}"
        )
    else:
        print(
            f"REFUTATION REJECTED: the conclusion holds at the reported "
            f"coefficient; left={left}, right={right}, modulo {modulus}. "
            f"Reported values were {reported_left}, {reported_right}."
        )


if __name__ == "__main__":
    main()