import Mathlib

open Finset

def indices (m : ℕ) : Finset (Fin m) :=
  Finset.univ.filter (fun i => i.val ≠ 0)

def representative {m : ℕ} (a : Fin m → ℕ) (i : Fin m) : ℕ :=
  i.val + m * a i

-- This is precisely membership in the displayed semigroup, including
-- nonnegativity; the congruence and lower bound encode the parameter t ≥ 0.
def inS {m : ℕ} (a : Fin m → ℕ) (x : ℤ) : Prop :=
  0 ≤ x ∧
    (x % (m : ℤ) = 0 ∨
      ∃ i ∈ indices m,
        (representative a i : ℤ) ≤ x ∧
        x % (m : ℤ) = (i.val : ℤ))

instance {m : ℕ} (a : Fin m → ℕ) (x : ℤ) : Decidable (inS a x) := by
  unfold inS
  infer_instance

def kunz {m : ℕ} (a : Fin m → ℕ) : Prop :=
  ∀ i j : Fin m, i.val ≠ 0 → j.val ≠ 0 →
    (∀ k : Fin m,
      (i.val + j.val < m ∧ k.val = i.val + j.val →
        a k ≤ a i + a j) ∧
      (m < i.val + j.val ∧ k.val = i.val + j.val - m →
        a k ≤ a i + a j + 1))

instance {m : ℕ} (a : Fin m → ℕ) : Decidable (kunz a) := by
  unfold kunz
  infer_instance

def maxima {m : ℕ} (a : Fin m → ℕ) : Finset (Fin m) :=
  (indices m).filter fun i =>
    ∀ j : Fin m, j.val ≠ 0 →
      inS a ((representative a j : ℤ) - representative a i) → j = i

-- Any positive summands of x lie strictly between 0 and x.
def minimalGenerator {m : ℕ} (a : Fin m → ℕ) (x : ℕ) : Prop :=
  0 < x ∧ inS a (x : ℤ) ∧
    ∀ y : Fin x, y.val ≠ 0 →
      ¬ (inS a (y.val : ℤ) ∧ inS a ((x : ℤ) - y.val))

instance {m : ℕ} (a : Fin m → ℕ) (x : ℕ) :
    Decidable (minimalGenerator a x) := by
  unfold minimalGenerator
  infer_instance

def lower {m : ℕ} (a : Fin m → ℕ) (r : Fin m) : Fin m → ℕ :=
  fun i => if i = r then 2 else a i

def complementaryIndex {m : ℕ} (hm : 0 < m) (r j : Fin m) : Fin m :=
  ⟨(r.val + m - j.val) % m, Nat.mod_lt _ hm⟩

def candidates {m : ℕ} (hm : 0 < m)
    (a : Fin m → ℕ) (p r : Fin m) : Finset (Fin m) :=
  (indices m).filter fun j =>
    j ≠ p ∧ j ≠ r ∧
    a j + a (complementaryIndex hm r j) +
        (if j.val < r.val then 0 else 1) = 3 ∧
    minimalGenerator a (representative a (complementaryIndex hm r j)) ∧
    ¬ inS a ((representative a p : ℤ) - representative a j)

def retained {m : ℕ} (a : Fin m → ℕ) (p r : Fin m) :
    Finset (Fin m) :=
  if ¬ inS a ((representative a p : ℤ) -
      ((representative a r : ℤ) - m))
  then {r} else ∅

def exposed {m : ℕ} (hm : 0 < m)
    (a : Fin m → ℕ) (p r : Fin m) : Finset (Fin m) :=
  candidates hm a p r ∪ retained a p r

def genus {m : ℕ} (a : Fin m → ℕ) : ℕ :=
  ∑ i ∈ indices m, a i

def exactlyTwo {m : ℕ} (s : Finset (Fin m)) : Prop :=
  ∃ x y : Fin m, x ≠ y ∧ s = {x, y}

def residueGap {m : ℕ} (p q : Fin m) : ℕ :=
  ((p.val : ℤ) - q.val).natAbs

-- FAITHFULNESS:
-- m ranges over natural numbers with m ≥ 3, equivalently the integers ≥ 3.
-- Coordinates are functions on Fin m; coordinate zero is unused, and all
-- conditions and sums restrict to indices 1,...,m-1.
-- The universal a,p,r hypotheses give the coordinate range, both families
-- of Kunz inequalities, exactly the two distinct maximal indices, and a_r=3.
-- inS implements the stated S, so maxima uses exactly the Apéry order.
-- minimalGenerator excludes every decomposition into two positive members.
-- complementaryIndex and the conditional epsilon implement k(j) and ε(j);
-- candidates, retained, and exposed are respectively C, R, and D.
-- The conclusion includes Kunz(b), the asserted maximal set, the exact-two
-- equivalence, and, for every singleton witness q, genus g-1 and gap |p-q|.
theorem refutation :
    ¬ (∀ (m : ℕ) (hm : 3 ≤ m) (a : Fin m → ℕ) (p r : Fin m),
      (∀ i : Fin m, i.val ≠ 0 → a i ∈ ({1, 2, 3} : Finset ℕ)) →
      kunz a →
      p.val ≠ 0 → r.val ≠ 0 → p ≠ r →
      maxima a = {p, r} →
      a r = 3 →
      let b := lower a r
      let D := exposed (by omega : 0 < m) a p r
      kunz b ∧
      maxima b = {p} ∪ D ∧
      (exactlyTwo (maxima b) ↔ ∃ q : Fin m, D = {q}) ∧
      (∀ q : Fin m, D = {q} →
        genus b = genus a - 1 ∧
        maxima b = {p, q} ∧
        residueGap p q = ((p.val : ℤ) - q.val).natAbs)) := by
  intro claim
  let a : Fin 5 → ℕ := fun i =>
    if i.val = 1 then 3
    else if i.val = 2 then 1
    else if i.val = 3 then 3
    else 1
  let p : Fin 5 := ⟨3, by omega⟩
  let r : Fin 5 := ⟨1, by omega⟩
  have hrange : ∀ i : Fin 5,
      i.val ≠ 0 → a i ∈ ({1, 2, 3} : Finset ℕ) := by decide
  have hk : kunz a := by decide
  have hp : p.val ≠ 0 := by decide
  have hr : r.val ≠ 0 := by decide
  have hpr : p ≠ r := by decide
  have hmax : maxima a = {p, r} := by decide
  have har : a r = 3 := by decide
  have result := claim 5 (by omega) a p r hrange hk hp hr hpr hmax har
  have asserted :
      maxima (lower a r) =
        {p} ∪ exposed (by omega : 0 < 5) a p r :=
    result.2.1
  have mismatch :
      maxima (lower a r) ≠
        {p} ∪ exposed (by omega : 0 < 5) a p r := by decide
  exact mismatch asserted
set_option pp.fullNames true in
#print axioms refutation