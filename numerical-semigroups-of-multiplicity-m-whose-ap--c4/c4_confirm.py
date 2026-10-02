import sys


def kunz_violations(m, a):
    failures = []
    for i in range(1, m):
        for j in range(1, m):
            if i + j < m:
                lhs, rhs = a[i - 1] + a[j - 1], a[i + j - 1]
            elif i + j > m:
                lhs, rhs = a[i - 1] + a[j - 1] + 1, a[i + j - m - 1]
            else:
                continue
            if lhs < rhs:
                failures.append((i, j, lhs, rhs))
    return failures


def representatives(m, a):
    return {i: i + m * a[i - 1] for i in range(1, m)}


def in_S(x, m, w):
    # Directly test the union defining S, including t = 0.
    if x < 0:
        return False
    if x % m == 0:
        return True
    return any(x >= value and (x - value) % m == 0
               for value in w.values())


def maximal_indices(m, w):
    return {
        i for i in w
        if not any(j != i and in_S(w[j] - w[i], m, w) for j in w)
    }


def minimal_generator(x, m, w):
    if x <= 0 or not in_S(x, m, w):
        return False
    # Enumerate every possible decomposition into two positive integers.
    return not any(
        in_S(y, m, w) and in_S(x - y, m, w)
        for y in range(1, x)
    )


def main():
    witness = {
        "m": 5,
        "a": (3, 1, 3, 1),
        "p": 3,
        "r": 1,
    }
    m, a, p, r = (witness[key] for key in ("m", "a", "p", "r"))

    reasons = []
    if type(m) is not int or m < 3:
        reasons.append("m is not an integer >= 3")
    if len(a) != m - 1 or any(type(x) is not int or x not in (1, 2, 3)
                             for x in a):
        reasons.append("a is not in {1,2,3}^{m-1}")
    if any(type(x) is not int or not 1 <= x < m for x in (p, r)):
        reasons.append("p or r is outside I")
    if p == r:
        reasons.append("p and r are not distinct")

    if reasons:
        print("REFUTATION REJECTED:", "; ".join(reasons))
        return

    failures = kunz_violations(m, a)
    w = representatives(m, a)
    original_maxima = maximal_indices(m, w)
    if failures:
        reasons.append("a violates Kunz inequalities: " + repr(failures))
    if original_maxima != {p, r}:
        reasons.append("original maximal-index set is " +
                       repr(sorted(original_maxima)) + ", not {p,r}")
    if a[r - 1] != 3:
        reasons.append("a_r is not 3")

    if reasons:
        print("REFUTATION REJECTED:", "; ".join(reasons))
        return

    b = list(a)
    b[r - 1] = 2
    b = tuple(b)

    C = set()
    for j in range(1, m):
        if j in {p, r}:
            continue
        k = (r - j) % m
        epsilon = 0 if j < r else 1
        if (a[j - 1] + a[k - 1] + epsilon == 3
                and minimal_generator(w[k], m, w)
                and not in_S(w[p] - w[j], m, w)):
            C.add(j)

    R = {r} if not in_S(w[p] - (w[r] - m), m, w) else set()
    D = C | R
    claimed_maxima = {p} | D
    g = sum(a)

    claimed = {
        "Kunz(b)": True,
        "maximal_indices(b)": sorted(claimed_maxima),
        "exactly_two_maximal_indices": len(D) == 1,
    }
    if len(D) == 1:
        q = next(iter(D))
        claimed["genus(b)"] = g - 1
        claimed["maximal_residue_gap(b)"] = abs(p - q)

    wb = representatives(m, b)
    actual_maxima = maximal_indices(m, wb)
    actual = {
        "Kunz(b)": not kunz_violations(m, b),
        "maximal_indices(b)": sorted(actual_maxima),
        "exactly_two_maximal_indices": len(actual_maxima) == 2,
        "genus(b)": sum(b),
        "maximal_residue_gap(b)": (
            abs(max(actual_maxima) - min(actual_maxima))
            if len(actual_maxima) == 2 else None
        ),
    }

    violations = [key for key in claimed if claimed[key] != actual[key]]
    witness.update({"b": b, "C": sorted(C), "R": sorted(R)})

    if violations:
        print("REFUTATION CONFIRMED:", {
            "witness": witness,
            "claimed_side": claimed,
            "brute_force_side": actual,
        })
    else:
        print("REFUTATION REJECTED: witness satisfies the hypotheses "
              "but does not violate the conclusion")


if __name__ == "__main__":
    main()
    sys.exit(0)