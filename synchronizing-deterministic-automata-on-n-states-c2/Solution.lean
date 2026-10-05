import Mathlib

namespace Mathforge.SynchronizingDeterministicAutomataOnNStatesC2

namespace Counterexample

inductive Letter
  | a | b
  deriving DecidableEq

abbrev State (p q : ℤ) := ZMod p.toNat ⊕ ZMod q.toNat

def step (p q r s : ℤ) (l : Letter) : State p q → State p q :=
  match l with
  | .a => fun x =>
      match x with
      | .inl i => .inl (i + 1)
      | .inr j => .inr (j + 1)
  | .b => fun x =>
      match x with
      | .inl i => if i = 0 then .inr (r : ZMod q.toNat) else .inl i
      | .inr j => if j = 0 then .inl (s : ZMod p.toNat) else .inr j

def run (p q r s : ℤ) : List Letter → State p q → State p q
  | [], x => x
  | l :: w, x => run p q r s w (step p q r s l x)

def Resets (p q r s : ℤ) (w : List Letter) : Prop :=
  ∃ z : State p q, ∀ x, run p q r s w x = z

def ResetExists (p q r s : ℤ) : Prop :=
  ∃ w, Resets p q r s w

abbrev WitnessState := State 3 3

def Paired (x y : WitnessState) : Prop :=
  ∃ i : ZMod 3,
    (x = Sum.inl i ∧ y = Sum.inr i) ∨
    (x = Sum.inr i ∧ y = Sum.inl i)

instance (x y : WitnessState) : Decidable (Paired x y) :=
  inferInstanceAs (Decidable (∃ i : ZMod 3,
    (x = Sum.inl i ∧ y = Sum.inr i) ∨
    (x = Sum.inr i ∧ y = Sum.inl i)))

lemma paired_step :
    ∀ (l : Letter) (x y : WitnessState),
      Paired x y → Paired (step 3 3 1 1 l x) (step 3 3 1 1 l y) := by
  intro l x y h
  rcases h with ⟨i, h | h⟩
  · rcases h with ⟨rfl, rfl⟩
    cases l with
    | a =>
        refine ⟨i + 1, ?_⟩
        simp [step]
    | b =>
        by_cases hi : i = 0
        · refine ⟨1, ?_⟩
          simp [step, hi]
        · refine ⟨i, ?_⟩
          simp [step, hi]
  · rcases h with ⟨rfl, rfl⟩
    cases l with
    | a =>
        refine ⟨i + 1, ?_⟩
        simp [step]
    | b =>
        by_cases hi : i = 0
        · refine ⟨1, ?_⟩
          simp [step, hi]
        · refine ⟨i, ?_⟩
          simp [step, hi]

lemma paired_distinct :
    ∀ (x y : WitnessState), Paired x y → x ≠ y := by
  intro x y h
  rcases h with ⟨i, h | h⟩
  · rcases h with ⟨rfl, rfl⟩
    simp
  · rcases h with ⟨rfl, rfl⟩
    simp

lemma paired_run (w : List Letter) (x y : WitnessState)
    (h : Paired x y) :
    Paired (run 3 3 1 1 w x) (run 3 3 1 1 w y) := by
  induction w generalizing x y with
  | nil => exact h
  | cons l w ih =>
      exact ih _ _ (paired_step l x y h)

lemma witness_no_reset : ¬ ResetExists 3 3 1 1 := by
  rintro ⟨w, z, hz⟩
  have h : Paired (Sum.inl 0) (Sum.inr 0) := by
    exact ⟨0, Or.inl ⟨rfl, rfl⟩⟩
  have hn := paired_distinct _ _ (paired_run w _ _ h)
  exact hn ((hz (Sum.inl 0)).trans (hz (Sum.inr 0)).symm)

-- FAITHFULNESS:
-- p,q,r,s range over integers, with precisely the stated size and index bounds.
-- For admissible p,q, ZMod p.toNat and ZMod q.toNat represent the residues
-- indexing the distinct C and D states; Sum keeps the two cycles disjoint.
-- step implements a and b, and run applies a finite word left to right.
-- ResetExists expresses existence of a word constant on every state.
-- Nat.gcd (Int.gcd p q) (r+s).natAbs is the positive three-argument gcd.
-- The conjunction states both the reset iff and the conditional length bound.
theorem refutation :
    ¬ (∀ p q r s : ℤ,
      2 ≤ p → 2 ≤ q →
      1 ≤ r → r < q → 1 ≤ s → s < p →
      (ResetExists p q r s ↔
        Nat.gcd (Int.gcd p q) (r + s).natAbs = 1) ∧
      (Nat.gcd (Int.gcd p q) (r + s).natAbs = 1 →
        ∃ w : List Letter,
          Resets p q r s w ∧
          (w.length : ℤ) ≤ (p + q - 1) ^ 2)) := by
  intro h
  have hw := h 3 3 1 1 (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  apply witness_no_reset
  exact hw.1.mpr (by norm_num)

end Counterexample

end Mathforge.SynchronizingDeterministicAutomataOnNStatesC2
