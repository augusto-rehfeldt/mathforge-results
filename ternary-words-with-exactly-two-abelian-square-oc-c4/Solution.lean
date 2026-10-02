import Mathlib

namespace Mathforge.TernaryWordsWithExactlyTwoAbelianSquareOcC4

def letterCount (w : List (Fin 3)) (a k : ℕ) (c : Fin 3) : ℕ :=
  ((w.drop a).take k).count c

def AbelianSquare (w : List (Fin 3)) (n a k : ℕ) : Prop :=
  1 ≤ k ∧ a + 2 * k ≤ n ∧
    ∀ c : Fin 3, letterCount w a k c = letterCount w (a + k) k c

def witness : List (Fin 3) := [0, 1, 0, 1, 2, 1, 2]

-- FAITHFULNESS:
-- Natural numbers represent the nonnegative integer lengths and positions;
-- n ≥ 1 and h ≥ 1 impose the required positive integer bounds.
-- A list of Fin 3 is precisely a word over {0,1,2}, and w.length = n
-- imposes its length. AbelianSquare counts each letter in the two
-- half-open halves and requires the entire occurrence to lie in the word.
-- The inequalities below express i < j < i+2h ≤ n and j+2h ≤ n.
-- The biconditional says that the occurrences are exactly (i,h) and (j,h).
-- Quantifying a and k over Fin (n+1) loses no possible occurrence:
-- any valid occurrence satisfies a ≤ n and k ≤ n.
-- Thus all words, lengths, and candidate common-half-length pairs are
-- quantified, and the conclusion is exactly j = i+1.
theorem refutation :
    ¬ (∀ (n : ℕ), 1 ≤ n →
        ∀ (w : List (Fin 3)), w.length = n →
        ∀ (i j h : ℕ),
          1 ≤ h →
          i < j →
          j < i + 2 * h →
          i + 2 * h ≤ n →
          j + 2 * h ≤ n →
          (∀ (a k : Fin (n + 1)),
            AbelianSquare w n a.val k.val ↔
              ((a.val = i ∧ k.val = h) ∨
               (a.val = j ∧ k.val = h))) →
          j = i + 1) := by
  intro claim
  have exactOccurrences :
      ∀ (a k : Fin (7 + 1)),
        AbelianSquare witness 7 a.val k.val ↔
          ((a.val = 0 ∧ k.val = 2) ∨
           (a.val = 3 ∧ k.val = 2)) := by
    unfold AbelianSquare letterCount witness
    decide
  have impossible : (3 : ℕ) = 0 + 1 :=
    claim 7 (by decide) witness (by rfl) 0 3 2
      (by decide) (by decide) (by decide)
      (by decide) (by decide) exactOccurrences
  norm_num at impossible

end Mathforge.TernaryWordsWithExactlyTwoAbelianSquareOcC4
