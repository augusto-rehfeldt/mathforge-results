import Mathlib

namespace Mathforge.VertexSubsetsOfThe4NRectangularGridWhoseC1

open Finset

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace GridCounterexample

-- Vertex i has coordinates (i / n + 1, i % n + 1).
abbrev Vertex (n : ℕ) := Fin (4 * n)

def x {n : ℕ} (i : Vertex n) : ℕ := i.val / n

def y {n : ℕ} (i : Vertex n) : ℕ := i.val % n

def adjacent {n : ℕ} (i j : Vertex n) : Prop :=
  (x i = x j ∧ (y i + 1 = y j ∨ y j + 1 = y i)) ∨
  (y i = y j ∧ (x i + 1 = x j ∨ x j + 1 = x i))

instance {n : ℕ} (i j : Vertex n) : Decidable (adjacent i j) :=
  inferInstanceAs (Decidable ((_ ∧ _) ∨ (_ ∧ _)))

def neighbors {n : ℕ} (A : Finset (Vertex n)) (i : Vertex n) :=
  A.filter (adjacent i)

def regular {n : ℕ} (A : Finset (Vertex n)) : Prop :=
  ∀ i ∈ A, (neighbors A i).card = 2

instance {n : ℕ} (A : Finset (Vertex n)) : Decidable (regular A) :=
  inferInstanceAs (Decidable (∀ i ∈ A, (neighbors A i).card = 2))

def expand {n : ℕ} (A S : Finset (Vertex n)) :=
  S ∪ A.filter (fun j => ∃ i ∈ S, adjacent i j)

def flood {n : ℕ} (A : Finset (Vertex n)) (i : Vertex n) :
    ℕ → Finset (Vertex n)
  | 0 => {i}
  | k + 1 => expand A (flood A i k)

-- A simple path has at most 4*n - 1 edges.
def component {n : ℕ} (A : Finset (Vertex n)) (i : Vertex n) :=
  flood A i (4 * n)

def representatives {n : ℕ} (A : Finset (Vertex n)) :=
  A.filter (fun i => ∀ j ∈ component A i, i.val ≤ j.val)

-- The half-open horizontal-ray rule counts each polygon vertex correctly.
-- Only upward-oriented unit vertical edges are counted.
def crossings {n : ℕ} (C : Finset (Vertex n)) (p : Vertex n) :=
  C.filter (fun a =>
    x p < x a ∧ y a = y p ∧
      ∃ b ∈ C, x b = x a ∧ y b = y a + 1)

def inside {n : ℕ} (C : Finset (Vertex n)) (p : Vertex n) : Prop :=
  p ∉ C ∧ (crossings C p).card % 2 = 1

instance {n : ℕ} (C : Finset (Vertex n)) (p : Vertex n) :
    Decidable (inside C p) :=
  inferInstanceAs (Decidable (_ ∧ _))

def holes {n : ℕ} (A : Finset (Vertex n)) :=
  (univ : Finset (Vertex n)).filter (fun p =>
    p ∉ A ∧ ∃ r ∈ representatives A, inside (component A r) p)

-- A square is indexed by its lower-left vertex; its other three
-- corners are specified by their coordinates, avoiding boundary wrapping.
def squareInside {n : ℕ} (A C : Finset (Vertex n))
    (p : Vertex n) : Prop :=
  x p + 1 < 4 ∧ y p + 1 < n ∧
    ∀ t : Vertex n,
      ((x t = x p ∨ x t = x p + 1) ∧
       (y t = y p ∨ y t = y p + 1)) →
      t ∉ A ∧ inside C t

instance {n : ℕ} (A C : Finset (Vertex n)) (p : Vertex n) :
    Decidable (squareInside A C p) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ ∀ t : Vertex n, _ → _))

def squares {n : ℕ} (A : Finset (Vertex n)) :=
  (univ : Finset (Vertex n)).filter (fun p =>
    ∃ r ∈ representatives A, squareInside A (component A r) p)

def fourCycles {n : ℕ} (A : Finset (Vertex n)) :=
  (representatives A).filter (fun r => (component A r).card = 4)

def identity {n : ℕ} (A : Finset (Vertex n)) : Prop :=
  (A.card : ℤ) =
    2 * (holes A).card + 6 * (representatives A).card -
      2 * (squares A).card - 2 * (fourCycles A).card

instance {n : ℕ} (A : Finset (Vertex n)) : Decidable (identity A) :=
  inferInstanceAs (Decidable ((_ : ℤ) = _))

def witness : Finset (Vertex 4) :=
  {0, 1, 2, 4, 6, 7, 8, 9, 11, 13, 14, 15}

-- FAITHFULNESS:
-- n ranges over all natural numbers with n ≥ 1. Vertex n is precisely
-- {1,2,3,4} × {1,...,n}, encoded row by row. Every subset is a Finset
-- because this vertex type is finite; the empty subset is included.
-- adjacent is Euclidean unit-distance adjacency, and regular requires
-- degree two at every selected vertex, vacuously for the empty set.
-- component is bounded flood fill, which computes the entire connected
-- component in a graph with 4*n vertices. representatives selects exactly
-- its least vertex, so its cardinality is c. For a regular induced graph,
-- each component is a simple grid polygon. inside is the usual odd
-- horizontal-ray crossing test for its strict interior; integer grid
-- points cannot lie in the interior of a unit edge, and polygon vertices
-- are explicitly excluded. holes counts outside vertices inside at least
-- one component. squares counts unit squares with all four corners outside
-- A and strictly inside one common component. fourCycles counts components
-- with exactly four vertices. A.card is v. Integer arithmetic preserves
-- the subtraction in the claimed identity. All counts vanish for A empty.
theorem refutation :
    ¬ (∀ n : ℕ, 1 ≤ n →
        ∀ A : Finset (Vertex n), regular A → identity A) := by
  sorry

end GridCounterexample

end Mathforge.VertexSubsetsOfThe4NRectangularGridWhoseC1
