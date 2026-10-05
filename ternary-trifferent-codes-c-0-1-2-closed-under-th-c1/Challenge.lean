import Mathlib

namespace Mathforge.TernaryTrifferentCodesC012ClosedUnderThC1

open Finset

set_option maxRecDepth 100000
set_option maxHeartbeats 0

abbrev Word (m : ℕ) := Fin m → ZMod 3 × Fin 2

def shift {m : ℕ} (p : Word m) : Word m :=
  fun j => ((p j).1 + 1, (p j).2)

def good {m : ℕ} (p q r : Word m) : Prop :=
  ∃ j,
    ((p j).2 = (q j).2 ∧ (q j).2 = (r j).2 ∧
      (p j).1 ≠ (q j).1 ∧ (p j).1 ≠ (r j).1 ∧
      (q j).1 ≠ (r j).1) ∨
    ((p j).2 = (q j).2 ∧ (p j).2 ≠ (r j).2 ∧
      (p j).1 ≠ (q j).1) ∨
    ((p j).2 = (r j).2 ∧ (p j).2 ≠ (q j).2 ∧
      (p j).1 ≠ (r j).1) ∨
    ((q j).2 = (r j).2 ∧ (q j).2 ≠ (p j).2 ∧
      (q j).1 ≠ (r j).1)

def tripleProperty {m : ℕ} (D : Finset (Word m)) : Prop :=
  ∀ p ∈ D, ∀ q ∈ D, ∀ r ∈ D,
    p ≠ q → p ≠ r → q ≠ r → good p q r

instance {m : ℕ} (D : Finset (Word m)) :
    Decidable (tripleProperty D) := by
  unfold tripleProperty good
  infer_instance

abbrev Representative := ZMod 3 × Fin 2 × Fin 2

def representative (p : Word 2) : Representative :=
  ((p 1).1 - (p 0).1, (p 0).2, (p 1).2)

def expand (r : Representative) (c : ZMod 3) : Word 2 :=
  fun i => if i = 0 then (c, r.2.1) else (c + r.1, r.2.2)

def wordTranslate (c : ZMod 3) (p : Word 2) : Word 2 :=
  fun i => ((p i).1 + c, (p i).2)

def orbitSet (S : Finset Representative) : Finset (Word 2) :=
  univ.filter fun p => representative p ∈ S

-- FAITHFULNESS:
-- m ranges over all natural numbers with the hypothesis 1 ≤ m.
-- Word m is exactly m pairs: the first component is F₃ and the second
-- is {0,1}, represented by Fin 2. A finite set is used for D because
-- the ambient space is finite, so this loses no subsets.
-- The cardinality bound is 3 * 2^m. Closure under shift is invariance:
-- shift is a permutation of order three, so closure gives equality.
-- tripleProperty quantifies over every ordered triple of distinct
-- members. Its first disjunct is condition (i); its remaining three
-- disjuncts are precisely the three possibilities in condition (ii).
theorem refutation :
    ¬ (∀ m : ℕ, 1 ≤ m →
      ∃ D : Finset (Word m),
        3 * 2 ^ m ≤ D.card ∧
        (∀ p ∈ D, shift p ∈ D) ∧
        tripleProperty D) := by
  sorry

end Mathforge.TernaryTrifferentCodesC012ClosedUnderThC1
