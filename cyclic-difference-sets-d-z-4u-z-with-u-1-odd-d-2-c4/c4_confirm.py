import sys

def main():
    # Use only the reported parameter and vector, not the reported checks.
    u = 3
    x = [-3, 1, 1, 1, -3, 1, 1, 1, 3, 1, 1, 1]

    def reject(reason):
        print("REFUTATION REJECTED:", reason)

    if type(u) is not int or u <= 1 or u % 2 != 1:
        reject("u is not an odd integer greater than 1")
        return

    # Checking all integer squares also checks every prime square.
    d = 2
    while d * d <= u:
        if u % (d * d) == 0:
            reject("u is not squarefree")
            return
        d += 1

    n = 4 * u
    if len(x) != n:
        reject("the vector does not have length 4u")
        return

    total = 0
    for i in range(n):
        if type(x[i]) is not int or x[i] % 2 != 1:
            reject("entry %d is not an odd integer" % i)
            return
        if abs(x[i]) > u:
            reject("entry %d violates |x_i| <= u" % i)
            return
        total += x[i]

    if total != 2 * u:
        reject("the vector sum is not 2u")
        return

    correlations = []
    required_correlations = []
    for t in range(n):
        correlation = 0
        for i in range(n):
            correlation += x[i] * x[(i + t) % n]
        correlations.append(correlation)
        required_correlations.append(4 * u * u if t == 0 else 0)

    computed_side = True  # Whether this vector satisfies every requirement.
    for t in range(n):
        if correlations[t] != required_correlations[t]:
            computed_side = False

    # The claim says no such satisfying vector exists, so it requires
    # the satisfaction predicate to be False for this candidate.
    claim_side = False
    if computed_side != claim_side:
        print("REFUTATION CONFIRMED:", {
            "witness": {"u": u, "x": x},
            "sum": total,
            "correlations": correlations,
            "required_correlations": required_correlations,
            "computed_side": computed_side,
            "claim_side": claim_side,
        })
    else:
        reject("the vector fails the required periodic correlations")

if __name__ == "__main__":
    main()
    sys.exit(0)