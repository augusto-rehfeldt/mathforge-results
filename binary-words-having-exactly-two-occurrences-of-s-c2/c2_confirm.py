import itertools
import json

witness = {
    "brute_force_side": 0,
    "claimed_side": 1,
    "k": 2,
    "n": 5,
    "occurrences": [[1, 2], [4, 1]],
    "r": 1,
    "relation": "continuation count",
    "t": 0,
    "w": "10100",
}


def squares(word):
    """Return every square occurrence (1-based start, root length)."""
    result = []
    n = len(word)
    for i in range(1, n + 1):
        for r in range(1, (n - i + 1) // 2 + 1):
            if all(word[i - 1 + j] == word[i - 1 + r + j]
                   for j in range(r)):
                result.append((i, r))
    return result


def reject(reason):
    print("REFUTATION REJECTED: " + reason)


def main():
    w = witness["w"]
    n = witness["n"]
    k = witness["k"]

    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        reject("n is not an integer at least 1")
        return
    if not isinstance(w, str) or len(w) != n or any(c not in "01" for c in w):
        reject("w is not a binary word of length n")
        return
    if not isinstance(k, int) or isinstance(k, bool) or k < 0:
        reject("k is not an integer at least 0")
        return

    occurrences = squares(w)
    if len(occurrences) != 2:
        reject("w does not have exactly two square occurrences")
        return

    intervals = [(i, i + 2 * r - 1) for i, r in occurrences]
    (a, b1), (c, d) = intervals
    if max(a, c) > min(b1, d):
        reject("the square intervals do not overlap")
        return
    if (a <= c and d <= b1) or (c <= a and b1 <= d):
        reject("one square interval contains the other")
        return

    later_i, r = max(occurrences, key=lambda occurrence: occurrence[0])
    b = later_i + 2 * r - 1
    t = n - b

    if [list(o) for o in occurrences] != witness["occurrences"]:
        reject("reported occurrences disagree with literal enumeration")
        return
    if r != witness["r"] or t != witness["t"]:
        reject("reported r or t disagrees with the definitions")
        return
    if witness["relation"] != "continuation count":
        reject("unsupported reported comparison")
        return

    valid_extensions = []
    for bits in itertools.product("01", repeat=k):
        x = "".join(bits)
        if len(squares(w + x)) == 2:
            valid_extensions.append(x)
    actual = len(valid_extensions)

    structural_conclusion = (
        r in (1, 2)
        and ((r == 1 and 0 <= t <= 2) or (r == 2 and t == 0))
    )
    if r == 1:
        claimed = 1 if k <= 2 - t else 0
    elif r == 2:
        claimed = 1 if k == 0 else 0
    else:
        claimed = None

    if not structural_conclusion or actual != claimed:
        report = dict(witness)
        report["computed_occurrences"] = [list(o) for o in occurrences]
        report["b"] = b
        report["computed_r"] = r
        report["computed_t"] = t
        report["brute_force_side"] = actual
        report["claimed_side"] = claimed
        report["valid_extensions"] = valid_extensions
        report["structural_conclusion"] = structural_conclusion
        print("REFUTATION CONFIRMED: " + json.dumps(report, sort_keys=True))
    else:
        reject("the hypotheses hold, but the computed conclusion is satisfied")


if __name__ == "__main__":
    main()