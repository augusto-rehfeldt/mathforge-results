import Mathlib

open Finset Function

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def label {n : ℕ} (i : Fin n) : ℤ := (i.val : ℤ) + 1

def displacement {n : ℕ} (p : Equiv.Perm (Fin n)) (i : Fin n) : ℤ :=
  label (p i) - label i

def displacementCount {n : ℕ} (p : Equiv.Perm (Fin n)) (d : ℤ) : ℕ :=
  (univ.filter fun i => displacement p i = d).card

def admissible {n : ℕ} (p : Equiv.Perm (Fin n)) (a b c : ℤ) : Prop :=
  displacementCount p a = 1 ∧ displacementCount p (-a) = 1 ∧
  displacementCount p b = 1 ∧ displacementCount p (-b) = 1 ∧
  displacementCount p c = 1 ∧ displacementCount p (-c) = 1 ∧
  ∀ i, displacement p i = 0 ∨
    displacement p i ∈ ([a, -a, b, -b, c, -c] : List ℤ)

instance {n : ℕ} (p : Equiv.Perm (Fin n)) (a b c : ℤ) :
    Decidable (admissible p a b c) := by
  unfold admissible
  infer_instance

-- A permutation has a cycle longer than two exactly when it is not an involution.
def longCycle {n : ℕ} (p : Equiv.Perm (Fin n)) : Prop :=
  ∃ i, p (p i) ≠ i

instance {n : ℕ} (p : Equiv.Perm (Fin n)) : Decidable (longCycle p) := by
  unfold longCycle
  infer_instance

def exceptionalCount (n : ℕ) (a b c : ℤ) : ℕ :=
  (univ.filter fun p : Equiv.Perm (Fin n) =>
    admissible p a b c ∧ longCycle p).card

def fixedCount {n : ℕ} (p : Equiv.Perm (Fin n)) : ℕ :=
  (univ.filter fun i => p i = i).card

-- Each orbit contributes exactly its least element; n iterations cover every orbit.
def cycleCount {n : ℕ} (p : Equiv.Perm (Fin n)) : ℕ :=
  (univ.filter fun i =>
    ∀ k : Fin n, i.val ≤ ((p : Fin n → Fin n)^[k.val] i).val).card

def positiveDisplacement {n : ℕ} (p : Equiv.Perm (Fin n)) : ℤ :=
  ∑ i, max (displacement p i) 0

def cycleEntries (a b c t : ℤ) : Fin 6 → ℤ :=
  ![t + b - a, t + b, t, t + c, t + c - a, t + (a + c - b)]

def prescribedCycle {n : ℕ} (p : Equiv.Perm (Fin n))
    (a b c t : ℤ) (reverse : Bool) : Prop :=
  let v := cycleEntries a b c t
  Function.Injective v ∧
  (∀ j : Fin 6, ∃ i : Fin n, label i = v j) ∧
  (∀ j : Fin 6, ∀ i : Fin n, label i = v j →
    label (p i) =
      v ⟨(j.val + if reverse then 5 else 1) % 6, Nat.mod_lt _ (by decide)⟩) ∧
  (∀ i : Fin n, (∀ j : Fin 6, label i ≠ v j) → p i = i)

def threeTranspositions {n : ℕ} (p : Equiv.Perm (Fin n)) : Prop :=
  ∃ x : Fin 6 → Fin n,
    Function.Injective x ∧
    (∀ j : Fin 6, p (x j) = x ((![1, 0, 3, 2, 5, 4] : Fin 6 → Fin 6) j)) ∧
    (∀ i : Fin n, (∀ j : Fin 6, i ≠ x j) → p i = i)

-- FAITHFULNESS:
-- n,a,b,c range over integers; n ≥ 1 makes Fin n.toNat a relabeling of [n].
-- The strict half-bound is written  n-1 < 2*a, avoiding integer division.
-- admissible says each of the six signed displacements occurs once and every
-- other displacement is zero. exceptionalCount counts precisely those members
-- with a cycle longer than two. The next conjunct gives the asserted exact
-- cycle description (including its inverse and the integer range for t).
-- The last conjunct states all three numerical consequences for exceptional
-- members and the three-transposition/fixed-point description for the rest.
theorem refutation :
    ¬ (∀ n a b c : ℤ,
      1 ≤ n →
      n - 1 < 2 * a →
      a < b →
      b < c →
      c ≤ n - 1 →
      let s := a + c - b
      ((exceptionalCount n.toNat a b c : ℤ) = 2 * (n - s)) ∧
      (∀ p : Equiv.Perm (Fin n.toNat), admissible p a b c →
        (longCycle p ↔
          ∃ t : ℤ, 1 ≤ t ∧ t ≤ n - s ∧
            ∃ reverse : Bool, prescribedCycle p a b c t reverse)) ∧
      (∀ p : Equiv.Perm (Fin n.toNat), admissible p a b c →
        (longCycle p →
          (fixedCount p : ℤ) = n - 6 ∧
          (cycleCount p : ℤ) = n - 5 ∧
          positiveDisplacement p = a + b + c) ∧
        (¬ longCycle p →
          threeTranspositions p ∧ (fixedCount p : ℤ) = n - 6))) := by
  intro h
  have hw := h 6 3 4 5 (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num)
  have computation : exceptionalCount 6 3 4 5 = 0 := by
    decide
  have hc := hw.1
  norm_num [computation] at hc
set_option pp.fullNames true in
#print axioms refutation