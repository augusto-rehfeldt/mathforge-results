import Mathlib

namespace Mathforge.SetPartitionsOfNInWhichAllGapsBetweenSuC1

open Finset

set_option maxHeartbeats 0
set_option maxRecDepth 100000

def ground (n : ℕ) : Finset ℕ := Icc 1 n

def successivePairs (B : Finset ℕ) : Finset (ℕ × ℕ) :=
  (B.product B).filter fun p =>
    p.1 < p.2 ∧ ¬ ∃ z ∈ B, p.1 < z ∧ z < p.2

def allPairs (P : Finset (Finset ℕ)) : Finset (ℕ × ℕ) :=
  P.biUnion successivePairs

def gap (p : ℕ × ℕ) : ℕ := p.2 - p.1

def validPartition (n : ℕ) (P : Finset (Finset ℕ)) : Prop :=
  (∀ B ∈ P, B.Nonempty) ∧
  (∀ B ∈ P, ∀ C ∈ P, B ≠ C → Disjoint B C) ∧
  P.biUnion id = ground n ∧
  (allPairs P).card = ((allPairs P).image gap).card

instance (n : ℕ) (P : Finset (Finset ℕ)) :
    Decidable (validPartition n P) := by
  unfold validPartition
  infer_instance

def A (n k s t m : ℕ) : ℕ :=
  (((ground n).powerset.powerset).filter fun P =>
    validPartition n P ∧
    P.card = k ∧
    (P.filter fun B => B.card = 1).card = s ∧
    (allPairs P).sum gap = t ∧
    P.sum (fun B => B.sup id) = m).card

def subsetCount (n : ℤ) (k t : ℕ) : ℕ :=
  (((Icc 1 (n.toNat / 2)).powerset).filter fun I =>
    (I.card : ℤ) = n - (k : ℤ) ∧
    I.sum (fun i => n + 1 - 2 * (i : ℤ)) = (t : ℤ)).card

-- FAITHFULNESS:
-- n ranges over integers with n ≥ 1; k,s,t,m range over nonnegative
-- integers, represented by ℕ. ground n.toNat is exactly [n].
-- The double powerset enumerates collections of blocks. validPartition
-- requires nonempty, pairwise disjoint blocks covering [n].
-- successivePairs records precisely adjacent elements in each sorted block.
-- Equality of the cardinalities of allPairs and its gap image means that
-- every successive-element gap is globally distinct. Disjointness ensures
-- that pairs from different blocks cannot coincide.
-- A filters by block count, singleton count, total gap sum, and sum of maxima.
-- subsetCount enumerates subsets of {1,...,floor(n/2)}, requiring cardinality
-- n-k in ℤ (so negative cardinalities have no solutions), and the stated sum.
-- The two exceptional conditions are interpreted in ℤ, without truncated
-- subtraction. When either fails, the claimed parity is zero.
theorem refutation :
    ¬ (∀ n : ℤ, n ≥ 1 →
       ∀ k s t m : ℕ,
         A n.toNat k s t m % 2 =
           if (s : ℤ) = 2 * (k : ℤ) - n ∧
              2 * (m : ℤ) = (k : ℤ) * (n + 1) + (t : ℤ)
           then subsetCount n k t % 2
           else 0) := by
  sorry

end Mathforge.SetPartitionsOfNInWhichAllGapsBetweenSuC1
