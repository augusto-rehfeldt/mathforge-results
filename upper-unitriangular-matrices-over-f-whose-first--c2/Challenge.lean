import Mathlib

namespace Mathforge.UpperUnitriangularMatricesOverFWhoseFirstC2

def admissible (n : ℕ) (A : Matrix (Fin n) (Fin n) (ZMod 2)) : Prop :=
  ∀ i j,
    (i = j → A i j = 1) ∧
    (i.val + 1 = j.val → A i j = 1) ∧
    (i.val ≠ j.val ∧ i.val + 1 ≠ j.val ∧ i.val + 2 ≠ j.val →
      A i j = 0)

def hasSecond (n : ℕ) (A : Matrix (Fin n) (Fin n) (ZMod 2)) : Prop :=
  ∃ i j, i.val + 2 = j.val ∧ A i j ≠ 0

def endPattern (n : ℕ) (A : Matrix (Fin n) (Fin n) (ZMod 2)) : Prop :=
  ∃ k : Fin n,
    (k.val = 0 ∨ k.val + 3 = n) ∧
      ∀ i j, i.val + 2 = j.val → (A i j ≠ 0 ↔ i = k)

def inverseWeight (n : ℕ) (B : Matrix (Fin n) (Fin n) (ZMod 2)) : ℕ :=
  ∑ i : Fin n, ∑ j : Fin n, if i < j ∧ B i j ≠ 0 then 1 else 0

def claimedBound (n : ℕ) : ℕ :=
  n * (n - 1) / 2 - (n - 2)

def witnessA : Matrix (Fin 6) (Fin 6) (ZMod 2) :=
  fun i j =>
    if i.val = j.val ∨ i.val + 1 = j.val ∨
        ((i.val = 0 ∨ i.val = 1) ∧ i.val + 2 = j.val)
    then 1 else 0

def witnessB : Matrix (Fin 6) (Fin 6) (ZMod 2) :=
  fun i j =>
    if i = j ∨
        (i.val = 0 ∧ (j.val = 1 ∨ 3 ≤ j.val)) ∨
        (i.val = 1 ∧ j.val = 2) ∨
        (2 ≤ i.val ∧ i.val < j.val)
    then 1 else 0

-- FAITHFULNESS: `n` ranges over all integers n ≥ 6, represented by natural
-- numbers since the matrix size cannot be negative. `A` ranges over all
-- matrices; `admissible` imposes the unit diagonal, all-one first
-- superdiagonal, and zero entries outside the first two superdiagonals.
-- `hasSecond` excludes the zero second superdiagonal. `B` ranges over right
-- inverses of `A`; a square matrix over a field has at most one right inverse,
-- so every such `B` is precisely A⁻¹. `inverseWeight` counts its nonzero
-- entries above the diagonal. `endPattern` says the second superdiagonal has
-- exactly one one, in its first or last position.
theorem refutation :
    ¬ (∀ (n : ℕ), 6 ≤ n →
      ∀ (A : Matrix (Fin n) (Fin n) (ZMod 2)),
        admissible n A →
        hasSecond n A →
        ∀ (B : Matrix (Fin n) (Fin n) (ZMod 2)),
          A * B = 1 →
          inverseWeight n B ≤ claimedBound n ∧
            (inverseWeight n B = claimedBound n ↔ endPattern n A)) := by
  sorry

end Mathforge.UpperUnitriangularMatricesOverFWhoseFirstC2
