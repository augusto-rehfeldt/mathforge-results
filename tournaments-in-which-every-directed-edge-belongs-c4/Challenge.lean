import Mathlib

namespace Mathforge.TournamentsInWhichEveryDirectedEdgeBelongsC4

open Finset

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace TournamentRefutation

abbrev Digraph (n : ℕ) := Fin n → Fin n → Bool

def Tournament {n : ℕ} (E : Digraph n) : Prop :=
  (∀ x, E x x = false) ∧
  (∀ x y, x ≠ y → (E x y = true ↔ E y x = false))

/-- The outgoing-cut characterization of strong connectivity. -/
def Strong {n : ℕ} (E : Digraph n) (A : Finset (Fin n)) : Prop :=
  ∀ S ∈ A.powerset, S.Nonempty → S ≠ A →
    ∃ x ∈ S, ∃ y ∈ A, y ∉ S ∧ E x y = true

/-- Each three-element set is represented uniquely by its increasing triple. -/
def triangles {n : ℕ} (E : Digraph n) :
    Finset (Fin n × Fin n × Fin n) :=
  (univ ×ˢ (univ ×ˢ univ)).filter fun t =>
    t.1 < t.2.1 ∧ t.2.1 < t.2.2 ∧
      ((E t.1 t.2.1 = true ∧ E t.2.1 t.2.2 = true ∧
          E t.2.2 t.1 = true) ∨
       (E t.1 t.2.2 = true ∧ E t.2.2 t.2.1 = true ∧
          E t.2.1 t.1 = true))

def contains {n : ℕ} (t : Fin n × Fin n × Fin n) (v : Fin n) : Prop :=
  v = t.1 ∨ v = t.2.1 ∨ v = t.2.2

instance {n : ℕ} (t : Fin n × Fin n × Fin n) (v : Fin n) :
    Decidable (contains t v) := inferInstanceAs
      (Decidable (v = t.1 ∨ v = t.2.1 ∨ v = t.2.2))

def c {n : ℕ} (E : Digraph n) (x y : Fin n) : ℕ :=
  ((triangles E).filter fun t => contains t x ∧ contains t y).card

def cAfter {n : ℕ} (E : Digraph n) (v x y : Fin n) : ℕ :=
  ((triangles E).filter fun t =>
    contains t x ∧ contains t y ∧ ¬ contains t v).card

def a {n : ℕ} (E : Digraph n) (v : Fin n) : ℕ :=
  ((triangles E).filter fun t => contains t v).card

def b {n : ℕ} (E : Digraph n) (v : Fin n) : ℕ :=
  ((univ ×ˢ univ).filter fun p =>
    p.1 ≠ v ∧ p.2 ≠ v ∧ E p.1 p.2 = true ∧
      c E p.1 p.2 = 2 ∧ cAfter E v p.1 p.2 = 1).card

def witness : Digraph 7 := fun x y =>
  decide ((x.val, y.val) ∈
    ([(0, 2), (0, 5), (0, 6),
      (1, 0), (1, 4), (1, 6),
      (2, 1), (2, 3), (2, 6),
      (3, 0), (3, 1), (3, 5),
      (4, 0), (4, 2), (4, 3),
      (5, 1), (5, 2), (5, 4),
      (6, 3), (6, 4), (6, 5)] : List (ℕ × ℕ)))

-- FAITHFULNESS:
-- The claim quantifies over every natural number n >= 4 and every tournament
-- on Fin n. This is equivalent to quantifying over integers n >= 4 and all
-- n-vertex tournaments, by converting n to a natural number and relabeling
-- the vertices. Tournament asserts no loops and exactly one orientation for
-- each distinct pair. Strong is the standard equivalent finite-graph
-- characterization: every nonempty proper vertex subset has an outgoing
-- edge. Thus Strong E univ means directed-path strong connectivity, and
-- Strong E (univ.erase v) means strong connectivity of the induced deletion.
-- triangles enumerates each cyclic three-element vertex set exactly once,
-- using its increasing ordering. c counts triangles containing an edge;
-- cAfter counts those avoiding the deleted vertex. The edge hypothesis
-- bounds c by two for every directed edge. a counts triangles through v,
-- and b counts precisely surviving directed edges with c = 2 and
-- cAfter = 1. The conclusion has the required existential vertex and both
-- the deletion-connectivity and a + b <= 8 conditions.
theorem refutation :
    ¬ (∀ n : ℕ, 4 ≤ n →
        ∀ E : Digraph n,
          Tournament E →
          Strong E univ →
          (∀ x y, E x y = true → c E x y ≤ 2) →
          ∃ v : Fin n,
            Strong E (univ.erase v) ∧ a E v + b E v ≤ 8) := by
  sorry

end TournamentRefutation

end Mathforge.TournamentsInWhichEveryDirectedEdgeBelongsC4
