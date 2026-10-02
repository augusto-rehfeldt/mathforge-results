import Mathlib

namespace Mathforge.OrderedTriplesOfDyckPathsOfTheSameSemileC2

open Finset

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace DyckCounterexample

abbrev Path (n : ℕ) := Fin (2 * n) → Bool

abbrev Triple (n : ℕ) := Path n × Path n × Path n

def height {n : ℕ} (p : Path n) (t : ℕ) : ℤ :=
  ∑ i ∈ Finset.range t,
    if h : i < 2 * n then
      if p ⟨i, h⟩ then (1 : ℤ) else -1
    else 0

def dyck {n : ℕ} (p : Path n) : Prop :=
  height p (2 * n) = 0 ∧
    ∀ t ∈ Finset.range (2 * n + 1), 0 ≤ height p t

instance {n : ℕ} (p : Path n) : Decidable (dyck p) := by
  unfold dyck
  infer_instance

def internal (n : ℕ) : Finset ℕ :=
  (Finset.range (2 * n)).erase 0

def ordered {n : ℕ} (q : Triple n) : Prop :=
  ∀ t ∈ Finset.range (2 * n + 1),
    height q.1 t ≤ height q.2.1 t ∧
    height q.2.1 t ≤ height q.2.2 t

instance {n : ℕ} (q : Triple n) : Decidable (ordered q) := by
  unfold ordered
  infer_instance

def contacts {n : ℕ} (q : Triple n) : Finset ℕ :=
  (internal n).filter fun t =>
    height q.1 t = height q.2.1 t ∧
    height q.2.1 t = height q.2.2 t

def lowerOnly {n : ℕ} (q : Triple n) : Finset ℕ :=
  (internal n).filter fun t =>
    height q.1 t = height q.2.1 t ∧
    height q.2.1 t < height q.2.2 t

def upperOnly {n : ℕ} (q : Triple n) : Finset ℕ :=
  (internal n).filter fun t =>
    height q.1 t < height q.2.1 t ∧
    height q.2.1 t = height q.2.2 t

def area {n : ℕ} (p q : Path n) : ℤ :=
  (∑ t ∈ Finset.range (2 * n + 1), (height q t - height p t)) / 2

def peak {n : ℕ} (p : Path n) (t : ℕ) : Prop :=
  height p (t - 1) = height p t - 1 ∧
  height p (t + 1) = height p t - 1

def valley {n : ℕ} (p : Path n) (t : ℕ) : Prop :=
  height p (t - 1) = height p t + 1 ∧
  height p (t + 1) = height p t + 1

instance {n : ℕ} (p : Path n) (t : ℕ) : Decidable (peak p t) := by
  unfold peak
  infer_instance

instance {n : ℕ} (p : Path n) (t : ℕ) : Decidable (valley p t) := by
  unfold valley
  infer_instance

def peaks {n : ℕ} (a b : ℤ) (S : Finset ℕ) (p q : Path n) : ℕ :=
  (S.filter fun (t : ℕ) =>
    a < (t : ℤ) ∧ (t : ℤ) < b ∧ peak p t ∧ peak q t).card

def valleys {n : ℕ} (a b : ℤ) (S : Finset ℕ) (p q : Path n) : ℕ :=
  (S.filter fun (t : ℕ) =>
    a < (t : ℤ) ∧ (t : ℤ) < b ∧ valley p t ∧ valley q t).card

def reflect (a b : ℤ) (S : Finset ℕ) : Finset ℕ :=
  S.image fun (t : ℕ) =>
    if a < (t : ℤ) ∧ (t : ℤ) < b then
      (a + b - (t : ℤ)).toNat
    else t

def satisfies (n : ℕ) (a b H : ℤ) (A B : ℕ)
    (L U : Finset ℕ) (p12 v12 p23 v23 : ℕ) (q : Triple n) : Prop :=
  dyck q.1 ∧ dyck q.2.1 ∧ dyck q.2.2 ∧ ordered q ∧
  contacts q = {a.toNat, b.toNat} ∧
  height q.1 a.toNat = H ∧ height q.1 b.toNat = H ∧
  area q.1 q.2.1 = (A : ℤ) ∧ area q.2.1 q.2.2 = (B : ℤ) ∧
  lowerOnly q = L ∧ upperOnly q = U ∧
  peaks a b L q.1 q.2.1 = p12 ∧
  valleys a b L q.1 q.2.1 = v12 ∧
  peaks a b U q.2.1 q.2.2 = p23 ∧
  valleys a b U q.2.1 q.2.2 = v23

instance (n : ℕ) (a b H : ℤ) (A B : ℕ)
    (L U : Finset ℕ) (p12 v12 p23 v23 : ℕ) (q : Triple n) :
    Decidable (satisfies n a b H A B L U p12 v12 p23 v23 q) := by
  unfold satisfies
  infer_instance

def family (n : ℕ) (a b H : ℤ) (A B : ℕ)
    (L U : Finset ℕ) (p12 v12 p23 v23 : ℕ) : Finset (Triple n) :=
  Finset.univ.filter (satisfies n a b H A B L U p12 v12 p23 v23)

-- FAITHFULNESS:
-- n,a,b,H are integers, with precisely the stated bounds. A,B and the
-- four counts are naturals, i.e. nonnegative integers. L,U are finite
-- subsets of the positive internal times excluding a,b; using natural
-- time indices loses no integer times under these hypotheses.
-- A path is encoded by its 2n up/down steps. `height` is their integer
-- partial sum, so height(0)=0 and every increment is ±1 by construction.
-- `dyck` imposes the endpoint and nonnegativity conditions. This encoding
-- is bijective with the height-function definition in the question.
-- `ordered`, `contacts`, and the two specified heights impose exactly
-- the order and the two internal triple contacts at common height H.
-- The area sum is divided by two after summation: all differences are
-- even because every height has the parity of its time.
-- `lowerOnly` and `upperOnly` specify the complete pair-only sets.
-- `peaks` and `valleys` count only strict middle-block times.
-- `reflect` fixes all other times and sends t to a+b-t in that block.
-- `family` is the finite set of all encoded ordered triples satisfying
-- these conditions; the second family reflects both sets and swaps
-- each adjacent pair's peak/valley counts.

theorem refutation :
    ¬ (∀ (n a b H : ℤ) (A B : ℕ) (L U : Finset ℕ)
        (p12 v12 p23 v23 : ℕ),
      2 ≤ n →
      1 ≤ a →
      a < b →
      b ≤ 2 * n - 1 →
      0 ≤ H →
      L ⊆ (internal n.toNat).filter
        (fun t => (t : ℤ) ≠ a ∧ (t : ℤ) ≠ b) →
      U ⊆ (internal n.toNat).filter
        (fun t => (t : ℤ) ≠ a ∧ (t : ℤ) ≠ b) →
      (family n.toNat a b H A B L U p12 v12 p23 v23).card =
      (family n.toNat a b H A B
        (reflect a b L) (reflect a b U) v12 p12 v23 p23).card) := by
  intro h
  have e := h 2 1 3 1 0 1 {2} ∅ 0 1 0 0
    (by decide) (by decide) (by decide) (by decide) (by decide)
    (by decide) (by decide)
  have ne :
      (family 2 1 3 1 0 1 {2} ∅ 0 1 0 0).card ≠
      (family 2 1 3 1 0 1
        (reflect 1 3 {2}) (reflect 1 3 ∅) 1 0 0 0).card := by
    decide
  exact ne e

end DyckCounterexample

end Mathforge.OrderedTriplesOfDyckPathsOfTheSameSemileC2
