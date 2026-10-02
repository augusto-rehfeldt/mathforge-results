import Mathlib

open Finset

abbrev Permutation (n : ℕ) := Equiv.Perm (Fin n)
abbrev Triple (n : ℕ) := Fin n × Fin n × Fin n

def Is132 {n : ℕ} (p : Permutation n) (a : Triple n) : Prop :=
  a.1 < a.2.1 ∧ a.2.1 < a.2.2 ∧
    p a.1 < p a.2.2 ∧ p a.2.2 < p a.2.1

instance {n : ℕ} (p : Permutation n) (a : Triple n) :
    Decidable (Is132 p a) := inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

def occurrences {n : ℕ} (p : Permutation n) : Finset (Triple n) :=
  univ.filter (Is132 p)

def Incident {n : ℕ} (i : Fin n) (a : Triple n) : Prop :=
  i = a.1 ∨ i = a.2.1 ∨ i = a.2.2

instance {n : ℕ} (i : Fin n) (a : Triple n) :
    Decidable (Incident i a) := inferInstanceAs (Decidable (_ ∨ _ ∨ _))

abbrev Vertex {n : ℕ} (p : Permutation n) :=
  Fin n ⊕ {a : Triple n // Is132 p a}

def Adj {n : ℕ} (p : Permutation n) : Vertex p → Vertex p → Prop
  | .inl i, .inr a => Incident i a.val
  | .inr a, .inl i => Incident i a.val
  | _, _ => False

def Connected {n : ℕ} (p : Permutation n) : Prop :=
  ∀ S : Finset (Vertex p), S.Nonempty → S ≠ univ →
    ∃ u ∈ S, ∃ v, v ∉ S ∧ Adj p u v

-- For a finite nonempty undirected graph, connectedness together with
-- |E| + 1 = |V| is equivalent to connectedness and absence of cycles.
-- Each occurrence has three distinct neighbors, so |E| = 3 * #occurrences.
def InT {n : ℕ} (p : Permutation n) : Prop :=
  (∀ i : Fin n, ∃ a ∈ occurrences p, Incident i a) ∧
  Connected p ∧
  3 * (occurrences p).card + 1 = n + (occurrences p).card

def Canonical {n : ℕ} (p : Permutation n) : Prop :=
  ∀ i : Fin n,
    (p i).val =
      if i.val = 0 then 0
      else if i.val % 2 = 1 then i.val + 1 else i.val - 1

def inv {n : ℕ} (p : Permutation n) : ℕ :=
  (univ.filter fun ij : Fin n × Fin n =>
    ij.1 < ij.2 ∧ p ij.2 < p ij.1).card

def des {n : ℕ} (p : Permutation n) : ℕ :=
  (univ.filter fun ij : Fin n × Fin n =>
    ij.2.val = ij.1.val + 1 ∧ p ij.2 < p ij.1).card

def exclusive {n : ℕ} (p : Permutation n) (a : Triple n) : Finset (Fin n) :=
  univ.filter fun i =>
    Incident i a ∧
      ∀ b ∈ occurrences p, Incident i b → b = a

-- An increasing enumeration of the retained positions, with all comparisons
-- of values preserved, specifies standardization without choosing an algorithm.
def StandardizedDeletion {n : ℕ} (p : Permutation n) (a : Triple n)
    (p' : Permutation (n - 2)) : Prop :=
  ∃ f : Fin (n - 2) → Fin n,
    StrictMono f ∧
    (∀ i : Fin n, (∃ j, f j = i) ↔ i ∉ exclusive p a) ∧
    (∀ i j, p' i < p' j ↔ p (f i) < p (f j))

noncomputable def weight {n : ℕ} (p : Permutation n) :
    MvPolynomial (Fin 2) ℤ :=
  MvPolynomial.X (0 : Fin 2) ^ inv p *
    MvPolynomial.X (1 : Fin 2) ^ des p

noncomputable def enumerator (n : ℕ) : MvPolynomial (Fin 2) ℤ :=
  by
    classical
    exact ∑ p ∈ (univ : Finset (Permutation n)).filter InT, weight p

-- FAITHFULNESS:
-- Fin n uses zero-based positions and values; adding one recovers the notation
-- {1,...,n}. Is132 lists exactly the position and value inequalities.
-- Vertex and Adj are the entry–occurrence incidence graph. InT requires every
-- entry to occur, connectedness, and the finite-tree edge-count criterion.
-- The first conjunct below quantifies over every n >= 1 and every permutation:
-- membership is equivalent to n = 2m+1 for some m >= 1 and the displayed
-- permutation. Thus it includes both emptiness and exact membership.
-- The second conjunct is the stated polynomial identity for every m >= 1,
-- with commuting indeterminates X 0 and X 1.
-- The third quantifies over m >= 2, every member, and every occurrence.
-- exclusive is precisely the entries belonging only to that occurrence;
-- its cardinality must be two. StandardizedDeletion deletes those positions
-- and preserves the relative order of retained values. The result is in T,
-- is the displayed unique member, and both statistics decrease by one.
def Claim : Prop :=
  (∀ n : ℕ, 1 ≤ n → ∀ p : Permutation n,
    InT p ↔ ∃ m : ℕ, 1 ≤ m ∧ n = 2 * m + 1 ∧ Canonical p) ∧
  (∀ m : ℕ, 1 ≤ m →
    enumerator (2 * m + 1) =
      MvPolynomial.X (0 : Fin 2) ^ m *
        MvPolynomial.X (1 : Fin 2) ^ m) ∧
  (∀ m : ℕ, 2 ≤ m → ∀ p : Permutation (2 * m + 1),
    InT p → ∀ a : Triple (2 * m + 1), Is132 p a →
      (exclusive p a).card = 2 ∧
      ∃ p' : Permutation ((2 * m + 1) - 2),
        StandardizedDeletion p a p' ∧ InT p' ∧ Canonical p' ∧
        inv p = inv p' + 1 ∧ des p = des p' + 1)

def witnessFunction : Fin 5 → Fin 5 :=
  ![0, 2, 1, 4, 3]

noncomputable def witness : Permutation 5 :=
  Equiv.ofBijective witnessFunction (by decide)

theorem witness_canonical : Canonical witness := by
  unfold Canonical
  decide

theorem witness_occurrences : (occurrences witness).card = 4 := by
  decide

theorem refutation : ¬ Claim := by
  intro h
  have ht : InT witness :=
    (h.1 5 (by norm_num) witness).2
      ⟨2, by norm_num, by norm_num, witness_canonical⟩
  have he := ht.2.2
  rw [witness_occurrences] at he
  norm_num at he
set_option pp.fullNames true in
#print axioms witness_canonical
set_option pp.fullNames true in
#print axioms witness_occurrences
set_option pp.fullNames true in
#print axioms refutation