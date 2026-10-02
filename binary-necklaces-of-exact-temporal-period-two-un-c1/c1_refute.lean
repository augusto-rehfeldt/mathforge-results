import Mathlib

open scoped BigOperators

abbrev Word (n : ℕ) := Fin n → Bool

def bit {n : ℕ} (x : Word n) (i : ℕ) : Bool :=
  if h : n = 0 then false else x ⟨i % n, Nat.mod_lt _ (Nat.pos_of_ne_zero h)⟩

def step {n : ℕ} (x : Word n) : Word n :=
  fun i => xor (x i)
    (bit x (i.val + n - 1) && bit x (i.val + 1))

def periodTwo {n : ℕ} (x : Word n) : Prop :=
  step (step x) = x ∧ step x ≠ x

instance {n : ℕ} (x : Word n) : Decidable (periodTwo x) := by
  unfold periodTwo
  infer_instance

def consecutiveZeros {n : ℕ} (x : Word n) : Prop :=
  ∃ i : Fin n, x i = false ∧ bit x (i.val + 1) = false

instance {n : ℕ} (x : Word n) : Decidable (consecutiveZeros x) := by
  unfold consecutiveZeros
  infer_instance

-- A block starts at the first one following a zero run of length ≥ 2.
def blockStart {n : ℕ} (x : Word n) (i : Fin n) : Bool :=
  x i && !(bit x (i.val + n - 1)) && !(bit x (i.val + n - 2))

-- Stop just before the first zero of the next removed zero run.
def blockAt {n : ℕ} (x : Word n) (i : Fin n) : List Bool :=
  ((List.range n).takeWhile fun j =>
    !(!(bit x (i.val + j)) && !(bit x (i.val + j + 1)))).map
      (fun j => bit x (i.val + j))

def allowedBlocks : List (List Bool) :=
  [[true], [true, true], [true, true, true], [true, false, true]]

def activeBlocks : List (List Bool) :=
  [[true, true, true], [true, false, true]]

def blockCriterion {n : ℕ} (x : Word n) : Prop :=
  (∀ i : Fin n, blockStart x i = true → blockAt x i ∈ allowedBlocks) ∧
  (∃ i : Fin n, blockStart x i = true ∧ blockAt x i ∈ activeBlocks)

instance {n : ℕ} (x : Word n) : Decidable (blockCriterion x) := by
  unfold blockCriterion
  infer_instance

def weight {n : ℕ} (x : Word n) : ℕ :=
  ((Finset.univ : Finset (Fin n)).filter fun i => x i = true).card

def changed {n : ℕ} (x : Word n) : ℕ :=
  ((Finset.univ : Finset (Fin n)).filter fun i => step x i ≠ x i).card

def longRuns {n : ℕ} (x : Word n) : ℕ :=
  if ∀ i, x i = false then 1
  else ((Finset.univ : Finset (Fin n)).filter fun i => blockStart x i = true).card

def weightPair {n : ℕ} (x : Word n) (a b : ℕ) : Prop :=
  (weight x = a ∧ weight (step x) = b) ∨
  (weight x = b ∧ weight (step x) = a)

instance {n : ℕ} (x : Word n) (a b : ℕ) : Decidable (weightPair x a b) := by
  unfold weightPair
  infer_instance

-- Counting representatives is exactly the necklace sum Σ_N n / s(N):
-- each rotation orbit contributes its number of distinct representatives.
def M (n k a b c : ℕ) : ℚ :=
  (((Finset.univ : Finset (Word n)).filter fun x =>
    periodTwo x ∧ longRuns x = k ∧ weightPair x a b ∧ changed x = c).card : ℚ)

def tileLength (r : Fin 4) : ℕ :=
  if r.val = 0 then 1 else if r.val = 1 then 2 else 3

def tileU (r : Fin 4) : ℕ :=
  if r.val = 0 then 1 else if r.val = 2 then 3 else 2

def tileV (r : Fin 4) : ℕ :=
  if r.val = 0 then 1 else if r.val = 3 then 3 else 2

def tileQ (r : Fin 4) : ℕ :=
  if r.val < 2 then 0 else 1

-- Coefficient extraction in P^k by its ordered choices of monomials.
-- z records the length of the zero run contributed by t²/(1-t).
def coefficient (n k a b c : ℕ) : ℚ :=
  (((Finset.univ :
      Finset ((Fin k → Fin (n + 1)) × (Fin k → Fin 4))).filter
    fun p =>
      (∀ i, 2 ≤ (p.1 i).val) ∧
      (∑ i, ((p.1 i).val + tileLength (p.2 i))) = n ∧
      (∑ i, tileU (p.2 i)) = a ∧
      (∑ i, tileV (p.2 i)) = b ∧
      (∑ i, tileQ (p.2 i)) = c).card : ℚ)

def witness : Word 7 :=
  ![true, true, true, false, true, false, false]

-- FAITHFULNESS:
-- n : ℕ with n ≥ 3 represents exactly the integers n ≥ 3.
-- Word n ranges over every indexed cyclic binary word; bit implements
-- modular indexing, and xor/and implement addition/multiplication in F₂.
-- The first universal assertion is the stated iff, restricted to words
-- containing consecutive zeros. blockAt reads the blocks between maximal
-- long zero runs; blockCriterion requires all four allowed types and at
-- least one of the two active types. The all-zero word has no such block.
-- In the second assertion, natural a,b and positive k,c represent exactly
-- the specified integer ranges. longRuns includes the all-zero convention.
-- M counts labeled representatives, equivalently the stipulated necklace
-- sum n/s(N), since every orbit has n/s(N) representatives.
-- coefficient expands P^k: the four tile types have precisely its four
-- monomials, and every zero length ≥2 occurs once. Lengths exceeding n
-- cannot contribute to t^n, so the finite bound loses no coefficients.
-- The equal/unequal weight cases implement unordered pairs with repetition.
theorem refutation :
    ¬ (
      (∀ n : ℕ, 3 ≤ n →
        ∀ x : Word n, consecutiveZeros x →
          (periodTwo x ↔ blockCriterion x)) ∧
      (∀ n : ℕ, 3 ≤ n →
        ∀ k a b c : ℕ, 1 ≤ k → 1 ≤ c →
          M n k a b c =
            (n : ℚ) / (k : ℚ) *
              (if a = b then coefficient n k a b c
               else coefficient n k a b c + coefficient n k b a c))
    ) := by
  intro h
  have hz : consecutiveZeros witness := by decide
  have hp : periodTwo witness := by decide
  have hb : ¬ blockCriterion witness := by decide
  exact hb ((h.1 7 (by norm_num) witness hz).mp hp)
set_option pp.fullNames true in
#print axioms refutation