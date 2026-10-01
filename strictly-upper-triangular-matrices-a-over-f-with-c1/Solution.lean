import Mathlib

namespace Mathforge.StrictlyUpperTriangularMatricesAOverFWithC1

open Finset

namespace Counterexample

abbrev B := ZMod 2

abbrev V := Fin 3 → B

abbrev Boundary := Fin 6 → Fin 3 → B

abbrev Interior (n : ℕ) := Fin n → Fin n → B

abbrev Exponents := Fin 4 → ℕ

def IsSubspace (I : Finset V) : Prop :=
  (0 : V) ∈ I ∧
  ∀ u ∈ I, ∀ v ∈ I, u + v ∈ I

instance (I : Finset V) : Decidable (IsSubspace I) := by
  unfold IsSubspace
  infer_instance

def admissible {n : ℕ} (A : Interior n) : Prop :=
  (∀ i j, A i j ≠ 0 →
    i.val + 1 ≤ j.val ∧ j.val ≤ i.val + 3) ∧
  ∀ i j, (∑ k, A i k * A k j) = 0

instance {n : ℕ} (A : Interior n) : Decidable (admissible A) := by
  unfold admissible
  infer_instance

def applyMatrix {n : ℕ} (A : Interior n) (z : Fin n → B) :
    Fin n → B :=
  fun i => ∑ j, A i j * z j

def image {n : ℕ} (A : Interior n) : Finset (Fin n → B) :=
  Finset.univ.image (applyMatrix A)

-- A binary vector space of dimension r has exactly 2^r elements.
def matrixRank {n : ℕ} (A : Interior n) : ℕ :=
  Nat.log 2 (image A).card

def padded {n : ℕ} (A : Interior n) (i j : ℤ) : B :=
  ∑ a : Fin n, ∑ b : Fin n,
    if i = (a.val : ℤ) + 1 ∧ j = (b.val : ℤ) + 1 then A a b else 0

def boundary {n : ℕ} (A : Interior n) : Boundary :=
  fun r c => padded A ((n : ℤ) - 5 + r.val) ((n : ℤ) - 2 + c.val)

def embed (n : ℕ) (u : V) : Fin n → B :=
  fun i => ∑ c : Fin 3,
    if (i.val : ℤ) + 1 = (n : ℤ) - 2 + c.val then u c else 0

def boundaryImage {n : ℕ} (A : Interior n) : Finset V :=
  Finset.univ.filter fun u =>
    embed n u ∈ image A ∧
    ∀ c : Fin 3, (n : ℤ) - 2 + c.val ≤ 0 → u c = 0

def diagonalCount {n : ℕ} (A : Interior n) (k : ℕ) : ℕ :=
  (Finset.univ.filter fun p : Fin n × Fin n =>
    p.2.val = p.1.val + k ∧ A p.1 p.2 = 1).card

def weight {n : ℕ} (A : Interior n) : Exponents :=
  ![matrixRank A, diagonalCount A 1, diagonalCount A 2, diagonalCount A 3]

-- Coefficients determine the polynomials uniquely; all coefficients are natural.
def F (n : ℕ) (H : Boundary) (I : Finset V) (e : Exponents) : ℕ :=
  ∑ A : Interior n,
    if admissible A ∧ boundary A = H ∧ boundaryImage A = I ∧ weight A = e
    then 1 else 0

def annihilates (H : Boundary) (v : V) : Prop :=
  ∀ r, (∑ c, H r c * v c) = 0

instance (H : Boundary) (v : V) : Decidable (annihilates H v) := by
  unfold annihilates
  infer_instance

def nextBoundary (H : Boundary) (v : V) : Boundary :=
  fun r c =>
    if hc : c.val < 2 then
      if h : r.val < 5 then
        H ⟨r.val + 1, by omega⟩ ⟨c.val + 1, by omega⟩
      else 0
    else
      if r.val = 2 then v 0
      else if r.val = 3 then v 1
      else if r.val = 4 then v 2
      else 0

def nextImage (I : Finset V) (v : V) : Finset V :=
  Finset.univ.filter fun u =>
    u 2 = 0 ∧
    ∃ w ∈ I, ∃ s : B, (![0, u 0, u 1] : V) = w + s • v

def increment (I : Finset V) (v : V) : Exponents :=
  ![if v ∈ I then 0 else 1,
    if v 2 = 1 then 1 else 0,
    if v 1 = 1 then 1 else 0,
    if v 0 = 1 then 1 else 0]

-- This is the recurrence's coefficient, with the source-state sums expanded
-- using the defining sum for F_n.
def predicted (n : ℕ) (H : Boundary) (I : Finset V) (e : Exponents) : ℕ :=
  ∑ A : Interior n, ∑ v : V,
    if admissible A ∧ annihilates (boundary A) v ∧
       nextBoundary (boundary A) v = H ∧
       nextImage (boundaryImage A) v = I ∧
       weight A + increment (boundaryImage A) v = e
    then 1 else 0

-- FAITHFULNESS:
-- n : ℕ is precisely the quantifier over integers n ≥ 0.
-- Boundary enumerates all 6-by-3 binary matrices. Finset V with IsSubspace
-- enumerates exactly all subspaces of F₂³: containing zero and being closed
-- under addition suffices over F₂. Interior n enumerates all binary n-by-n
-- matrices; admissible imposes the bandwidth and A² = 0 conditions.
-- padded implements the zero-outside-index convention; boundary and
-- boundaryImage implement H(A) and I(A), including the missing-coordinate
-- condition. matrixRank is rank, computed from the cardinality of im(A).
-- Exponents quantifies over every monomial in t,x₁,x₂,x₃. F is its defined
-- coefficient. predicted expands the sum over source states and F_n into
-- a sum over their defining matrices, without any extra restriction on v.
-- Thus the last equality is exactly the proposed autonomous recurrence,
-- for every target state and every coefficient, not merely its witness.
-- The first conjunct states the prescribed initialization.
def Claim : Prop :=
  (∀ H I e, IsSubspace I →
    F 0 H I e =
      if H = 0 ∧ I = {0} ∧ e = 0 then 1 else 0) ∧
  (∀ n H I e, IsSubspace I →
    F (n + 1) H I e = predicted n H I e)

def witnessH : Boundary :=
  ![![0, 0, 0], ![0, 0, 0], ![0, 0, 0],
    ![0, 0, 0], ![0, 0, 1], ![0, 0, 0]]

def witnessI : Finset V :=
  {![0, 0, 0], ![0, 1, 0]}

def witnessExponent : Exponents := ![1, 1, 0, 0]

theorem refutation : ¬ Claim := by
  intro h
  have hs : IsSubspace witnessI := by decide
  have he := h.2 0 witnessH witnessI witnessExponent hs
  have actual : F 1 witnessH witnessI witnessExponent = 0 := by decide
  have proposed : predicted 0 witnessH witnessI witnessExponent = 1 := by decide
  rw [actual, proposed] at he
  exact Nat.zero_ne_one he

end Counterexample

end Mathforge.StrictlyUpperTriangularMatricesAOverFWithC1
