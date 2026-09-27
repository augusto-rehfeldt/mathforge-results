import Mathlib

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

private def witnessA : Matrix (Fin 6) (Fin 6) (ZMod 2) :=
  fun i j =>
    if i.val = j.val ∨ i.val + 1 = j.val ∨
        ((i.val = 0 ∨ i.val = 1) ∧ i.val + 2 = j.val)
    then 1 else 0

private def witnessB : Matrix (Fin 6) (Fin 6) (ZMod 2) :=
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
  intro claim
  have hA : admissible 6 witnessA := by
    unfold admissible
    intro i j
    fin_cases i <;> fin_cases j <;> decide
  have hSecond : hasSecond 6 witnessA := by
    unfold hasSecond
    exact ⟨0, 2, by decide, by decide⟩
  have hInverse : witnessA * witnessB = 1 := by decide
  have hWeight : inverseWeight 6 witnessB = claimedBound 6 := by decide
  have hNotEnd : ¬ endPattern 6 witnessA := by
    intro h
    unfold endPattern at h
    obtain ⟨k, _, hk⟩ := h
    have hk0 : (0 : Fin 6) = k :=
      (hk 0 2 (by decide)).mp (by decide)
    have hk1 : (1 : Fin 6) = k :=
      (hk 1 3 (by decide)).mp (by decide)
    have hne : (0 : Fin 6) ≠ 1 := by decide
    exact hne (hk0.trans hk1.symm)
  exact hNotEnd ((claim 6 (by norm_num) witnessA hA hSecond
    witnessB hInverse).2.mp hWeight)
set_option pp.fullNames true in
#print axioms refutation