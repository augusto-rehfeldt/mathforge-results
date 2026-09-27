import itertools
import sys

def is_sidon(srt):
    sums = []
    for i in range(len(srt)):
        for j in range(i, len(srt)):
            sums.append(srt[i] + srt[j])
    return len(set(sums)) == len(sums)

def count_N(n, k, s, m):
    count = 0
    good = []
    for combo in itertools.combinations(range(1, n + 1), k):
        if sum(combo) != s:
            continue
        if max(combo) != m:
            continue
        if not is_sidon(list(combo)):
            continue
        count += 1
        good.append(combo)
    return count, good

def main():
    n, k, s, m = 7, 3, 12, 7
    # Check every hypothesis of the claim from scratch.
    if not (isinstance(n, int) and isinstance(k, int) and isinstance(s, int) and isinstance(m, int)):
        print("REFUTATION REJECTED: witness parameters are not all integers")
        return 0
    if not (n >= 1):
        print("REFUTATION REJECTED: hypothesis n >= 1 fails")
        return 0
    if not (k >= 3):
        print("REFUTATION REJECTED: hypothesis k >= 3 fails")
        return 0
    if not (m >= 1):
        print("REFUTATION REJECTED: hypothesis m >= 1 fails")
        return 0
    if not (s >= 1):
        print("REFUTATION REJECTED: hypothesis s >= 1 fails")
        return 0
    if not (m <= n):
        print("REFUTATION REJECTED: hypothesis m <= n fails")
        return 0
    lhs = 2 * s
    rhs = k * (m + 1)
    if lhs != rhs:
        print("REFUTATION REJECTED: hypothesis 2*s == k*(m+1) fails: 2*s=%d k*(m+1)=%d" % (lhs, rhs))
        return 0
    N, good = count_N(n, k, s, m)
    N_even = (N % 2 == 0)
    if N_even:
        print("REFUTATION REJECTED: conclusion holds at witness n=%d k=%d s=%d m=%d: 2*s=%d k*(m+1)=%d N=%d (even), sets=%s" % (n, k, s, m, lhs, rhs, N, good))
        return 0
    else:
        print("REFUTATION CONFIRMED: n=%d k=%d s=%d m=%d 2*s=%d k*(m+1)=%d N=%d N_even=%s sets=%s" % (n, k, s, m, lhs, rhs, N, N_even, good))
        return 0

if __name__ == "__main__":
    sys.exit(main())