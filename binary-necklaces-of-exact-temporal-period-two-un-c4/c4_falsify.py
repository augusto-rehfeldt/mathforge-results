import time
import sys

START = time.monotonic()
DEADLINE = START + 225.0


def bits(w, n):
    return [(w >> k) & 1 for k in range(n)]


def encode(v):
    return sum(b << k for k, b in enumerate(v))


def plain_T(v):
    n = len(v)
    return [v[k] ^ (v[(k - 1) % n] & v[(k + 1) % n])
            for k in range(n)]


def fast_T(w, n):
    mask = (1 << n) - 1
    left = ((w << 1) & mask) | (w >> (n - 1))
    right = (w >> 1) | ((w & 1) << (n - 1))
    return w ^ (left & right)


def exact(v):
    t = plain_T(v)
    return t != v and plain_T(t) == v


def sanity():
    v = [1, 0, 1, 0, 0]
    ok = (plain_T(v) == [1, 1, 1, 0, 0] and exact(v)
          and plain_T([1] * 5) == [0] * 5)
    print("Sanity 1: known updates and exact two-cycle:", "PASS" if ok else "FAIL")
    if not ok:
        return False

    checked = 0
    for n in range(1, 9):
        for w in range(1 << n):
            v = bits(w, n)
            t = plain_T(v)
            ft = fast_T(w, n)
            ok = (ft == encode(t)
                  and fast_T(ft, n) == encode(plain_T(t))
                  and (w ^ ft).bit_count() == sum(a != b for a, b in zip(v, t)))
            if not ok:
                print("Sanity 2: exhaustive independent list/bit cross-check: FAIL")
                return False
            checked += 1
    print("Sanity 2: exhaustive independent list/bit cross-check: PASS;",
          checked, "words")
    return True


def report_forward(x, z, c, d):
    # Independently reconstruct and evaluate every relation with lists.
    assert len(x) >= 5 and len(z) >= 5
    tx, tz = plain_T(x), plain_T(z)
    assert exact(x) and exact(z) and tx[0] != x[0] and tz[0] != z[0]
    u = x[1:] + [c] + z[1:] + [d]
    tu = plain_T(u)
    relations = [
        ("T²(u)=u", plain_T(tu), u),
        ("T(u) != u", tu != u, True),
        ("D(u)=D(x)+D(z)",
         sum(p != q for p, q in zip(u, tu)),
         sum(p != q for p, q in zip(x, tx)) +
         sum(p != q for p, q in zip(z, tz))),
        ("wt(u)=wt(x)+wt(z)-a-b+c+d",
         sum(u), sum(x) + sum(z) - x[0] - z[0] + c + d),
        ("wt(T(u))=wt(T(x))+wt(T(z))+a+b-c-d",
         sum(tu), sum(tx) + sum(tz) + x[0] + z[0] - c - d),
    ]
    for name, actual, claimed in relations:
        if actual != claimed:
            print("COUNTEREXAMPLE:", {
                "operation": "forward", "x": x, "z": z,
                "i": 0, "j": 0, "c": c, "d": d, "u": u,
                "relation": name, "actual": actual, "claimed": claimed
            })
            sys.exit(0)
    raise RuntimeError("Fast candidate failed independent confirmation")


def report_reverse(v, i, j, c, d):
    assert len(v) >= 10 and exact(v)
    t = plain_T(v)
    assert t[i] != v[i] and t[j] != v[j]
    assert j - i >= 5 and len(v) - (j - i) >= 5
    paths = [v[i + 1:j] + [c], v[j + 1:] + v[:i] + [d]]
    for side, p in enumerate(paths):
        assert len(p) >= 5
        actual = exact(p)
        if not actual:
            print("COUNTEREXAMPLE:", {
                "operation": "reverse", "u": v, "i": i, "j": j,
                "c": c, "d": d, "side": side, "closed_word": p,
                "T(word)": plain_T(p),
                "T²(word)": plain_T(plain_T(p)),
                "relation": "closed word has exact temporal period two",
                "actual": actual, "claimed": True
            })
            sys.exit(0)
    raise RuntimeError("Fast candidate failed independent confirmation")


if not sanity():
    print("SANITY FAILED")
    sys.exit(0)

