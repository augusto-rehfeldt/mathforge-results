from itertools import permutations

def main():
    witness = {"n": 6, "a": 3, "b": 4, "c": 5}
    n, a, b, c = (witness[key] for key in ("n", "a", "b", "c"))

    if not all(type(x) is int for x in (n, a, b, c)):
        print("REFUTATION REJECTED: n, a, b, c must all be integers")
        return
    if n < 1:
        print("REFUTATION REJECTED: n must be at least 1")
        return
    # Multiplication by two avoids floating-point arithmetic.
    if not (n - 1 < 2 * a and a < b < c <= n - 1):
        print("REFUTATION REJECTED: displacement hypotheses are not satisfied")
        return

    required_displacements = sorted((a, -a, b, -b, c, -c))
    brute_force_side = 0

    # Every tuple here is a bijection of [n], with pi(i) = pi[i - 1].
    for pi in permutations(range(1, n + 1)):
        nonzero_displacements = sorted(
            image - i
            for i, image in enumerate(pi, start=1)
            if image != i
        )
        if nonzero_displacements != required_displacements:
            continue

        # Decompose the permutation into cycles directly.
        visited = set()
        has_cycle_longer_than_two = False
        for start in range(1, n + 1):
            if start in visited:
                continue
            current = start
            length = 0
            while current not in visited:
                visited.add(current)
                length += 1
                current = pi[current - 1]
            if length > 2:
                has_cycle_longer_than_two = True

        if has_cycle_longer_than_two:
            brute_force_side += 1

    # Literal numerical conclusion of the claim.
    s = a + c - b
    claimed_side = 2 * (n - s)

    if brute_force_side != claimed_side:
        print(
            "REFUTATION CONFIRMED:",
            witness,
            "brute_force_side =", brute_force_side,
            "claimed_side =", claimed_side,
        )
    else:
        print(
            "REFUTATION REJECTED: the reported count agrees with the claim;",
            witness,
            "brute_force_side =", brute_force_side,
            "claimed_side =", claimed_side,
        )

if __name__ == "__main__":
    main()