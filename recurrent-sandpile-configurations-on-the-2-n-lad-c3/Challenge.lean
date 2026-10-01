import Mathlib

namespace Mathforge.RecurrentSandpileConfigurationsOnThe2NLadC3

open Finset Polynomial

namespace Ladder

abbrev Vertex (n : ℕ) := Fin (2 * n)

abbrev Config (n : ℕ) := Vertex n → Fin 3

-- Vertex 2*i is u_(i+1), and vertex 2*i+1 is v_(i+1).
def adjacent {n : ℕ} (a b : Vertex n) : Bool :=
  decide ((a.val / 2 = b.val / 2 ∧ a.val ≠ b.val) ∨
    a.val + 2 = b.val ∨ b.val + 2 = a.val)

def burnStep {n : ℕ} (η : Config n)
    (burned : Finset (Vertex n)) : Finset (Vertex n) :=
  burned ∪ Finset.univ.filter (fun v =>
    (Finset.univ.filter (fun w =>
      adjacent v w = true ∧ w ∉ burned)).card ≤ (η v).val)

def burn {n : ℕ} (η : Config n) : ℕ → Finset (Vertex n)
  | 0 => ∅
  | k + 1 => burnStep η (burn η k)

def recurrent {n : ℕ} (η : Config n) : Prop :=
  burn η (2 * n) = Finset.univ

instance {n : ℕ} (η : Config n) : Decidable (recurrent η) :=
  inferInstanceAs (Decidable (burn η (2 * n) = Finset.univ))

def mass {n : ℕ} (η : Config n) : ℕ :=
  ∑ v, (η v).val

def topple {n : ℕ} (c : Vertex n → ℕ) (v : Vertex n) :
    Vertex n → ℕ :=
  fun w =>
    if w = v then c w - 3
    else c w + if adjacent v w then 1 else 0

def stabilize {n : ℕ} :
    ℕ → (Vertex n → ℕ) → Finset (Vertex n) → Finset (Vertex n)
  | 0, _, seen => seen
  | k + 1, c, seen =>
      match (List.finRange (2 * n)).find? (fun v => decide (3 ≤ c v)) with
      | none => seen
      | some v => stabilize k (topple c v) (insert v seen)

def avalanche {n : ℕ} (η : Config n) : ℕ :=
  (stabilize ((4 * n + 1) * n * n)
    (fun v => (η v).val + if v.val = 0 then 1 else 0) ∅).card

noncomputable def lhs (n : ℕ) : Polynomial ℤ :=
  ∑ η ∈ (Finset.univ : Finset (Config n)).filter
      (fun η => recurrent η ∧ mass η = 4 * n - 2),
    (X : Polynomial ℤ) ^ avalanche η

noncomputable def rhs (n : ℕ) : Polynomial ℤ :=
  C (2 * (n : ℤ)) + X +
    (∑ j ∈ Finset.Icc 1 (n - 1), (X : Polynomial ℤ) ^ (2 * j)) +
    C 3 * X ^ (2 * n - 1) +
    C (2 * (n : ℤ) ^ 2 - 2 * (n : ℤ) - 3) * X ^ (2 * n)

-- FAITHFULNESS:
-- The claim quantifies over every integer n with n ≥ 2; n.toNat indexes
-- its 2n nonsink vertices. Config assigns precisely heights 0, 1, or 2.
-- adjacent gives exactly the rung and rail edges; missing degree-three
-- edges lead to the sink and therefore do not appear in topple.
-- recurrent implements the burning test. Each nonterminal burning round
-- burns at least one new vertex, so 2n rounds suffice.
-- mass is |η|, and the filtered sum includes exactly recurrent configurations
-- of mass 4n-2. avalanche records distinct vertices in legal stabilization
-- after adding one chip at u_1.
-- Its fuel is sufficient: give both vertices in column i weight
-- i*(n+1-i). Every legal toppling decreases weighted chip mass by 2.
-- Initial weighted mass is at most (4n+1)*n², so the fuel exceeds the
-- number of possible legal topplings. Stabilization on this sink-connected
-- graph is abelian, so choosing the first unstable vertex does not alter A.
-- The natural interval 1,...,n-1 in rhs is exactly the indicated integer
-- summation interval, and coefficients lie in ℤ.

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem refutation :
    ¬ (∀ n : ℤ, 2 ≤ n → lhs n.toNat = rhs n.toNat) := by
  sorry

end Ladder

end Mathforge.RecurrentSandpileConfigurationsOnThe2NLadC3
