from fractions import Fraction

def main():
    m = 24
    a = [
        1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1,
        1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1,
        -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1,
        1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1
    ]

    def reject(reason):
        print("REFUTATION REJECTED:", reason)

    if type(m) is not int or m < 1:
        reject("m is not an integer >= 1")
        return

    N = 2 * m + 1
    if len(a) != N:
        reject("witness length is not 2m+1")
        return
    if any(type(x) is not int or x not in (-1, 1) for x in a):
        reject("a coordinate is not in {-1, 1}")
        return

    for j in range(m + 1):
        if a[m + j] != (-1) ** j * a[m - j]:
            reject("skew symmetry fails at j={}".format(j))
            return

    def energy(sequence):
        total = 0
        for r in range(1, 2 * m + 1):
            correlation = 0
            for j in range(0, 2 * m - r + 1):
                correlation += sequence[j] * sequence[j + r]
            total += correlation * correlation
        return total

    def transform(sequence, u, v, d):
        S = set(range(u, v + 1, d))
        result = []
        for i in range(N):
            if i in S or 2 * m - i in S:
                result.append(-sequence[i])
            else:
                result.append(sequence[i])
        return result

    lhs = energy(a)
    for d in (1, 2):
        for u in range(m + 1):
            for v in range(u, m + 1):
                if (v - u) % d != 0:
                    continue
                moved = transform(a, u, v, d)
                moved_energy = energy(moved)
                if lhs > moved_energy:
                    reject(
                        "local-minimum hypothesis fails for "
                        "(u,v,d)=({},{},{}): E(a)={} > E(Ta)={}".format(
                            u, v, d, lhs, moved_energy
                        )
                    )
                    return

    rhs = Fraction((2 * m + 1) ** 2, 8) + 2 * (2 * m + 1)
    if lhs <= rhs:
        reject("conclusion holds: E(a)={} <= {}".format(lhs, rhs))
        return

    print(
        "REFUTATION CONFIRMED:",
        {"m": m, "a": a},
        "E(a)={}; (2m+1)^2/8 + 2(2m+1)={}".format(lhs, rhs)
    )

if __name__ == "__main__":
    main()