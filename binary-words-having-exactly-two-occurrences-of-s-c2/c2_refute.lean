import Mathlib

namespace BinarySquares

def Square {n : ℕ} (w : Fin n → Bool)
    (p : Fin n × Fin (n + 1)) : Prop :=
  0 < p.2.val ∧
  p.1.val + 2 * p.2.val ≤ n ∧
  ∀ j : Fin p.2.val,
    ∀ h₁ : p.1.val + j.val < n,
    ∀ h₂ : p.1.val + p.2.val + j.val < n,
      w ⟨p.1.val + j.val, h₁⟩ =
        w ⟨p.1.val + p.2.val + j.val, h₂⟩

instance {n : ℕ} (w : Fin n → Bool)
    (p : Fin n × Fin (n + 1)) : Decidable (Square w p) :=
  inferInstanceAs (Decidable
    (0 < p.2.val ∧
      p.1.val + 2 * p.2.val ≤ n ∧
      ∀ j : Fin p.2.val,
        ∀ h₁ : p.1.val + j.val < n,
        ∀ h₂ : p.1.val + p.2.val + j.val < n,
          w ⟨p.1.val + j.val, h₁⟩ =
            w ⟨p.1.val + p.2.val + j.val, h₂⟩))

def squares {n : ℕ} (w : Fin n → Bool) :
    Finset (Fin n × Fin (n + 1)) :=
  Finset.univ.filter (Square w)

def append {n k : ℕ} (w : Fin n → Bool) (x : Fin k → Bool) :
    Fin (n + k) → Bool :=
  fun j =>
    if h : j.val < n then
      w ⟨j.val, h⟩
    else
      x ⟨j.val - n, by have := j.isLt; omega⟩

def witness : Fin 5 → Bool :=
  ![true, false, true, false, false]

def first : Fin 5 × Fin 6 := (⟨0, by decide⟩, ⟨2, by decide⟩)
def later : Fin 5 × Fin 6 := (⟨3, by decide⟩, ⟨1, by decide⟩)

-- FAITHFULNESS:
-- Natural n ≥ 1 and natural k represent precisely the integer ranges n ≥ 1
-- and k ≥ 0. Functions Fin n → Bool are all binary words of length n.
-- An occurrence p uses zero-based start p.1 and positive root length p.2;
-- its one-based interval is [p.1 + 1, p.1 + 2*p.2].
-- Square expresses exactly the required equalities and bounds, and squares
-- counts distinct occurrence pairs, not distinct factors.
-- The universally quantified a,c are the two occurrences in start order.
-- Their strict start and end inequalities express noncontainment; the middle
-- inequality expresses overlap. Together with cardinality two they give
-- exactly the informal hypothesis.
-- The later final position b is c.1 + 2*c.2, so the displayed subtraction
-- is t = n-b (nonnegative by the occurrence bound).
-- ∃! quantifies exactly one word, while ¬∃ quantifies no word. All k,
-- including zero, are quantified; Fin 0 → Bool has exactly one element.
theorem refutation :
    ¬ (∀ (n : ℕ), 1 ≤ n →
      ∀ (w : Fin n → Bool),
      ∀ (a c : Fin n × Fin (n + 1)),
        (squares w).card = 2 →
        a ∈ squares w →
        c ∈ squares w →
        a.1.val < c.1.val →
        c.1.val < a.1.val + 2 * a.2.val →
        a.1.val + 2 * a.2.val < c.1.val + 2 * c.2.val →
        (c.2.val = 1 ∨ c.2.val = 2) ∧
        (c.2.val = 1 →
          n - (c.1.val + 2 * c.2.val) ≤ 2 ∧
          ∀ k : ℕ,
            (k ≤ 2 - (n - (c.1.val + 2 * c.2.val)) →
              ∃! x : Fin k → Bool, (squares (append w x)).card = 2) ∧
            (2 - (n - (c.1.val + 2 * c.2.val)) < k →
              ¬ ∃ x : Fin k → Bool,
                (squares (append w x)).card = 2)) ∧
        (c.2.val = 2 →
          n - (c.1.val + 2 * c.2.val) = 0 ∧
          ∀ k : ℕ, 0 < k →
            ¬ ∃ x : Fin k → Bool,
              (squares (append w x)).card = 2)) := by
  intro claim
  have result := claim 5 (by decide) witness first later
    (by decide) (by decide) (by decide)
    (by decide) (by decide) (by decide)
  have uniqueExtension :=
    ((result.2.1 (by rfl)).2 2).1 (by decide)
  obtain ⟨x, hx, _⟩ := uniqueExtension
  have noExtension :
      ¬ ∃ x : Fin 2 → Bool,
        (squares (append witness x)).card = 2 := by
    decide
  exact noExtension ⟨x, hx⟩

end BinarySquares
set_option pp.fullNames true in
#print axioms BinarySquares.refutation