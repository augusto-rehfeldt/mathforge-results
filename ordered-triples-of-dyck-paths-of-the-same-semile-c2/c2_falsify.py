import itertools
import time
from collections import Counter

LIMIT_SECONDS = 225
START = time.monotonic()


def dyck_paths(n):
    result = []

    def visit(h, ups, downs):
        if ups == downs == n:
            result.append(tuple(h))
            return
        if ups < n:
            visit(h + [h[-1] + 1], ups + 1, downs)
        if downs < ups:
            visit(h + [h[-1] - 1], ups, downs + 1)

    visit([0], 0, 0)
    return result


def below(x, y):
    return all(a <= b for a, b in zip(x, y))


def literal_key(x, y, z):
    """Direct implementation of all the statement's statistics."""
    N = len(x) - 1
    contacts = [t for t in range(1, N) if x[t] == y[t] == z[t]]
    if len(contacts) != 2:
        return None
    a, b = contacts
    if x[a] != x[b]:
        return None
    H = x[a]
    A = sum(y[t] - x[t] for t in range(N + 1)) // 2
    B = sum(z[t] - y[t] for t in range(N + 1)) // 2
    L = [t for t in range(1, N) if x[t] == y[t] < z[t]]
    U = [t for t in range(1, N) if x[t] < y[t] == z[t]]

    def counts(s, f, g):
        p = v = 0
        for t in s:
            if a < t < b:
                p += (
                    f[t - 1] == f[t + 1] == f[t] - 1
                    and g[t - 1] == g[t + 1] == g[t] - 1
                )
                v += (
                    f[t - 1] == f[t + 1] == f[t] + 1
                    and g[t - 1] == g[t + 1] == g[t] + 1
                )
        return p, v

    p12, v12 = counts(L, x, y)
    p23, v23 = counts(U, y, z)
    return (
        a, b, H, A, B,
        sum(1 << t for t in L), sum(1 << t for t in U),
        p12, v12, p23, v23,
    )


def transform(k):
    a, b, H, A, B, L, U, p12, v12, p23, v23 = k

    def reflect(mask):
        result = 0
        while mask:
            bit = mask & -mask
            t = bit.bit_length() - 1
            r = a + b - t if a < t < b else t
            result |= 1 << r
            mask -= bit
        return result

    return (a, b, H, A, B, reflect(L), reflect(U),
            v12, p12, v23, p23)


def fast_groups(paths, deadline=None):
    m = len(paths)
    N = len(paths[0]) - 1
    peaks, valleys = [], []
    for h in paths:
        peaks.append(sum(
            1 << t for t in range(1, N)
            if h[t - 1] == h[t + 1] == h[t] - 1
        ))
        valleys.append(sum(
            1 << t for t in range(1, N)
            if h[t - 1] == h[t + 1] == h[t] + 1
        ))

    lower = [[] for _ in paths]
    upper = [[] for _ in paths]
    for i, x in enumerate(paths):
        for j, y in enumerate(paths):
            if below(x, y):
                eq = sum(1 << t for t in range(1, N) if x[t] == y[t])
                area = sum(v - u for u, v in zip(x, y)) // 2
                data = (eq, area, peaks[i] & peaks[j],
                        valleys[i] & valleys[j])
                upper[i].append((j, data))
                lower[j].append((i, data))

    groups = Counter()
    accepted = 0
    for j in range(m):
        if deadline is not None and time.monotonic() >= deadline:
            return None
        for i, d12 in lower[j]:
            e12, A, pk12, vl12 = d12
            for z, d23 in upper[j]:
                e23, B, pk23, vl23 = d23
                T = e12 & e23
                if T.bit_count() != 2:
                    continue
                first = T & -T
                a = first.bit_length() - 1
                b = (T ^ first).bit_length() - 1
                H = paths[j][a]
                if H != paths[j][b]:
                    continue
                L, U = e12 ^ T, e23 ^ T
                interior = ((1 << b) - 1) ^ ((1 << (a + 1)) - 1)
                lm, um = L & interior, U & interior
                k = (
                    a, b, H, A, B, L, U,
                    (lm & pk12).bit_count(), (lm & vl12).bit_count(),
                    (um & pk23).bit_count(), (um & vl23).bit_count(),
                )
                groups[k] += 1
                accepted += 1
    return groups, accepted


def plain_groups(paths):
    groups = Counter()
    for x, y, z in itertools.product(paths, repeat=3):
        if below(x, y) and below(y, z):
            k = literal_key(x, y, z)
            if k is not None:
                groups[k] += 1
    return groups


def independently_recount(paths, left, right):
    """No pair tables or bit-statistic routines: enumerate actual triples."""
    a, b, H = left[:3]
    eligible = [h for h in paths if h[a] == H and h[b] == H]
    c1 = c2 = 0
    for x in eligible:
        for y in eligible:
            if not below(x, y):
                continue
            for z in eligible:
                if not below(y, z):
                    continue
                k = literal_key(x, y, z)
                c1 += k == left
                c2 += k == right
    return c1, c2


def display(n, k):
    a, b, H, A, B, L, U, p12, v12, p23, v23 = k
    return dict(
        n=n, a=a, b=b, H=H, A=A, B=B,
        L=[t for t in range(1, 2 * n) if L & (1 << t)],
        U=[t for t in range(1, 2 * n) if U & (1 << t)],
        p12=p12, v12=v12, p23=p23, v23=v23,
    )


def main():
    expected = [1, 1, 2, 5, 14, 42, 132, 429]
    actual = [len(dyck_paths(n)) for n in range(8)]
    ok = actual == expected
    print("Sanity 1: Catalan counts n=0..7:", actual, "PASS" if ok else "FAIL",
          flush=True)
    if not ok:
        print("SANITY FAILED")
        return

    small = dyck_paths(3)
    fast = fast_groups(small)[0]
    plain = plain_groups(small)
    ok = fast == plain
    print("Sanity 2: independent full Cartesian enumeration at n=3:",
          "PASS" if ok else "FAIL", flush=True)
    if not ok:
        print("SANITY FAILED")
        return

    completed = []
    cases = triples = 0
    for n in range(2, 8):
        paths = dyck_paths(n)
        result = fast_groups(paths, START + LIMIT_SECONDS)
        if result is None:
            break
        groups, accepted = result
        # The transformation is an involution. Testing this union also covers
        # unrealized parameter groups whose transformed group is realized.
        keys = set(groups)
        keys.update(transform(k) for k in groups)
        for k in keys:
            target = transform(k)
            left, right = groups.get(k, 0), groups.get(target, 0)
            if left != right:
                c1, c2 = independently_recount(paths, k, target)
                if (c1, c2) != (left, right) or c1 == c2:
                    print("SANITY FAILED")
                    return
                print("COUNTEREXAMPLE:")
                print("witness =", display(n, k))
                print("transformed requirements =", display(n, target))
                print("first cardinality =", c1)
                print("second cardinality =", c2)
                return
        completed.append(n)
        cases += len(keys)
        triples += accepted

    print("NO COUNTEREXAMPLE")
    print("Exact completed n range:", completed)
    print("For each completed n: all ordered Dyck triples; all valid a,b,H,"
          " A,B,L,U and nonnegative count parameters.")
    print("Cases tested (realized keys and their transformed keys):", cases)
    print("Triples satisfying the hypotheses:", triples)
    print("All remaining parameter keys at completed n have both sides zero.")


if __name__ == "__main__":
    main()