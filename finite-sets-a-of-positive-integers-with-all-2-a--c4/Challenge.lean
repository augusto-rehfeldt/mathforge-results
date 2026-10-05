import Mathlib

namespace Mathforge.FiniteSetsAOfPositiveIntegersWithAll2AC4

open Finset

def signedSums (m : ℕ) (r : Fin m → ℤ) : Finset ℤ :=
  Finset.univ.image fun e : Fin m → Fin 3 =>
    ∑ i : Fin m, (((e i).val : ℤ) - 1) * r i

def admissible (m : ℕ) (r : Fin m → ℤ) (x y : ℤ) : Prop :=
  x ∉ signedSums m r ∧
  y ∉ signedSums m r ∧
  y - x ∉ signedSums m r ∧
  x + y ∉ signedSums m r

def witnessR (i : Fin 2) : ℤ :=
  if i.val = 0 then 1 else 6

-- FAITHFULNESS:
-- m ranges over all natural numbers with m ≥ 1, and r indexes the m
-- positive integers. Strict increase and the filtered prefix-sum inequality
-- express exactly the ordering and superincreasing hypotheses.
-- signedSums enumerates every coefficient vector in {-1,0,1}^m.
-- The universally quantified h₁,h₂ are characterized as the first two
-- positive integers outside that set by the two intervening membership
-- conditions. x,y range over all positive ordered integer pairs.
-- admissible expresses the equivalent signed-sum formulation of pairwise
-- disjointness of the four subset-sum translates. The conclusion quantifies
-- positive integers u<v≤y with u equal to one of the two gaps.
theorem refutation :
    ¬ (∀ (m : ℕ) (r : Fin m → ℤ),
      1 ≤ m →
      (∀ i, 0 < r i) →
      (∀ i j, i < j → r i < r j) →
      (∀ i : Fin m, 1 ≤ i.val →
        (∑ j ∈ Finset.univ.filter (fun j : Fin m => j < i), r j) < r i) →
      ∀ h₁ h₂ : ℤ,
        0 < h₁ →
        h₁ < h₂ →
        h₁ ∉ signedSums m r →
        h₂ ∉ signedSums m r →
        (∀ t : ℤ, 0 < t → t < h₁ → t ∈ signedSums m r) →
        (∀ t : ℤ, h₁ < t → t < h₂ → t ∈ signedSums m r) →
        ∀ x y : ℤ,
          0 < x →
          x < y →
          admissible m r x y →
          ∃ u v : ℤ,
            0 < u ∧ u < v ∧ v ≤ y ∧
            (u = h₁ ∨ u = h₂) ∧ admissible m r u v) := by
  sorry

end Mathforge.FiniteSetsAOfPositiveIntegersWithAll2AC4
