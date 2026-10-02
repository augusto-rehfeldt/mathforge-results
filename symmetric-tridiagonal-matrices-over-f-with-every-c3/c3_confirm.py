from itertools import permutations, product

# Polynomials over F_2 are encoded as integers: bit i is the x^i coefficient.
def poly_add(a, b):
    return a ^ b

def poly_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result

def poly_eval(p, a):
    result = 0
    for i in range(p.bit_length()):
        if (p >> i) & 1:
            result ^= a ** i
    return result

def poly_derivative(p):
    result = 0
    for i in range(1, p.bit_length(), 2):
        if (p >> i) & 1:
            result ^= 1 << (i - 1)
    return result

def reverse(t):
    return tuple(reversed(t))

def M(t):
    n = len(t)
    return [
        [t[i] if i == j else int(abs(i - j) == 1)
         for j in range(n)]
        for i in range(n)
    ]

def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

def add_matrices(A, B):
    return [[a ^ b for a, b in zip(row_a, row_b)]
            for row_a, row_b in zip(A, B)]

def multiply_matrices(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] ^= A[i][k] & B[k][j]
    return result

def p(t):
    if not t:
        return 1
    A = M(t)
    n = len(t)
    # Literal determinant expansion of xI + M(t).
    # In characteristic two all permutation signs equal 1.
    entries = [
        [A[i][j] ^ (2 if i == j else 0) for j in range(n)]
        for i in range(n)
    ]
    result = 0
    for permutation in permutations(range(n)):
        term = 1
        for i, j in enumerate(permutation):
            term = poly_mul(term, entries[i][j])
        result = poly_add(result, term)
    return result

def q(t):
    if not t:
        raise ValueError("q requires a nonempty word")
    return p(t[:-1])

def r(t):
    if not t:
        raise ValueError("r requires a nonempty word")
    return 0 if len(t) == 1 else p(t[1:-1])

def B(t):
    return (poly_eval(p(t), 0), poly_eval(q(t), 0),
            poly_eval(p(t), 1), poly_eval(q(t), 1))

def kernel_dimension(A):
    # Enumerate every vector, rather than using a rank algorithm.
    n = len(A)
    count = 0
    for vector in product((0, 1), repeat=n):
        image = []
        for row in A:
            value = 0
            for coefficient, coordinate in zip(row, vector):
                value ^= coefficient & coordinate
            image.append(value)
        if not any(image):
            count += 1
    dimension = 0
    while count > 1:
        if count % 2:
            raise ValueError("Kernel size is not a power of two")
        count //= 2
        dimension += 1
    return dimension

def generalized_kernel_dimension(A, a):
    shifted = add_matrices(
        A, [[a * entry for entry in row] for row in identity(len(A))]
    )
    return kernel_dimension(multiply_matrices(shifted, shifted))

def claimed_dimension(u, v, a):
    # f_a(x) = p_u(a) p_v(x) + q_u(a) r_v(x), literally.
    f = poly_add(
        poly_mul(poly_eval(p(u), a), p(v)),
        poly_mul(poly_eval(q(u), a), r(v))
    )
    if poly_eval(f, a) == 1:
        return 0
    if poly_eval(poly_derivative(f), a) == 1:
        return 1
    return 2

def main():
    witness = {
        "relation": "identity",
        "u": (0,),
        "v": (0, 1),
        "matrix_dimension": 4
    }
    u, v = witness["u"], witness["v"]

    if witness["relation"] != "identity":
        print("REFUTATION REJECTED: reported relation is not the identity")
        return
    for name, word in (("u", u), ("v", v)):
        if not isinstance(word, tuple) or not word:
            print("REFUTATION REJECTED: " + name + " is not a nonempty word")
            return
        if any(type(letter) is not int or letter not in (0, 1)
               for letter in word):
            print("REFUTATION REJECTED: " + name + " is not binary")
            return

    t = u + v + reverse(u)
    A = M(t)
    expected_size = 2 * len(u) + len(v)
    if (len(A) != expected_size
            or any(len(row) != expected_size for row in A)
            or witness["matrix_dimension"] != expected_size):
        print("REFUTATION REJECTED: matrix dimension does not match the claim")
        return

    parameters = (0, 1)
    if any(a not in (0, 1) for a in parameters):
        print("REFUTATION REJECTED: parameter a is outside F_2")
        return

    direct = tuple(generalized_kernel_dimension(A, a) for a in parameters)
    claimed = tuple(claimed_dimension(u, v, a) for a in parameters)
    if direct != claimed:
        print("REFUTATION CONFIRMED:", witness,
              "direct =", direct, "claimed =", claimed)
    else:
        print("REFUTATION REJECTED: the literal identity agrees at the witness")

if __name__ == "__main__":
    main()