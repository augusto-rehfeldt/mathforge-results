import itertools
import time
import sys

LIMIT_SECONDS = 215
MAX_N = 22


def mask_of(S):
    return sum(1 << x for x in S)


def elements(mask, n):
    return [i for i in range(n + 1) if mask & (1 << i)]


def brute_vector(S, n):
    counts = [0] * n
    for a in S:
        for b in S:
            if b > a:
                counts[b - a - 1] += 1
    return tuple(counts)


def fast_vector(mask, n):
    return tuple((mask & (mask >> t)).bit_count()
                 for t in range(1, n + 1))


def signature(mask, n):
    # Five bits suffice: every positive-difference count is at most 22.
    result = 0
    for t in range(1, n + 1):
        result = (result << 5) | (mask & (mask >> t)).bit_count()
    return result


def reflect(mask, n):
    result = 0
    while mask:
        low = mask & -mask
        result |= 1 << (n - (low.bit_length() - 1))
        mask ^= low
    return result


def sanity_failed():
    print("SANITY FAILED")
    sys.exit(0)


# Independent check 1: explicit ordered-pair counting versus bit operations.
try:
    assert brute_vector([0, 1, 3], 3) == (1, 1, 1)
    for n in range(1, 9):
        for mask in range(1 << (n + 1)):
            S = elements(mask, n)
            assert fast_vector(mask, n) == brute_vector(S, n)
            assert elements(reflect(mask, n), n) == sorted(n - x for x in S)
except AssertionError:
    sanity_failed()
print("SANITY 1 PASSED: difference counts and reflection, all masks through n=8")


def eligible_masks(n):
    endpoints = 1 | (1 << n)
    for interior in range(1 << (n - 1)):
        mask = endpoints | (interior << 1)
        if 2 * mask.bit_count() > n + 1:
            yield mask


# Independent check 2: signature grouping versus literal delete/insert search.
try:
    for n in range(1, 9):
        literal = set()
        for a in eligible_masks(n):
            A = set(elements(a, n))
            for removed in itertools.combinations(sorted(A - {0, n}), 2):
                for inserted in itertools.combinations(
                        sorted(set(range(n + 1)) - A), 2):
                    B = (A - set(removed)) | set(inserted)
                    b = mask_of(B)
                    if b != reflect(a, n) and brute_vector(A, n) == brute_vector(B, n):
                        literal.add(tuple(sorted((a, b))))

        grouped = set()
        buckets = {}
        for a in eligible_masks(n):
            key = signature(a, n)
            for b in buckets.get(key, ()):
                if (a ^ b).bit_count() == 4 and b != reflect(a, n):
                    grouped.add(tuple(sorted((a, b))))
            buckets.setdefault(key, []).append(a)
        assert literal == grouped
except AssertionError:
    sanity_failed()
print("SANITY 2 PASSED: grouped search equals delete/insert search through n=8")


start = time.monotonic()
completed_n = 0
sets_tested = 0
equal_signature_pairs_tested = 0
partial_n = None
last_interior = None
stopped = False

# Grouping is exhaustive: every equal-vector pair shares a signature.
# XOR popcount four is exactly two deletions and two insertions when
# cardinalities agree. Each unordered pair is checked once.
for n in range(1, MAX_N + 1):
    buckets = {}
    endpoints = 1 | (1 << n)
    for interior in range(1 << (n - 1)):
        if interior % 2048 == 0 and time.monotonic() - start >= LIMIT_SECONDS:
            partial_n = n
            last_interior = interior - 1
            stopped = True
            break

        a = endpoints | (interior << 1)
        k = a.bit_count()
        if 2 * k <= n + 1:
            continue
        sets_tested += 1
        key = signature(a, n)
        previous = buckets.get(key)
        if previous is not None:
            for b in previous:
                equal_signature_pairs_tested += 1
                if b.bit_count() != k:
                    continue
                if (a ^ b).bit_count() != 4:
                    continue
                if b == reflect(a, n):
                    continue

                # Recompute every hypothesis and the literal conclusion using
                # plain sets and ordered-pair loops before reporting.
                A = set(elements(a, n))
                B = set(elements(b, n))
                plain_k = len(A)
                hypotheses = (
                    n >= 1
                    and A != B
                    and {0, n} <= A
                    and {0, n} <= B
                    and len(B) == plain_k
                    and len(A & B) == plain_k - 2
                    and brute_vector(A, n) == brute_vector(B, n)
                    and B != {n - x for x in A}
                )
                left = n
                right = 2 * plain_k - 1
                if hypotheses and not (left >= right):
                    print(
                        "COUNTEREXAMPLE:",
                        f"n={n}, k={plain_k}, A={sorted(A)}, B={sorted(B)}; "
                        f"claimed relation: {left} >= {right}; "
                        f"difference vectors={brute_vector(A, n)}"
                    )
                    sys.exit(0)
            previous.append(a)
        else:
            buckets[key] = [a]

    if stopped:
        break
    completed_n = n
    del buckets

ranges = f"full n=1..{completed_n}"
if partial_n is not None:
    ranges += (
        f"; partial n={partial_n}, interior masks=0..{last_interior}"
        " (only endpoint-containing sets with 2|A|>n+1)"
    )
print(
    "NO COUNTEREXAMPLE",
    f"{ranges}; sets tested={sets_tested}; "
    f"equal-signature unordered pair cases tested={equal_signature_pairs_tested}"
)
sys.exit(0)