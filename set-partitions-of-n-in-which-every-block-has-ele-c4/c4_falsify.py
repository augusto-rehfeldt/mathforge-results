import math
import time
from functools import lru_cache

START = time.monotonic()
DEADLINE = START + 225


class TimeLimit(Exception):
    pass


def engine(modulus=None, timed=False):
    calls = 0

    @lru_cache(None)
    def blocks(z, o, t, a, b, ar, br):
        nonlocal calls
        calls += 1
        if timed and calls % 16 == 0 and time.monotonic() > DEADLINE:
            raise TimeLimit
        counts = (z, o, t)
        size = z + o + t + a + b
        if not size:
            return (1,)
        # Anchor the first available ordinary residue class, otherwise a special.
        anchor = next((i for i, c in enumerate(counts) if c), 3 if a else 4)
        available = list(counts)
        aa, bb = a, b
        base = [0, 0, 0]
        ba = bb0 = 0
        if anchor < 3:
            available[anchor] -= 1
            base[anchor] = 1
        elif anchor == 3:
            aa -= 1
            ba = 1
        else:
            bb -= 1
            bb0 = 1
        out = [0] * (size + 1)
        choices = [
            [math.comb(c, i) for i in range(c + 1)]
            for c in available
        ]
        for i in range(available[0] + 1):
            for j in range(available[1] + 1):
                for k in range(available[2] + 1):
                    mult = choices[0][i] * choices[1][j] * choices[2][k]
                    used = (i + base[0], j + base[1], k + base[2])
                    for u in range(aa + 1):
                        for v in range(bb + 1):
                            ua, vb = u + ba, v + bb0
                            if (used[1] + 2 * used[2] + ar * ua + br * vb) % 3:
                                continue
                            q = blocks(z - used[0], o - used[1], t - used[2],
                                       a - ua, b - vb, ar, br)
                            for degree, value in enumerate(q):
                                out[degree + 1] += mult * value
        if modulus:
            out = [v % modulus for v in out]
        return tuple(out)

    def polynomial(z, o, t, a=0, b=0, ar=0, br=0):
        # Mark selected ordinary zero-residue singletons with x(y-1).
        out = {}
        for j in range(z + 1):
            q = blocks(z - j, o, t, a, b, ar, br)
            factor = math.comb(z, j)
            for k, value in enumerate(q):
                if not value:
                    continue
                for s in range(j + 1):
                    key = (k + j, s)
                    out[key] = out.get(key, 0) + (
                        factor * value * math.comb(j, s) * (-1) ** (j - s)
                    )
        if modulus:
            out = {key: v % modulus for key, v in out.items()}
        return {key: v for key, v in out.items() if v}

    return polynomial


def brute_polynomial(weights, ordinary):
    # Direct restricted-growth enumeration of labeled set partitions.
    out = {}
    sums, members = [], []

    def visit(i):
        if i == len(weights):
            if all(s % 3 == 0 for s in sums):
                singletons = sum(
                    len(block) == 1 and ordinary[block[0]] for block in members
                )
                key = (len(sums), singletons)
                out[key] = out.get(key, 0) + 1
            return
        for j in range(len(sums)):
            sums[j] += weights[i]
            members[j].append(i)
            visit(i + 1)
            members[j].pop()
            sums[j] -= weights[i]
        sums.append(weights[i])
        members.append([i])
        visit(i + 1)
        members.pop()
        sums.pop()

    visit(0)
    return out


