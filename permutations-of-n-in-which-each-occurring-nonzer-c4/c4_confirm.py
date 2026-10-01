from itertools import permutations

def check_permutation(pi, n, a, b, c):
    if len(pi) != n or sorted(pi) != list(range(1, n + 1)):
        return False, "not a bijection of {1,...,n}"

    displacements = [pi[i - 1] - i for i in range(1, n + 1)]
    nonzero = sorted(d for d in displacements if d != 0)
    if nonzero != sorted([a, -a, b, -b, c, -c]):
        return False, "incorrect nonzero signed displacements"

    seen = set()
    cycles = []
    for start in range(1, n + 1):
        if start in seen:
            continue
        cycle = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = pi[current - 1]
        if current != start:
            return False, "cycle does not close at its starting point"
        cycles.append(cycle)

    if sorted(map(len, cycles)) != [1] * (n - 6) + [6]:
        return False, "not exactly one six-cycle and n-6 fixed points"
    if sum(d == 0 for d in displacements) != n - 6:
        return False, "incorrect number of fixed points"
    if len(cycles) != n - 5:
        return False, "incorrect total number of cycles"
    if sum(d for d in displacements if d > 0) != a + b + c:
        return False, "incorrect total positive displacement"
    return True, ""

def main():
    n, a, b, c = 7, 1, 3, 5
    reported_cycle = (1, 2, 7, 4, 3, 6)
    witness = (n, a, b, c, reported_cycle)

    def reject(reason):
        print("REFUTATION REJECTED:", reason)

    if not all(type(x) is int for x in (n, a, b, c)):
        reject("parameters are not integers")
        return
    if not (1 <= a < b < c and c != a + b and n >= 6):
        reject("parameters violate the claim's hypotheses")
        return
    if (len(reported_cycle) != 6
            or any(type(v) is not int for v in reported_cycle)
            or len(set(reported_cycle)) != 6
            or any(v < 1 or v > n for v in reported_cycle)):
        reject("reported cycle is not six distinct integers in {1,...,n}")
        return

    pi = list(range(1, n + 1))
    for j, v in enumerate(reported_cycle):
        pi[v - 1] = reported_cycle[(j + 1) % 6]

    valid, reason = check_permutation(pi, n, a, b, c)
    if not valid:
        reject("reported witness fails: " + reason)
        return

    # Exhaustively evaluate existence over every bijection, without
    # selecting or reporting any alternative witness.
    existence_side = False
    for candidate in permutations(range(1, n + 1)):
        valid, _ = check_permutation(candidate, n, a, b, c)
        if valid:
            existence_side = True

    claimed_side = n >= b + c - a + 1
    if existence_side != claimed_side:
        print(
            "REFUTATION CONFIRMED:",
            "witness=" + repr(witness),
            "exists=" + repr(existence_side),
            "(n >= b+c-a+1)=" + repr(claimed_side),
        )
    else:
        reject("the brute-force existence side equals the claimed side")

if __name__ == "__main__":
    main()