#!/usr/bin/env python3
import itertools
import json
import sys
import time

LIMIT = 16
TIME_BUDGET = 225.0


def brute_occurrences(word):
    """Direct implementation using independently counted half-words."""
    occurrences = []
    for i in range(len(word)):
        for h in range(1, (len(word) - i) // 2 + 1):
            left = word[i:i + h]
            right = word[i + h:i + 2 * h]
            if all(left.count(c) == right.count(c) for c in (0, 1, 2)):
                occurrences.append((i + 1, h))
    return sorted(occurrences)


def prefix_occurrences(word):
    """Two prefix counts suffice because the compared lengths are equal."""
    zeros, ones = [0], [0]
    occurrences = []
    for length, c in enumerate(word, 1):
        zeros.append(zeros[-1] + (c == 0))
        ones.append(ones[-1] + (c == 1))
        for h in range(1, length // 2 + 1):
            middle, start = length - h, length - 2 * h
            if (zeros[length] + zeros[start] == 2 * zeros[middle]
                    and ones[length] + ones[start] == 2 * ones[middle]):
                occurrences.append((start + 1, h))
    return sorted(occurrences)


def sanity_checks():
    known = [
        ((), []),
        ((0,), []),
        ((0, 0), [(1, 1)]),
        ((0, 1, 0, 1), [(1, 2)]),
        ((0, 1, 1, 0), [(1, 2), (2, 1)]),
        ((0, 0, 0), [(1, 1), (2, 1)]),
    ]
    for word, expected in known:
        if brute_occurrences(word) != expected or prefix_occurrences(word) != expected:
            print("SANITY FAILED: known example", word, flush=True)
            sys.exit(0)

    histogram = [0, 0, 0]
    for word in itertools.product(range(3), repeat=3):
        histogram[len(brute_occurrences(word))] += 1
    if histogram != [12, 12, 3]:
        print("SANITY FAILED: length-three histogram", histogram, flush=True)
        sys.exit(0)
    print("Sanity 1 passed: known examples and length-three histogram.", flush=True)

    checked = 0
    for n in range(7):
        for word in itertools.product(range(3), repeat=n):
            if prefix_occurrences(word) != brute_occurrences(word):
                print("SANITY FAILED: independent routine cross-check", word, flush=True)
                sys.exit(0)
            checked += 1
    print("Sanity 2 passed: brute-force cross-check of", checked, "words.", flush=True)


class DeadlineReached(Exception):
    pass


def main():
    sanity_checks()
    deadline = time.monotonic() + TIME_BUDGET
    nodes = 0
    completed_length = 0
    completed_cases = 0
    completed_hypothesis_cases = 0

    def inspect(word, occurrences):
        if len(occurrences) != 2:
            return False
        (a, p), (b, q) = sorted(occurrences)
        n = len(word)
        if not (p >= 1 and q >= 1
                and 1 <= a < b <= a + 2 * p - 1
                < b + 2 * q - 1 <= n):
            return False

        lhs = n + a + 2 * p - b
        rhs = 15
        if lhs > rhs:
            # Recompute every occurrence and every hypothesis independently.
            verified = brute_occurrences(tuple(word))
            if len(verified) != 2:
                print("SANITY FAILED: witness occurrence count", flush=True)
                sys.exit(0)
            (aa, pp), (bb, qq) = verified
            nn = len(word)
            hypotheses = (
                nn >= 1 and all(c in (0, 1, 2) for c in word)
                and pp >= 1 and qq >= 1
                and 1 <= aa < bb <= aa + 2 * pp - 1
                < bb + 2 * qq - 1 <= nn
            )
            second_lhs = nn + aa + 2 * pp - bb
            second_rhs = 15
            if not hypotheses or second_lhs != lhs or second_lhs <= second_rhs:
                print("SANITY FAILED: independent witness verification", flush=True)
                sys.exit(0)
            witness = {
                "word": "".join(map(str, word)),
                "n": nn,
                "intervals": [
                    [aa, aa + 2 * pp - 1],
                    [bb, bb + 2 * qq - 1],
                ],
                "p": pp,
                "q": qq,
                "t": aa + 2 * pp - bb,
                "lhs_n+a+2p-b": second_lhs,
                "rhs": second_rhs,
                "failing_relation": f"{second_lhs} <= {second_rhs}",
            }
            print("COUNTEREXAMPLE:", json.dumps(witness), flush=True)
            sys.exit(0)
        return True

    # Restricted-growth words represent every letter-renaming orbit exactly once.
    for target in range(1, LIMIT + 1):
        word = []
        zeros, ones = [0], [0]
        occurrences = []
        cases = 0
        hypothesis_cases = 0

        def dfs(largest):
            nonlocal nodes, cases, hypothesis_cases
            nodes += 1
            if nodes % 1024 == 0 and time.monotonic() >= deadline:
                raise DeadlineReached

            if len(word) == target:
                cases += 1
                if inspect(word, occurrences):
                    hypothesis_cases += 1
                return

            for c in range(min(2, largest + 1) + 1):
                word.append(c)
                zeros.append(zeros[-1] + (c == 0))
                ones.append(ones[-1] + (c == 1))
                length = len(word)
                old_count = len(occurrences)

                for h in range(1, length // 2 + 1):
                    middle, start = length - h, length - 2 * h
                    if (zeros[length] + zeros[start] == 2 * zeros[middle]
                            and ones[length] + ones[start] == 2 * ones[middle]):
                        occurrences.append((start + 1, h))
                        if len(occurrences) > 2:
                            break

                # Existing occurrences can never disappear when extending a word.
                if len(occurrences) <= 2:
                    dfs(max(largest, c))

                del occurrences[old_count:]
                zeros.pop()
                ones.pop()
                word.pop()

        try:
            dfs(-1)
        except DeadlineReached:
            # Do not claim coverage or count cases from the incomplete length.
            break

        completed_length = target
        completed_cases += cases
        completed_hypothesis_cases += hypothesis_cases

    print(
        "NO COUNTEREXAMPLE",
        f"exact ranges checked: 1 <= n <= {completed_length}, "
        "alphabet {0,1,2}, all letter-renaming orbits, "
        "prefixes with more than two occurrences pruned; "
        f"cases tested={completed_cases}; "
        f"cases satisfying all hypotheses={completed_hypothesis_cases}",
        flush=True,
    )


if __name__ == "__main__":
    main()