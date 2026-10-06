from itertools import combinations, product
from math import gcd

WITNESS = {
    "L": 315,
    "m": (3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315),
    "a": (2, 2, 2, 7, 10, 19, 18, 9, 24, 36, 255),
    "claimed_box_exists": True,
    "brute_force_box_exists": False,
}


def factor(n):
    factors = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def check_hypotheses(w):
    m, a = w["m"], w["a"]
    k = len(m)
    if k < 1:
        return "k must be at least 1", None
    if len(a) != k:
        return "there must be exactly k choices of a_i", None
    if any(type(v) is not int for v in m + a):
        return "all m_i and a_i must be integers", None
    if any(v <= 1 or v % 2 == 0 for v in m):
        return "each m_i must be odd and greater than 1", None
    if len(set(m)) != k:
        return "the m_i must be pairwise distinct", None
    if any(e >= 3 for v in m for e in factor(v).values()):
        return "a prime cube divides some m_i", None

    L = 1
    for v in m:
        L = (L // gcd(L, v)) * v
    if type(w["L"]) is not int or w["L"] != L:
        return "the reported L is not the least common multiple", None
    return None, L


def all_local_images(p, e):
    """Enumerate every B and every function f satisfying the statement."""
    modulus = p ** e
    images = []
    for size in range(p - 2, p + 1):
        for B in combinations(range(p), size):
            # These are exactly the residues congruent to b modulo p.
            lift_options = [range(b, modulus, p) for b in B]
            for lifts in product(*lift_options):
                images.append(frozenset(lifts))
    return images


def literal_conclusion(L, m, a):
    primes_and_exponents = sorted(factor(L).items())
    moduli = [p ** e for p, e in primes_and_exponents]
    local_choices = [
        all_local_images(p, e) for p, e in primes_and_exponents
    ]

    # A residue is forbidden exactly when at least one stated congruence holds.
    forbidden_coordinates = []
    for x in range(L):
        if any(x % mi == ai % mi for mi, ai in zip(m, a)):
            forbidden_coordinates.append(tuple(x % q for q in moduli))

    # This enumerates all sizes >= p-2, not merely minimal-size boxes.
    for images in product(*local_choices):
        valid = True
        for coordinates in forbidden_coordinates:
            if all(c in image for c, image in zip(coordinates, images)):
                valid = False
                break
        if valid:
            return True
    return False


def main():
    reason, L = check_hypotheses(WITNESS)
    if reason is not None:
        print("REFUTATION REJECTED:", reason)
        return

    # The claimed conclusion asserts that such a box exists.
    claimed_side = True
    brute_force_side = literal_conclusion(L, WITNESS["m"], WITNESS["a"])
    if claimed_side and not brute_force_side:
        print(
            "REFUTATION CONFIRMED:",
            WITNESS,
            "claimed_side =", claimed_side,
            "literal_brute_force_side =", brute_force_side,
        )
    else:
        print("REFUTATION REJECTED: the required uncovered CRT box exists")


if __name__ == "__main__":
    main()