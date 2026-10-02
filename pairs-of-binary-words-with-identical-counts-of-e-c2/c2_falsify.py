import itertools
import time
import sys

LIMIT_SECONDS = 225
MAX_N = 12

PATTERNS = [
    "".join(p)
    for k in range(1, 5)
    for p in itertools.product("01", repeat=k)
]
INDEX = {s: i for i, s in enumerate(PATTERNS)}
FOUR = PATTERNS[14:]
M = ((2, 1), (1, 2))

# Descending lengths prevent an input position from being used twice.
UPDATES = {
    b: [
        (INDEX[s], INDEX[s[:-1]] if len(s) > 1 else None)
        for s in reversed(PATTERNS)
        if s[-1] == b
    ]
    for b in "01"
}


def counts(w):
    result = [0] * 30
    for b in w:
        for target, source in UPDATES[b]:
            result[target] += 1 if source is None else result[source]
    return result


def brute_counts(w):
    result = [0] * 30
    for k in range(1, 5):
        for positions in itertools.combinations(range(len(w)), k):
            s = "".join(w[i] for i in positions)
            result[INDEX[s]] += 1
    return result


def encode(w):
    return "".join("001" if b == "0" else "011" for b in w)


def runs(w):
    return sum(i == 0 or w[i] != w[i - 1] for i in range(len(w)))


# Compute the coefficients directly from the formula in the claim.
COEFFICIENTS = []
for t in FOUR:
    row = []
    for s in FOUR:
        product = 1
        for i in range(4):
            product *= M[int(t[i])][int(s[i])]
        row.append(2 * product)
    COEFFICIENTS.append(row)


def failure(n, u, v, U, V, cu, cv, cU, cV):
    for name, w in (("U", U), ("V", V)):
        properties = [
            ("length", len(w), 6 * n),
            ("zero count", w.count("0"), 3 * n),
            ("one count", w.count("1"), 3 * n),
            ("run count", runs(w), 4 * n),
        ]
        for prop, actual, claimed in properties:
            if actual != claimed:
                return (name + " " + prop, actual, claimed)

    for i, s in enumerate(PATTERNS[:14]):
        if cU[i] != cV[i]:
            return ("C_" + s + "(U) = C_" + s + "(V)", cU[i], cV[i])

    delta = [cu[i] - cv[i] for i in range(14, 30)]
    output_delta = [cU[i] - cV[i] for i in range(14, 30)]
    for j, t in enumerate(FOUR):
        claimed = sum(COEFFICIENTS[j][i] * delta[i] for i in range(16))
        if output_delta[j] != claimed:
            return ("fourth-order identity for " + t, output_delta[j], claimed)

    original_squared = sum(x * x for x in delta)
    output_squared = sum(x * x for x in output_delta)
    if output_squared < 36 * original_squared:
        return ("squared lower bound: actual >= claimed",
                output_squared, 36 * original_squared)
    if output_squared > 2916 * original_squared:
        return ("squared upper bound: actual <= claimed",
                output_squared, 2916 * original_squared)
    return None


def sanity_fail(message):
    print("SANITY FAILED:", message)
    sys.exit(0)


known = {
    "0": 2, "1": 1, "00": 1, "01": 2, "10": 0, "11": 0,
    "000": 0, "001": 1, "010": 0, "011": 0,
    "100": 0, "101": 0, "110": 0, "111": 0,
}
small = counts("001")
if any(small[INDEX[s]] != value for s, value in known.items()):
    sanity_fail("known subsequence counts for 001")
print("SANITY 1 PASSED: known counts for 001")

cross_checks = 0
for length in range(6):
    for letters in itertools.product("01", repeat=length):
        w = "".join(letters)
        if counts(w) != brute_counts(w):
            sanity_fail("DP versus explicit index combinations for " + repr(w))
        cross_checks += 1
print("SANITY 2 PASSED: explicit combinations for all", cross_checks,
      "binary words of lengths 0 through 5")

if encode("01") != "001011" or runs("001011") != 4:
    sanity_fail("encoding and runs")
print("SANITY 3 PASSED: E(01)=001011, with four runs")

start = time.monotonic()
total_cases = 0
completed_n = 0
per_length = []
partial = None
stop = False

for n in range(1, MAX_N + 1):
    groups = {}
    enumeration_complete = True
    words_enumerated = 0
    for letters in itertools.product("01", repeat=n):
        if time.monotonic() - start >= LIMIT_SECONDS:
            enumeration_complete = False
            break
        w = "".join(letters)
        c = counts(w)
        groups.setdefault(tuple(c[:14]), []).append((w, c))
        words_enumerated += 1

    if not enumeration_complete:
        partial = (
            f"n={n}: word enumeration stopped after {words_enumerated}/{2**n} "
            "words; no pairs tested at this length"
        )
        break

    cases_at_n = 0
    for group in groups.values():
        for a in range(len(group)):
            for b in range(a + 1, len(group)):
                if time.monotonic() - start >= LIMIT_SECONDS:
                    stop = True
                    break

                u, cu = group[a]
                v, cv = group[b]
                # Explicitly enforce every hypothesis.
                if len(u) != n or len(v) != n or cu[:14] != cv[:14]:
                    sanity_fail("invalid search pair")

                U = encode(u + v[::-1])
                V = encode(v + u[::-1])
                cU, cV = counts(U), counts(V)
                problem = failure(n, u, v, U, V, cu, cv, cU, cV)
                total_cases += 1
                cases_at_n += 1

                if problem is not None:
                    # Independently reconstruct the words and enumerate all
                    # increasing index tuples, rather than using the DP.
                    U2 = "".join(
                        ("0", "0", "1") if bit == "0" else ("0", "1", "1")
                        for bit in []
                    )  # Empty initialization; literal reconstruction below.
                    U2 = ""
                    V2 = ""
                    for bit in list(u) + list(reversed(v)):
                        U2 += "001" if bit == "0" else "011"
                    for bit in list(v) + list(reversed(u)):
                        V2 += "001" if bit == "0" else "011"

                    bu, bv = brute_counts(u), brute_counts(v)
                    bU, bV = brute_counts(U2), brute_counts(V2)
                    if bu[:14] != bv[:14]:
                        sanity_fail("brute-force hypothesis verification")
                    verified = failure(n, u, v, U2, V2, bu, bv, bU, bV)
                    if verified != problem:
                        sanity_fail("candidate failed independent verification")
                    print("COUNTEREXAMPLE:", {
                        "n": n, "u": u, "v": v, "U": U2, "V": V2,
                        "relation": verified[0],
                        "actual_side": verified[1],
                        "claimed_side": verified[2],
                    })
                    sys.exit(0)
            if stop:
                break
        if stop:
            break

    if stop:
        partial = (
            f"n={n}: all {2**n} words grouped; first {cases_at_n} eligible "
            "unordered pairs tested, in lexicographic word-enumeration / "
            "group-insertion order"
        )
        break

    completed_n = n
    per_length.append((n, cases_at_n))

details = (
    f"complete lengths 1..{completed_n}; "
    f"cases tested={total_cases}; per-length cases={per_length}"
)
if partial is not None:
    details += "; partial slice: " + partial
print("NO COUNTEREXAMPLE", details)
sys.exit(0)