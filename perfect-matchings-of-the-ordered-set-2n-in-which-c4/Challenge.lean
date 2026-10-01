import Mathlib

namespace Mathforge.PerfectMatchingsOfTheOrderedSet2nInWhichC4

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace ArcMatchings

abbrev Arc := Nat × Nat

def crosses (a b : Arc) : Bool :=
  decide ((a.1 < b.1 ∧ b.1 < a.2 ∧ a.2 < b.2) ∨
    (b.1 < a.1 ∧ a.1 < b.2 ∧ b.2 < a.2))

def nested (a b : Arc) : Bool :=
  decide ((a.1 < b.1 ∧ b.2 < a.2) ∨
    (b.1 < a.1 ∧ a.2 < b.2))

/-- Choose the partner of the least remaining endpoint, recursively. -/
def matchings : Nat → List Nat → List (List Arc)
  | 0, xs => if xs.isEmpty then [[]] else []
  | _ + 1, [] => []
  | k + 1, x :: xs =>
      xs.flatMap fun y =>
        (matchings k (xs.filter fun z => z != y)).map
          fun rest => (x, y) :: rest

def degreeTwo (m : List Arc) : Bool :=
  m.all fun a => decide ((m.filter fun b => crosses a b).length = 2)

def expand (m : List Arc) (seen : List Nat) : List Nat :=
  (List.range m.length).filter fun i =>
    seen.contains i ||
      seen.any fun k =>
        crosses (m[i]?.getD (0, 0)) (m[k]?.getD (0, 0))

def reachable (m : List Arc) (i : Nat) : List Nat :=
  (List.range m.length).foldl (fun seen _ => expand m seen) [i]

/-- Each component contributes precisely its least vertex index. -/
def components (m : List Arc) : Nat :=
  ((List.range m.length).filter fun i =>
    (reachable m i).all fun k => decide (i ≤ k)).length

def nestingCount : List Arc → Nat
  | [] => 0
  | a :: rest =>
      (rest.filter fun b => nested a b).length + nestingCount rest

def A (n c j : Nat) : Nat :=
  ((matchings n (List.range (2 * n) |>.map (fun k => k + 1))).filter
    fun m =>
      degreeTwo m &&
      decide (components m = c) &&
      decide (nestingCount m = j)).length

-- FAITHFULNESS:
-- c, n, and j are quantified as integers, with exactly the stated lower bounds.
-- Their toNat conversions are used only where those bounds ensure nonnegativity.
-- matchings enumerates every perfect matching of {1,...,2n} exactly once:
-- it pairs the least unused endpoint with each possible partner.
-- crosses is precisely arc crossing; degreeTwo requires degree two at every
-- arc vertex. reachable computes graph reachability, and components counts
-- connected components by their least index. nestingCount counts each unordered
-- nested pair once. A counts the matchings satisfying these three conditions.
-- The conjunction below states both the vanishing assertion for every eligible
-- integer j and the asserted boundary value, using Nat.choose for binomial.

theorem refutation :
    ¬ (∀ c n : ℤ, 1 ≤ c → 3 * c ≤ n →
      (∀ j : ℤ, 0 ≤ j → j < n - 3 * c →
        A n.toNat c.toNat j.toNat = 0) ∧
      A n.toNat c.toNat (n - 3 * c).toNat =
        2 ^ (n - 3 * c).toNat *
          Nat.choose (n - 2 * c - 1).toNat (c - 1).toNat) := by
  sorry

end ArcMatchings

end Mathforge.PerfectMatchingsOfTheOrderedSet2nInWhichC4
