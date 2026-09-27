# Check only the reported witness; do not search for others.
n = 6
second_superdiagonal = [1, 1, 0, 0]


def reject(reason):
    print(f"REFUTATION REJECTED: {reason}")


def inverse_over_f2(matrix):
    size = len(matrix)
    augmented = [
        matrix[i][:] + [int(i == j) for j in range(size)]
        for i in range(size)
    ]

    for col in range(size):
        pivot = next((r for r in range(col, size) if augmented[r][col]), None)
        if pivot is None:
            return None
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        for row in range(size):
            if row != col and augmented[row][col]:
                augmented[row] = [
                    x ^ y for x, y in zip(augmented[row], augmented[col])
                ]

    return [row[size:] for row in augmented]


if n < 6:
    reject("n is less than 6")
elif len(second_superdiagonal) != n - 2:
    reject("the second superdiagonal has the wrong length")
elif any(bit not in (0, 1) for bit in second_superdiagonal):
    reject("an entry is not in F₂")
else:
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 1
        if i + 1 < n:
            A[i][i + 1] = 1
        if i + 2 < n:
            A[i][i + 2] = second_superdiagonal[i]

    valid_matrix = all(
        A[i][j] == (
            1 if j == i or j == i + 1
            else second_superdiagonal[i] if j == i + 2
            else 0
        )
        for i in range(n)
        for j in range(n)
    )

    if not valid_matrix:
        reject("A does not satisfy the stipulated matrix form")
    elif not any(second_superdiagonal):
        reject("A has a zero second superdiagonal")
    else:
        inverse = inverse_over_f2(A)
        if inverse is None:
            reject("A is not invertible")
        elif any(
            sum(A[i][k] * inverse[k][j] for k in range(n)) % 2 != int(i == j)
            for i in range(n)
            for j in range(n)
        ):
            reject("the computed inverse fails multiplication over F₂")
        else:
            weight = sum(
                inverse[i][j] != 0
                for i in range(n)
                for j in range(i + 1, n)
            )
            bound = n * (n - 1) // 2 - (n - 2)
            endpoint_single_one = (
                sum(second_superdiagonal) == 1
                and (second_superdiagonal[0] == 1
                     or second_superdiagonal[-1] == 1)
            )

            witness = f"n={n}, second superdiagonal={second_superdiagonal}"
            sides = f"inverse weight={weight}, claimed bound={bound}"
            if weight > bound or (weight == bound) != endpoint_single_one:
                print(f"REFUTATION CONFIRMED: {witness}; {sides}")
            else:
                reject(f"{witness}; {sides}; the conclusion holds")