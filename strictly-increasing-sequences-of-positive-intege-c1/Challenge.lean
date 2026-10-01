import Mathlib

namespace Mathforge.StrictlyIncreasingSequencesOfPositiveIntegeC1

open Finset

def subsetCode {n : ℕ} (I : Finset (Fin n)) : ℕ :=
  ∑ i ∈ I, 2 ^ i.val

def balancedPair {n : ℕ} (a : Fin n → ℕ)
    (I J : Finset (Fin n)) : Prop :=
  I.Nonempty ∧ J.Nonempty ∧ Disjoint I J ∧
    subsetCode I < subsetCode J ∧
    (∑ i ∈ I, a i) = ∑ j ∈ J, a j

def coversInterval {n : ℕ} (a : Fin n → ℕ) : Prop :=
  ∀ m : Fin ((∑ i : Fin n, a i) + 1),
    ∃ I : Finset (Fin n), (∑ i ∈ I, a i) = m.val

def witness : Fin 4 → ℕ := ![1, 2, 3, 6]

-- FAITHFULNESS:
-- n ranges over all natural numbers with n ≥ 1. The indices Fin n represent
-- {1,...,n}, shifted by one. Positive natural-valued sequences represent
-- precisely the positive integer sequences; StrictMono expresses their order.
-- Finsets represent subsets, and their sums use each index at most once.
-- subsetCode is the binary encoding of a subset, hence is injective.
-- Requiring its strict inequality selects exactly one orientation of each
-- unordered pair of disjoint nonempty subsets.
-- The two displayed balanced pairs are distinct, and the biconditional says
-- that they exhaust all such pairs, expressing "exactly two".
-- coversInterval quantifies over every integer from zero to the total sum.
-- Finally, union, intersection, and card express the asserted support size.
theorem refutation :
    ¬ (∀ (n : ℕ) (a : Fin n → ℕ),
      1 ≤ n →
      (∀ i, 0 < a i) →
      StrictMono a →
      ∀ (I₁ J₁ I₂ J₂ : Finset (Fin n)),
        balancedPair a I₁ J₁ →
        balancedPair a I₂ J₂ →
        (I₁, J₁) ≠ (I₂, J₂) →
        (∀ I J : Finset (Fin n),
          balancedPair a I J ↔
            (I = I₁ ∧ J = J₁) ∨ (I = I₂ ∧ J = J₂)) →
        coversInterval a →
        ((I₁ ∪ J₁) ∩ (I₂ ∪ J₂)).card = 2) := by
  sorry

end Mathforge.StrictlyIncreasingSequencesOfPositiveIntegeC1
