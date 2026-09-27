import Mathlib

namespace Mathforge.ConnectedCellSetsInA2NStripThatMeetBotC1

set_option maxRecDepth 2048
set_option maxHeartbeats 0

def adjacent {n : ℕ} (x y : Fin 2 × Fin n) : Prop :=
  (x.1 = y.1 ∧
    (x.2.val + 1 = y.2.val ∨ y.2.val + 1 = x.2.val)) ∨
  (x.2 = y.2 ∧
    (x.1.val + 1 = y.1.val ∨ y.1.val + 1 = x.1.val))

instance {n : ℕ} : DecidableRel (@adjacent n) := by
  intro x y
  unfold adjacent
  infer_instance

def connected {n : ℕ} (s : Finset (Fin 2 × Fin n)) : Prop :=
  ∀ t ∈ s.powerset, t.Nonempty → (s \ t).Nonempty →
    ∃ x ∈ t, ∃ y ∈ s \ t, adjacent x y

instance {n : ℕ} (s : Finset (Fin 2 × Fin n)) :
    Decidable (connected s) := by
  unfold connected
  infer_instance

def perimeter {n : ℕ} (s : Finset (Fin 2 × Fin n)) : ℕ :=
  s.sum fun x => 4 - (s.filter (adjacent x)).card

def stripCount (n a p : ℕ) : ℕ :=
  (Finset.univ.powerset.filter fun s : Finset (Fin 2 × Fin n) =>
    connected s ∧
    (∃ x ∈ s, x.1 = (0 : Fin 2) ∧ x.2.val = 0) ∧
    ¬ (∃ x ∈ s, x.1 = (1 : Fin 2) ∧ x.2.val = 0) ∧
    ¬ (∃ x ∈ s, x.1 = (0 : Fin 2) ∧ x.2.val + 1 = n) ∧
    (∃ x ∈ s, x.1 = (1 : Fin 2) ∧ x.2.val + 1 = n) ∧
    s.card = a ∧ perimeter s = p).card

-- FAITHFULNESS: `n a p : ℤ` are the three informal integer quantifiers, with
-- their lower bounds stated explicitly. `stripCount` enumerates all occupied
-- subsets of the 2 × n strip; `toNat` is used only after those bounds hold.
-- The four membership tests say that the first column is top-only and the
-- last column is bottom-only. `adjacent` means sharing an edge. `connected`
-- uses the equivalent condition that every cut into two nonempty occupied
-- parts has an adjacent pair across it. Each occupied cell contributes four
-- edges minus its occupied neighbours to `perimeter`. The final implication
-- is precisely the claimed parity condition and conclusion.
theorem refutation :
    ¬ (∀ n a p : ℤ, 2 ≤ n → 0 ≤ a → 0 ≤ p →
      (Odd a ∨ p % 4 ≠ (2 * (n - 1)) % 4) →
      Even (stripCount n.toNat a.toNat p.toNat)) := by
  intro h
  have hc : stripCount 3 4 10 = 1 := by decide
  have he : Even (stripCount 3 4 10) :=
    h 3 4 10 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  rw [hc] at he
  norm_num at he

end Mathforge.ConnectedCellSetsInA2NStripThatMeetBotC1
