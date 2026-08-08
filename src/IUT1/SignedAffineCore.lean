import IUT1.SymmetryCore
import Mathlib.Data.Bool.Basic
import Mathlib.Data.Fintype.Card

/-!
# IUT1-I1-SYM-001: coordinatized signed-affine core

This copy-on-write module implements only T06--T08.  Its carrier is a visible
translation/sign pair, and its group law is proved from the displayed action.
It makes no geometric identification and contains no geometric application objects.
-/

namespace IUT1

/-- A signed-affine coordinate pair.  `false` denotes `+1`; `true` denotes `-1`. -/
structure SignedAffine (l : ℕ) where
  translation : Fl l
  negative : Bool
deriving DecidableEq

/-- The action of the sign bit on the additive coordinate. -/
def signAct {l : ℕ} (s : Bool) (x : Fl l) : Fl l :=
  match s with
  | false => x
  | true => -x

/-- The contracted semidirect multiplication on visible coordinate pairs. -/
def signedAffineMul {l : ℕ} (g h : SignedAffine l) : SignedAffine l where
  translation := g.translation + signAct g.negative h.translation
  negative := Bool.xor g.negative h.negative

/-- The identity signed-affine pair. -/
def signedAffineOne {l : ℕ} : SignedAffine l where
  translation := 0
  negative := false

/-- The inverse computed from the same sign action as multiplication. -/
def signedAffineInv {l : ℕ} (g : SignedAffine l) : SignedAffine l where
  translation := -signAct g.negative g.translation
  negative := g.negative

instance instMulSignedAffine {l : ℕ} : Mul (SignedAffine l) :=
  ⟨signedAffineMul⟩

instance instOneSignedAffine {l : ℕ} : One (SignedAffine l) :=
  ⟨signedAffineOne⟩

instance instInvSignedAffine {l : ℕ} : Inv (SignedAffine l) :=
  ⟨signedAffineInv⟩

@[simp] private theorem signedAffine_mul_translation {l : ℕ}
    (g h : SignedAffine l) :
    (g * h).translation = g.translation + signAct g.negative h.translation :=
  rfl

@[simp] private theorem signedAffine_mul_negative {l : ℕ}
    (g h : SignedAffine l) :
    (g * h).negative = Bool.xor g.negative h.negative :=
  rfl

@[simp] private theorem signedAffine_one_translation {l : ℕ} :
    (1 : SignedAffine l).translation = 0 :=
  rfl

@[simp] private theorem signedAffine_one_negative {l : ℕ} :
    (1 : SignedAffine l).negative = false :=
  rfl

@[simp] private theorem signedAffine_inv_translation {l : ℕ}
    (g : SignedAffine l) :
    g⁻¹.translation = -signAct g.negative g.translation :=
  rfl

@[simp] private theorem signedAffine_inv_negative {l : ℕ}
    (g : SignedAffine l) : g⁻¹.negative = g.negative :=
  rfl

private theorem signedAffine_ext {l : ℕ} {g h : SignedAffine l}
    (htranslation : g.translation = h.translation)
    (hnegative : g.negative = h.negative) : g = h := by
  cases g
  cases h
  simp_all

/-- The group laws derived from the displayed pair multiplication. -/
instance instGroupSignedAffine {l : ℕ} : Group (SignedAffine l) where
  mul_assoc g h k := by
    rcases g with ⟨a, s⟩
    rcases h with ⟨b, t⟩
    rcases k with ⟨c, u⟩
    cases s <;> cases t <;> cases u <;>
      apply signedAffine_ext <;>
      simp [signAct, add_assoc, add_comm, add_left_comm]
  one_mul g := by
    rcases g with ⟨a, s⟩
    cases s <;>
      apply signedAffine_ext <;>
      simp [signAct]
  mul_one g := by
    rcases g with ⟨a, s⟩
    cases s <;>
      apply signedAffine_ext <;>
      simp [signAct]
  inv_mul_cancel g := by
    rcases g with ⟨a, s⟩
    cases s <;>
      apply signedAffine_ext <;>
      simp [signAct]

/-- The affine action represented by a signed-affine coordinate pair. -/
def SignedAffine.act {l : ℕ} (g : SignedAffine l) (z : Fl l) : Fl l :=
  signAct g.negative z + g.translation

