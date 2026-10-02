#!/usr/bin/env python3
from itertools import product
from functools import lru_cache
import sys

MIN_N, MAX_N = 3, 14


def prefix_occurrences(word):
    """List all occurrences using three-letter prefix counts."""
    pref = [(0, 0, 0)]
    for letter in word:
        row = list(pref[-1])
        row[letter] += 1
        pref.append(tuple(row))
    result = []
    n = len(word)
    for a in range(n):
        for k in range(1, (n - a) // 2 + 1):
            if all(pref[a + k][c] - pref[a][c] ==
                   pref[a + 2 * k][c] - pref[a + k][c]
                   for c in range(3)):
                result.append((a, k))
    return sorted(result)


def plain_occurrences(word):
    """Independent, direct slice-and-count implementation."""
    result = []
    for a in range(len(word)):
        for k in range(1, (len(word) - a) // 2 + 1):
            left = word[a:a + k]
            right = word[a + k:a + 2 * k]
            if all(left.count(c) == right.count(c) for c in (0, 1, 2)):
                result.append((a, k))
    return sorted(result)


def ending_occurrences(pref):
    """All occurrences ending at the current prefix's right boundary."""
    b = len(pref) - 1
    result = []
    end = pref[b]
    for k in range(1, b // 2 + 1):
        start, middle = pref[b - 2 * k], pref[b - k]
        if (end[0] + start[0] == 2 * middle[0] and
                end[1] + start[1] == 2 * middle[1] and
                end[2] + start[2] == 2 * middle[2]):
            result.append((b - 2 * k, k))
    return result


def fail():
    print("SANITY FAILED")
    sys.exit(0)


# Sanity check 1: explicit, independently known small examples.
known = [
    ((), []),
    ((0,), []),
    ((0, 0), [(0, 1)]),
    ((0, 0, 0, 0), [(0, 1), (0, 2), (1, 1), (2, 1)]),
    ((0, 1, 0, 1), [(0, 2)]),
    ((0, 1, 2, 0, 1, 2), [(0, 3)]),
]
for word, expected in known:
    if prefix_occurrences(word) != expected or plain_occurrences(word) != expected:
        fail()
print("Sanity 1: known small occurrence lists passed.", flush=True)

# Sanity check 2: every ternary word through length 7, including the
# incremental boundary routine used by the exhaustive search.
cross_checked = 0
for n in range(8):
    for word in product(range(3), repeat=n):
        pref = [(0, 0, 0)]
        incremental = []
        for letter in word:
            row = list(pref[-1])
            row[letter] += 1
            pref.append(tuple(row))
            incremental.extend(ending_occurrences(pref))
        expected = plain_occurrences(word)
        if prefix_occurrences(word) != expected or sorted(incremental) != expected:
            fail()
        cross_checked += 1
print("Sanity 2: prefix and incremental routines match direct counting on",
      cross_checked, "words.", flush=True)


@lru_cache(None)
def canonical_completions(distinct, remaining):
    """Number of canonical extensions of a prefix using 'distinct' letters."""
    if remaining == 0:
        return 1
    total = distinct * canonical_completions(distinct, remaining - 1)
    if distinct < 3:
        total += canonical_completions(distinct + 1, remaining - 1)
    return total


# Sanity check 3: validate the counting routine used for pruned subtrees.
for n in range(8):
    explicit = 0
    for word in product(range(3), repeat=n):
        distinct = 0
        valid = True
        for letter in word:
            if letter > distinct:
                valid = False
                break
            if letter == distinct:
                distinct += 1
        explicit += valid
    if explicit != canonical_completions(0, n):
        fail()
print("Sanity 3: canonical-extension counts passed.", flush=True)

word = []
pref = [(0, 0, 0)]
examined = {n: 0 for n in range(MIN_N, MAX_N + 1)}
eliminated = {n: 0 for n in range(MIN_N, MAX_N + 1)}
retained = 0


def search(distinct, occurrences):
    global retained
    n = len(word)

    if n >= MIN_N:
        examined[n] += 1

    # Occurrences already present cannot disappear upon extension.
    # Thus every descendant of this node is outside the hypotheses.
    if len(occurrences) > 2:
        for target in range(max(MIN_N, n + 1), MAX_N + 1):
            eliminated[target] += canonical_completions(distinct, target - n)
        return

    if n >= MIN_N and len(occurrences) == 2:
        (i, h), (j, other_h) = sorted(occurrences)
        if (h == other_h and h >= 1 and
                0 <= i < j < i + 2 * h <= n and j + 2 * h <= n):
            retained += 1
            # Literal claimed equality: j = i + 1.
            lhs, rhs = j, i + 1
            if lhs != rhs:
                witness = tuple(word)
                direct = plain_occurrences(witness)
                second_prefix = prefix_occurrences(witness)
                if direct != second_prefix or direct != sorted(occurrences):
                    fail()
                if len(direct) != 2:
                    fail()
                (ii, hh), (jj, hh2) = direct
                hypotheses = (
                    hh == hh2 and hh >= 1 and
                    0 <= ii < jj < ii + 2 * hh <= len(witness) and
                    jj + 2 * hh <= len(witness)
                )
                lhs2, rhs2 = jj, ii + 1
                if not hypotheses or (lhs2, rhs2) != (lhs, rhs):
                    fail()
                if lhs2 != rhs2:
                    print("COUNTEREXAMPLE:",
                          "w=" + "".join(map(str, witness)),
                          "n=" + str(len(witness)),
                          "occurrences=" + repr(direct),
                          "j=" + str(lhs2),
                          "i+1=" + str(rhs2))
                    sys.exit(0)

    if n == MAX_N:
        return

    # Restricted-growth words: first new letters occur in order 0,1,2.
    for letter in range(min(distinct + 1, 3)):
        word.append(letter)
        row = list(pref[-1])
        row[letter] += 1
        pref.append(tuple(row))
        search(max(distinct, letter + 1),
               occurrences + ending_occurrences(pref))
        pref.pop()
        word.pop()


search(0, [])

for n in range(MIN_N, MAX_N + 1):
    if examined[n] + eliminated[n] != canonical_completions(0, n):
        fail()

print("NO COUNTEREXAMPLE",
      f"lengths={MIN_N}..{MAX_N}; alphabet={{0,1,2}};",
      "first appearances ordered 0,1,2;",
      f"cases tested={sum(examined.values())};",
      f"additional cases rigorously eliminated={sum(eliminated.values())};",
      f"total canonical words covered={sum(examined.values()) + sum(eliminated.values())};",
      f"hypothesis-satisfying cases tested={retained};",
      "per-length (tested, eliminated)=" +
      repr({n: (examined[n], eliminated[n]) for n in examined}))
sys.exit(0)