import IUT1.SignedAffineCore
import IUT1.SignOrbitBridge
import Mathlib.GroupTheory.IndexNormal
import Mathlib.GroupTheory.SpecificGroups.Dihedral

/-!
# IUT1-I1-SYM-001: translations and the dihedral comparison

This copy-on-write module implements only T09--T11.  The signed-affine group
remains the coordinate-pair structure constructed in `SignedAffineCore`; the
dihedral group appears only as the target of an explicit comparison.
-/

namespace IUT1

/-!
`source_id=SRC-OFFICIAL-7360E3ED27C235B5`.
Section I1, printed p. 3 supplies the sign semidirect-product role;
Definition 6.1(i), printed p. 155 supplies the transformations `z ↦ ±z + λ`.
Epistemic status: `DERIVED_ALGEBRAIC_MODEL`.
Discriminant: translations are selected by the visible equation
`negative = false`; the reflection `(0,true)` lies outside and toggles that
equation under right multiplication.
-/

/-- The subgroup consisting of coordinate transformations with positive sign. -/
def translationSubgroup (l : ℕ) : Subgroup (SignedAffine l) where
  carrier := {g | g.negative = false}
  one_mem' := rfl
  mul_mem' := by
    intro g h hg hh
    change g.negative = false at hg
    change h.negative = false at hh
    change Bool.xor g.negative h.negative = false
    simp [hg, hh]
  inv_mem' := by
    intro g hg
    exact hg

/-- Membership is exactly the vanishing of the visible sign bit. -/
theorem T09_C06_translation_mem_iff {l : ℕ} (g : SignedAffine l) :
    g ∈ translationSubgroup l ↔ g.negative = false :=
  Iff.rfl

/-- The translation subgroup has index two, proved by the sign bit. -/
theorem T09_C06_translation_index (l : ℕ) :
    (translationSubgroup l).index = 2 := by
  apply (Subgroup.index_eq_two_iff).2
  refine ⟨(⟨0, true⟩ : SignedAffine l), ?_⟩
  rintro ⟨a, s⟩
  cases s <;> simp [translationSubgroup]

/-- Normality is deduced from the proved index-two theorem. -/
instance instNormalTranslationSubgroup (l : ℕ) :
    (translationSubgroup l).Normal :=
  Subgroup.normal_of_index_eq_two (T09_C06_translation_index l)

/-- Closed T09 witness: the reflection is outside and right multiplication toggles membership. -/
theorem T09_example_l5_reflection_toggle :
    let q : SignedAffine 5 := ⟨0, true⟩
    q ∉ translationSubgroup 5 ∧
      ∀ g : SignedAffine 5,
        (g * q ∈ translationSubgroup 5) ↔ g ∉ translationSubgroup 5 := by
  dsimp
  constructor
  · simp [translationSubgroup]
  · rintro ⟨a, s⟩
    cases s <;> simp [translationSubgroup]

/-!
`source_id=SRC-OFFICIAL-7360E3ED27C235B5`.
Section I1, printed p. 3 and Definition 6.1(i), printed p. 155 supply the
coordinate role. Epistemic status: `DERIVED_ALGEBRAIC_MODEL`;
mathematical priority status: `PRIOR_ART_ESTABLISHED`.
Discriminant: the negative pair maps to `sr (-a)`, not `sr a`; the forward and
reverse maps are displayed constructor by constructor, and multiplication is
checked in all four sign branches.
-/

/-- Forward comparison, written separately so both sign branches remain visible. -/
def signedAffineToDihedral {l : ℕ} : SignedAffine l → DihedralGroup l
  | ⟨a, false⟩ => DihedralGroup.r a
  | ⟨a, true⟩ => DihedralGroup.sr (-a)

/-- Reverse comparison, displayed independently on both dihedral constructors. -/
def dihedralToSignedAffine {l : ℕ} : DihedralGroup l → SignedAffine l
  | DihedralGroup.r a => ⟨a, false⟩
  | DihedralGroup.sr c => ⟨-c, true⟩

