import Mathlib

namespace Mathforge.ApRySetsASSSMSOfNumericalSemigroupsSC2

set_option maxHeartbeats 0

open Finset

def InS (m a b d n : ℕ) : Prop :=
  ∃ u ∈ range (n + 1), ∃ x ∈ range (n + 1),
    ∃ y ∈ range (n + 1), ∃ z ∈ range (n + 1),
      n = u * m + x * a + y * b + z * d

instance (m a b d n : ℕ) : Decidable (InS m a b d n) := by
  unfold InS
  infer_instance

def GeneratorMinimal (m a b d : ℕ) : Prop :=
  ¬ InS 0 a b d m ∧ ¬ InS m 0 b d a ∧
  ¬ InS m a 0 d b ∧ ¬ InS m a b 0 d

def Conductor (m a b d c : ℕ) : Prop :=
  (∀ n, c ≤ n → InS m a b d n) ∧
  ∀ e, (∀ n, e ≤ n → InS m a b d n) → c ≤ e

def LeftPart (m a b d c : ℕ) : Finset ℕ :=
  (range c).filter (InS m a b d)

def Ambiguous (a b d w : ℕ) : Prop :=
  ∃ x y z x' y' z' : ℕ,
    w = x * a + y * b + z * d ∧
    w = x' * a + y' * b + z' * d ∧
    (x, y, z) ≠ (x', y', z')

noncomputable def Q (m a b d c : ℕ) : ℕ := by
  classical
  exact ((range (c + m)).filter fun w =>
    InS m a b d w ∧
    (w < m ∨ ¬ InS m a b d (w - m)) ∧
    Ambiguous a b d w).card

-- FAITHFULNESS:
-- The four generators are quantified as integers, with the stated ordering;
-- consequently they are positive, and toNat preserves their values.
-- InS enumerates all nonnegative coefficient quadruples: any coefficient
-- of a positive generator in a representation of n is at most n.
-- Zero generators in GeneratorMinimal delete the corresponding generator, so its
-- four clauses express precisely the four required non-memberships.
-- The nested gcd is the gcd of all four generators.
-- Conductor states both the eventual-membership property and leastness.
-- LeftPart is S intersected with [0,c). For a conductor c, every Apéry
-- element is below c+m; the subtraction clause also includes w<m,
-- where integer subtraction is negative and hence outside S.
-- Q counts elements, not representations; Ambiguous uses two distinct
-- triples of nonnegative integers. The final inequality is in integers.
-- Universally quantifying over conductors expresses the claim for its
-- uniquely determined conductor.

lemma witness_tail : ∀ n, 18 ≤ n → InS 9 10 12 13 n := by
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    intro hn
    by_cases hsmall : n < 27
    · interval_cases n <;> decide
    · have hprev : InS 9 10 12 13 (n - 9) :=
        ih (n - 9) (by omega) (by omega)
      rcases hprev with ⟨u, hu, x, hx, y, hy, z, hz, he⟩
      simp only [mem_range] at hu hx hy hz
      refine ⟨u + 1, ?_, x, ?_, y, ?_, z, ?_, ?_⟩
      · simp only [mem_range]; omega
      · simp only [mem_range]; omega
      · simp only [mem_range]; omega
      · simp only [mem_range]; omega
      · omega

lemma witness_conductor : Conductor 9 10 12 13 18 := by
  constructor
  · exact witness_tail
  · intro e he
    by_contra h
    have he17 := he 17 (by omega)
    have hn : ¬ InS 9 10 12 13 17 := by decide
    exact hn he17

theorem refutation :
    ¬ (∀ m a b d : ℤ,
      4 ≤ m → m < a → a < b → b < d →
      Nat.gcd (Nat.gcd (Nat.gcd m.toNat a.toNat) b.toNat) d.toNat = 1 →
      a + b = m + d →
      GeneratorMinimal m.toNat a.toNat b.toNat d.toNat →
      ∀ c : ℕ, Conductor m.toNat a.toNat b.toNat d.toNat c →
      4 * (LeftPart m.toNat a.toNat b.toNat d.toNat c).card -
          (c : ℤ) ≥
        m - 4 + (Q m.toNat a.toNat b.toNat d.toNat c : ℤ)) := by
  intro h
  have hmin : GeneratorMinimal 9 10 12 13 := by
    unfold GeneratorMinimal
    decide
  have hh := h 9 10 12 13 (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    hmin 18 witness_conductor
  have hc : (LeftPart 9 10 12 13 18).card = 5 := by decide
  have hq : (0 : ℤ) ≤ (Q 9 10 12 13 18 : ℤ) :=
    Nat.cast_nonneg _
  change 4 * ((LeftPart 9 10 12 13 18).card : ℤ) - 18 ≥
    9 - 4 + (Q 9 10 12 13 18 : ℤ) at hh
  rw [hc] at hh
  omega

end Mathforge.ApRySetsASSSMSOfNumericalSemigroupsSC2
