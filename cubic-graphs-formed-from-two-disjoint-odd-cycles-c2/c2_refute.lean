import Mathlib

open Finset

set_option maxRecDepth 100000
set_option maxHeartbeats 0

abbrev Colors := Finset (Fin 6)

def ColorPartition (a b c : Colors) : Prop :=
  a.card = 2 ∧ b.card = 2 ∧ c.card = 2 ∧
  Disjoint a b ∧ Disjoint a c ∧ Disjoint b c ∧
  a ∪ b ∪ c = univ

def Compatible (d : Fin 4 → Colors) : Prop :=
  (∀ j, (d j).card = 2) ∧
  ∀ c : Fin 6, Even ((univ.filter fun j => c ∈ d j).card)

def Realizes (m : ℕ) (π : Equiv.Perm (Fin m))
    (d : Fin 4 → Colors) : Prop :=
  ∃ (up vp : ℕ → Colors) (cross : Fin m → Colors),
    ∀ i : Fin m,
      ColorPartition
        (if i.val = 0 then d 0 else up (i.val - 1))
        (if i.val + 1 = m then d 2 else up i.val)
        (cross i) ∧
      ColorPartition
        (if i.val = 0 then d 1 else vp (i.val - 1))
        (if i.val + 1 = m then d 3 else vp i.val)
        (cross (π.symm i))

def A : Colors := {2, 3}
def D : Colors := {4, 5}
def K : Colors := {0, 1}

def boundary : Fin 4 → Colors :=
  ![A, A, D, D]

def swapTwo : Equiv.Perm (Fin 2) :=
  Equiv.swap 0 1

lemma forced :
    ∀ x : Colors, x.card = 2 →
      Disjoint A x → Disjoint D x → x = K := by
  decide

lemma blocked :
    ∀ x : Colors, ColorPartition A x K → ¬ Disjoint x D := by
  unfold ColorPartition
  decide

lemma witness_impossible : ¬ Realizes 2 swapTwo boundary := by
  rintro ⟨up, vp, cross, h⟩
  have hu0 := (h (0 : Fin 2)).1
  have hu1 := (h (1 : Fin 2)).1
  have hv1 := (h (1 : Fin 2)).2
  have h0 : ColorPartition A (up 0) (cross 0) := by
    simpa [boundary] using hu0
  have h1 : ColorPartition (up 0) D (cross 1) := by
    simpa [boundary] using hu1
  have hv : ColorPartition (vp 0) D (cross 0) := by
    simpa [boundary, swapTwo, Equiv.swap_apply_def] using hv1
  have hk : cross 0 = K :=
    forced (cross 0) h0.2.2.1 h0.2.2.2.2.1 hv.2.2.2.2.2.1
  have hp : ColorPartition A (up 0) K := by
    simpa [hk] using h0
  exact blocked (up 0) hp h1.2.2.2.1

-- FAITHFULNESS:
-- Positive integers m ≥ 2 are represented by naturals m ≥ 2; Even m
-- imposes the stated evenness hypothesis. Fin m represents positions
-- 1,...,m by subtracting one, which preserves whether two parities differ.
-- π ranges over every permutation. Fin 6 represents colors 1,...,6.
-- d ranges over every ordered boundary quadruple in the order u₁,v₁,uₘ,vₘ.
-- Compatible requires two colors per boundary edge and an even occurrence
-- count for each color. up k and vp k label the path edges from position
-- k to k+1 (zero-based); only k < m-1 is used. Unused function values
-- impose no condition. cross i labels u_i--v_{π(i)}, so the matching edge
-- at v_i is cross (π.symm i). ColorPartition says that the three incident
-- labels each have size two, are pairwise disjoint, and cover all colors.
-- Thus Realizes is exactly existence of the required edge assignment.
theorem refutation :
    ¬ (∀ (m : ℕ), 2 ≤ m → Even m →
      ∀ π : Equiv.Perm (Fin m),
        (∃ i : Fin m, i.val % 2 ≠ (π i).val % 2) ↔
        (∀ d : Fin 4 → Colors, Compatible d → Realizes m π d)) := by
  intro claim
  have he : Even (2 : ℕ) := by decide
  have mismatch :
      ∃ i : Fin 2, i.val % 2 ≠ (swapTwo i).val % 2 := by
    decide
  have hc : Compatible boundary := by
    unfold Compatible
    decide
  exact witness_impossible ((claim 2 (by decide) he swapTwo).mp mismatch boundary hc)
set_option pp.fullNames true in
#print axioms forced
set_option pp.fullNames true in
#print axioms blocked
set_option pp.fullNames true in
#print axioms witness_impossible
set_option pp.fullNames true in
#print axioms refutation