def verify_coefficient(weights, ordinary, target):
    # Independent labeled-mask block deletion, counting only the requested term.
    n = len(weights)
    residues = [w % 3 for w in weights]

    @lru_cache(None)
    def rec(mask, k, s):
        size = mask.bit_count()
        if not mask:
            return int(k == 0 and s == 0)
        if k <= 0 or s < 0 or s > k or k > size:
            return 0
        if size < s + 2 * (k - s):
            # Special singleton blocks are possible only at residue zero.
            specials = sum(
                not ordinary[i] and residues[i] == 0
                for i in range(n) if mask >> i & 1
            )
            if size < s + 2 * (k - s) - specials:
                return 0
        anchor = mask & -mask
        rest = mask ^ anchor
        ai = anchor.bit_length() - 1
        total = 0
        sub = rest
        while True:
            block = sub | anchor
            count = block.bit_count()
            remaining = size - count
            single = int(count == 1 and ordinary[ai])
            if remaining >= k - 1 and s >= single:
                residue = residues[ai]
                bits = sub
                while bits:
                    bit = bits & -bits
                    residue += residues[bit.bit_length() - 1]
                    bits ^= bit
                if residue % 3 == 0:
                    total += rec(mask ^ block, k - 1, s - single)
            if not sub:
                break
            sub = (sub - 1) & rest
        return total

    return rec((1 << n) - 1, *target)


def counts(values):
    return tuple(sum(v % 3 == r for v in values) for r in range(3))


exact = engine()
known = [
    ((0, 0, 0), {(0, 0): 1}),
    ((1, 0, 0), {(1, 1): 1}),
    ((0, 1, 1), {(1, 0): 1}),
    ((2, 0, 0), {(1, 0): 1, (2, 2): 1}),
]
ok = all(exact(*c) == expected for c, expected in known)
print("Sanity 1 (known small polynomials):", "PASS" if ok else "FAIL")
if not ok:
    print("SANITY FAILED")
    raise SystemExit(0)

ok = True
for n in range(8):
    weights = list(range(1, n + 1))
    ok &= exact(*counts(weights)) == brute_polynomial(weights, [True] * n)
for p in (5, 7):
    for n in range(5):
        ordinary_weights = list(range(1, n + 1))
        weights = ordinary_weights + [p, 2 * p]
        expected = brute_polynomial(weights, [True] * n + [False, False])
        ok &= exact(*counts(ordinary_weights), 1, 1, p % 3, 2 * p % 3) == expected
print("Sanity 2 (labeled exhaustive partitions, including specials):",
      "PASS" if ok else "FAIL")
if not ok:
    print("SANITY FAILED")
    raise SystemExit(0)

checked = []
for p in (5, 7):
    modulus = p * p
    poly = engine(modulus, timed=True)
    for n in range(3 * p - 1, 3 * p + 9):
        if time.monotonic() > DEADLINE:
            break
        A = {1 + 3 * i for i in range(p)}
        B = {2 + 3 * i for i in range(p)}
        R = [i for i in range(1, n + 1) if i not in A | B]
        assert p >= 5 and n >= 3 * p - 1 and A | B <= set(range(1, n + 1))
        try:
            left = poly(*counts(range(1, n + 1)))
            right = dict(poly(*counts(R), 1, 1, p % 3, 2 * p % 3))
            for (k, s), value in poly(*counts(R)).items():
                key = (k + p, s)
                right[key] = (right.get(key, 0) + math.factorial(p) * value) % modulus
        except TimeLimit:
            break
        failures = [
            key for key in sorted(left.keys() | right.keys())
            if left.get(key, 0) != right.get(key, 0)
        ]
        if failures:
            key = failures[0]
            lhs = verify_coefficient(list(range(1, n + 1)), [True] * n, key)
            rhs = verify_coefficient(
                R + [p, 2 * p], [True] * len(R) + [False, False], key
            )
            if key[0] >= p:
                rhs += math.factorial(p) * verify_coefficient(
                    R, [True] * len(R), (key[0] - p, key[1])
                )
            if (lhs - rhs) % modulus:
                print("COUNTEREXAMPLE:",
                      f"p={p}, n={n}, coefficient x^{key[0]} y^{key[1]}, "
                      f"left={lhs}, right={rhs}, "
                      f"residues modulo {modulus}: {lhs % modulus}, {rhs % modulus}")
                raise SystemExit(0)
            print("SANITY FAILED")
            raise SystemExit(0)
        checked.append((p, n))

ranges = []
for p in (5, 7):
    ns = [n for q, n in checked if q == p]
    ranges.append(f"p={p}: n={min(ns)}..{max(ns)}" if ns else f"p={p}: none")
print("NO COUNTEREXAMPLE", "; ".join(ranges), f"; cases tested={len(checked)}")