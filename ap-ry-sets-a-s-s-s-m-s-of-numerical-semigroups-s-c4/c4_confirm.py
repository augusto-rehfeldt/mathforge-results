def gcd_from_scratch(numbers):
    result = 0
    for number in numbers:
        number = abs(number)
        while number:
            result, number = number, result % number
    return result


def belongs(target, generators):
    """Literal nonnegative-sum membership, by finite dynamic programming."""
    if target < 0:
        return False
    reachable = [False] * (target + 1)
    reachable[0] = True
    for n in range(1, target + 1):
        reachable[n] = any(
            n >= u and reachable[n - u] for u in generators
        )
    return reachable[target]


def is_minimal(generators):
    for i, u in enumerate(generators):
        others = generators[:i] + generators[i + 1:]
        if belongs(u, others):
            return False
    return True


def brute_force_invariants(generators, m):
    # Once m consecutive integers belong, all subsequent integers belong:
    # m itself is a generator, so repeatedly adding m covers every residue.
    reachable = [True]
    run = 1
    n = 0
    while run < m:
        n += 1
        present = any(
            n >= u and reachable[n - u] for u in generators
        )
        reachable.append(present)
        run = run + 1 if present else 0

    c = n - m + 1
    g = sum(not reachable[k] for k in range(c))
    L = sum(reachable[k] for k in range(c))
    W4 = 4 * L - c

    # Enumerate enough additional membership values to compute the
    # Apéry set literally: u belongs but u-m does not.
    while len(reachable) <= c + m - 1:
        k = len(reachable)
        reachable.append(any(
            k >= u and reachable[k - u] for u in generators
        ))
    apery = [
        u for u in range(c + m)
        if reachable[u] and (u < m or not reachable[u - m])
    ]
    w = [None] * m
    for u in apery:
        w[u % m] = u

    return {"c": c, "g": g, "L": L, "W4": W4,
            "apery": apery, "w": w}


def main():
    witness = (11, 16, 21, 23)
    m, a, b, d = witness

    def reject(reason):
        print("REFUTATION REJECTED:", reason)

    if not all(type(x) is int for x in witness):
        reject("the witness is not a quadruple of integers")
        return
    if not (4 <= m < a < b < 2 * m <= d):
        reject("the required ordering inequalities fail")
        return
    if gcd_from_scratch(witness) != 1:
        reject("gcd(m,a,b,d) is not 1")
        return

    S = [m, a, b, d]
    T = [m, a, b, d - m]
    if not is_minimal(S):
        reject("the displayed generating set of S is not minimal")
        return
    if not is_minimal(T):
        reject("the displayed generating set of T is not minimal")
        return

    s = brute_force_invariants(S, m)
    t = brute_force_invariants(T, m)
    conductor_difference = s["c"] - t["c"]
    if conductor_difference < m:
        reject("c(S)-c(T) < m")
        return

    left = 4 * (s["g"] - t["g"])
    right = 3 * (s["c"] - t["c"])
    if left > right:
        print(
            "REFUTATION CONFIRMED:", witness,
            f"4(g(S)-g(T))={left}; 3(c(S)-c(T))={right}"
        )
    else:
        reject(f"the conclusion holds: {left} <= {right}")


if __name__ == "__main__":
    main()