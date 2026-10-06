import Mathlib

namespace Mathforge.FiniteCoveringSystemsAIModMIWithPairwisC4

open Finset

set_option maxRecDepth 0
set_option maxHeartbeats 0

def mods : Fin 11 → ℕ := ![3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315]

def offsets : Fin 11 → ℤ := ![2, 2, 2, 7, 10, 19, 18, 9, 24, 36, 255]

def r5 (x : ℕ) : Fin 5 := ⟨x % 5, Nat.mod_lt _ (by decide)⟩

def r7 (x : ℕ) : Fin 7 := ⟨x % 7, Nat.mod_lt _ (by decide)⟩

theorem finite_obstruction :
    ∀ t : Fin 9, ∀ B : Finset (Fin 5), ∀ C : Finset (Fin 7),
      3 ≤ B.card → 5 ≤ C.card →
      ∃ x : Fin 315,
        x.val % 9 = t.val ∧ r5 x.val ∈ B ∧ r7 x.val ∈ C ∧
        ∃ i : Fin 11,
          (x.val : ℤ) % (mods i : ℤ) = offsets i % (mods i : ℤ) := by
  decide

-- FAITHFULNESS:
-- Positive integer moduli are represented by natural numbers greater than one.
-- Fin k indexes the collection; Injective expresses pairwise distinctness.
-- Odd and the prime-cube condition are imposed on every modulus.
-- L is characterized by the defining divisibility property of the lcm.
-- The indices p : Fin (L+1) include every prime divisor of the positive L.
-- e gives exactly its exponent, by maximal prime-power divisibility.
-- B p is a subset of the residues Fin p, and f p selects residues modulo p^e.
-- The cardinal bound is p-2 (natural subtraction), and the remainder equation
-- is precisely the first-digit condition. Fin L ranges over all CRT residues.
-- Functions are extended outside B; this does not constrain their restrictions.
theorem refutation :
    ¬ (∀ (k : ℕ), 1 ≤ k →
      ∀ (m : Fin k → ℕ) (a : Fin k → ℤ),
        Function.Injective m →
        (∀ i, 1 < m i ∧ Odd (m i) ∧
          ∀ q : ℕ, Nat.Prime q → ¬ q ^ 3 ∣ m i) →
        ∀ L : ℕ, 0 < L →
          (∀ i, m i ∣ L) →
          (∀ n : ℕ, (∀ i, m i ∣ n) → L ∣ n) →
        ∀ e : Fin (L + 1) → ℕ,
          (∀ p, Nat.Prime p.val → p.val ∣ L →
            p.val ^ e p ∣ L ∧ ¬ p.val ^ (e p + 1) ∣ L) →
        ∃ (B : (p : Fin (L + 1)) → Finset (Fin p.val))
          (f : (p : Fin (L + 1)) → Fin p.val → Fin (p.val ^ e p)),
          (∀ p, Nat.Prime p.val → p.val ∣ L →
            p.val - 2 ≤ (B p).card ∧
            ∀ b ∈ B p, (f p b).val % p.val = b.val) ∧
          ∀ x : Fin L,
            (∀ p, Nat.Prime p.val → p.val ∣ L →
              ∃ b ∈ B p, x.val % (p.val ^ e p) = (f p b).val) →
            ∀ i, (x.val : ℤ) % (m i : ℤ) ≠ a i % (m i : ℤ)) := by
  intro H
  let e : Fin 316 → ℕ := fun p => if p.val = 3 then 2 else 1
  have hm : Function.Injective mods := by decide
  have hconditions :
      ∀ i, 1 < mods i ∧ Odd (mods i) ∧
        ∀ q : ℕ, Nat.Prime q → ¬ q ^ 3 ∣ mods i := by
    intro i
    have small :
        ∀ j : Fin 11, ∀ q : Fin 316,
          Nat.Prime q.val → ¬ q.val ^ 3 ∣ mods j := by decide
    refine ⟨by fin_cases i <;> decide, by fin_cases i <;> decide, ?_⟩
    intro q hq hd
    have hi : mods i ≤ 315 := by fin_cases i <;> decide
    have hp : 0 < mods i := by fin_cases i <;> decide
    have hcube : q ^ 3 ≤ mods i := Nat.le_of_dvd hp hd
    have hqle : q ≤ 315 := by
      have : q ≤ q ^ 3 := by
        have := hq.two_le
        nlinarith [Nat.pow_succ q 2]
      omega
    exact small i ⟨q, by omega⟩ hq hd
  have hdiv : ∀ i, mods i ∣ 315 := by decide
  have hleast : ∀ n, (∀ i, mods i ∣ n) → 315 ∣ n := by
    intro n hn
    exact hn ⟨10, by decide⟩
  have he :
      ∀ p : Fin 316, Nat.Prime p.val → p.val ∣ 315 →
        p.val ^ e p ∣ 315 ∧ ¬ p.val ^ (e p + 1) ∣ 315 := by
    decide
  obtain ⟨B, f, hf, avoid⟩ :=
    H 11 (by decide) mods offsets hm hconditions 315 (by decide)
      hdiv hleast e he
  let p3 : Fin 316 := ⟨3, by decide⟩
  let p5 : Fin 316 := ⟨5, by decide⟩
  let p7 : Fin 316 := ⟨7, by decide⟩
  have h3 := hf p3 (by decide) (by decide)
  have h5 := hf p5 (by decide) (by decide)
  have h7 := hf p7 (by decide) (by decide)
  have hb : (B p3).Nonempty := by
    apply Finset.card_pos.mp
    have := h3.1
    change 1 ≤ (B p3).card at this
    omega
  obtain ⟨b, hb⟩ := hb
  let t : Fin 9 := f p3 b
  obtain ⟨x, hx9, hx5, hx7, i, hi⟩ :=
    finite_obstruction t (B p5) (B p7) h5.1 h7.1
  apply avoid x ?_ i hi
  intro p hp hd
  have primes :
      ∀ p : Fin 316, Nat.Prime p.val → p.val ∣ 315 →
        p.val = 3 ∨ p.val = 5 ∨ p.val = 7 := by decide
  rcases primes p hp hd with h | h | h
  · have : p = p3 := Fin.ext h
    subst p
    exact ⟨b, hb, hx9⟩
  · have : p = p5 := Fin.ext h
    subst p
    refine ⟨r5 x.val, hx5, ?_⟩
    have hh := h5.2 (r5 x.val) hx5
    have bound : (f p5 (r5 x.val)).val < 5 :=
      (f p5 (r5 x.val)).isLt
    change (f p5 (r5 x.val)).val % 5 = x.val % 5 at hh
    rw [Nat.mod_eq_of_lt bound] at hh
    change x.val % 5 = (f p5 (r5 x.val)).val
    exact hh.symm
  · have : p = p7 := Fin.ext h
    subst p
    refine ⟨r7 x.val, hx7, ?_⟩
    have hh := h7.2 (r7 x.val) hx7
    have bound : (f p7 (r7 x.val)).val < 7 :=
      (f p7 (r7 x.val)).isLt
    change (f p7 (r7 x.val)).val % 7 = x.val % 7 at hh
    rw [Nat.mod_eq_of_lt bound] at hh
    change x.val % 7 = (f p7 (r7 x.val)).val
    exact hh.symm

end Mathforge.FiniteCoveringSystemsAIModMIWithPairwisC4
