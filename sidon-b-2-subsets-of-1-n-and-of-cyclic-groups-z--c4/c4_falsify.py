import sys
import itertools


def is_sidon(a_list):
    sums = []
    k = len(a_list)
    for i in range(k):
        for j in range(i, k):
            sums.append(a_list[i] + a_list[j])
    return len(set(sums)) == len(sums)


def is_sidon_plain(a_list):
    seen = set()
    k = len(a_list)
    for i in range(k):
        for j in range(i, k):
            v = a_list[i] + a_list[j]
            if v in seen:
                return False
            seen.add(v)
    return True


def count_plain(n, k, s, m):
    cnt = 0
    for mask in range(1 << n):
        A = [x + 1 for x in range(n) if mask & (1 << x)]
        if len(A) != k:
            continue
        if not A:
            continue
        if sum(A) != s:
            continue
        if max(A) != m:
            continue
        if is_sidon_plain(sorted(A)):
            cnt += 1
    return cnt


def main():
    # Sanity check 1: known small values from definitions.
    sc1 = []
    sc1.append(is_sidon([]) is True)
    sc1.append(is_sidon([1]) is True)
    sc1.append(is_sidon([1, 2]) is True)
    # 1+3 == 2+2 so {1,2,3} is not Sidon.
    sc1.append(is_sidon([1, 2, 3]) is False)
    # {1,2,5} sums: 2,3,6,4,7,10 all distinct.
    sc1.append(is_sidon([1, 2, 5]) is True)
    # {1,2,3,4}: 1+4 == 2+3 so not Sidon.
    sc1.append(is_sidon([1, 2, 3, 4]) is False)
    print("Sanity 1 (known values):", sc1)
    if not all(sc1):
        print("SANITY FAILED")
        sys.exit(1)

    # Sanity check 2: cross-check fast routine vs plain routine on all subsets of {1..6}.
    mismatch = 0
    total = 0
    for mask in range(1 << 6):
        A = sorted([x + 1 for x in range(6) if mask & (1 << x)])
        total += 1
        if is_sidon(A) != is_sidon_plain(A):
            mismatch += 1
    print("Sanity 2 (cross-check is_sidon vs plain): total=%d mismatches=%d" % (total, mismatch))
    if mismatch != 0:
        print("SANITY FAILED")
        sys.exit(1)

    # Sanity check 3: brute-force count cross-check on one bin.
    # N(4,3,s,m): enumerate {1,2,3},{1,2,4},{1,3,4},{2,3,4}, none is Sidon except check directly.
    c = count_plain(4, 3, 6, 3)
    # Only A={1,2,3} has k=3,s=6,m=3 and it is not Sidon, so count must be 0.
    print("Sanity 3 (count_plain(4,3,6,3)=%d, expected 0)" % c)
    if c != 0:
        print("SANITY FAILED")
        sys.exit(1)

    n_min, n_max = 1, 12
    counts = {}
    subsets_enumerated = 0
    for n in range(n_min, n_max + 1):
        for mask in range(1 << n):
            subsets_enumerated += 1
            A = [x + 1 for x in range(n) if mask & (1 << x)]
            if not A:
                continue
            k = len(A)
            if k < 3:
                continue
            s = sum(A)
            m = max(A)
            if m < 1 or m > n:
                continue
            if is_sidon(A):
                key = (n, k, s, m)
                counts[key] = counts.get(key, 0) + 1

    # Collect every (n,k,s,m) bin with k>=3 that was realized or could occur;
    # to test the claim we must examine all bins satisfying hypotheses, including zero counts
    # (zero is even, so only nonzero odd bins can refute). Build full bin range per n.
    # Max sum for given n,k,m: largest k-subset of {1..n} with max exactly m.
    bins_tested = 0
    for n in range(n_min, n_max + 1):
        for k in range(3, n + 1):
            for m in range(1, n + 1):
                if m < k * (k + 1) // 2 // m + 1 and False:
                    pass
                # s range: min sum with max exactly m and size k:
                # must include m plus smallest k-1 from {1..m-1}; requires m-1 >= k-1 i.e. m >= k.
                if m < k:
                    continue
                s_min = m + (k - 1) * k // 2
                s_max = m + sum(range(m - k + 1, m))
                for s in range(s_min, s_max + 1):
                    # hypotheses: m<=n (held), k>=3 (held), 2*s==k*(m+1)
                    if 2 * s != k * (m + 1):
                        continue
                    bins_tested += 1
                    v = counts.get((n, k, s, m), 0)
                    if v % 2 == 1:
                        # Recompute both sides by plainest brute force.
                        lhs = 2 * s
                        rhs = k * (m + 1)
                        v2 = count_plain(n, k, s, m)
                        if lhs == rhs and v2 % 2 == 1 and v2 == v:
                            print("COUNTEREXAMPLE: n=%d k=%d s=%d m=%d N=%d 2*s=%d k*(m+1)=%d" % (n, k, s, m, v2, lhs, rhs))
                            sys.exit(0)
                        # else spurious: continue searching

    print("NO COUNTEREXAMPLE ranges n=%d..%d k>=3 m<=n condition 2*s==k*(m+1) bins_tested=%d nonzero_bins=%d subsets_enumerated=%d" % (n_min, n_max, bins_tested, len(counts), subsets_enumerated))
    sys.exit(0)


if __name__ == "__main__":
    main()