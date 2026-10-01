import Mathlib

namespace Mathforge.SpanningTreesOfThe3NRectangularGridInWhC3

open Finset

abbrev Vertex (n : ℕ) := Fin 3 × Fin n

abbrev Edge (n : ℕ) := Vertex n × Vertex n

def gridEdges (n : ℕ) : Finset (Edge n) :=
  Finset.univ.filter fun e =>
    (e.1.1.val < e.2.1.val ∨
      (e.1.1 = e.2.1 ∧ e.1.2.val < e.2.2.val)) ∧
      Nat.dist e.1.1.val e.2.1.val +
        Nat.dist e.1.2.val e.2.2.val = 1

def treeAdj {n : ℕ} (T : Finset (Edge n)) (u v : Vertex n) : Prop :=
  (min u v, max u v) ∈ T

instance {n : ℕ} (T : Finset (Edge n)) (u v : Vertex n) :
    Decidable (treeAdj T u v) := by
  unfold treeAdj
  infer_instance

-- Reachability by a walk of at most k edges.
def reaches {n : ℕ} (T : Finset (Edge n)) :
    ℕ → Vertex n → Vertex n → Prop
  | 0, u, v => u = v
  | k + 1, u, v =>
      u = v ∨ ∃ w, treeAdj T u w ∧ reaches T k w v

instance {n : ℕ} (T : Finset (Edge n)) (k : ℕ)
    (u v : Vertex n) : Decidable (reaches T k u v) := by
  induction k generalizing u v with
  | zero =>
      unfold reaches
      infer_instance
  | succ k ih =>
      unfold reaches
      infer_instance

def spanningTree {n : ℕ} (T : Finset (Edge n)) : Prop :=
  T ⊆ gridEdges n ∧
  (∀ u v : Vertex n, reaches T (3 * n - 1) u v) ∧
  T.card + 1 = 3 * n

instance {n : ℕ} (T : Finset (Edge n)) :
    Decidable (spanningTree T) := by
  unfold spanningTree
  infer_instance

def distanceIs {n : ℕ} (T : Finset (Edge n))
    (k : ℕ) (u v : Vertex n) : Prop :=
  ¬ reaches T (k - 1) u v ∧ reaches T k u v

instance {n : ℕ} (T : Finset (Edge n)) (k : ℕ)
    (u v : Vertex n) : Decidable (distanceIs T k u v) := by
  unfold distanceIs
  infer_instance

def allowedCycles {n : ℕ} (T : Finset (Edge n)) : Prop :=
  ∀ e ∈ gridEdges n, e ∉ T →
    distanceIs T 3 e.1 e.2 ∨ distanceIs T 5 e.1 e.2

instance {n : ℕ} (T : Finset (Edge n)) :
    Decidable (allowedCycles T) := by
  unfold allowedCycles
  infer_instance

def leaves {n : ℕ} (T : Finset (Edge n)) : ℕ :=
  (Finset.univ.filter fun u : Vertex n =>
    (Finset.univ.filter fun v : Vertex n => treeAdj T u v).card = 1).card

def sixCycles {n : ℕ} (T : Finset (Edge n)) : ℕ :=
  ((gridEdges n \ T).filter fun e => distanceIs T 5 e.1 e.2).card

def witness : Finset (Edge 2) :=
  { ((0, 0), (1, 0)),
    ((0, 0), (0, 1)),
    ((1, 0), (1, 1)),
    ((1, 1), (2, 1)),
    ((2, 0), (2, 1)) }

-- FAITHFULNESS:
-- Fin 3 × Fin n represents the stated vertices by subtracting one from
-- each coordinate; gridEdges is exactly the Manhattan-distance-one graph.
-- Edges are stored once, with their endpoints in increasing order.
-- The universal quantifiers below range over every n ≥ 1 and every
-- spanning tree T.  For a finite simple graph on 3*n vertices, being
-- connected and having 3*n-1 edges is equivalent to being a tree.
-- Connectivity is tested by walks of length at most 3*n-1, which suffices
-- because any reachable pair has a simple path of at most that length.
-- In a tree, the unique cycle created by an absent edge has length one
-- more than the distance between its endpoints.  Thus allowedCycles
-- expresses exactly cycle length four or six, and sixCycles counts
-- exactly the absent edges producing a six-edge cycle.  leaves counts
-- exactly the vertices of degree one.
theorem refutation :
    ¬ (∀ n : ℕ, n ≥ 1 →
      ∀ T : Finset (Edge n), spanningTree T → allowedCycles T →
        leaves T + sixCycles T ≥ n + 1) := by
  intro h
  have ht : spanningTree witness := by decide
  have hc : allowedCycles witness := by decide
  have hl : leaves witness = 2 := by decide
  have hs : sixCycles witness = 0 := by decide
  have bad := h 2 (by decide) witness ht hc
  rw [hl, hs] at bad
  norm_num at bad

end Mathforge.SpanningTreesOfThe3NRectangularGridInWhC3
