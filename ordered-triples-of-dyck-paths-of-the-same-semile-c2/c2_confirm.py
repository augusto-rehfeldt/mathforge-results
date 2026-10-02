from itertools import product

WITNESS = {
    "n": 2, "a": 1, "b": 3, "H": 1, "A": 0, "B": 1,
    "L": [2], "U": [],
    "p12": 0, "v12": 1, "p23": 0, "v23": 0,
}


def validate(w):
    integer_keys = (
        "n", "a", "b", "H", "A", "B",
        "p12", "v12", "p23", "v23",
    )
    for key in integer_keys:
        if type(w[key]) is not int:
            return f"{key} is not an integer"

    n, a, b = w["n"], w["a"], w["b"]
    if n < 2:
        return "n must be at least 2"
    if not (1 <= a < b <= 2 * n - 1):
        return "a and b violate 1 <= a < b <= 2n-1"
    for key in ("H", "A", "B", "p12", "v12", "p23", "v23"):
        if w[key] < 0:
            return f"{key} must be nonnegative"

    allowed = set(range(1, 2 * n)) - {a, b}
    for key in ("L", "U"):
        values = w[key]
        if not isinstance(values, (list, tuple, set, frozenset)):
            return f"{key} does not represent a subset"
        if any(type(t) is not int for t in values):
            return f"{key} contains a noninteger"
        if len(set(values)) != len(values):
            return f"{key} contains duplicate elements"
        if not set(values) <= allowed:
            return f"{key} is not a subset of the permitted times"
    return None


def dyck_paths(n):
    paths = []
    for steps in product((-1, 1), repeat=2 * n):
        heights = [0]
        for step in steps:
            heights.append(heights[-1] + step)
        if heights[-1] == 0 and all(h >= 0 for h in heights):
            paths.append(tuple(heights))
    return paths


def peak(h, t):
    return h[t - 1] == h[t + 1] == h[t] - 1


def valley(h, t):
    return h[t - 1] == h[t + 1] == h[t] + 1


def matches(triple, requirements):
    h1, h2, h3 = triple
    n = requirements["n"]
    a, b = requirements["a"], requirements["b"]
    times = range(2 * n + 1)
    internal = range(1, 2 * n)

    if not all(h1[t] <= h2[t] <= h3[t] for t in times):
        return False

    contacts = {
        t for t in internal if h1[t] == h2[t] == h3[t]
    }
    if contacts != {a, b}:
        return False
    if any(h1[t] != requirements["H"] for t in contacts):
        return False

    # Comparing doubled areas avoids any rounding or floating-point arithmetic.
    if sum(h2[t] - h1[t] for t in times) != 2 * requirements["A"]:
        return False
    if sum(h3[t] - h2[t] for t in times) != 2 * requirements["B"]:
        return False

    L = {t for t in internal if h1[t] == h2[t] < h3[t]}
    U = {t for t in internal if h1[t] < h2[t] == h3[t]}
    if L != set(requirements["L"]) or U != set(requirements["U"]):
        return False

    for contact_set, lower, upper, pkey, vkey in (
        (L, h1, h2, "p12", "v12"),
        (U, h2, h3, "p23", "v23"),
    ):
        middle = [t for t in contact_set if a < t < b]
        p = sum(peak(lower, t) and peak(upper, t) for t in middle)
        v = sum(valley(lower, t) and valley(upper, t) for t in middle)
        if p != requirements[pkey] or v != requirements[vkey]:
            return False
    return True


def main():
    reason = validate(WITNESS)
    if reason is not None:
        print("REFUTATION REJECTED:", reason)
        return

    a, b = WITNESS["a"], WITNESS["b"]

    def r(t):
        return a + b - t if a < t < b else t

    transformed = dict(WITNESS)
    transformed["L"] = sorted(r(t) for t in WITNESS["L"])
    transformed["U"] = sorted(r(t) for t in WITNESS["U"])
    transformed["p12"] = WITNESS["v12"]
    transformed["v12"] = WITNESS["p12"]
    transformed["p23"] = WITNESS["v23"]
    transformed["v23"] = WITNESS["p23"]

    paths = dyck_paths(WITNESS["n"])
    first = second = 0
    for triple in product(paths, repeat=3):
        first += int(matches(triple, WITNESS))
        second += int(matches(triple, transformed))

    if first != second:
        print(
            "REFUTATION CONFIRMED:",
            WITNESS,
            "first cardinality =", first,
            "second cardinality =", second,
        )
    else:
        print(
            "REFUTATION REJECTED:",
            f"the cardinalities are equal: first={first}, second={second}",
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("REFUTATION REJECTED:", f"verification error: {exc}")