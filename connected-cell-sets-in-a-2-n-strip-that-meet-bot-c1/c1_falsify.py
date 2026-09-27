from collections import Counter
from itertools import product


def count_by_columns(n):
    """Enumerate the three allowed states of each intermediate column."""
    counts = Counter()
    for middle in product((1, 2, 3), repeat=n - 2):
        columns = (1,) + middle + (2,)  # 1=top, 2=bottom, 3=both
        cells = {
            (row, col)
            for col, state in enumerate(columns)
            for row, bit in ((0, 1), (1, 2))
            if state & bit
        }

        reached = {next(iter(cells))}
        stack = list(reached)
        while stack:
            row, col = stack.pop()
            for neighbor in (
                (row - 1, col), (row + 1, col),
                (row, col - 1), (row, col + 1),
            ):
                if neighbor in cells and neighbor not in reached:
                    reached.add(neighbor)
                    stack.append(neighbor)
        if len(reached) != len(cells):
            continue

        perimeter = sum(
            neighbor not in cells
            for row, col in cells
            for neighbor in (
                (row - 1, col), (row + 1, col),
                (row, col - 1), (row, col + 1),
            )
        )
        counts[(len(cells), perimeter)] += 1
    return counts


def count_by_all_subsets(n):
    """Independent brute force over every subset of the 2n cells."""
    counts = Counter()

    def occupied(mask, row, col):
        return 0 <= row < 2 and 0 <= col < n and bool(mask & (1 << (2 * col + row)))

    for mask in range(1 << (2 * n)):
        if not (occupied(mask, 0, 0) and not occupied(mask, 1, 0)):
            continue
        if not (occupied(mask, 1, n - 1) and not occupied(mask, 0, n - 1)):
            continue

        cells = [(row, col) for col in range(n) for row in range(2)
                 if occupied(mask, row, col)]
        reached = {(0, 0)}
        frontier = [(0, 0)]
        while frontier:
            row, col = frontier.pop(0)
            for r, c in ((row - 1, col), (row + 1, col),
                         (row, col - 1), (row, col + 1)):
                if occupied(mask, r, c) and (r, c) not in reached:
                    reached.add((r, c))
                    frontier.append((r, c))
        if len(reached) != len(cells):
            continue

        perimeter = 0
        for row, col in cells:
            for r, c in ((row - 1, col), (row + 1, col),
                         (row, col - 1), (row, col + 1)):
                if not occupied(mask, r, c):
                    perimeter += 1
        counts[(len(cells), perimeter)] += 1
    return counts


def sanity_fail():
    print("SANITY FAILED")
    raise SystemExit(0)


# Check known small values independently of the exhaustive cross-check.
if count_by_columns(2) != Counter() or count_by_columns(3) != Counter({(4, 10): 1}):
    sanity_fail()
print("SANITY OK: known n=2 and n=3 counts")

# Check the column enumeration against unrestricted subset enumeration.
for n in range(2, 6):
    if count_by_columns(n) != count_by_all_subsets(n):
        sanity_fail()
print("SANITY OK: independent all-subsets cross-check for n=2..5")

cases_tested = 0
for n in range(2, 13):
    counts = count_by_columns(n)
    for (a, p), count in sorted(counts.items()):
        cases_tested += 1
        claimed_even = (a % 2 == 1 or p % 4 != (2 * (n - 1)) % 4)
        if claimed_even and count % 2 != 0:
            # Recompute both sides before reporting, using plain all-subsets brute force.
            fresh_count = count_by_all_subsets(n)[(a, p)]
            fresh_claimed_even = (a % 2 == 1 or p % 4 != (2 * (n - 1)) % 4)
            if fresh_claimed_even and fresh_count % 2 != 0:
                print(
                    f"COUNTEREXAMPLE: n={n}, a={a}, p={p}; "
                    f"C(n,a,p)={fresh_count} (parity {fresh_count % 2}), "
                    "claimed parity=0"
                )
                raise SystemExit(0)

print(
    "NO COUNTEREXAMPLE "
    f"n=2..12, all attainable (a,p) for the specified connected sets; "
    f"cases tested={cases_tested}"
)