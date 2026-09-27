from itertools import product

# Reported witness; do not search for another.
n, a, p = 3, 4, 10

def connected(cells):
    if not cells:
        return False
    seen = {next(iter(cells))}
    pending = list(seen)
    while pending:
        row, col = pending.pop()
        for neighbor in ((row - 1, col), (row + 1, col),
                         (row, col - 1), (row, col + 1)):
            if neighbor in cells and neighbor not in seen:
                seen.add(neighbor)
                pending.append(neighbor)
    return seen == cells

def perimeter(cells):
    total = 0
    for row, col in cells:
        for neighbor in ((row - 1, col), (row + 1, col),
                         (row, col - 1), (row, col + 1)):
            if neighbor not in cells:
                total += 1
    return total

if not all(type(value) is int for value in (n, a, p)):
    print("REFUTATION REJECTED: n, a, and p must be integers")
elif n < 2 or a < 0 or p < 0:
    print("REFUTATION REJECTED: n must be at least 2 and a, p nonnegative")
elif not (a % 2 == 1 or p % 4 != (2 * (n - 1)) % 4):
    print("REFUTATION REJECTED: the claim imposes no evenness conclusion here")
else:
    positions = [(row, col) for row in range(2) for col in range(n)]
    count = 0
    for choices in product((False, True), repeat=len(positions)):
        cells = {cell for cell, occupied in zip(positions, choices) if occupied}
        if cells & {(0, 0), (1, 0)} != {(0, 0)}:
            continue
        if cells & {(0, n - 1), (1, n - 1)} != {(1, n - 1)}:
            continue
        if len(cells) == a and perimeter(cells) == p and connected(cells):
            count += 1

    claimed_parity = 0  # The applicable conclusion says C(n,a,p) is even.
    actual_parity = count % 2
    if actual_parity != claimed_parity:
        print(f"REFUTATION CONFIRMED: n={n}, a={a}, p={p}; "
              f"C(n,a,p)={count}, actual parity={actual_parity}, "
              f"claimed parity={claimed_parity}")
    else:
        print(f"REFUTATION REJECTED: C(n,a,p)={count} has the claimed even parity")