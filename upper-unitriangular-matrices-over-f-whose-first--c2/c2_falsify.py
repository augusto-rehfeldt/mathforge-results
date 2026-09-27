#!/usr/bin/env python3

def make_matrix(n, mask):
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        a[i][i] = 1
        if i + 1 < n:
            a[i][i + 1] = 1
        if i + 2 < n:
            a[i][i + 2] = (mask >> i) & 1
    return a


def fast_inverse_rows(n, mask):
    rows = [0] * n
    for i in range(n - 1, -1, -1):
        row = 1 << i
        if i + 1 < n:
            row ^= rows[i + 1]
        if i + 2 < n and (mask >> i) & 1:
            row ^= rows[i + 2]
        rows[i] = row
    return rows


def brute_inverse_rows(a):
    """Invert [A | I] by Gauss-Jordan elimination over F_2."""
    n = len(a)
    rows = [
        sum(a[i][j] << j for j in range(n)) | (1 << (n + i))
        for i in range(n)
    ]
    for pivot in range(n):
        if not (rows[pivot] & (1 << pivot)):
            raise ValueError("Missing pivot")
        for r in range(n):
            if r != pivot and (rows[r] & (1 << pivot)):
                rows[r] ^= rows[pivot]
    return [(row >> n) & ((1 << n) - 1) for row in rows]


def inverse_weight(rows):
    return sum(row.bit_count() - 1 for row in rows)


def claimed_equality_condition(a):
    n = len(a)
    second = [a[i][i + 2] for i in range(n - 2)]
    return sum(second) == 1 and (second[0] == 1 or second[-1] == 1)


def sanity_checks():
    for n in (6, 7):
        if inverse_weight(brute_inverse_rows(make_matrix(n, 0))) != n * (n - 1) // 2:
            return False
        expected = n * (n - 1) // 2 - (n - 2)
        for mask in (1, 1 << (n - 3)):
            if inverse_weight(brute_inverse_rows(make_matrix(n, mask))) != expected:
                return False
    print("SANITY: known zero-mask and endpoint weights passed")

    for mask in range(1 << (6 - 2)):
        if fast_inverse_rows(6, mask) != brute_inverse_rows(make_matrix(6, mask)):
            return False
    print("SANITY: fast inverses match Gauss-Jordan for all n=6 masks")
    return True


def verified_failure(n, mask):
    """Recompute the inverse and both claimed comparisons independently."""
    a = make_matrix(n, mask)
    weight = inverse_weight(brute_inverse_rows(a))
    bound = n * (n - 1) // 2 - (n - 2)
    claimed_equal = claimed_equality_condition(a)

    if weight > bound:
        return f"inverse weight={weight}, claimed upper bound={bound}"
    if (weight == bound) != claimed_equal:
        return (
            f"inverse weight equals bound={weight == bound}, "
            f"claimed equality condition={claimed_equal} "
            f"(weight={weight}, bound={bound})"
        )
    return None


def main():
    if not sanity_checks():
        print("SANITY FAILED")
        return

    tested = 0
    for n in range(6, 15):
        bound = n * (n - 1) // 2 - (n - 2)
        for mask in range(1, 1 << (n - 2)):  # Exclude the zero second superdiagonal.
            tested += 1
            weight = inverse_weight(fast_inverse_rows(n, mask))
            endpoint_single = mask in (1, 1 << (n - 3))
            if weight > bound or ((weight == bound) != endpoint_single):
                failure = verified_failure(n, mask)
                if failure is not None:
                    bits = [(mask >> i) & 1 for i in range(n - 2)]
                    print(
                        f"COUNTEREXAMPLE: n={n}, second superdiagonal={bits}; "
                        f"{failure}"
                    )
                    return
                print("SANITY FAILED")
                return

    print(
        f"NO COUNTEREXAMPLE n=6..14, "
        f"mask=1..2^(n-2)-1 for each n, cases tested={tested}"
    )


if __name__ == "__main__":
    main()