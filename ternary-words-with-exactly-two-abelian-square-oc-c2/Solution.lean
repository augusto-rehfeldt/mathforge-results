import Mathlib

namespace Mathforge.TernaryWordsWithExactlyTwoAbelianSquareOcC2

open Finset

def letterCount (w : ℤ → Fin 3) (l r : ℤ) (c : Fin 3) : ℕ :=
  ((Finset.Icc l r).filter fun j => w j = c).card

def AbelianSquare (n : ℤ) (w : ℤ → Fin 3) (i h : ℤ) : Prop :=
  1 ≤ i ∧ 1 ≤ h ∧ i + 2 * h - 1 ≤ n ∧
    ∀ c : Fin 3,
      letterCount w i (i + h - 1) c =
        letterCount w (i + h) (i + 2 * h - 1) c

def witness (i : ℤ) : Fin 3 :=
  if i = 2 ∨ i = 6 then 1
  else if i = 4 ∨ i = 8 then 2
  else 0

lemma witness_exactly_two :
    ∀ i h : ℤ, AbelianSquare 9 witness i h ↔
      (i = 1 ∧ h = 4) ∨ (i = 2 ∧ h = 4) := by
  intro i h
  constructor
  · intro hs
    have hi : 1 ≤ i := hs.1
    have hh : 1 ≤ h := hs.2.1
    have hend : i + 2 * h - 1 ≤ 9 := hs.2.2.1
    have hi' : i ≤ 8 := by omega
    have hh' : h ≤ 4 := by omega
    interval_cases i <;> interval_cases h
    all_goals
      first
      | exact Or.inl ⟨rfl, rfl⟩
      | exact Or.inr ⟨rfl, rfl⟩
      | (exfalso; revert hs; unfold AbelianSquare; decide)
  · rintro (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩) <;> unfold AbelianSquare <;> decide

-- FAITHFULNESS:
-- n, a, b, p, q are integers, with positivity explicitly required.
-- A word is represented by w : ℤ → Fin 3; only positions 1 through n
-- are inspected, so values outside that interval are irrelevant.
-- AbelianSquare requires a positive start and half-length, an endpoint
-- at most n, and equal counts of every one of the three letters in
-- the two halves. The universally quantified equivalence says that
-- precisely the two specified occurrences exist. A start and half-length
-- uniquely determine an interval, so this counts occurrences by intervals.
-- The chained inequalities express the stipulated crossing overlap.
-- The conclusion is exactly n + a + 2*p - b ≤ 15.
theorem refutation :
    ¬ (∀ (n : ℤ) (w : ℤ → Fin 3) (a b p q : ℤ),
      1 ≤ n →
      1 ≤ a → 1 ≤ b → 1 ≤ p → 1 ≤ q →
      a < b →
      b ≤ a + 2 * p - 1 →
      a + 2 * p - 1 < b + 2 * q - 1 →
      b + 2 * q - 1 ≤ n →
      (∀ i h : ℤ, AbelianSquare n w i h ↔
        (i = a ∧ h = p) ∨ (i = b ∧ h = q)) →
      n + a + 2 * p - b ≤ 15) := by
  intro claim
  have bad := claim 9 witness 1 2 4 4
    (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num)
    witness_exactly_two
  norm_num at bad

end Mathforge.TernaryWordsWithExactlyTwoAbelianSquareOcC2
