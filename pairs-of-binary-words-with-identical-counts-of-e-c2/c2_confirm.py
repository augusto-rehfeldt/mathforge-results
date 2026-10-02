import itertools
import math


def counts(word, k):
    """Count all subsequences of length k by strictly increasing indices."""
    result = {"".join(s): 0 for s in itertools.product("01", repeat=k)}
    for indices in itertools.combinations(range(len(word)), k):
        s = "".join(word[i] for i in indices)
        result[s] += 1
    return result


def reverse(word):
    return "".join(word[i] for i in range(len(word) - 1, -1, -1))


def encode(word):
    blocks = {"0": "001", "1": "011"}
    return "".join(blocks[letter] for letter in word)


def runs(word):
    if not word:
        return 0
    return 1 + sum(word[i] != word[i - 1] for i in range(1, len(word)))


def main():
    witness = {
        "n": 7,
        "u": "0110001",
        "v": "1000110",
        "U": "001011011001001001011001011011001001001011",
        "V": "011001001001011011001011001001001011011001",
    }
    n, u, v = witness["n"], witness["u"], witness["v"]

    reasons = []
    if type(n) is not int or n < 1:
        reasons.append("n is not an integer >= 1")
    for name, word in (("u", u), ("v", v)):
        if not isinstance(word, str) or any(c not in "01" for c in word):
            reasons.append(name + " is not a binary word")
        elif len(word) != n:
            reasons.append(name + " does not have length n")

    if reasons:
        print("REFUTATION REJECTED:", "; ".join(reasons))
        return

    cu = {k: counts(u, k) for k in range(1, 5)}
    cv = {k: counts(v, k) for k in range(1, 5)}
    for k in range(1, 4):
        for s in cu[k]:
            if cu[k][s] != cv[k][s]:
                reasons.append(
                    f"hypothesis C_{s}(u)=C_{s}(v) fails: "
                    f"{cu[k][s]} != {cv[k][s]}"
                )
    if reasons:
        print("REFUTATION REJECTED:", "; ".join(reasons))
        return

    U = encode(u + reverse(v))
    V = encode(v + reverse(u))
    for name, computed in (("U", U), ("V", V)):
        if witness[name] != computed:
            reasons.append(f"reported {name} differs from its defined value")
    if reasons:
        print("REFUTATION REJECTED:", "; ".join(reasons))
        return

    cU = {k: counts(U, k) for k in range(1, 5)}
    cV = {k: counts(V, k) for k in range(1, 5)}
    violations = []

    def check(relation, actual, claimed):
        if actual != claimed:
            violations.append({
                "relation": relation,
                "actual_side": actual,
                "claimed_side": claimed,
            })

    for name, word in (("U", U), ("V", V)):
        check(name + " length", len(word), 6 * n)
        for letter in "01":
            check(name + " " + letter + " count",
                  sum(c == letter for c in word), 3 * n)
        check(name + " runs", runs(word), 4 * n)

    for k in range(1, 4):
        for s in cU[k]:
            check(f"C_{s}(U)=C_{s}(V)", cU[k][s], cV[k][s])

    M = ((2, 1), (1, 2))
    delta_uv = {s: cu[4][s] - cv[4][s] for s in cu[4]}
    delta_UV = {t: cU[4][t] - cV[4][t] for t in cU[4]}
    for t in delta_UV:
        claimed = 0
        for s in delta_uv:
            product = 1
            for i in range(4):
                product *= M[int(t[i])][int(s[i])]
            claimed += delta_uv[s] * product
        claimed *= 2
        check(f"fourth-order formula for {t}", delta_UV[t], claimed)

    norm_uv = math.sqrt(sum(d * d for d in delta_uv.values()))
    norm_UV = math.sqrt(sum(d * d for d in delta_UV.values()))
    lower = 6 * norm_uv
    upper = 54 * norm_uv
    if not lower <= norm_UV:
        violations.append({
            "relation": "6||Delta(u,v)||_2 <= ||Delta(U,V)||_2",
            "left_side": lower,
            "right_side": norm_UV,
        })
    if not norm_UV <= upper:
        violations.append({
            "relation": "||Delta(U,V)||_2 <= 54||Delta(u,v)||_2",
            "left_side": norm_UV,
            "right_side": upper,
        })

    if violations:
        print("REFUTATION CONFIRMED:", {
            "witness": witness,
            "violations": violations,
        })
    else:
        print("REFUTATION REJECTED: all hypotheses and conclusions hold")


if __name__ == "__main__":
    main()