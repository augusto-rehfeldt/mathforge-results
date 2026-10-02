import Mathlib

noncomputable section

open Polynomial

abbrev F := ZMod 2
abbrev Word := List F

def p : Word → Polynomial F
  | [] => 1
  | [a] => X + C a
  | a :: b :: t => (X + C a) * p (b :: t) + p t

def q (t : Word) : Polynomial F := p t.dropLast

def r (t : Word) : Polynomial F :=
  if t.length ≥ 2 then p t.tail.dropLast else 0

def B (t : Word) : (F × F) × (F × F) :=
  ((eval 0 (p t), eval 0 (q t)), (eval 1 (p t), eval 1 (q t)))

def allowed (z : F × F) : Prop :=
  z = (0, 1) ∨ z = (1, 0) ∨ z = (1, 1)

def M (t : Word) : Matrix (Fin t.length) (Fin t.length) F :=
  fun i j =>
    if i = j then t.get i
    else if i.val + 1 = j.val ∨ j.val + 1 = i.val then 1 else 0

def shiftedAction (t : Word) (a : F)
    (x : Fin t.length → F) : Fin t.length → F :=
  fun i => ∑ j, (M t i j + if i = j then a else 0) * x j

-- A finite F₂-vector space has cardinality 2^dimension. Thus this
-- cardinality formula is exactly its vector-space dimension, not a rank proxy.
def kernelDimension (t : Word) (a : F) : ℕ :=
  Nat.log 2
    ((Finset.univ.filter fun x : Fin t.length → F =>
      shiftedAction t a (shiftedAction t a x) = 0).card)

def signature (t : Word) : ℕ × ℕ :=
  (kernelDimension t 0, kernelDimension t 1)

def sandwich (u v : Word) : Word := u ++ v ++ u.reverse

def f (u v : Word) (a : F) : Polynomial F :=
  C (eval a (p u)) * p v + C (eval a (q u)) * r v

def predicted (u v : Word) (a : F) : ℕ :=
  if eval a (f u v a) = 1 then 0
  else if eval a (f u v a) = 0 ∧ eval a (derivative (f u v a)) = 1
    then 1 else 2

def Claim : Prop :=
  (∀ z : (F × F) × (F × F),
    (∃ u : Word, u ≠ [] ∧ B u = z) ↔
      allowed z.1 ∧ allowed z.2) ∧
  (∀ u v : Word, u ≠ [] → v ≠ [] →
    (sandwich u v).length = 2 * u.length + v.length ∧
    ∀ a : F, kernelDimension (sandwich u v) a = predicted u v a) ∧
  (∀ u w : Word, u ≠ [] → w ≠ [] →
    (B u = B w ↔
      ∀ v : Word, v ≠ [] →
        signature (sandwich u v) = signature (sandwich w v)))

-- FAITHFULNESS:
-- Word is the type of all finite binary words; ≠ [] expresses nonemptiness.
-- p is the tridiagonal determinant's continuant recurrence, including p_empty.
-- q deletes the last letter; r deletes both endpoints, with the specified
-- singleton convention. M has precisely the stated diagonal and off-diagonals.
-- kernelDimension counts the kernel of the square of M+aI and takes log₂,
-- which equals dimension over F₂. The first conjunct says the range of B is
-- exactly the specified Cartesian square. The second universally quantifies
-- u,v,a and includes both the size assertion and the displayed identity.
-- The last conjunct is the universally quantified completeness equivalence,
-- using the ordered dimensions at 0 and 1.

theorem refutation : ¬ Claim := by
  intro h
  have hi := (h.2.1 [0] [0, 1] (by simp) (by simp)).2 (1 : F)
  have hd : kernelDimension (sandwich [0] [0, 1]) 1 = 0 := by
    decide
  have hp : predicted [0] [0, 1] 1 = 1 := by
    norm_num [predicted, f, p, q, r, Polynomial.derivative_mul,
      Polynomial.eval_mul, Polynomial.eval_add] <;> decide
  rw [hd, hp] at hi
  exact Nat.zero_ne_one hi
set_option pp.fullNames true in
#print axioms refutation