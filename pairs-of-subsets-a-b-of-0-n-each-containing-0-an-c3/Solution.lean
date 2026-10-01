import Mathlib

namespace Mathforge.PairsOfSubsetsABOf0NEachContaining0AnC3

open Finset

def positiveDifferences (S : Finset ℤ) : Multiset ℤ :=
  ((S.product S).filter (fun p => p.1 < p.2)).val.map
    (fun p => p.2 - p.1)

-- FAITHFULNESS:
-- n ranges over integers with n ≥ 1; A and B range over finite sets of integers.
-- The bounded-membership hypotheses say they are subsets of {0,...,n}.
-- The four membership hypotheses require both endpoints in both sets.
-- positiveDifferences counts one occurrence of t-s for every s<t in the set,
-- so its equality is exactly equality of the positive-difference multisets.
-- (A \ B).card ≤ 2 is the stated overlap condition.
-- The conclusion is equality or equality with the image under a ↦ n-a.
-- Finsets faithfully represent all subsets of the finite interval {0,...,n}.
theorem refutation :
    ¬ (∀ n : ℤ, 1 ≤ n →
      ∀ A B : Finset ℤ,
        (∀ a ∈ A, 0 ≤ a ∧ a ≤ n) →
        (∀ b ∈ B, 0 ≤ b ∧ b ≤ n) →
        0 ∈ A → n ∈ A →
        0 ∈ B → n ∈ B →
        positiveDifferences A = positiveDifferences B →
        (A \ B).card ≤ 2 →
        A = B ∨ B = A.image (fun a => n - a)) := by
  intro h
  let A : Finset ℤ := {0, 1, 2, 6, 8, 11}
  let B : Finset ℤ := {0, 1, 6, 7, 9, 11}
  have conclusion : A = B ∨ B = A.image (fun a => 11 - a) :=
    h 11 (by decide) A B
      (by decide) (by decide)
      (by decide) (by decide)
      (by decide) (by decide)
      (by decide) (by decide)
  have not_conclusion : ¬ (A = B ∨ B = A.image (fun a => 11 - a)) := by
    decide
  exact not_conclusion conclusion

end Mathforge.PairsOfSubsetsABOf0NEachContaining0AnC3
