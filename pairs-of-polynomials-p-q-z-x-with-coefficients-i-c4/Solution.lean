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

lemma split_test {A B : Finset ℕ} (h : Split A B) :
    SplitTest A B := by
  rcases h with ⟨U, V, cU, cV, hUV, hd, hu, hv, hz, hs, hcU, hcV, ht⟩
  have hUA : U ⊆ A := by
    intro x hx
    rw [← hUV]
    exact mem_union_left V hx
  have hVA : V ⊆ A := by
    intro x hx
    rw [← hUV]
    exact mem_union_right U hx
  refine ⟨U, mem_powerset.mpr hUA, V, mem_powerset.mpr hVA,
    hUV, hd, hu, hv, hz, hs, ?_, ?_⟩
  · rw [hcU]
    simp
  · rw [hcV]
    simp

def TripleTest (B : Finset ℕ) : Prop :=
  ∃ v ∈ B, ∃ d ∈ range (B.sup id + 1),
    0 < d ∧ ({v, v + d, v + 2 * d} : Finset ℕ) ⊆ B

lemma pattern_test {A B : Finset ℕ} (h : Pattern A B) :
    TripleTest B := by
  rcases h with ⟨u, v, d, hd, ha, hb, hp, hs⟩
  have hv : v ∈ B := hb (by simp)
  have hlast : v + 2 * d ∈ B := hb (by simp)
  have hbound : v + 2 * d ≤ B.sup id :=
    le_sup (f := id) hlast
  refine ⟨v, hv, d, mem_range.mpr ?_, hd, hb⟩
  omega

def A : Finset ℕ := {0, 1, 3}

def B : Finset ℕ := {0, 1, 4}

lemma no_I : ¬ AlternativeI A B := by
  have h₁ : ¬ SplitTest A B := by
    unfold SplitTest
    decide
  have h₂ : ¬ SplitTest B A := by
    unfold SplitTest
    decide
  intro h
  rcases h with h | h
  · exact h₁ (split_test h)
  · exact h₂ (split_test h)

lemma no_II : ¬ AlternativeII A B := by
  have h₁ : ¬ TripleTest B := by
    unfold TripleTest
    decide
  have h₂ : ¬ TripleTest A := by
    unfold TripleTest
    decide
  rintro ⟨h, _⟩
  rcases h with h | h
  · exact h₁ (pattern_test h)
  · exact h₂ (pattern_test h)

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
  intro h
  have hzA : 0 ∈ A := by decide
  have hzB : 0 ∈ B := by decide
  have hbound : ∀ s ∈ sums A B, rep A B s ≤ 2 := by decide
  have hd : (doubles A B).card = 2 := by decide
  rcases h A B hzA hzB hbound hd with hI | hII
  · exact no_I hI.1
  · exact no_II hII.1

end Counterexample

end Mathforge.PairsOfPolynomialsPQZXWithCoefficientsIC4