@[simp] private theorem signedAffine_mul_def {l : ℕ} (g h : SignedAffine l) :
    g * h = signedAffineMul g h :=
  rfl

/-- Explicit multiplicative equivalence for the two coordinate presentations. -/
def signedAffineDihedralEquiv (l : ℕ) : SignedAffine l ≃* DihedralGroup l where
  toFun := signedAffineToDihedral
  invFun := dihedralToSignedAffine
  left_inv := by
    rintro ⟨a, s⟩
    cases s <;> simp [signedAffineToDihedral, dihedralToSignedAffine]
  right_inv := by
    rintro (a | a) <;> simp [signedAffineToDihedral, dihedralToSignedAffine]
  map_mul' := by
    rintro ⟨a, s⟩ ⟨b, t⟩
    cases s <;> cases t <;>
      simp [signedAffineToDihedral, signedAffineMul, signAct, sub_eq_add_neg,
        add_comm]

/-- Standard affine action read directly from the two Mathlib constructors. -/
def dihedralAct {l : ℕ} : DihedralGroup l → Fl l → Fl l
  | DihedralGroup.r a, z => z + a
  | DihedralGroup.sr a, z => -z - a

/-- The independently displayed dihedral action agrees with the signed-affine action. -/
theorem T10_C06_dihedral_action_compatible {l : ℕ}
    (g : SignedAffine l) (z : Fl l) :
    dihedralAct (signedAffineDihedralEquiv l g) z = g.act z := by
  rcases g with ⟨a, s⟩
  cases s <;>
    simp [signedAffineDihedralEquiv, signedAffineToDihedral, dihedralAct,
      SignedAffine.act, signAct]

/-- Closed T10 witness: the correct image gives `4`, while the rival `sr 1` gives `2`. -/
theorem T10_example_l5_action_discriminant :
    let g : SignedAffine 5 := ⟨1, true⟩
    let z : Fl 5 := 2
    dihedralAct (signedAffineDihedralEquiv 5 g) z = 4 ∧
      g.act z = 4 ∧ dihedralAct (DihedralGroup.sr 1) z = 2 := by
  decide

/-!
T11 introduces no new source claim. Epistemic status:
`EXECUTABLE_REGRESSION_SUITE`. The inherited coordinate context is
`source_id=SRC-OFFICIAL-7360E3ED27C235B5`, Section I1, printed p. 3 and
Definition 6.1(i), printed p. 155.
Discriminant: the multiplicative quotient, additive sign-orbit quotient, and
signed-affine group remain separately typed while reproducing `(2,3,10)` and
`(3,4,14)`.
-/

/-- Closed `l=5` cardinality vector for the three distinct coordinate objects. -/
theorem T11_l5_cardinality_vector :
    Nat.card (MultiplicativeLabelGroup 5) = 2 ∧
      Nat.card (AdditiveSignOrbit 5) = 3 ∧
      Fintype.card (SignedAffine 5) = 10 := by
  letI : Fact (Nat.Prime 5) := ⟨by decide⟩
  refine ⟨?_, ?_, ?_⟩
  · simpa [lStar] using T04_C02_C04_card_MultiplicativeLabelGroup 5 (by decide)
  · simpa [lPlusMinus] using
      (T05d_C01_C05_card_sign_orbits.{0} 5 (by decide)).1
  · exact T08_C06_card_signedAffine 5

/-- Closed `l=7` cardinality vector for the three distinct coordinate objects. -/
theorem T11_l7_cardinality_vector :
    Nat.card (MultiplicativeLabelGroup 7) = 3 ∧
      Nat.card (AdditiveSignOrbit 7) = 4 ∧
      Fintype.card (SignedAffine 7) = 14 := by
  letI : Fact (Nat.Prime 7) := ⟨by decide⟩
  refine ⟨?_, ?_, ?_⟩
  · simpa [lStar] using T04_C02_C04_card_MultiplicativeLabelGroup 7 (by decide)
  · simpa [lPlusMinus] using
      (T05d_C01_C05_card_sign_orbits.{0} 7 (by decide)).1
  · exact T08_C06_card_signedAffine 7

end IUT1