# Anchoring the selected changed position at index zero covers every forward
# input up to independent rotations. No asserted gluing property is used.
records = {}
for n in range(5, 13):
    rows = []
    for w in range(1 << n):
        t = fast_T(w, n)
        if t != w and fast_T(t, n) == w and ((w ^ t) & 1):
            rows.append((w, w & 1, (w ^ t).bit_count(),
                         w.bit_count(), t.bit_count()))
    records[n] = rows

forward_count = 0
forward_done = []
forward_partial = None
forward_stop = min(START + 105.0, DEADLINE)
stop = False

for n in range(5, 13):
    if stop:
        break
    for m in range(5, 13):
        block_count = 0
        for ix, rx in enumerate(records[n]):
            if stop:
                break
            xw, a, dx, wx, wtx = rx
            for iz, rz in enumerate(records[m]):
                if stop:
                    break
                zw, b, dz, wz, wtz = rz
                for c in range(2):
                    if stop:
                        break
                    for d in range(2):
                        if time.monotonic() >= forward_stop:
                            forward_partial = {
                                "n": n, "m": m,
                                "completed_cases": block_count,
                                "next_case": (ix, iz, c, d),
                                "order": "ascending anchored x, anchored z, c, d"
                            }
                            stop = True
                            break
                        # P occupies indices 0..n-2, c index n-1.
                        uw = ((xw >> 1) | (c << (n - 1)) |
                              ((zw >> 1) << n) | (d << (n + m - 1)))
                        r = n + m
                        ut = fast_T(uw, r)
                        failed = (
                            fast_T(ut, r) != uw or ut == uw or
                            (uw ^ ut).bit_count() != dx + dz or
                            uw.bit_count() != wx + wz - a - b + c + d or
                            ut.bit_count() != wtx + wtz + a + b - c - d
                        )
                        forward_count += 1
                        block_count += 1
                        if failed:
                            report_forward(bits(xw, n), bits(zw, m), c, d)
        if stop:
            break
        forward_done.append((n, m))

reverse_count = 0
reverse_scanned = 0
reverse_done = []
reverse_partial = None
stop = False

for n in range(10, 21):
    for w in range(1 << n):
        if time.monotonic() >= DEADLINE:
            reverse_partial = {
                "n": n, "all_words_below": w,
                "next_word": w, "next_case": "before word evaluation"
            }
            stop = True
            break
        reverse_scanned += 1
        t = fast_T(w, n)
        if t == w or fast_T(t, n) != w:
            continue
        changed = [k for k in range(n) if ((w ^ t) >> k) & 1]
        v = bits(w, n)
        for i in changed:
            if stop:
                break
            for j in changed:
                if j <= i or j - i < 5 or n - (j - i) < 5:
                    continue
                if stop:
                    break
                for c in range(2):
                    if stop:
                        break
                    for d in range(2):
                        if time.monotonic() >= DEADLINE:
                            reverse_partial = {
                                "n": n, "all_words_below": w,
                                "current_word": w, "next_case": (i, j, c, d),
                                "order": "ascending word, i, j, c, d"
                            }
                            stop = True
                            break
                        p = v[i + 1:j] + [c]
                        q = v[j + 1:] + v[:i] + [d]
                        failed = False
                        for path in (p, q):
                            pw = encode(path)
                            pt = fast_T(pw, len(path))
                            if pt == pw or fast_T(pt, len(path)) != pw:
                                failed = True
                        reverse_count += 1
                        if failed:
                            report_reverse(v, i, j, c, d)
        if stop:
            break
    if stop:
        break
    reverse_done.append(n)

print("NO COUNTEREXAMPLE", {
    "forward_complete_length_pairs": forward_done,
    "forward_partial_prefix": forward_partial,
    "forward_cases_tested": forward_count,
    "forward_coverage": "all changed positions via rotation anchoring",
    "reverse_complete_lengths": reverse_done,
    "reverse_partial_prefix": reverse_partial,
    "reverse_words_scanned": reverse_scanned,
    "reverse_cases_tested": reverse_count,
    "reverse_pair_coverage": "i<j; both paths and all four closing choices",
    "total_cases_tested": forward_count + reverse_count
})
sys.exit(0)