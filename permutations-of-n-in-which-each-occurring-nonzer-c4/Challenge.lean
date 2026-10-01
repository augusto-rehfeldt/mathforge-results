import Mathlib

namespace Mathforge.PermutationsOfNInWhichEachOccurringNonzerC4

open Equiv

def nextSix (i : Fin 6) : Fin 6 :=
  ⟨(i.val + 1) % 6, Nat.mod_lt _ (by decide)⟩

def displacements {n : ℕ} (π : Equiv.Perm (Fin n)) : Multiset ℤ :=
  (Finset.univ.val.map
    (fun i : Fin n => ((π i).val : ℤ) - (i.val : ℤ))).filter
      (fun d => d ≠ 0)

def Realizes (n a b c : ℤ) : Prop :=
  ∃ π : Equiv.Perm (Fin n.toNat), ∃ v : Fin 6 → Fin n.toNat,
    Function.Injective v ∧
    (∀ j, π (v j) = v (nextSix j)) ∧
    (∀ i, (∀ j, i ≠ v j) → π i = i) ∧
    (Finset.univ.filter (fun i => π i = i)).card = n.toNat - 6 ∧
    displacements π = [a, -a, b, -b, c, -c]

def witnessPerm : Equiv.Perm (Fin 7) where
  toFun := ![1, 6, 5, 2, 4, 0, 3]
  invFun := ![5, 0, 3, 6, 4, 2, 1]
  left_inv := by
    intro i
    fin_cases i <;> rfl
  right_inv := by
    intro i
    fin_cases i <;> rfl

def witnessVertices : Fin 6 → Fin 7 :=
  ![0, 1, 6, 3, 2, 5]

-- FAITHFULNESS:
-- The four universal integer quantifiers are a, b, c, and n.
-- The hypotheses express 1 ≤ a < b < c, c ≠ a+b, and n ≥ 6.
-- Fin n.toNat represents {1,...,n} by sending i to i.val+1;
-- this shift leaves every signed displacement unchanged.
-- Realizes quantifies over a bijection and six distinct cycle vertices.
-- nextSix specifies their cyclic order, and every other vertex is fixed.
-- The fixed-point cardinality explicitly records n−6 fixed points.
-- The filtered displacement multiset records exactly the six prescribed
-- nonzero signed displacements, including their multiplicities.
-- The equivalence is precisely existence iff n ≥ b+c−a+1.
theorem refutation :
    ¬ (∀ a b c n : ℤ,
      1 ≤ a → a < b → b < c → c ≠ a + b → 6 ≤ n →
      (Realizes n a b c ↔ n ≥ b + c - a + 1)) := by
  sorry

end Mathforge.PermutationsOfNInWhichEachOccurringNonzerC4
