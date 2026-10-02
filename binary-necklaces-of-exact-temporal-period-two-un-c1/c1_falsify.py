#!/usr/bin/env python3
import time
import itertools
from collections import Counter
from fractions import Fraction
from functools import lru_cache

START = time.monotonic()
LIMIT = 225.0
MAX_N = 22

def transform(x, n):
    mask = (1 << n) - 1
    left = ((x << 1) & mask) | (x >> (n - 1))
    right = (x >> 1) | ((x & 1) << (n - 1))
    return x ^ (left & right)

def bits(x, n):
    return [(x >> i) & 1 for i in range(n)]

def plain_transform(a):
    n = len(a)
    return [a[i] ^ (a[(i - 1) % n] & a[(i + 1) % n])
            for i in range(n)]

def cuts(x, n):
    """Remove maximal long zero runs, returning the intervening blocks."""
    a = bits(x, n)
    if not any(a):
        return [n], []
    anchor = a.index(1)
    runs, blocks = [], []
    current = []
    j = 1
    while j <= n:
        i = (anchor + j) % n
        if a[i]:
            current.append("1")
            j += 1
        else:
            length = 0
            while j <= n and not a[(anchor + j) % n]:
                length += 1
                j += 1
            if length >= 2:
                runs.append(length)
                blocks.append("".join(current))
                current = []
            else:
                current.append("0")
    if not runs:
        return [], []
    blocks[0] = "".join(current) + blocks[0]
    return runs, blocks

def plain_cuts(a):
    n = len(a)
    if not any(a):
        return [n], []
    removed = set()
    lengths = []
    for i in range(n):
        if not a[i] and a[(i - 1) % n]:
            j = i
            run = []
            while not a[j]:
                run.append(j)
                j = (j + 1) % n
            if len(run) >= 2:
                lengths.append(len(run))
                removed.update(run)
    if not removed:
        return [], []
    blocks = []
    for i in range(n):
        if i not in removed and (i - 1) % n in removed:
            block = []
            j = i
            while j not in removed:
                block.append(str(a[j]))
                j = (j + 1) % n
            blocks.append("".join(block))
    return lengths, blocks

def property_side(runs, blocks):
    return (bool(runs) and bool(blocks)
            and all(b in {"1", "11", "111", "101"} for b in blocks)
            and any(b in {"111", "101"} for b in blocks))

def has_consecutive_zeros(x, n):
    z = x ^ ((1 << n) - 1)
    return bool(z & (((z << 1) & ((1 << n) - 1)) | (z >> (n - 1))))

def canonical(x, n):
    mask = (1 << n) - 1
    best = x
    for _ in range(n - 1):
        x = ((x << 1) & mask) | (x >> (n - 1))
        best = min(best, x)
    return best

def fail(witness, lhs, rhs):
    print("COUNTEREXAMPLE:", witness, "brute_force =", lhs, "claimed =", rhs)
    raise SystemExit(0)

# Sanity 1: independent bit-list evolution and independent zero-run removal.
for n in range(3, 9):
    for x in range(1 << n):
        a = bits(x, n)
        slow = plain_transform(a)
        r, b = cuts(x, n)
        rr, bb = plain_cuts(a)
        if (bits(transform(x, n), n) != slow
                or sorted(r) != sorted(rr) or sorted(b) != sorted(bb)):
            print("SANITY FAILED")
            raise SystemExit(0)
print("SANITY 1 PASSED: independent evolution and cuts, all words n=3..8")

# Sanity 2: known orbit and necklace orbit-stabilizer identity.
a = [1, 1, 1, 0, 0]
b = plain_transform(a)
if b != [1, 0, 1, 0, 0] or plain_transform(b) != a:
    print("SANITY FAILED")
    raise SystemExit(0)
for n in range(3, 9):
    classes = Counter(canonical(x, n) for x in range(1 << n))
    for representative, size in classes.items():
        a = bits(representative, n)
        stabilizer = sum(a == a[j:] + a[:j] for j in range(n))
        if Fraction(n, stabilizer) != size:
            print("SANITY FAILED")
            raise SystemExit(0)
print("SANITY 2 PASSED: known two-cycle and orbit-stabilizer, n=3..8")

# Literally expand P: a long zero run of length L followed by one
# of its four monomials. Keys are (degree_t, degree_u, degree_v, degree_q).
terms = []
for L in range(2, MAX_N):
    for d, u, v, q in [(1, 1, 1, 0), (2, 2, 2, 0),
                        (3, 3, 2, 1), (3, 2, 3, 1)]:
        if L + d <= MAX_N:
            terms.append((L + d, u, v, q))

