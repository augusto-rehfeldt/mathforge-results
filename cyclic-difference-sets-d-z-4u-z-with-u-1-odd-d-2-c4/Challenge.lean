import Mathlib

namespace Mathforge.CyclicDifferenceSetsDZ4uZWithU1OddD2C4

open Finset

-- FAITHFULNESS:
-- u ranges over integers; Odd u, Squarefree u.natAbs, and 1 < u express
-- precisely the restrictions on u. Squarefreeness of the absolute value
-- is equivalent to no prime square dividing the integer.
-- Fin (4 * u.toNat) indexes the 4u entries (since u > 1).
-- Each entry is an odd integer with absolute value at most u.
-- The sum is 2u. The shift t ranges over the same Fin type, representing
-- exactly the integers 0 ≤ t < 4u. Fin addition reduces indices modulo
-- 4u, so the correlation is periodic. Its prescribed value is 4u² at
-- t = 0 and zero at every other shift.

def witness : Fin 12 → ℤ :=
  ![-3, 1, 1, 1, -3, 1, 1, 1, 3, 1, 1, 1]

theorem refutation :
    ¬ (∀ u : ℤ, Odd u → Squarefree u.natAbs → 1 < u →
      ¬ ∃ x : Fin (4 * u.toNat) → ℤ,
        (∀ i, Odd (x i) ∧ |x i| ≤ u) ∧
        (∑ i, x i) = 2 * u ∧
        (∀ t : Fin (4 * u.toNat),
          (∑ i, x i * x (i + t)) =
            if t.val = 0 then 4 * u ^ 2 else 0)) := by
  sorry

end Mathforge.CyclicDifferenceSetsDZ4uZWithU1OddD2C4
