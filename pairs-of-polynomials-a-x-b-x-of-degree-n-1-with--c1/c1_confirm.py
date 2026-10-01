def main():
    witness = {
        "n": 5,
        "A": (1, -1, 1, 1, 1),
        "B": (1, -1, -1, 1, 1),
        "d": 2,
        "e": 4,
        "c": -2,
        "h": 1,
    }

    def reject(reason):
        print("REFUTATION REJECTED:", reason)

    n, d, e, c = (witness[k] for k in ("n", "d", "e", "c"))
    A, B = witness["A"], witness["B"]

    if not all(type(v) is int for v in (n, d, e, c)):
        reject("n, d, e, and c must be integers")
        return
    if not (n >= 3 and 1 <= d < e < n and c != 0):
        reject("integer bounds or nonzero-c hypothesis fails")
        return
    if len(A) != n or len(B) != n:
        reject("coefficient lists must each have length n")
        return
    if not all(type(v) is int and v in (-1, 1) for v in A + B):
        reject("every coefficient must be an integer in {-1, 1}")
        return

    # Multiply the Laurent polynomials literally:
    # (sum_i a_i x^i)(sum_j a_j x^(-j)), and likewise for B.
    lhs = {k: 0 for k in range(-(n - 1), n)}
    for coefficients in (A, B):
        for i in range(n):
            for j in range(n):
                lhs[i - j] += coefficients[i] * coefficients[j]

    # Construct exactly 2n + c(x^d + x^(-d) - x^e - x^(-e)).
    rhs = {k: 0 for k in range(-(n - 1), n)}
    for exponent, coefficient in (
        (0, 2 * n), (d, c), (-d, c), (e, -c), (-e, -c)
    ):
        rhs[exponent] += coefficient

    if lhs != rhs:
        reject({"reason": "Laurent-polynomial identity fails",
                "left_side": lhs, "right_side": rhs})
        return

    h = sum(1 for i in range(n) if A[i] != B[i])
    if witness["h"] != h:
        reject({"reason": "reported Hamming distance is incorrect",
                "reported": witness["h"], "computed": h})
        return

    # Integer-scaled comparisons express n/2 exactly, without rounding.
    n_even = n % 2 == 0
    c_even = c % 2 == 0
    if c % 4 == 0:
        additional_conclusion = 2 * h == n
        claimed_side = {"n_even": True, "c_even": True, "2*h": n}
    else:
        additional_conclusion = (
            d + e == n and 2 * h in (n - 4, n, n + 4)
        )
        claimed_side = {
            "n_even": True,
            "c_even": True,
            "d+e": n,
            "2*h_in": (n - 4, n, n + 4),
        }

    actual_side = {
        "n_even": n_even,
        "c_even": c_even,
        "h": h,
        "2*h": 2 * h,
        "d+e": d + e,
    }

    if n_even and c_even and additional_conclusion:
        reject("all hypotheses and the entire conclusion hold")
        return

    print("REFUTATION CONFIRMED:", {
        "witness": witness,
        "identity_left_side": lhs,
        "identity_right_side": rhs,
        "conclusion_actual_side": actual_side,
        "conclusion_claimed_side": claimed_side,
    })


if __name__ == "__main__":
    main()