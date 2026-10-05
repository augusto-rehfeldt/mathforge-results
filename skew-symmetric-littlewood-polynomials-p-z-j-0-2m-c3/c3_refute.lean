import Mathlib

open Finset

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

def correlation (m r : ℕ) (a : ℕ → ℤ) : ℤ :=
  ∑ j ∈ Finset.range (2 * m + 1 - r), a j * a (j + r)

def energy (m : ℕ) (a : ℕ → ℤ) : ℤ :=
  ∑ r ∈ Finset.range (2 * m), (correlation m (r + 1) a) ^ 2

def inProgression (u v d i : ℕ) : Prop :=
  u ≤ i ∧ i ≤ v ∧ d ∣ i - u

instance (u v d i : ℕ) : Decidable (inProgression u v d i) :=
  inferInstanceAs (Decidable (u ≤ i ∧ i ≤ v ∧ d ∣ i - u))

def transform (m u v d : ℕ) (a : ℕ → ℤ) : ℕ → ℤ :=
  fun i =>
    if inProgression u v d i ∨ inProgression u v d (2 * m - i)
    then -(a i)
    else a i

def witness : ℕ → ℤ :=
  fun i =>
    ([1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1,
      -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1,
      -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1,
      1] : List ℤ).getD i 0

-- FAITHFULNESS:
-- Nonnegative integer indices are represented by naturals. The quantifier
-- m ≥ 1 is explicit. A function a is used only on indices 0 through 2m,
-- with its sign condition quantified over Fin (2m+1).
-- Fin (m+1) represents exactly the integers j, u, v between 0 and m.
-- Fin 3 together with d = 1 or d = 2 represents exactly the allowed steps.
-- The symmetry equation, u ≤ v, and d ∣ (v-u) are explicit hypotheses.
-- inProgression describes {u,u+d,...,v}; transform uses a disjunction,
-- so a coordinate belonging to both reflected sets is negated only once.
-- correlation and energy are precisely the stated finite sums.
-- The conclusion is multiplied by 8: since energy is integral, this is
-- equivalent to the proposed rational inequality
-- E ≤ (2m+1)^2/8 + 2(2m+1).
-- Values of a outside 0 through 2m are irrelevant to every condition.
theorem refutation :
    ¬ (∀ (m : ℕ), 1 ≤ m →
      ∀ (a : ℕ → ℤ),
        (∀ i : Fin (2 * m + 1), a i.val = -1 ∨ a i.val = 1) →
        (∀ j : Fin (m + 1),
          a (m + j.val) = (-1 : ℤ) ^ j.val * a (m - j.val)) →
        (∀ (u v : Fin (m + 1)) (d : Fin 3),
          (d.val = 1 ∨ d.val = 2) →
          u.val ≤ v.val →
          d.val ∣ v.val - u.val →
          energy m a ≤ energy m (transform m u.val v.val d.val a)) →
        8 * energy m a ≤
          ((2 * (m : ℤ) + 1) ^ 2 + 16 * (2 * (m : ℤ) + 1))) := by
  intro claim
  have signs :
      ∀ i : Fin 49, witness i.val = -1 ∨ witness i.val = 1 := by
    decide
  have skew :
      ∀ j : Fin 25,
        witness (24 + j.val) =
          (-1 : ℤ) ^ j.val * witness (24 - j.val) := by
    decide
  have local_minimum :
      ∀ (u v : Fin 25) (d : Fin 3),
        (d.val = 1 ∨ d.val = 2) →
        u.val ≤ v.val →
        d.val ∣ v.val - u.val →
        energy 24 witness ≤
          energy 24 (transform 24 u.val v.val d.val witness) := by
    decide
  have computed_energy : energy 24 witness = 424 := by
    decide
  have bound := claim 24 (by norm_num) witness signs skew local_minimum
  rw [computed_energy] at bound
  norm_num at bound
set_option pp.fullNames true in
#print axioms refutation