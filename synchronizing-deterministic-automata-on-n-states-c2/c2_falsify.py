#!/usr/bin/env python3
import math
import time
from collections import deque


def maps(p, q, r, s):
    a = [(i + 1) % p for i in range(p)]
    a += [p + (j + 1) % q for j in range(q)]
    b = list(range(p + q))
    b[0] = p + r
    b[p] = s
    return a, b


def fast_bfs(p, q, r, s):
    """Exact subset BFS using bit masks and precomputed transitions."""
    a, b = maps(p, q, r, s)
    n = p + q
    size = 1 << n
    ta = [0] * size
    tb = [0] * size
    for mask in range(1, size):
        bit = mask & -mask
        i = bit.bit_length() - 1
        rest = mask ^ bit
        ta[mask] = ta[rest] | (1 << a[i])
        tb[mask] = tb[rest] | (1 << b[i])

    start = size - 1
    distances = [-1] * size
    distances[start] = 0
    queue = deque([start])
    while queue:
        mask = queue.popleft()
        distance = distances[mask]
        if mask & (mask - 1) == 0:
            return distance
        for nxt in (ta[mask], tb[mask]):
            if distances[nxt] == -1:
                distances[nxt] = distance + 1
                queue.append(nxt)
    return None


def plain_bfs(p, q, r, s):
    """Independent implementation: labeled states and ordinary sets."""
    states = [('C', i) for i in range(p)]
    states += [('D', j) for j in range(q)]

    def step(state, letter):
        cycle, index = state
        if letter == 'a':
            return (cycle, (index + 1) % (p if cycle == 'C' else q))
        if state == ('C', 0):
            return ('D', r)
        if state == ('D', 0):
            return ('C', s)
        return state

    start = frozenset(states)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        subset, distance = queue.popleft()
        if len(subset) == 1:
            return distance
        for letter in ('a', 'b'):
            nxt = frozenset(step(x, letter) for x in subset)
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, distance + 1))
    return None


def sanity():
    # Explicit known transitions, including both exceptional b images.
    a, b = maps(3, 4, 2, 1)
    good = (
        a == [1, 2, 0, 4, 5, 6, 3]
        and b == [5, 1, 2, 1, 4, 5, 6]
        and all(b[b[x]] == b[x] for x in range(7))
        and len(set(b)) == 5
    )
    print("SANITY 1: explicit maps and idempotence:", "PASS" if good else "FAIL")
    if not good:
        print("SANITY FAILED")
        return False

    # In the 2+2 case, {C0,D1} and {C1,D0} are disjoint
    # invariant blocks under b, exchanged by a; reset is impossible.
    good = (
        fast_bfs(2, 2, 1, 1) is None
        and plain_bfs(2, 2, 1, 1) is None
    )
    print("SANITY 2: known nonreset 2+2 case:", "PASS" if good else "FAIL")
    if not good:
        print("SANITY FAILED")
        return False

    count = 0
    for p in range(2, 5):
        for q in range(2, 7 - p):
            for r in range(1, q):
                for s in range(1, p):
                    if fast_bfs(p, q, r, s) != plain_bfs(p, q, r, s):
                        print("SANITY 3: independent BFS cross-check: FAIL",
                              (p, q, r, s))
                        print("SANITY FAILED")
                        return False
                    count += 1
    print("SANITY 3: independent BFS cross-check: PASS;", count, "cases")
    return True


def fails(distance, gcd_value, bound):
    return ((distance is not None) != (gcd_value == 1)
            or (gcd_value == 1 and distance is not None and distance > bound))


def main():
    started = time.monotonic()
    if not sanity():
        return

    checked = []
    for total in range(4, 13):
        for p in range(2, total - 1):
            q = total - p
            for r in range(1, q):
                for s in range(1, p):
                    if time.monotonic() - started > 225:
                        print("NO COUNTEREXAMPLE")
                        print("Exact checked (p,q,r,s) tuples:", checked)
                        print("Cases tested:", len(checked))
                        return

                    distance = fast_bfs(p, q, r, s)
                    gcd_value = math.gcd(math.gcd(p, q), r + s)
                    bound = (p + q - 1) ** 2

                    if fails(distance, gcd_value, bound):
                        # Recompute both sides without the optimized BFS or gcd.
                        verified_distance = plain_bfs(p, q, r, s)
                        verified_gcd = max(
                            d for d in range(1, min(p, q, r + s) + 1)
                            if p % d == q % d == (r + s) % d == 0
                        )
                        verified_bound = (p + q - 1) * (p + q - 1)
                        if verified_distance != distance:
                            print("SANITY FAILED")
                            return
                        if fails(verified_distance, verified_gcd, verified_bound):
                            if ((verified_distance is not None)
                                    != (verified_gcd == 1)):
                                print(
                                    "COUNTEREXAMPLE:",
                                    (p, q, r, s),
                                    "actual reset existence =", verified_distance is not None,
                                    "claimed reset existence =", verified_gcd == 1,
                                    "minimum length =", verified_distance,
                                    "gcd(p,q,r+s) =", verified_gcd
                                )
                            else:
                                print(
                                    "COUNTEREXAMPLE:",
                                    (p, q, r, s),
                                    "actual minimum reset length =", verified_distance,
                                    "claimed maximum =", verified_bound,
                                    "gcd(p,q,r+s) =", verified_gcd
                                )
                            return
                        print("SANITY FAILED")
                        return
                    checked.append((p, q, r, s))

    print("NO COUNTEREXAMPLE")
    print("Exact ranges: integers p,q >= 2, p+q <= 12;"
          " 1 <= r < q; 1 <= s < p.")
    print("Cases tested:", len(checked))


if __name__ == "__main__":
    main()