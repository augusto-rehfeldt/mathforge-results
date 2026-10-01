from collections import Counter

def positive_difference_multiset(S):
    counts = Counter()
    for s in S:
        for t in S:
            if s < t:
                counts[t - s] += 1
    return counts

def main():
    witness = {
        "n": 11,
        "A": [0, 1, 2, 6, 8, 11],
        "B": [0, 1, 6, 7, 9, 11],
    }
    n = witness["n"]
    raw_A, raw_B = witness["A"], witness["B"]

    if type(n) is not int or n < 1:
        print("REFUTATION REJECTED: n must be an integer at least 1")
        return
    if any(type(a) is not int or not 0 <= a <= n
           for a in raw_A + raw_B):
        print("REFUTATION REJECTED: A and B must be subsets of {0,...,n}")
        return

    A, B = set(raw_A), set(raw_B)
    if not ({0, n} <= A and {0, n} <= B):
        print("REFUTATION REJECTED: both sets must contain 0 and n")
        return

    differences_A = positive_difference_multiset(A)
    differences_B = positive_difference_multiset(B)
    if differences_A != differences_B:
        print("REFUTATION REJECTED: positive difference multisets differ")
        return

    A_minus_B = {a for a in A if a not in B}
    if len(A_minus_B) > 2:
        print("REFUTATION REJECTED: |A\\B| exceeds 2")
        return
    if len(A) != len(B):
        print("REFUTATION REJECTED: implied equal cardinalities fail")
        return

    reflection_A = {n - a for a in A}
    conclusion = (A == B) or (B == reflection_A)
    if conclusion:
        print("REFUTATION REJECTED: the claim's conclusion holds")
        return

    both_sides = {
        "hypotheses": True,
        "conclusion_A_equals_B_or_B_equals_reflection_of_A": conclusion,
        "A_equals_B": A == B,
        "B_equals_reflection_of_A": B == reflection_A,
        "reflection_of_A": sorted(reflection_A),
        "A_minus_B": sorted(A_minus_B),
        "difference_multiplicities_A": dict(sorted(differences_A.items())),
        "difference_multiplicities_B": dict(sorted(differences_B.items())),
    }
    print("REFUTATION CONFIRMED:", witness, both_sides)

if __name__ == "__main__":
    main()