private def signedAffineEquivProd (l : ℕ) : SignedAffine l ≃ Fl l × Bool where
  toFun g := (g.translation, g.negative)
  invFun p := ⟨p.1, p.2⟩
  left_inv g := by cases g; rfl
  right_inv p := by cases p; rfl

instance instFintypeSignedAffine (l : ℕ) [NeZero l] : Fintype (SignedAffine l) :=
  Fintype.ofEquiv (Fl l × Bool) (signedAffineEquivProd l).symm

/-!
`source_id=SRC-OFFICIAL-7360E3ED27C235B5`.
Section I1, printed p. 3 supplies the sign semidirect-product role;
Definition 6.1(i), printed p. 155 supplies the transformations `z ↦ ±z + λ`.
Epistemic status: `DERIVED_COORDINATIZED_MODEL`.
Discriminant: the theorem exposes both coordinates of the contracted law; the
closed `l=5` witness evaluates the translation to `4`, not the direct-product
value `3`.
-/
theorem T06_C06_mul_formula {l : ℕ} (g h : SignedAffine l) :
    (g * h).translation = g.translation + signAct g.negative h.translation ∧
      (g * h).negative = Bool.xor g.negative h.negative :=
  ⟨rfl, rfl⟩

/-- Closed T06 regression witness for the semidirect, rather than direct, product. -/
theorem T06_example_l5_semidirect :
    let g : SignedAffine 5 := ⟨1, true⟩
    let h : SignedAffine 5 := ⟨2, false⟩
    g * h = ⟨4, true⟩ ∧ (g * h).translation ≠ 3 := by
  decide

/-!
`source_id=SRC-OFFICIAL-7360E3ED27C235B5`.
Definition 6.1(i), printed p. 155 supplies the action convention
`z ↦ ±z + λ`. Epistemic status: `DERIVED_COORDINATIZED_MODEL`.
Discriminant: `g*h` acts by first applying `h` and then `g`; at `l=5` the two
sides both evaluate to `1`, while the reversed convention does not.
-/
theorem T07_C06_act_mul {l : ℕ} (g h : SignedAffine l) (z : Fl l) :
    (g * h).act z = g.act (h.act z) := by
  rcases g with ⟨a, s⟩
  rcases h with ⟨b, t⟩
  change signAct (Bool.xor s t) z + (a + signAct s b) =
    signAct s (signAct t z + b) + a
  cases s <;> cases t <;>
    simp [signAct, add_assoc, add_comm, add_left_comm]

/-- Closed T07 regression witness for the contracted composition order. -/
theorem T07_example_l5_action_order :
    let g : SignedAffine 5 := ⟨1, true⟩
    let h : SignedAffine 5 := ⟨2, false⟩
    let z : Fl 5 := 3
    (g * h).act z = 1 ∧ g.act (h.act z) = 1 := by
  decide

section Prime

variable (l : ℕ) [Fact l.Prime]

local instance : NeZero l :=
  ⟨(Fact.out : Nat.Prime l).pos.ne'⟩

/-!
`source_id=SRC-OFFICIAL-7360E3ED27C235B5`.
Section I1, printed p. 3 and Definition 6.1(i), printed p. 155 supply the finite
coordinate/sign roles. Epistemic status: `DERIVED`.
Discriminant: the cardinality is computed from the visible carrier and
`ZMod.card`; it is neither stored in `SignedAffine` nor accepted as a hypothesis.
-/
theorem T08_C06_card_signedAffine : Fintype.card (SignedAffine l) = 2 * l := by
  calc
    Fintype.card (SignedAffine l) = Fintype.card (Fl l × Bool) :=
      Fintype.card_congr (signedAffineEquivProd l)
    _ = Fintype.card (Fl l) * Fintype.card Bool := Fintype.card_prod _ _
    _ = l * 2 := by simp [T01_C01_card_Fl l]
    _ = 2 * l := Nat.mul_comm l 2

end Prime

/-- Closed T08 cardinality witness. -/
theorem T08_example_l5_card : Fintype.card (SignedAffine 5) = 10 := by
  letI : Fact (Nat.Prime 5) := ⟨by decide⟩
  simpa using T08_C06_card_signedAffine 5

end IUT1
