from fractions import Fraction
from itertools import product

WITNESS = "1110100"


def evolve(x):
    n = len(x)
    return tuple(x[i] ^ (x[(i - 1) % n] & x[(i + 1) % n])
                 for i in range(n))


def exact_period_two(x):
    y = evolve(x)
    return y != x and evolve(y) == x


def zero_runs_and_blocks(x):
    """Return maximal cyclic zero runs and blocks after removing long runs."""
    n = len(x)
    if not any(x):
        return [tuple(range(n))], []
    runs = []
    for i in range(n):
        if x[i] == 0 and x[(i - 1) % n] == 1:
            run = []
            j = i
            while x[j] == 0:
                run.append(j)
                j = (j + 1) % n
            runs.append(tuple(run))

    long_runs = [r for r in runs if len(r) >= 2]
    if not long_runs:
        return runs, []

    blocks = []
    for index, run in enumerate(long_runs):
        stop = long_runs[(index + 1) % len(long_runs)][0]
        j = (run[-1] + 1) % n
        block = []
        while j != stop:
            block.append(str(x[j]))
            j = (j + 1) % n
        blocks.append("".join(block))
    return runs, blocks


def rotations(x):
    return [x[i:] + x[:i] for i in range(len(x))]


def brute_force_M(n, k, a, b, c):
    """Enumerate all necklaces, then apply the definitions literally."""
    seen = set()
    total = Fraction(0)
    for x in product((0, 1), repeat=n):
        representative = min(rotations(x))
        if representative in seen:
            continue
        seen.add(representative)
        y = evolve(representative)
        runs, _ = zero_runs_and_blocks(representative)
        if not exact_period_two(representative):
            continue
        if sum(len(r) >= 2 for r in runs) != k:
            continue
        if sorted((sum(representative), sum(y))) != sorted((a, b)):
            continue
        if sum(p != q for p, q in zip(representative, y)) != c:
            continue
        stabilizer = sum(r == representative
                         for r in rotations(representative))
        total += Fraction(n, stabilizer)
    return total


def coefficient_P_power(n, k, a, b, c):
    """
    Expand P literally, truncating t degree at n:
    (sum_{z>=2} t^z) *
    (tuv + t^2u^2v^2 + t^3q(u^3v^2 + u^2v^3)).
    """
    block_terms = [
        (1, 1, 1, 0),
        (2, 2, 2, 0),
        (3, 3, 2, 1),
        (3, 2, 3, 1),
    ]
    terms = []
    for z in range(2, n + 1):
        for length, u, v, q in block_terms:
            if z + length <= n:
                terms.append((z + length, u, v, q))

    expansion = {(0, 0, 0, 0): 1}
    for _ in range(k):
        following = {}
        for exponent, multiplicity in expansion.items():
            for term in terms:
                new = tuple(x + y for x, y in zip(exponent, term))
                if new[0] <= n:
                    following[new] = following.get(new, 0) + multiplicity
        expansion = following
    return expansion.get((n, a, b, c), 0)


def main():
    if not WITNESS or any(ch not in "01" for ch in WITNESS):
        print("REFUTATION REJECTED: witness is not a binary word")
        return

    x = tuple(map(int, WITNESS))
    n = len(x)
    runs, blocks = zero_runs_and_blocks(x)
    if n < 3:
        print("REFUTATION REJECTED: n is below 3")
        return
    if not any(x[i] == x[(i + 1) % n] == 0 for i in range(n)):
        print("REFUTATION REJECTED: no cyclic consecutive zeros")
        return

    actual_period = exact_period_two(x)
    allowed = {"1", "11", "111", "101"}
    claimed_period = (
        all(block in allowed for block in blocks)
        and any(block in {"111", "101"} for block in blocks)
    )

    y = evolve(x)
    k = sum(len(r) >= 2 for r in runs)
    a, b = sorted((sum(x), sum(y)))
    c = sum(p != q for p, q in zip(x, y))

    if not actual_period:
        print("REFUTATION REJECTED: witness is not an exact temporal two-cycle")
        return
    if not (k >= 1 and a >= 0 and b >= 0 and c >= 1):
        print("REFUTATION REJECTED: counting parameters violate the hypotheses")
        return

    actual_M = brute_force_M(n, k, a, b, c)
    coefficient = coefficient_P_power(n, k, a, b, c)
    if a != b:
        coefficient += coefficient_P_power(n, k, b, a, c)
    claimed_M = Fraction(n, k) * coefficient

    if actual_period != claimed_period or actual_M != claimed_M:
        print(
            f"REFUTATION CONFIRMED: {WITNESS}; "
            f"period-two brute_force={actual_period}, claimed={claimed_period}; "
            f"blocks={blocks}; "
            f"M({n},{k},{a},{b},{c}) brute_force={actual_M}, "
            f"claimed={claimed_M}"
        )
    else:
        print("REFUTATION REJECTED: witness violates neither conclusion")


if __name__ == "__main__":
    main()