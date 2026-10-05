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

lemma reconstruct (p : Word 2) :
    expand (representative p) (p 0).1 = p := by
  funext i
  fin_cases i <;>
    simp [expand, representative, sub_eq_add_neg,
      add_assoc, add_comm, add_left_comm]

lemma translate_expand (r : Representative) (a c : ZMod 3) :
    wordTranslate c (expand r a) = expand r (a + c) := by
  funext i
  fin_cases i <;>
    simp [wordTranslate, expand, add_assoc, add_comm, add_left_comm]

lemma closed_translate (D : Finset (Word 2))
    (h : ∀ p ∈ D, shift p ∈ D) (p : Word 2) (hp : p ∈ D)
    (c : ZMod 3) : wordTranslate c p ∈ D := by
  have hc : c = 0 ∨ c = 1 ∨ c = 2 :=
    (by decide : ∀ c : ZMod 3, c = 0 ∨ c = 1 ∨ c = 2) c
  rcases hc with rfl | rfl | rfl
  · have he : wordTranslate 0 p = p := by
      funext i
      simp [wordTranslate]
    rw [he]
    exact hp
  · have he : wordTranslate 1 p = shift p := by
      funext i
      rfl
    rw [he]
    exact h p hp
  · have he : wordTranslate 2 p = shift (shift p) := by
      funext i
      simp [wordTranslate, shift, add_assoc]
      norm_num
    rw [he]
    exact h (shift p) (h p hp)

lemma orbit_description (D : Finset (Word 2))
    (h : ∀ p ∈ D, shift p ∈ D) :
    orbitSet (D.image representative) = D := by
  ext p
  simp only [orbitSet, mem_filter, mem_univ, true_and, mem_image]
  constructor
  · rintro ⟨q, hq, heq⟩
    have ht := closed_translate D h q hq ((p 0).1 - (q 0).1)
    have he : wordTranslate ((p 0).1 - (q 0).1) q = p := by
      calc
        wordTranslate ((p 0).1 - (q 0).1) q =
            wordTranslate ((p 0).1 - (q 0).1)
              (expand (representative q) (q 0).1) :=
          congrArg (wordTranslate ((p 0).1 - (q 0).1)) (reconstruct q).symm
        _ = expand (representative q)
              ((q 0).1 + ((p 0).1 - (q 0).1)) :=
          translate_expand _ _ _
        _ = expand (representative p) (p 0).1 := by
          rw [heq]
          congr 1
          abel
        _ = p := reconstruct p
    simpa [he] using ht
  · intro hp
    exact ⟨p, hp, rfl⟩

-- This computation ranges over only 2^12 sets of orbit representatives,
-- rather than 2^36 arbitrary subsets of the ambient space.
lemma finite_obstruction :
    ∀ S : Finset Representative,
      ¬ (12 ≤ (orbitSet S).card ∧ tripleProperty (orbitSet S)) := by
  decide

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
  intro claim
  obtain ⟨D, hcard, hinv, htriple⟩ := claim 2 (by omega)
  have heq := orbit_description D hinv
  apply finite_obstruction (D.image representative)
  rw [heq]
  exact ⟨by norm_num at hcard ⊢; exact hcard, htriple⟩

end Mathforge.TernaryTrifferentCodesC012ClosedUnderThC1
