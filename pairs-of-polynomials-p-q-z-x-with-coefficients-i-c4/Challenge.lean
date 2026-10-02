import Mathlib

namespace Mathforge.PairsOfPolynomialsPQZXWithCoefficientsIC4

open Finset

namespace Counterexample

def sums (A B : Finset ℕ) : Finset ℕ :=
  (A.product B).image (fun p => p.1 + p.2)

def rep (A B : Finset ℕ) (s : ℕ) : ℕ :=
  ((A.product B).filter (fun p => p.1 + p.2 = s)).card

def doubles (A B : Finset ℕ) : Finset ℕ :=
  (sums A B).filter (fun s => rep A B s = 2)

def participants (A B : Finset ℕ) : Finset (ℕ × ℕ) :=
  (A.product B).filter (fun p => rep A B (p.1 + p.2) = 2)

def moved (U V : Finset ℕ) (T : ℕ) : Finset ℕ :=
  U ∪ V.image (fun v => v + T)

def Split (A B : Finset ℕ) : Prop :=
  ∃ U V : Finset ℕ, ∃ cU cV : ℕ,
    U ∪ V = A ∧ Disjoint U V ∧
    U.Nonempty ∧ V.Nonempty ∧ 0 ∈ U ∧
    Disjoint (sums U B) (sums V B) ∧
    doubles U B = {cU} ∧ doubles V B = {cV} ∧
    ∀ T : ℕ, A.sup id + B.sup id < T →
      (moved U V T).card = A.card ∧
      B.card = B.card ∧
      doubles (moved U V T) B = {cU, cV + T} ∧
      Nat.dist cU (cV + T) = T + cV - cU

def AlternativeI (A B : Finset ℕ) : Prop :=
  Split A B ∨ Split B A

def Pattern (A B : Finset ℕ) : Prop :=
  ∃ u v d : ℕ, 0 < d ∧
    ({u, u + d} : Finset ℕ) ⊆ A ∧
    ({v, v + d, v + 2 * d} : Finset ℕ) ⊆ B ∧
    participants A B =
      {(u, v + d), (u + d, v), (u, v + 2 * d), (u + d, v + d)} ∧
    Nat.dist (u + v + d) (u + v + 2 * d) = d

def AlternativeII (A B : Finset ℕ) : Prop :=
  (Pattern A B ∨ Pattern B A) ∧ ¬ AlternativeI A B

-- A finite necessary condition for a splitting.
def SplitTest (A B : Finset ℕ) : Prop :=
  ∃ U ∈ A.powerset, ∃ V ∈ A.powerset,
    U ∪ V = A ∧ Disjoint U V ∧
    U.Nonempty ∧ V.Nonempty ∧ 0 ∈ U ∧
    Disjoint (sums U B) (sums V B) ∧
    (doubles U B).card = 1 ∧ (doubles V B).card = 1

def TripleTest (B : Finset ℕ) : Prop :=
  ∃ v ∈ B, ∃ d ∈ range (B.sup id + 1),
    0 < d ∧ ({v, v + d, v + 2 * d} : Finset ℕ) ⊆ B

def A : Finset ℕ := {0, 1, 3}

def B : Finset ℕ := {0, 1, 4}

-- FAITHFULNESS:
-- A and B range over all finite subsets of the nonnegative integers.
-- Membership of 0 supplies the constant terms. The bound on rep is quantified
-- over sums A B: outside this set rep is identically zero, so this is exactly
-- the bound at every nonnegative integer. The cardinality of doubles counts
-- exactly the exponents with coefficient 2.
-- Split quantifies U,V,cU,cV and every natural T above the two maxima
-- (sup id is the maximum for these nonempty supports). It records the
-- partition, nonemptiness, zero membership, disjoint sum supports, the two
-- restricted doubled exponents, both sizes, the shifted doubled exponents,
-- and their separation. AlternativeI allows exchange of the supports.
-- Pattern quantifies the nonnegative u,v and positive d, both inclusions,
-- the complete participating-pair set, and separation d. AlternativeII
-- allows exchange and excludes splitting on either side.
-- The final disjunction is exclusive: exactly one alternative holds.
theorem refutation :
    ¬ (∀ A B : Finset ℕ,
      0 ∈ A → 0 ∈ B →
      (∀ s ∈ sums A B, rep A B s ≤ 2) →
      (doubles A B).card = 2 →
      ((AlternativeI A B ∧ ¬ AlternativeII A B) ∨
       (AlternativeII A B ∧ ¬ AlternativeI A B))) := by
  sorry

end Counterexample

end Mathforge.PairsOfPolynomialsPQZXWithCoefficientsIC4
