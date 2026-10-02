import Mathlib

namespace CyclicCounterexample

abbrev Word := List Bool

def bit (b : Bool) : ℤ := if b then 1 else 0

def read (v : Word) (h : ℕ) : Bool :=
  v.getD (h % v.length) false

def T (v : Word) : Word :=
  (List.range v.length).map fun h =>
    Bool.xor (read v h)
      (read v (h + v.length - 1) && read v (h + 1))

def periodTwo (v : Word) : Prop :=
  T (T v) = v ∧ T v ≠ v

def changed (v : Word) (h : ℕ) : Prop :=
  read (T v) h ≠ read v h

def D (v : Word) : ℕ :=
  ((List.range v.length).filter fun h =>
    read (T v) h != read v h).length

def wt (v : Word) : ℤ :=
  (v.map bit).sum

def path (v : Word) (start count : ℕ) : Word :=
  (List.range count).map fun h => read v (start + h)

def glue (x z : Word) (i j : ℕ) (c d : Bool) : Word :=
  path x (i + 1) (x.length - 1) ++ [c] ++
    path z (j + 1) (z.length - 1) ++ [d]

def cutFirst (u : Word) (i k : ℕ) (c : Bool) : Word :=
  path u (i + 1) (k - 1) ++ [c]

def cutSecond (u : Word) (i k : ℕ) (d : Bool) : Word :=
  path u (i + k + 1) (u.length - k - 1) ++ [d]

def x : Word := [false, true, false, false, true]
def z : Word := [true, true, false, true, false, false, true]

-- FAITHFULNESS:
-- Bool is exactly the binary alphabet; xor and && implement addition and
-- multiplication in F₂. Lists are indexed cyclically by `read`, so `T`
-- is the stated update. `periodTwo` includes both temporal conditions.
-- Natural lengths ≥ 5 (or ≥ 10) parameterize exactly the integer lengths
-- allowed in the claim; the length equations tie those parameters to words.
-- The forward universal quantifiers cover both words, every valid changed
-- index, and both freely chosen bits. `path` omits the selected entry and
-- reads the remaining entries clockwise; `glue` is precisely P c Q d.
-- Weights are ordinary integers, D counts changed indices, and the multiset
-- records the unordered temporal weight pair, including its correction.
-- The reverse quantifiers cover every word of length N, every initial index,
-- and every clockwise distance k with k ≥ 5 and N-k ≥ 5. The second index
-- is i+k modulo N. Both paths omit both cut positions and are closed with
-- independently arbitrary bits. Representatives suffice: rotations do not
-- change any condition or conclusion, so no necklace quotient is required.

theorem refutation :
    ¬ (
      (∀ (n m : ℕ), 5 ≤ n → 5 ≤ m →
        ∀ (x z : Word), x.length = n → z.length = m →
        periodTwo x → periodTwo z →
        ∀ (i j : ℕ), i < n → j < m →
        changed x i → changed z j →
        ∀ (c d : Bool),
          let u := glue x z i j c d
          let a := bit (read x i)
          let b := bit (read z j)
          periodTwo u ∧
          D u = D x + D z ∧
          wt u = wt x + wt z - a - b + bit c + bit d ∧
          wt (T u) = wt (T x) + wt (T z) + a + b - bit c - bit d ∧
          wt u + wt (T u) = wt x + wt (T x) + wt z + wt (T z) ∧
          ({wt u, wt (T u)} : Multiset ℤ) =
            {wt x + wt z - a - b + bit c + bit d,
             wt (T x) + wt (T z) + a + b - bit c - bit d}) ∧
      (∀ (N : ℕ), 10 ≤ N →
        ∀ (u : Word), u.length = N → periodTwo u →
        ∀ (i k : ℕ), i < N → 5 ≤ k → k + 5 ≤ N →
        changed u i → changed u (i + k) →
        ∀ (c d : Bool),
          periodTwo (cutFirst u i k c) ∧
          periodTwo (cutSecond u i k d))
    ) := by
  intro h
  have hxlen : x.length = 5 := by decide
  have hzlen : z.length = 7 := by decide
  have hx : periodTwo x := by unfold periodTwo; decide
  have hz : periodTwo z := by unfold periodTwo; decide
  have hix : changed x 0 := by unfold changed; decide
  have hjz : changed z 0 := by unfold changed; decide
  have result :=
    h.1 5 7 (by decide) (by decide)
      x z hxlen hzlen hx hz
      0 0 (by decide) (by decide) hix hjz false false
  have bad :
      T (T (glue x z 0 0 false false)) ≠
        glue x z 0 0 false false := by
    decide
  exact bad result.1.1

end CyclicCounterexample
set_option pp.fullNames true in
#print axioms CyclicCounterexample.refutation