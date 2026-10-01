import Mathlib

namespace Mathforge.SetPartitionsOfNInWhichEveryBlockHasEleC4

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace PartitionCounterexample

/-- An element's weight and whether its singleton contributes a factor `y`. -/
abbrev Item := Nat × Bool

structure Bin where
  weight : Nat
  size : Nat
  ordinary : Bool
  deriving DecidableEq

def emptyBin : Bin := ⟨0, 0, true⟩

def insertItem (a : Item) (b : Bin) : Bin :=
  ⟨(b.weight + a.1) % 3, b.size + 1, b.ordinary && a.2⟩

def updateBin (a : Item) : Nat → List Bin → List Bin
  | _, [] => []
  | 0, b :: bs => insertItem a b :: bs
  | i + 1, b :: bs => b :: updateBin a i bs

def acceptable (bs : List Bin) (t : Nat) : Bool :=
  bs.all (fun b => decide (0 < b.size) && decide (b.weight % 3 = 0)) &&
    decide ((bs.filter (fun b => decide (b.size = 1) && b.ordinary)).length = t)

/-- Count assignments to labeled blocks. Only nonempty valid blocks are accepted. -/
def orderedCount : List Item → List Bin → Nat → Nat
  | [], bs, t => if acceptable bs t then 1 else 0
  | a :: rest, bs, t =>
      ((List.range bs.length).map
        (fun i => orderedCount rest (updateBin a i bs) t)).sum

/--
Every partition into `k` nonempty blocks has exactly `k!` labelings.
Thus this quotient is its coefficient, not a count of labeled partitions.
-/
def coefficient (items : List Item) (k t : Nat) : ℤ :=
  (orderedCount items (List.replicate k emptyBin) t / Nat.factorial k : Nat)

def ground (n : Nat) : List Nat :=
  (List.range n).map (fun i => i + 1)

def remainder (p n : Nat) : List Nat :=
  (ground n).filter fun r =>
    !((decide (r % 3 = 1) && decide (r ≤ 3 * p - 2)) ||
      (decide (r % 3 = 2) && decide (r ≤ 3 * p - 1)))

def ordinaryItems (s : List Nat) : List Item :=
  s.map (fun r => (r, true))

def leftCoefficient (n k t : Nat) : ℤ :=
  coefficient (ordinaryItems (ground n)) k t

def rightCoefficient (p n k t : Nat) : ℤ :=
  coefficient ((p, false) :: (2 * p, false) ::
    ordinaryItems (remainder p n)) k t +
  if p ≤ k then
    (Nat.factorial p : ℤ) *
      coefficient (ordinaryItems (remainder p n)) (k - p) t
  else 0

-- FAITHFULNESS:
-- p and n range over all natural numbers, with precisely the hypotheses
-- that p is prime, p ≥ 5, and n ≥ 3p−1. `ground n` is {1,...,n}.
-- Under these hypotheses the removed residue-1 elements are exactly
-- 1,4,...,3p−2, and the removed residue-2 elements are 2,5,...,3p−1.
-- Items are distinct list positions; hence the two added positions are
-- distinct formal objects even if some weights coincide.
-- `orderedCount` assigns every item to a labeled block, requires every
-- block to be nonempty with weight divisible by 3, and counts exactly t
-- ordinary singleton blocks. Dividing by k! forgets block labels.
-- For ordinary items this gives F; the two false-tagged items give H.
-- The empty partition is included. The conditional shifted coefficient
-- is exactly the coefficient of p! x^p F_R.
-- Quantification over all k,t is coefficientwise congruence in Z[x,y],
-- expressed by divisibility of every coefficient difference by p².

theorem refutation :
    ¬ (∀ p n : Nat, Nat.Prime p → 5 ≤ p → 3 * p - 1 ≤ n →
      ∀ k t : Nat,
        (p ^ 2 : ℤ) ∣
          (leftCoefficient n k t - rightCoefficient p n k t)) := by
  sorry

end PartitionCounterexample

end Mathforge.SetPartitionsOfNInWhichEveryBlockHasEleC4