powers = [{(0, 0, 0, 0): 1}]
for k in range(1, MAX_N // 3 + 1):
    out = Counter()
    for (n, a, b, c), coefficient in powers[-1].items():
        for d, u, v, q in terms:
            if n + d <= MAX_N:
                out[n + d, a + u, b + v, c + q] += coefficient
    powers.append(out)

def claimed(n, k, a, b, c):
    value = powers[k].get((n, a, b, c), 0)
    if a != b:
        value += powers[k].get((n, b, a, c), 0)
    return Fraction(n * value, k)

# Independent literal coefficient calculation for witness verification.
@lru_cache(None)
def plain_coefficient(k, n, a, b, c):
    if min(n, a, b, c) < 0:
        return 0
    if k == 0:
        return int((n, a, b, c) == (0, 0, 0, 0))
    total = 0
    for L in range(2, n + 1):
        for d, u, v, q in [(1, 1, 1, 0), (2, 2, 2, 0),
                            (3, 3, 2, 1), (3, 2, 3, 1)]:
            total += plain_coefficient(k - 1, n - L - d,
                                       a - u, b - v, c - q)
    return total

def plain_M(n, k, a, b, c):
    # Sum over necklaces explicitly, using plain list-based evolution.
    necklaces = set()
    for word in itertools.product((0, 1), repeat=n):
        t = plain_transform(word)
        if t == list(word) or plain_transform(t) != list(word):
            continue
        runs, _ = plain_cuts(word)
        if len(runs) != k:
            continue
        if sorted((sum(word), sum(t))) != [a, b]:
            continue
        if sum(u != v for u, v in zip(word, t)) != c:
            continue
        necklaces.add(min(word[j:] + word[:j] for j in range(n)))
    total = Fraction(0)
    for word in necklaces:
        s = sum(word == word[j:] + word[:j] for j in range(n))
        total += Fraction(n, s)
    return total

classification_cases = 0
formula_cases = 0
completed = 2
previous_duration = None

for n in range(3, MAX_N + 1):
    remaining = LIMIT - (time.monotonic() - START)
    if previous_duration is not None and remaining < 2.7 * previous_duration + 3:
        break
    begin = time.monotonic()
    observed = Counter()
    necklace_sizes = Counter()
    necklace_keys = {}
    for x in range(1 << n):
        if not has_consecutive_zeros(x, n):
            continue
        classification_cases += 1
        y = transform(x, n)
        actual = y != x and transform(y, n) == x
        runs, blocks = cuts(x, n)
        predicted = property_side(runs, blocks)
        if actual != predicted:
            a = bits(x, n)
            t = plain_transform(a)
            lhs = t != a and plain_transform(t) == a
            rr, bb = plain_cuts(a)
            rhs = property_side(rr, bb)
            if lhs != rhs:
                fail({"n": n, "word": "".join(map(str, a)),
                      "zero_runs": rr, "blocks": bb}, lhs, rhs)
            print("SANITY FAILED")
            raise SystemExit(0)
        if actual:
            weights = sorted((x.bit_count(), y.bit_count()))
            key = (len(runs), weights[0], weights[1], (x ^ y).bit_count())
            representative = canonical(x, n)
            necklace_sizes[representative] += 1
            necklace_keys[representative] = key

    # Explicitly aggregate n/s(N), independently checking each orbit size.
    for representative, size in necklace_sizes.items():
        a = bits(representative, n)
        s = sum(a == a[j:] + a[:j] for j in range(n))
        if Fraction(n, s) != size:
            print("SANITY FAILED")
            raise SystemExit(0)
        observed[necklace_keys[representative]] += Fraction(n, s)

    for k in range(1, n // 3 + 1):
        for a in range(n + 1):
            for b in range(a, n + 1):
                for c in range(1, n + 1):
                    formula_cases += 1
                    lhs = observed.get((k, a, b, c), 0)
                    rhs = claimed(n, k, a, b, c)
                    if lhs != rhs:
                        lhs2 = plain_M(n, k, a, b, c)
                        coefficient = plain_coefficient(k, n, a, b, c)
                        if a != b:
                            coefficient += plain_coefficient(k, n, b, a, c)
                        rhs2 = Fraction(n * coefficient, k)
                        if lhs2 != rhs2:
                            fail({"n": n, "k": k, "a": a, "b": b, "c": c},
                                 lhs2, rhs2)
                        print("SANITY FAILED")
                        raise SystemExit(0)
    completed = n
    previous_duration = time.monotonic() - begin

print("NO COUNTEREXAMPLE",
      f"classification: all consecutive-zero words, 3<=n<={completed};",
      f"formula: 3<=n<={completed}, 1<=k<=floor(n/3), "
      "0<=a<=b<=n, 1<=c<=n;",
      f"cases tested={classification_cases + formula_cases} "
      f"(classification={classification_cases}, formula={formula_cases})")