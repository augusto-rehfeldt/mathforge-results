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
  sorry

end Mathforge.PairsOfPolynomialsAXBXOfDegreeN1WithC1
