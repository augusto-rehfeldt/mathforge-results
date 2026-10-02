import Mathlib

open scoped BigOperators

set_option maxRecDepth 100000
set_option maxHeartbeats 0

abbrev Word := List Bool

-- C s w counts occurrences of s as a scattered subword of w.
def C (s : Word) (w : Word) : Nat :=
  match w with
  | [] => if s = [] then 1 else 0
  | a :: w' =>
      C s w' +
        match s with
        | [] => 0
        | b :: s' => if a = b then C s' w' else 0
termination_by structural w

def E (w : Word) : Word :=
  w.flatMap (fun b =>
    if b then [false, true, true] else [false, false, true])

def runs : Word → Nat
  | [] => 0
  | [_] => 1
  | a :: b :: w => (if a = b then 0 else 1) + runs (b :: w)

abbrev Pattern (k : Nat) := Fin k → Bool

def patternWord {k : Nat} (s : Pattern k) : Word := List.ofFn s

def delta {k : Nat} (s : Pattern k) (x y : Word) : ℝ :=
  (C (patternWord s) x : ℝ) - (C (patternWord s) y : ℝ)

noncomputable def deltaNorm (x y : Word) : ℝ :=
  Real.sqrt (∑ s : Pattern 4, (delta s x y) ^ 2)

def M (a b : Bool) : ℝ := if a = b then 2 else 1

def shortEqual (x y : Word) : Prop :=
  ∀ k : Fin 3, ∀ s : Pattern (k.val + 1),
    C (patternWord s) x = C (patternWord s) y

def u : Word := [false, true, true, false, false, false, true]
def v : Word := [true, false, false, false, true, true, false]

-- FAITHFULNESS:
-- Words are lists of Bool, with false = 0 and true = 1.
-- The universal n is a natural number constrained by 1 ≤ n; u and v
-- are universally quantified words constrained to have length n.
-- shortEqual quantifies over lengths 1, 2, 3 and every binary pattern
-- of each length. C counts strictly increasing selections, including
-- the empty-pattern base case needed by its recursion.
-- U and V are exactly E (u ++ reverse v) and E (v ++ reverse u).
-- The conclusion asserts both lengths, both letter counts for both
-- words, both run counts, all short-pattern equalities, all sixteen
-- fourth-order identities, and both Euclidean-norm inequalities.
-- Fourth-order patterns are functions Fin 4 → Bool; delta uses the
-- real embedding of the integer count difference, and the finite sums
-- and products therefore express precisely the stated formula and norm.
theorem refutation :
    ¬ (∀ (n : Nat) (x y : Word),
      1 ≤ n →
      x.length = n →
      y.length = n →
      shortEqual x y →
      let U := E (x ++ y.reverse)
      let V := E (y ++ x.reverse)
      U.length = 6 * n ∧
      V.length = 6 * n ∧
      C [false] U = 3 * n ∧
      C [true] U = 3 * n ∧
      C [false] V = 3 * n ∧
      C [true] V = 3 * n ∧
      runs U = 4 * n ∧
      runs V = 4 * n ∧
      shortEqual U V ∧
      (∀ t : Pattern 4,
        delta t U V =
          2 * ∑ s : Pattern 4,
            delta s x y * ∏ i : Fin 4, M (t i) (s i)) ∧
      6 * deltaNorm x y ≤ deltaNorm U V ∧
      deltaNorm U V ≤ 54 * deltaNorm x y) := by
  intro h
  have hshort : shortEqual u v := by
    unfold shortEqual
    decide
  have hw := h 7 u v (by decide) (by decide) (by decide) hshort
  have hzero : C [false] (E (u ++ v.reverse)) = 3 * 7 :=
    hw.2.2.1
  have hbad : C [false] (E (u ++ v.reverse)) ≠ 3 * 7 := by
    decide
  exact hbad hzero
set_option pp.fullNames true in
#print axioms refutation