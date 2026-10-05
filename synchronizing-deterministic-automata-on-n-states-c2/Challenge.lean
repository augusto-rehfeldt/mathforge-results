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
  sorry

end Counterexample

end Mathforge.SynchronizingDeterministicAutomataOnNStatesC2
