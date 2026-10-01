#!/usr/bin/env python3
from collections import Counter, deque
from itertools import combinations, product
import sys


def graph(n):
    # Indices 2*i and 2*i+1 represent u_{i+1} and v_{i+1}.
    adj = [[] for _ in range(2 * n)]
    for i in range(n):
        a, b = 2 * i, 2 * i + 1
        adj[a].append(b)
        adj[b].append(a)
        if i + 1 < n:
            for x in (a, b):
                adj[x].append(x + 2)
                adj[x + 2].append(x)
    return adj


def recurrent(heights, adj):
    remaining = [len(neighbors) for neighbors in adj]
    burned = [False] * len(adj)
    queue = deque(i for i in range(len(adj))
                  if heights[i] >= remaining[i])
    while queue:
        i = queue.popleft()
        if burned[i]:
            continue
        burned[i] = True
        for j in adj[i]:
            if not burned[j]:
                remaining[j] -= 1
                if heights[j] >= remaining[j]:
                    queue.append(j)
    return all(burned)


def avalanche(heights, adj):
    chips = list(heights)
    chips[0] += 1
    queue = deque([0] if chips[0] >= 3 else [])
    toppled = set()
    while queue:
        i = queue.popleft()
        if chips[i] < 3:
            continue
        chips[i] -= 3
        toppled.add(i)
        for j in adj[i]:
            chips[j] += 1
            if chips[j] >= 3:
                queue.append(j)
        if chips[i] >= 3:
            queue.append(i)
    return len(toppled), tuple(chips)


# Independent, plain implementations used for checks and confirmation.
def plain_recurrent(heights, adj):
    unburned = set(range(len(adj)))
    while unburned:
        burn_now = {
            i for i in unburned
            if heights[i] >= sum(j in unburned for j in adj[i])
        }
        if not burn_now:
            return False
        unburned.difference_update(burn_now)
    return True


def plain_avalanche(heights, adj):
    chips = list(heights)
    chips[0] += 1
    toppled = set()
    while True:
        for i in range(len(chips)):
            if chips[i] >= 3:
                chips[i] -= 3
                toppled.add(i)
                for j in adj[i]:
                    chips[j] += 1
                break
        else:
            return len(toppled), tuple(chips)


def candidates(n):
    m = 2 * n
    for i in range(m):
        h = [2] * m
        h[i] = 0
        yield tuple(h)
    for i, j in combinations(range(m), 2):
        h = [2] * m
        h[i] = h[j] = 1
        yield tuple(h)


def plain_candidates(n):
    # Independently enumerate every height vector with deficit exactly two.
    m = 2 * n
    h = [0] * m

    def visit(i, deficit):
        if i == m:
            if deficit == 0:
                yield tuple(h)
            return
        for height in range(3):
            cost = 2 - height
            if cost <= deficit <= cost + 2 * (m - i - 1):
                h[i] = height
                yield from visit(i + 1, deficit - cost)

    yield from visit(0, 2)


def claimed(n):
    coefficients = Counter()
    coefficients[0] += 2 * n
    coefficients[1] += 1
    for j in range(1, n):
        coefficients[2 * j] += 1
    coefficients[2 * n - 1] += 3
    coefficients[2 * n] += 2 * n * n - 2 * n - 3
    return dict(sorted(coefficients.items()))


def literal_claim_again(n):
    # Second computation directly as a coefficient array.
    c = [0] * (2 * n + 1)
    c[0] = 2 * n
    c[1] += 1
    for j in range(1, n):
        c[2 * j] += 1
    c[2 * n - 1] += 3
    c[2 * n] += 2 * n**2 - 2 * n - 3
    return {i: value for i, value in enumerate(c) if value}


def histogram(n, plain=False):
    adj = graph(n)
    counts = Counter()
    tested = 0
    generate = plain_candidates if plain else candidates
    burn = plain_recurrent if plain else recurrent
    stabilize = plain_avalanche if plain else avalanche
    for h in generate(n):
        tested += 1
        if burn(h, adj):
            counts[stabilize(h, adj)[0]] += 1
    return dict(sorted(counts.items())), tested


def fail(message):
    print("SANITY FAILED:", message)
    sys.exit(0)


def sanity_checks():
    # Known values, independent of the proposed polynomial.
    for n in range(2, 13):
        adj = graph(n)
        maximum = (2,) * (2 * n)
        zero = (0,) * (2 * n)
        if not recurrent(maximum, adj) or recurrent(zero, adj):
            fail("maximum/zero burning checks")
        if avalanche(maximum, adj)[0] != 2 * n:
            fail("all-height-two avalanche must reach every vertex")
        if avalanche(zero, adj) != (0, (1,) + (0,) * (2 * n - 1)):
            fail("zero configuration receives one chip without toppling")
    print("SANITY 1 PASSED: known burning and avalanche values, n=2..12")

    # Full ternary brute force, including configurations outside the target
    # height slice solely as implementation checks, not claim witnesses.
    checked = 0
    for n in (2, 3):
        adj = graph(n)
        target = set()
        full_hist = Counter()
        for h in product(range(3), repeat=2 * n):
            checked += 1
            r = plain_recurrent(h, adj)
            if recurrent(h, adj) != r:
                fail("burning implementations disagree")
            if avalanche(h, adj) != plain_avalanche(h, adj):
                fail("stabilization implementations disagree")
            if sum(h) == 4 * n - 2:
                target.add(h)
                if r:
                    full_hist[plain_avalanche(h, adj)[0]] += 1
        generated = list(candidates(n))
        if len(generated) != len(set(generated)) or set(generated) != target:
            fail("candidate enumeration disagrees with full ternary enumeration")
        if set(plain_candidates(n)) != target:
            fail("recursive enumeration disagrees with full ternary enumeration")
        if histogram(n)[0] != dict(sorted(full_hist.items())):
            fail("histogram disagrees with full ternary enumeration")
    print(f"SANITY 2 PASSED: independent full brute-force cross-check, {checked} configurations")


def main():
    sanity_checks()
    tested_total = 0
    for n in range(2, 13):
        actual, tested = histogram(n)
        tested_total += tested
        expected = claimed(n)
        if actual != expected:
            confirmed, confirmed_count = histogram(n, plain=True)
            expected_again = literal_claim_again(n)
            if confirmed != actual or confirmed_count != tested:
                fail("independent witness recomputation disagrees")
            if expected_again != expected:
                fail("independent formula recomputation disagrees")
            if confirmed != expected_again:
                print(
                    "COUNTEREXAMPLE:",
                    f"n={n}; brute-force coefficients={confirmed}; "
                    f"claimed coefficients={expected_again}; "
                    f"stable configurations tested={confirmed_count}"
                )
                return
    print(
        "NO COUNTEREXAMPLE",
        f"n=2..12 inclusive; all stable configurations with |eta|=4n-2; "
        f"cases tested={tested_total}"
    )


if __name__ == "__main__":
    main()