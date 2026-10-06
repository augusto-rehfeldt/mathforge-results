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
  sorry

end Mathforge.ApRySetsASSSMSOfNumericalSemigroupsSC2
