import Mathlib

namespace Mathforge.SidonB2SubsetsOf1NAndOfCyclicGroupsZC4

def IsSidon (A : Finset ℕ) : Prop :=
  (((A.product A).filter (fun p : ℕ × ℕ => p.1 ≤ p.2)).image (fun p : ℕ × ℕ => p.1 + p.2)).card =
    ((A.product A).filter (fun p : ℕ × ℕ => p.1 ≤ p.2)).card

instance : DecidablePred IsSidon := fun A => by unfold IsSidon; infer_instance

def N (n k s m : ℕ) : ℕ :=
  (((Finset.Icc 1 n).powersetCard k).filter
    (fun A : Finset ℕ => A.sum id = s ∧ A.sup id = m ∧ IsSidon A)).card

theorem refutation : ¬ (∀ n k s m : ℕ, 1 ≤ n → 3 ≤ k → 1 ≤ m → 1 ≤ s → m ≤ n → 2 * s = k * (m + 1) → Even (N n k s m)) := by
  intro h
  have hc := h 7 3 12 7 (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have hN : N 7 3 12 7 = 1 := by decide
  have hodd : ¬ Even (1 : ℕ) := by decide
  rw [hN] at hc
  exact hodd hc

end Mathforge.SidonB2SubsetsOf1NAndOfCyclicGroupsZC4
