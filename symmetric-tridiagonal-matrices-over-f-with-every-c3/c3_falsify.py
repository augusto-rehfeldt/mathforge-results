import itertools
import time
import sys

# Polynomials over F_2 are encoded as bit masks.
def words(n):
    return itertools.product((0, 1), repeat=n)

def pmul(a, b):
    z = 0
    while b:
        if b & 1:
            z ^= a
        a <<= 1
        b >>= 1
    return z

def poly(t):
    previous, current = 0, 1
    for b in t:
        previous, current = current, (current << 1) ^ (current if b else 0) ^ previous
    return current

def peval(p, a):
    return (p & 1) if a == 0 else (p.bit_count() & 1)

def derivative(p):
    d = 0
    for k in range(1, p.bit_length(), 2):
        if (p >> k) & 1:
            d ^= 1 << (k - 1)
    return d

def boundary(t):
    p, q = poly(t), poly(t[:-1])
    return (peval(p, 0), peval(q, 0), peval(p, 1), peval(q, 1))

def predicted(u, v):
    p, q = poly(u), poly(u[:-1])
    pv = poly(v)
    rv = poly(v[1:-1]) if len(v) >= 2 else 0
    result = []
    for a in (0, 1):
        f = (pv if peval(p, a) else 0) ^ (rv if peval(q, a) else 0)
        result.append(0 if peval(f, a) else (1 if peval(derivative(f), a) else 2))
    return tuple(result)

def bitrank(rows):
    pivots = {}
    for row in rows:
        while row:
            k = row.bit_length() - 1
            if k in pivots:
                row ^= pivots[k]
            else:
                pivots[k] = row
                break
    return len(pivots)

def actual(t):
    n = len(t)
    result = []
    for a in (0, 1):
        rows = [
            ((t[i] ^ a) << i)
            ^ ((1 << (i - 1)) if i else 0)
            ^ ((1 << (i + 1)) if i + 1 < n else 0)
            for i in range(n)
        ]
        squared = []
        for row in rows:
            s = 0
            while row:
                bit = row & -row
                s ^= rows[bit.bit_length() - 1]
                row ^= bit
            squared.append(s)
        result.append(n - bitrank(squared))
    return tuple(result)

# Independent, deliberately plain implementations used for verification.
def padd(a, b):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] ^= x
    for i, x in enumerate(b):
        c[i] ^= x
    return c

def listmul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] ^= x & y
    return c

def determinant_poly(t):
    n = len(t)
    answer = [0]
    # Literal determinant expansion; signs disappear in characteristic two.
    for perm in itertools.permutations(range(n)):
        term = [1]
        for i, j in enumerate(perm):
            if i == j:
                factor = [t[i], 1]
            elif abs(i - j) == 1:
                factor = [1]
            else:
                term = [0]
                break
            term = listmul(term, factor)
        answer = padd(answer, term)
    return sum(x << i for i, x in enumerate(answer))

def plain_poly(t):
    # Dense polynomial determinant via leading-principal-minor expansion.
    before, now = [0], [1]
    for b in t:
        before, now = now, padd(listmul([b, 1], now), before)
    return now

def plain_prediction(u, v):
    p, q = plain_poly(u), plain_poly(u[:-1])
    pv = plain_poly(v)
    rv = plain_poly(v[1:-1]) if len(v) >= 2 else [0]
    evaluate = lambda c, a: sum(x * (a ** i) for i, x in enumerate(c)) % 2
    out = []
    for a in (0, 1):
        f = padd([evaluate(p, a) * x for x in pv],
                 [evaluate(q, a) * x for x in rv])
        df = [(i * f[i]) % 2 for i in range(1, len(f))]
        out.append(0 if evaluate(f, a) else (1 if evaluate(df, a) else 2))
    return tuple(out)

def dense_actual(t):
    n = len(t)
    answers = []
    for a in (0, 1):
        m = [[0] * n for _ in range(n)]
        for i in range(n):
            m[i][i] = t[i] ^ a
            if i + 1 < n:
                m[i][i + 1] = m[i + 1][i] = 1
        s = [[sum(m[i][k] * m[k][j] for k in range(n)) % 2
              for j in range(n)] for i in range(n)]
        rank = 0
        for col in range(n):
            pivot = next((i for i in range(rank, n) if s[i][col]), None)
            if pivot is None:
                continue
            s[rank], s[pivot] = s[pivot], s[rank]
            for i in range(rank + 1, n):
                if s[i][col]:
                    s[i] = [x ^ y for x, y in zip(s[i], s[rank])]
            rank += 1
        answers.append(n - rank)
    return tuple(answers)

