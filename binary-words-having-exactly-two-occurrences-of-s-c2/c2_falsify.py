import itertools
import json
import sys


def squares_plain(word):
    """Literal definition, using 1-based occurrence positions."""
    out = []
    n = len(word)
    for i in range(n):
        for r in range(1, (n - i) // 2 + 1):
            if all(word[i + j] == word[i + r + j] for j in range(r)):
                out.append((i + 1, r))
    return out


def squares_fast(v, n):
    """Bit 0 is position 1. Return occurrences, or None if more than two."""
    out = []
    for r in range(1, n // 2 + 1):
        equal = ~(v ^ (v >> r)) & ((1 << (n - r)) - 1)
        length = 1
        while length < r:
            step = min(length, r - length)
            equal &= equal >> step
            length += step
        starts = equal & ((1 << (n - 2 * r + 1)) - 1)
        if len(out) + starts.bit_count() > 2:
            return None
        while starts:
            low = starts & -starts
            out.append((low.bit_length(), r))
            starts ^= low
    return sorted(out)


def word_of(v, n):
    return "".join(str((v >> i) & 1) for i in range(n))


def eligible(occ):
    if occ is None or len(occ) != 2:
        return False
    (i, p), (j, r) = sorted(occ)
    a, b = i + 2 * p - 1, j + 2 * r - 1
    return i < j <= a < b


def verify_plain(word, failure):
    """Recompute hypotheses and both sides without bit operations."""
    occ = sorted(squares_plain(word))
    if not eligible(occ):
        return None
    j, r = occ[1]
    t = len(word) - (j + 2 * r - 1)
    kind = failure["relation"]
    if kind == "r belongs to {1,2}":
        actual, claimed = r in (1, 2), True
    elif kind == "r=1 implies 0<=t<=2":
        if r != 1:
            return None
        actual, claimed = 0 <= t <= 2, True
    elif kind == "r=2 implies t=0":
        if r != 2:
            return None
        actual, claimed = t, 0
    else:
        k = failure["k"]
        actual = sum(
            len(squares_plain(word + "".join(bits))) == 2
            for bits in itertools.product("01", repeat=k)
        )
        if r == 1:
            claimed = 1 if k <= 2 - t else 0
        elif r == 2:
            claimed = 1 if k == 0 else 0
        else:
            return None
    if actual == claimed:
        return None
    return {
        "w": word,
        "n": len(word),
        "occurrences": occ,
        "r": r,
        "t": t,
        "relation": kind,
        **({"k": failure["k"]} if "k" in failure else {}),
        "brute_force_side": actual,
        "claimed_side": claimed,
    }


def report(word, failure):
    checked = verify_plain(word, failure)
    if checked is None:
        print("SANITY FAILED: proposed witness failed plain recomputation")
        sys.exit(0)
    print("COUNTEREXAMPLE:", json.dumps(checked, sort_keys=True))
    sys.exit(0)


def sanity():
    known = {
        "": [],
        "0": [],
        "00": [(1, 1)],
        "000": [(1, 1), (2, 1)],
        "0000": [(1, 1), (1, 2), (2, 1), (3, 1)],
        "01010": [(1, 2), (2, 2)],
    }
    for word, expected in known.items():
        if sorted(squares_plain(word)) != expected:
            print("SANITY FAILED: literal routine on", repr(word))
            sys.exit(0)
    print("SANITY 1 PASSED: six independently specified small examples")

    tested = 0
    for n in range(10):
        for v in range(1 << n):
            plain = sorted(squares_plain(word_of(v, n)))
            expected = plain if len(plain) <= 2 else None
            if squares_fast(v, n) != expected:
                print("SANITY FAILED: bit routine on", word_of(v, n))
                sys.exit(0)
            tested += 1
    print("SANITY 2 PASSED: bit routine cross-checked against literal routine "
          "on all %d words of lengths 0..9" % tested)


def main():
    sanity()
    scanned = retained = continuation_cases = relations = 0

    for n in range(1, 21):
        for v in range(1 << n):
            scanned += 1
            occ = squares_fast(v, n)
            if not eligible(occ):
                continue
            retained += 1
            j, r = occ[1]
            t = n - (j + 2 * r - 1)

            relations += 1
            if r not in (1, 2):
                report(word_of(v, n), {"relation": "r belongs to {1,2}"})

            relations += 1
            if r == 1 and not (0 <= t <= 2):
                report(word_of(v, n),
                       {"relation": "r=1 implies 0<=t<=2"})
            if r == 2 and t != 0:
                report(word_of(v, n), {"relation": "r=2 implies t=0"})

            for k in range(7):
                actual = 0
                for x in range(1 << k):
                    continuation_cases += 1
                    extended = squares_fast(v | (x << n), n + k)
                    if extended is not None and len(extended) == 2:
                        actual += 1

                # Literal counts asserted by the claim, including k=0.
                if r == 1:
                    claimed = 1 if k <= 2 - t else 0
                else:
                    claimed = 1 if k == 0 else 0
                relations += 1
                if actual != claimed:
                    report(word_of(v, n),
                           {"relation": "continuation count", "k": k})

    print(
        "NO COUNTEREXAMPLE "
        "ranges: all binary w of lengths 1..20; "
        "for every hypothesis-satisfying w, all binary x of lengths 0..6; "
        "words_scanned=%d; hypothesis_cases=%d; "
        "continuation_cases=%d; relations_checked=%d"
        % (scanned, retained, continuation_cases, relations)
    )


if __name__ == "__main__":
    main()