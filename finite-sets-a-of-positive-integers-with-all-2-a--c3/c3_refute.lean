import Mathlib

open Finset

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def Positive (X : Finset ℕ) : Prop :=
  ∀ x ∈ X, 0 < x

def DistinctSubsetSums (X : Finset ℕ) : Prop :=
  ∀ U ∈ X.powerset, ∀ V ∈ X.powerset,
    U.sum id = V.sum id → U = V

def signedSums (X : Finset ℕ) : Finset ℤ :=
  (X.powerset ×ˢ X.powerset).image
    (fun p => (p.1.sum fun x => (x : ℤ)) - (p.2.sum fun x => (x : ℤ)))

def Replacement (n : ℕ) (A R T : Finset ℕ) : Prop :=
  R ⊆ A ∧
  Positive T ∧
  1 ≤ R.card ∧
  R.card ≤ n / 2 + 1 ∧
  T.card = R.card ∧
  Disjoint T (A \ R) ∧
  ((A \ R) ∪ T).sup id < A.sup id ∧
  DistinctSubsetSums T ∧
  signedSums T ∩ signedSums (A \ R) = {0}

def witnessA : Finset ℕ := {1, 2, 4, 8}
def witnessC : Finset ℕ := {3, 5, 6, 7}

-- FAITHFULNESS:
-- Positive natural numbers represent positive integers exactly.
-- The universal quantifiers range over n and every finite set A; n ≥ 2,
-- cardinality n, positivity, and distinct subset sums are explicit hypotheses.
-- The existential C has the same hypotheses and a strictly smaller maximum.
-- Subsets, including the empty subset, are enumerated by powerset.
-- signedSums is exactly D: differences of two subset sums give all coefficients
-- in {-1,0,1}, and conversely every such signed sum is such a difference.
-- R and T are existentially quantified finite sets. Replacement states every
-- required condition; natural division n / 2 is floor(n/2).
-- sup id is the maximum on nonempty sets. A and C are nonempty because n ≥ 2;
-- the replacement union is nonempty because T.card = R.card ≥ 1.
-- The finite bound used in the proof is derived from the required maximum
-- inequality, and is not an additional restriction in the claim.

theorem refutation :
    ¬ (∀ (n : ℕ) (A : Finset ℕ),
      2 ≤ n →
      A.card = n →
      Positive A →
      DistinctSubsetSums A →
      (∃ C : Finset ℕ,
        C.card = n ∧ Positive C ∧ DistinctSubsetSums C ∧
          C.sup id < A.sup id) →
      ∃ R T : Finset ℕ, Replacement n A R T) := by
  intro claim
  have haCard : witnessA.card = 4 := by decide
  have haPos : Positive witnessA := by
    unfold Positive
    decide
  have haSums : DistinctSubsetSums witnessA := by
    unfold DistinctSubsetSums
    decide
  have hc :
      ∃ C : Finset ℕ,
        C.card = 4 ∧ Positive C ∧ DistinctSubsetSums C ∧
          C.sup id < witnessA.sup id := by
    refine ⟨witnessC, ?_⟩
    unfold Positive DistinctSubsetSums
    decide
  obtain ⟨R, T, h⟩ :=
    claim 4 witnessA (by decide) haCard haPos haSums hc
  have finiteCheck :
      ∀ p ∈ witnessA.powerset ×ˢ (Finset.range 8).powerset,
        ¬ Replacement 4 witnessA p.1 p.2 := by
    unfold Replacement Positive DistinctSubsetSums
    decide
  have hR : R ∈ witnessA.powerset :=
    Finset.mem_powerset.mpr h.1
  have hmax :
      ((witnessA \ R) ∪ T).sup id < 8 := by
    have hh := h.2.2.2.2.2.2.1
    simpa [witnessA] using hh
  have hT : T ∈ (Finset.range 8).powerset := by
    apply Finset.mem_powerset.mpr
    intro x hx
    apply Finset.mem_range.mpr
    have hle : x ≤ ((witnessA \ R) ∪ T).sup id :=
      Finset.le_sup (f := id) (Finset.mem_union_right (witnessA \ R) hx)
    exact lt_of_le_of_lt hle hmax
  exact finiteCheck (R, T) (Finset.mem_product.mpr ⟨hR, hT⟩) h
set_option pp.fullNames true in
#print axioms refutation