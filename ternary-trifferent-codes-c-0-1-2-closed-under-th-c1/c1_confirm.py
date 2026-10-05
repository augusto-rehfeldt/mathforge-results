#!/usr/bin/env python3
import itertools

WITNESS = {
    "m": 2,
    "witness": "exhaustive UNSAT, independently rechecked",
    "brute_force_side": "maximum cardinality < 12",
    "claimed_side": "exists cardinality >= 12",
}


def shift(d):
    return tuple(((a + 1) % 3, b) for a, b in d)


def expansion(d):
    return tuple(
        (a + k * b) % 3
        for a, b in d
        for k in range(3)
    )


def literal_triple_condition(triple):
    for column in zip(*triple):
        a = [pair[0] for pair in column]
        b = [pair[1] for pair in column]

        # Condition (i).
        if b[0] == b[1] == b[2] and len(set(a)) == 3:
            return True

        # Condition (ii): the remaining b value must be different.
        for p, q, r in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            if b[p] == b[q] != b[r] and a[p] != a[q]:
                return True
    return False


def trifferent_triple(words):
    return any(len(set(column)) == 3 for column in zip(*words))


def reject(reason):
    print("REFUTATION REJECTED:", reason)


def main():
    m = WITNESS["m"]
    if type(m) is not int or m < 1:
        reject("the reported m is not an integer at least 1")
        return

    # This witness claims nonexistence at a fixed m, not a bad example D.
    # Audit that claim by exhaustively evaluating every invariant D at this m.
    alphabet = tuple(itertools.product(range(3), (0, 1)))
    universe = tuple(itertools.product(alphabet, repeat=m))
    universe_set = set(universe)

    orbits = []
    covered = set()
    for d in universe:
        if d in covered:
            continue
        orbit = frozenset((d, shift(d), shift(shift(d))))
        if (
            len(orbit) != 3
            or not orbit <= universe_set
            or {shift(x) for x in orbit} != set(orbit)
            or orbit & covered
        ):
            reject("failed to construct the shift-orbit partition")
            return
        orbits.append(tuple(sorted(orbit)))
        covered.update(orbit)

    if covered != universe_set:
        reject("orbit partition does not cover the stated universe")
        return

    # Independently verify the expansion interpretation, without using it
    # to decide the claim's literal triple condition.
    expanded = {d: expansion(d) for d in universe}
    if len(set(expanded.values())) != len(universe):
        reject("block expansion is not injective")
        return
    for triple in itertools.combinations(universe, 3):
        if literal_triple_condition(triple) != trifferent_triple(
            tuple(expanded[d] for d in triple)
        ):
            reject("literal and block definitions disagree")
            return

    threshold = 3 * (2 ** m)  # Exactly the bound in the statement.
    maximum = 0
    existence = False

    # Every invariant subset is exactly a union of full shift orbits.
    # Enumerate all such subsets; do not rely on the searcher's constraints.
    for mask in range(1 << len(orbits)):
        D = tuple(
            d
            for i, orbit in enumerate(orbits)
            if mask & (1 << i)
            for d in orbit
        )
        D_set = set(D)
        if len(D_set) != len(D) or not D_set <= universe_set:
            reject("enumerated candidate is not a subset of the universe")
            return
        if {shift(d) for d in D_set} != D_set:
            reject("enumerated candidate is not invariant")
            return

        valid = all(
            literal_triple_condition(triple)
            for triple in itertools.combinations(D, 3)
        )
        if valid:
            maximum = max(maximum, len(D))
            if len(D) >= threshold:
                existence = True

    if existence:
        reject(
            f"at m={m}, the literal claimed existence holds; "
            f"maximum cardinality={maximum}, required cardinality>={threshold}"
        )
        return

    print(
        "REFUTATION CONFIRMED:",
        repr(WITNESS),
        f"; brute_force_side: maximum cardinality={maximum} < {threshold}",
        f"; claimed_side: exists invariant D with cardinality >= {threshold} "
        "and the stated triple property; literal truth value=False",
    )


if __name__ == "__main__":
    main()