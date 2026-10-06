import Mathlib

namespace Mathforge.FiniteCoveringSystemsAIModMIWithPairwisC4

open Finset

set_option maxRecDepth 0
set_option maxHeartbeats 0

def mods : Fin 11 → ℕ := ![3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315]

def offsets : Fin 11 → ℤ := ![2, 2, 2, 7, 10, 19, 18, 9, 24, 36, 255]

def r5 (x : ℕ) : Fin 5 := ⟨x % 5, Nat.mod_lt _ (by decide)⟩

def r7 (x : ℕ) : Fin 7 := ⟨x % 7, Nat.mod_lt _ (by decide)⟩

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
  sorry

end Mathforge.FiniteCoveringSystemsAIModMIWithPairwisC4
