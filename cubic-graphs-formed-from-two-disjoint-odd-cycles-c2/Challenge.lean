import Mathlib

namespace Mathforge.CubicGraphsFormedFromTwoDisjointOddCyclesC2

open Finset

set_option maxRecDepth 100000
set_option maxHeartbeats 0

abbrev Colors := Finset (Fin 6)

def ColorPartition (a b c : Colors) : Prop :=
  a.card = 2 ∧ b.card = 2 ∧ c.card = 2 ∧
  Disjoint a b ∧ Disjoint a c ∧ Disjoint b c ∧
  a ∪ b ∪ c = univ

def Compatible (d : Fin 4 → Colors) : Prop :=
  (∀ j, (d j).card = 2) ∧
  ∀ c : Fin 6, Even ((univ.filter fun j => c ∈ d j).card)

def Realizes (m : ℕ) (π : Equiv.Perm (Fin m))
    (d : Fin 4 → Colors) : Prop :=
  ∃ (up vp : ℕ → Colors) (cross : Fin m → Colors),
    ∀ i : Fin m,
      ColorPartition
        (if i.val = 0 then d 0 else up (i.val - 1))
        (if i.val + 1 = m then d 2 else up i.val)
        (cross i) ∧
      ColorPartition
        (if i.val = 0 then d 1 else vp (i.val - 1))
        (if i.val + 1 = m then d 3 else vp i.val)
        (cross (π.symm i))

def A : Colors := {2, 3}

def D : Colors := {4, 5}

def K : Colors := {0, 1}

def boundary : Fin 4 → Colors :=
  ![A, A, D, D]

def swapTwo : Equiv.Perm (Fin 2) :=
  Equiv.swap 0 1

-- FAITHFULNESS:
-- Positive integers m ≥ 2 are represented by naturals m ≥ 2; Even m
-- imposes the stated evenness hypothesis. Fin m represents positions
-- 1,...,m by subtracting one, which preserves whether two parities differ.
-- π ranges over every permutation. Fin 6 represents colors 1,...,6.
-- d ranges over every ordered boundary quadruple in the order u₁,v₁,uₘ,vₘ.
-- Compatible requires two colors per boundary edge and an even occurrence
-- count for each color. up k and vp k label the path edges from position
-- k to k+1 (zero-based); only k < m-1 is used. Unused function values
-- impose no condition. cross i labels u_i--v_{π(i)}, so the matching edge
-- at v_i is cross (π.symm i). ColorPartition says that the three incident
-- labels each have size two, are pairwise disjoint, and cover all colors.
-- Thus Realizes is exactly existence of the required edge assignment.
theorem refutation :
    ¬ (∀ (m : ℕ), 2 ≤ m → Even m →
      ∀ π : Equiv.Perm (Fin m),
        (∃ i : Fin m, i.val % 2 ≠ (π i).val % 2) ↔
        (∀ d : Fin 4 → Colors, Compatible d → Realizes m π d)) := by
  sorry

end Mathforge.CubicGraphsFormedFromTwoDisjointOddCyclesC2
