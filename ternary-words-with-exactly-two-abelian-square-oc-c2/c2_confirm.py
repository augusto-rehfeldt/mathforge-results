import json

def main():
    witness = {
        "word": "010201020",
        "n": 9,
        "intervals": [[1, 8], [2, 9]],
        "p": 4,
        "q": 4,
        "t": 7,
        "lhs_n+a+2p-b": 16,
        "rhs": 15,
        "failing_relation": "16 <= 15",
    }

    def reject(reason):
        print("REFUTATION REJECTED: " + reason)

    w = witness["word"]
    n = witness["n"]
    p = witness["p"]
    q = witness["q"]
    intervals = witness["intervals"]

    if type(n) is not int or n < 1:
        reject("n is not a positive integer")
        return
    if not isinstance(w, str) or len(w) != n or any(c not in "012" for c in w):
        reject("word is not in {0,1,2}^n")
        return
    if (not isinstance(intervals, list) or len(intervals) != 2
            or any(not isinstance(iv, list) or len(iv) != 2
                   or any(type(x) is not int for x in iv)
                   for iv in intervals)):
        reject("invalid reported intervals")
        return

    a, end_a = intervals[0]
    b, end_b = intervals[1]
    if any(type(x) is not int or x < 1 for x in (a, b, p, q)):
        reject("a, b, p, q are not positive integers")
        return
    if end_a != a + 2 * p - 1 or end_b != b + 2 * q - 1:
        reject("reported intervals do not match a, b, p, q")
        return
    if not (1 <= a < b <= a + 2 * p - 1 < b + 2 * q - 1 <= n):
        reject("required interval inequalities fail")
        return

    # Enumerate every possible interval, using 1-based positions.
    occurrences = []
    for i in range(1, n + 1):
        for h in range(1, (n - i + 1) // 2 + 1):
            equal = True
            for c in "012":
                first_count = 0
                second_count = 0
                for position in range(i, i + h):
                    if w[position - 1] == c:
                        first_count += 1
                for position in range(i + h, i + 2 * h):
                    if w[position - 1] == c:
                        second_count += 1
                if first_count != second_count:
                    equal = False
            if equal:
                occurrences.append([i, i + 2 * h - 1])

    if len(occurrences) != 2 or sorted(occurrences) != sorted(intervals):
        reject("all abelian-square occurrences are " + json.dumps(occurrences)
               + ", not exactly the two reported intervals")
        return

    t = a + 2 * p - b
    lhs = n + a + 2 * p - b
    rhs = 15
    if witness["t"] != t:
        reject("reported overlap length is incorrect")
        return
    if witness["lhs_n+a+2p-b"] != lhs or witness["rhs"] != rhs:
        reject("reported numerical sides are incorrect")
        return
    if lhs <= rhs:
        reject("the conclusion holds: {} <= {}".format(lhs, rhs))
        return

    print("REFUTATION CONFIRMED: "
          + json.dumps(witness, sort_keys=True)
          + "; left side = {}; right side = {}".format(lhs, rhs))

if __name__ == "__main__":
    main()