def fail_sanity():
    print("SANITY FAILED")
    sys.exit(0)

def report(witness, left, right):
    print("COUNTEREXAMPLE:", witness, "direct =", left, "claimed =", right)
    sys.exit(0)

def main():
    start = time.monotonic()
    deadline = start + 210

    known = (
        poly(()) == 1 and poly((0,)) == 2 and poly((1,)) == 3
        and poly((0, 0)) == 5
        and actual((0,)) == (1, 0)
        and actual((0, 0)) == (0, 2)
    )
    print("Sanity 1: known small values:", "PASS" if known else "FAIL")
    if not known:
        fail_sanity()

    checks = 0
    for n in range(1, 6):
        for t in words(n):
            if poly(t) != determinant_poly(t) or actual(t) != dense_actual(t):
                fail_sanity()
            checks += 1
    print("Sanity 2: permutation determinants and dense squared-matrix ranks: PASS;",
          checks, "words")

    vs = [t for n in range(1, 8) for t in words(n)]
    completed = []
    seen_boundaries = {}
    identity_cases = 0
    last_full_length = 0
    partial_u = None

    for n in range(1, 10):
        for u in words(n):
            signature = []
            for v in vs:
                if time.monotonic() >= deadline:
                    partial_u = (u, len(signature))
                    break
                t = u + v + u[::-1]
                direct, claim = actual(t), predicted(u, v)
                identity_cases += 1
                if direct != claim:
                    direct2, claim2 = dense_actual(t), plain_prediction(u, v)
                    if direct2 != claim2:
                        report({"relation": "identity", "u": u, "v": v,
                                "matrix_dimension": len(t)}, direct2, claim2)
                    fail_sanity()
                signature.append(direct)
            if partial_u is not None:
                break
            b = boundary(u)
            seen_boundaries.setdefault(b, u)
            completed.append((u, b, tuple(signature)))
        if partial_u is not None:
            break
        last_full_length = n

    # Exhaustively compare the finite signatures for every unordered pair.
    # Equal finite signatures with different boundaries are NOT a universal
    # counterexample: a longer v might distinguish them.
    pair_cases = different_pairs = distinguished = unresolved = 0
    for i, (u, bu, su) in enumerate(completed):
        for w, bw, sw in completed[i + 1:]:
            pair_cases += 1
            if bu == bw:
                if su != sw:
                    j = next(j for j in range(len(vs)) if su[j] != sw[j])
                    v = vs[j]
                    left = dense_actual(u + v + u[::-1])
                    right = dense_actual(w + v + w[::-1])
                    if boundary(u) == boundary(w) and left != right:
                        report({"relation": "equal boundaries imply equal dimensions",
                                "u": u, "w": w, "v": v}, left, right)
                    fail_sanity()
            else:
                different_pairs += 1
                if su != sw:
                    distinguished += 1
                else:
                    unresolved += 1

    allowed = set(itertools.product(((0, 1), (1, 0), (1, 1)), repeat=2))
    allowed = {x + y for x, y in allowed}
    for b, u in seen_boundaries.items():
        if b not in allowed:
            p, q = plain_poly(u), plain_poly(u[:-1])
            b2 = (p[0], q[0], sum(p) % 2, sum(q) % 2)
            if b2 not in allowed:
                report({"relation": "boundary range", "u": u}, b2,
                       sorted(allowed))
            fail_sanity()

    print("Boundary values observed:", len(seen_boundaries), "of 9;",
          "all nine occur:", set(seen_boundaries) == allowed)
    print("Different-boundary pairs:", different_pairs,
          "distinguished:", distinguished, "unresolved:", unresolved)
    print("Boundary witnesses:", sorted(seen_boundaries.items()))
    print("NO COUNTEREXAMPLE",
          "; complete identity ranges: 1 <= |u| <=", last_full_length,
          ", 1 <= |v| <= 7;",
          "completed u rows =", len(completed),
          "; partial row (u, number of v checked) =", partial_u,
          "; identity cases =", identity_cases,
          "(two a values per case); pair cases =", pair_cases,
          "; pair range: all unordered pairs of completed u rows,",
          "each searched against all 254 nonempty v of length <= 7")

if __name__ == "__main__":
    main()