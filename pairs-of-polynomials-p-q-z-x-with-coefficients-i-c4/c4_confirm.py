from itertools import product

A = {0, 1, 3}
B = {0, 1, 4}


def representations(S, R):
    result = {}
    for s, r in product(sorted(S), sorted(R)):
        result.setdefault(s + r, []).append((s, r))
    return result


def verify_all_translations(U, V, R, c_U, c_V):
    """Check the universal T clause using its exact translation structure."""
    S = U | V
    M = max(S) + max(R)
    low = representations(U, R)
    high = representations(V, R)

    # For every integer T > M, all translated elements and sums lie
    # strictly above all untranslated ones. Thus no cross-collision
    # can occur, and within each block translation preserves coefficients.
    if not (
        max(U) <= M
        and min(V) >= 0
        and max(low) <= M
        and min(high) >= 0
        and c_U <= M
        and c_V >= 0
    ):
        return False

    if {s for s, pairs in low.items() if len(pairs) == 2} != {c_U}:
        return False
    if {s for s, pairs in high.items() if len(pairs) == 2} != {c_V}:
        return False
    if any(len(pairs) > 2 for pairs in list(low.values()) + list(high.values())):
        return False

    # Directly check the boundary integer. The bounds above certify that
    # the same disjoint-block calculation holds for every larger integer.
    T = M + 1
    A_T = U | {v + T for v in V}
    translated = representations(A_T, R)
    doubles = {s for s, pairs in translated.items() if len(pairs) == 2}
    return (
        len(A_T) == len(S)
        and len(R) == len(R)
        and doubles == {c_U, c_V + T}
        and all(len(pairs) <= 2 for pairs in translated.values())
        and abs((c_V + T) - c_U) == T + c_V - c_U
    )


def splitting_partitions(S, R):
    answers = []
    elements = sorted(S)
    for mask in range(1 << len(elements)):
        U = {elements[i] for i in range(len(elements)) if mask & (1 << i)}
        V = S - U
        if not U or not V or 0 not in U:
            continue
        ru = representations(U, R)
        rv = representations(V, R)
        if set(ru) & set(rv):
            continue
        du = [s for s, pairs in ru.items() if len(pairs) == 2]
        dv = [s for s, pairs in rv.items() if len(pairs) == 2]
        if len(du) == len(dv) == 1:
            answers.append((U, V, du[0], dv[0]))
    return answers


def alternative_I(A, B):
    for S, R in ((A, B), (B, A)):
        for U, V, c_U, c_V in splitting_partitions(S, R):
            if verify_all_translations(U, V, R, c_U, c_V):
                return True
    return False


def alternative_II(A, B):
    # The final no-partition clause quantifies over both orientations.
    if splitting_partitions(A, B) or splitting_partitions(B, A):
        return False

    for S, R in ((A, B), (B, A)):
        reps = representations(S, R)
        doubled = sorted(s for s, pairs in reps.items() if len(pairs) == 2)
        participating = {
            pair
            for s in doubled
            for pair in reps[s]
        }
        for u in sorted(S):
            for v in sorted(R):
                # Any eligible positive d is at most max(S).
                for d in range(1, max(S) + 1):
                    if not {u, u + d} <= S:
                        continue
                    if not {v, v + d, v + 2 * d} <= R:
                        continue
                    required = {
                        (u, v + d),
                        (u + d, v),
                        (u, v + 2 * d),
                        (u + d, v + d),
                    }
                    if (
                        participating == required
                        and len(doubled) == 2
                        and doubled[1] - doubled[0] == d
                    ):
                        return True
    return False


def main():
    witness = {"A": tuple(sorted(A)), "B": tuple(sorted(B))}
    reasons = []

    for name, S in (("A", A), ("B", B)):
        if not isinstance(S, set):
            reasons.append(name + " is not a set")
        if any(type(x) is not int or x < 0 for x in S):
            reasons.append(name + " contains a nonnegative-integer violation")
        if 0 not in S:
            reasons.append(name + " does not contain 0")

    if reasons:
        print("REFUTATION REJECTED:", "; ".join(reasons))
        return

    reps = representations(A, B)
    counts = {s: len(pairs) for s, pairs in reps.items()}
    # Every unlisted nonnegative exponent has coefficient zero.
    if any(n > 2 for n in counts.values()):
        reasons.append("a representation count exceeds 2")
    if sum(n == 2 for n in counts.values()) != 2:
        reasons.append("there are not exactly two doubled coefficients")

    if reasons:
        print("REFUTATION REJECTED:", "; ".join(reasons))
        return

    actual = (alternative_I(A, B), alternative_II(A, B))
    conclusion = sum(actual) == 1
    if not conclusion:
        print(
            "REFUTATION CONFIRMED:",
            witness,
            {
                "representation_counts": sorted(counts.items()),
                "actual_side": {"I": actual[0], "II": actual[1],
                                "exactly_one": conclusion},
                "claimed_side": {"exactly_one": True},
            },
        )
    else:
        print("REFUTATION REJECTED:", "the conclusion holds at", witness)


if __name__ == "__main__":
    main()