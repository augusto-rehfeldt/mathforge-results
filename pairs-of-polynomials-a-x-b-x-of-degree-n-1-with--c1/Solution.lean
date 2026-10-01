import Mathlib

namespace Mathforge.PairsOfPolynomialsAXBXOfDegreeN1WithC1

open Finset

-- The coefficient of x^k in A(x)A(x⁻¹).
def autocorr (n : ℕ) (a : ℕ → ℤ) (k : ℤ) : ℤ :=
  ∑ i ∈ range n, ∑ j ∈ range n,
    if (i : ℤ) - (j : ℤ) = k then a i * a j else 0

def hamming (n : ℕ) (a b : ℕ → ℤ) : ℕ :=
  ((range n).filter fun i => a i ≠ b i).card

def witnessA (i : ℕ) : ℤ := if i = 1 then -1 else 1

def witnessB (i : ℕ) : ℤ := if i = 1 ∨ i = 2 then -1 else 1

-- FAITHFULNESS:
-- n,d,e are natural numbers: under n ≥ 3 and 1 ≤ d < e < n this
-- is equivalent to quantifying over the integers in the informal claim.
-- c is an arbitrary nonzero integer. The functions a,b specify all
-- coefficients; only their values at indices below n are constrained or used.
-- Laurent-polynomial equality is expressed as equality at every integer
-- exponent k. The double sum is exactly the coefficient of A(x)A(x⁻¹).
-- hamming counts precisely the differing coefficients below n.
-- Even expresses ordinary evenness, and 4 ∣ c is integer divisibility.
-- The equations 2h=n and 2h=n±4 express h=n/2 and h=n/2±2
-- without any truncated division.
theorem refutation :
    ¬ (∀ (n d e : ℕ) (c : ℤ) (a b : ℕ → ℤ),
      3 ≤ n →
      1 ≤ d → d < e → e < n →
      c ≠ 0 →
      (∀ i < n, a i = -1 ∨ a i = 1) →
      (∀ i < n, b i = -1 ∨ b i = 1) →
      (∀ k : ℤ,
        autocorr n a k + autocorr n b k =
          (if k = 0 then 2 * (n : ℤ) else 0) +
          c * ((if k = (d : ℤ) then 1 else 0) +
               (if k = -(d : ℤ) then 1 else 0) -
               (if k = (e : ℤ) then 1 else 0) -
               (if k = -(e : ℤ) then 1 else 0))) →
      Even n ∧ Even c ∧
        ((4 ∣ c → 2 * (hamming n a b : ℤ) = (n : ℤ)) ∧
         (¬ (4 ∣ c) →
           d + e = n ∧
             (2 * (hamming n a b : ℤ) = (n : ℤ) - 4 ∨
              2 * (hamming n a b : ℤ) = (n : ℤ) ∨
              2 * (hamming n a b : ℤ) = (n : ℤ) + 4)))) := by
  intro claim
  have ha : ∀ i < 5, witnessA i = -1 ∨ witnessA i = 1 := by
    intro i hi
    by_cases h : i = 1 <;> simp [witnessA, h]
  have hb : ∀ i < 5, witnessB i = -1 ∨ witnessB i = 1 := by
    intro i hi
    by_cases h : i = 1 ∨ i = 2 <;> simp [witnessB, h]
  have hid : ∀ k : ℤ,
      autocorr 5 witnessA k + autocorr 5 witnessB k =
        (if k = 0 then 2 * (5 : ℤ) else 0) +
        (-2 : ℤ) * ((if k = (2 : ℤ) then 1 else 0) +
                    (if k = -(2 : ℤ) then 1 else 0) -
                    (if k = (4 : ℤ) then 1 else 0) -
                    (if k = -(4 : ℤ) then 1 else 0)) := by
    intro k
    by_cases hk : -4 ≤ k ∧ k ≤ 4
    · rcases hk with ⟨hlo, hhi⟩
      interval_cases k <;>
        norm_num [autocorr, witnessA, witnessB, sum_range_succ]
    · have h₁ : (-4 : ℤ) ≠ k := by omega
      have h₂ : (-3 : ℤ) ≠ k := by omega
      have h₃ : (-2 : ℤ) ≠ k := by omega
      have h₄ : (-1 : ℤ) ≠ k := by omega
      have h₅ : (0 : ℤ) ≠ k := by omega
      have h₆ : (1 : ℤ) ≠ k := by omega
      have h₇ : (2 : ℤ) ≠ k := by omega
      have h₈ : (3 : ℤ) ≠ k := by omega
      have h₉ : (4 : ℤ) ≠ k := by omega
      norm_num [autocorr, witnessA, witnessB, sum_range_succ,
        h₁, h₂, h₃, h₄, h₅, h₆, h₇, h₈, h₉,
        Ne.symm h₁, Ne.symm h₃, Ne.symm h₅,
        Ne.symm h₇, Ne.symm h₉]
  have result := claim 5 2 4 (-2) witnessA witnessB
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) ha hb hid
  have not_even : ¬ Even (5 : ℕ) := by decide
  exact not_even result.1

end Mathforge.PairsOfPolynomialsAXBXOfDegreeN1WithC1
