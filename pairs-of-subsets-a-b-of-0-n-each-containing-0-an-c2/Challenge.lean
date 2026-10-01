import Mathlib

namespace Mathforge.PairsOfSubsetsABOf0NEachContaining0AnC2

open Finset

def diffCount (S : Finset ℤ) (t : ℤ) : ℕ :=
  ((S ×ˢ S).filter (fun p => p.2 - p.1 = t)).card

-- FAITHFULNESS:
-- n ranges over integers with n ≥ 1; A and B are finite subsets of
-- the integer interval {0,...,n}. They are distinct and both contain 0,n.
-- k ranges over natural numbers and is the cardinality of each set;
-- their intersection has cardinality k-2. (The endpoint conditions
-- ensure k ≥ 2, so natural subtraction agrees with the informal subtraction.)
-- diffCount counts ordered pairs with the prescribed difference, and its
-- equality is required for every integer t with 1 ≤ t ≤ n.
-- The image under a ↦ n-a is precisely the reflected set.
-- The conclusion uses integer arithmetic for n ≥ 2k-1.
theorem refutation :
    ¬ (∀ (n : ℤ), 1 ≤ n →
        ∀ (A B : Finset ℤ),
          A ⊆ Finset.Icc 0 n →
          B ⊆ Finset.Icc 0 n →
          A ≠ B →
          0 ∈ A → n ∈ A →
          0 ∈ B → n ∈ B →
          ∀ (k : ℕ),
            A.card = k →
            B.card = k →
            (A ∩ B).card = k - 2 →
            (∀ (t : ℤ), 1 ≤ t → t ≤ n →
              diffCount A t = diffCount B t) →
            B ≠ A.image (fun a => n - a) →
            n ≥ 2 * (k : ℤ) - 1) := by
  sorry

end Mathforge.PairsOfSubsetsABOf0NEachContaining0AnC2
