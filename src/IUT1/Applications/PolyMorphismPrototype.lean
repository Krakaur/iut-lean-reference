import IUT1.SignedAffineDihedral

/-!
# Algebraic poly-morphism and quotient-fiber prototype

This module is deliberately restricted to sets of functions, group homomorphisms,
fibers, and left translations.  It constructs no geometric carrier, capsule,
Hodge theater, source automorphism subquotient, arithmetic/geometric provenance,
or IUT poly-action.

`source_id=SRC-OFFICIAL-7360E3ED27C235B5`.
Source localizers: section 0, printed pp. 33--34 (collections of morphisms and
pairwise composition); section I1, printed p. 4 (automorphism-subquotient role);
section 4, printed pp. 98--100 (labels/capsules/poly-morphism context); section 6,
printed pp. 155--163 (signed labels, poly-automorphisms, and equivariance context).

Epistemic status:
`ALGEBRAIC_PROTOTYPE_OF_SOURCE_POLYMORPHISM_AND_SUBQUOTIENT_PATTERN`.
Geometric status: `NO_GO_GEOMETRIC_CURRENT_T01_T11`.

Discriminating tests: the Boolean two-map collection is not a singleton; a
surjective quotient fiber can contain distinct left translations; deleting all
geometric and categorical data leaves every theorem in this module unchanged.
-/

namespace IUT1

universe u v w

/-! ## PA01: collections of functions -/

/-- An algebraic poly-morphism is extensionally a set of functions. -/
abbrev PolyMorphism (X : Type u) (Y : Type v) := Set (X → Y)

namespace PolyMorphism

/-- Embed one ordinary function as a singleton poly-morphism. -/
def singleton {X : Type u} {Y : Type v} (f : X → Y) : PolyMorphism X Y :=
  {f}

/-- Membership in the singleton embedding is ordinary function equality. -/
theorem mem_singleton_iff {X : Type u} {Y : Type v} {f g : X → Y} :
    f ∈ singleton g ↔ f = g :=
  Set.mem_singleton_iff

/-- PA01: the singleton embedding of ordinary maps is injective. -/
theorem PA01_singleton_injective {X : Type u} {Y : Type v} {f g : X → Y}
    (h : singleton f = singleton g) : f = g := by
  have hf : f ∈ singleton g := by
    rw [← h]
    exact Set.mem_singleton f
  exact mem_singleton_iff.mp hf

/-- The identity member of the closed Boolean two-map discriminator. -/
def boolIdentity : Bool → Bool :=
  id

/-- The negation member of the closed Boolean two-map discriminator. -/
def boolNegation : Bool → Bool :=
  Bool.not

/-- A two-arrow poly-morphism used to discriminate collections from selected maps. -/
def boolTwoMap : PolyMorphism Bool Bool :=
  {f | f = boolIdentity ∨ f = boolNegation}

/-- The two displayed Boolean functions are distinct. -/
theorem boolIdentity_ne_boolNegation : boolIdentity ≠ boolNegation := by
  intro h
  have hf := congrFun h false
  simp [boolIdentity, boolNegation] at hf

/-- PA01: the Boolean two-map collection is neither displayed singleton. -/
theorem PA01_bool_two_map_ne_singletons :
    boolTwoMap ≠ singleton boolIdentity ∧
      boolTwoMap ≠ singleton boolNegation := by
  constructor
  · intro h
    have hn : boolNegation ∈ singleton boolIdentity := by
      rw [← h]
      exact Or.inr rfl
    exact boolIdentity_ne_boolNegation (mem_singleton_iff.mp hn).symm
  · intro h
    have hi : boolIdentity ∈ singleton boolNegation := by
      rw [← h]
      exact Or.inl rfl
    exact boolIdentity_ne_boolNegation (mem_singleton_iff.mp hi)

/-! ## PA02: pairwise composition -/

/-- Pairwise composition: `q.comp p` applies a member of `p`, then one of `q`. -/
def comp {X : Type u} {Y : Type v} {Z : Type w}
    (q : PolyMorphism Y Z) (p : PolyMorphism X Y) : PolyMorphism X Z :=
  {h | ∃ f ∈ p, ∃ g ∈ q, h = g ∘ f}

/-- PA02: pairwise composition is extensionally associative. -/
theorem PA02_comp_assoc {X : Type u} {Y : Type v} {Z : Type w} {W : Type*}
    (r : PolyMorphism Z W) (q : PolyMorphism Y Z) (p : PolyMorphism X Y) :
    (r.comp q).comp p = r.comp (q.comp p) := by
  ext h
  constructor
  · rintro ⟨f, hf, k, ⟨g, hg, j, hj, rfl⟩, rfl⟩
    exact ⟨g ∘ f, ⟨f, hf, g, hg, rfl⟩, j, hj, rfl⟩
  · rintro ⟨k, ⟨f, hf, g, hg, rfl⟩, j, hj, rfl⟩
    exact ⟨f, hf, j ∘ g, ⟨g, hg, j, hj, rfl⟩, rfl⟩

/-- PA02: pairwise composition restricts to ordinary composition on singletons. -/
theorem PA02_comp_singleton {X : Type u} {Y : Type v} {Z : Type w}
    (g : Y → Z) (f : X → Y) :
    (singleton g).comp (singleton f) = singleton (g ∘ f) := by
  ext h
  constructor
  · rintro ⟨f', hf', g', hg', rfl⟩
    have hff : f' = f := mem_singleton_iff.mp hf'
    have hgg : g' = g := mem_singleton_iff.mp hg'
    subst f'
    subst g'
    exact Set.mem_singleton (g ∘ f)
  · intro hh
    have hcomp : h = g ∘ f := mem_singleton_iff.mp hh
    subst h
    exact ⟨f, Set.mem_singleton f, g, Set.mem_singleton g, rfl⟩

/-- PA02: the Boolean collection is closed under producing both displayed arrows. -/
theorem PA02_bool_two_map_self_comp :
    boolIdentity ∈ boolTwoMap.comp boolTwoMap ∧
      boolNegation ∈ boolTwoMap.comp boolTwoMap := by
  constructor
  · exact ⟨boolIdentity, Or.inl rfl, boolIdentity, Or.inl rfl, rfl⟩
  · exact ⟨boolIdentity, Or.inl rfl, boolNegation, Or.inr rfl, rfl⟩

end PolyMorphism

/-! ## PA03--PA05: a surjective-homomorphism fiber prototype -/

/--
The complete stored data of the algebraic prototype: a group homomorphism and
its surjectivity proof.  Nonempty fibers and composition laws are derived below.
-/
structure AlgebraicPolyActionPrototype (H : Type u) (G : Type v)
    [Group H] [Group G] where
  projection : H →* G
  surjective : Function.Surjective projection

namespace AlgebraicPolyActionPrototype

variable {H : Type u} {G : Type v} [Group H] [Group G]

/-- Left translation by a group element, retained as an actual permutation. -/
def leftTranslationPermutation (h : H) : Equiv.Perm H :=
  Equiv.mulLeft h

/-- PA03: all left translations whose translating elements lie over `g`. -/
def arrows (P : AlgebraicPolyActionPrototype H G) (g : G) : PolyMorphism H H :=
  {f | ∃ h, P.projection h = g ∧
    f = (leftTranslationPermutation h : H → H)}

/-- PA03: arrow collections are nonempty as a theorem, not as stored data. -/
theorem PA03_arrows_nonempty (P : AlgebraicPolyActionPrototype H G) (g : G) :
    (P.arrows g).Nonempty := by
  obtain ⟨h, hh⟩ := P.surjective g
  exact ⟨(leftTranslationPermutation h : H → H), h, hh, rfl⟩

/-- PA04: quotient-fiber arrows satisfy exact pairwise composition. -/
theorem PA04_arrows_mul (P : AlgebraicPolyActionPrototype H G) (g h : G) :
    P.arrows (g * h) = (P.arrows g).comp (P.arrows h) := by
  ext arrow
  constructor
  · rintro ⟨x, hx, rfl⟩
    obtain ⟨b, hb⟩ := P.surjective h
    let a : H := x * b⁻¹
    have ha : P.projection a = g := by
      dsimp [a]
      rw [map_mul, map_inv, hx, hb]
      simp
    refine ⟨(leftTranslationPermutation b : H → H), ⟨b, hb, rfl⟩,
      (leftTranslationPermutation a : H → H), ⟨a, ha, rfl⟩, ?_⟩
    funext z
    change x * z = a * (b * z)
    dsimp [a]
    simp [mul_assoc]
  · rintro ⟨fb, ⟨b, hb, rfl⟩, fa, ⟨a, ha, rfl⟩, rfl⟩
    refine ⟨a * b, ?_, ?_⟩
    · rw [map_mul, ha, hb]
    · funext z
      change a * (b * z) = (a * b) * z
      simp [mul_assoc]

/-- Every label has exactly one arrow. -/
def SingleValued (P : AlgebraicPolyActionPrototype H G) : Prop :=
  ∀ g, ∃! arrow, arrow ∈ P.arrows g

/-- PA05: an injective projection makes the prototype single-valued. -/
theorem PA05_singleValued_of_injective (P : AlgebraicPolyActionPrototype H G)
    (hinj : Function.Injective P.projection) : P.SingleValued := by
  intro g
  obtain ⟨x, hx⟩ := P.surjective g
  refine ⟨(leftTranslationPermutation x : H → H), ⟨x, hx, rfl⟩, ?_⟩
  intro arrow harrow
  rcases harrow with ⟨y, hy, rfl⟩
  have hyx : y = x := hinj (hy.trans hx.symm)
  subst y
  rfl

/--
PA05 discriminator: a nonidentity kernel element produces two distinct arrows
over the identity label; no representative is selected.
-/
theorem PA05_multiple_arrows_of_nontrivial_kernel
    (P : AlgebraicPolyActionPrototype H G) (k : H)
    (hk : P.projection k = 1) (hne : k ≠ 1) :
    (leftTranslationPermutation (1 : H) : H → H) ∈ P.arrows 1 ∧
      (leftTranslationPermutation k : H → H) ∈ P.arrows 1 ∧
      (leftTranslationPermutation (1 : H) : H → H) ≠
        (leftTranslationPermutation k : H → H) := by
  refine ⟨⟨1, map_one P.projection, rfl⟩, ⟨k, hk, rfl⟩, ?_⟩
  intro hfun
  apply hne
  have hvalue := congrFun hfun 1
  simpa [leftTranslationPermutation] using hvalue.symm

end AlgebraicPolyActionPrototype

/-! ## PA06: synthetic finite quotient-fiber example -/

/-!
`source_id=SRC-OFFICIAL-7360E3ED27C235B5`.
Localizers: section I1, printed p. 4; section 6, printed pp. 155--163.
Epistemic status: `SYNTHETIC_FINITE_QUOTIENT_FIBER_EXAMPLE`.
Dependency status: T09 supplies the proved normal translation subgroup and its
index.  This example is not identified with the source actions of the
multiplicative or signed label groups on `C_K`, `X_K`, or Hodge-theoretic data.
Discriminant: identity and translation lifts give different functions at the
identity element while sharing one quotient label.
-/

/-- The two-element quotient label group used only in the synthetic example. -/
abbrev SignedAffine5TranslationLabels :=
  SignedAffine 5 ⧸ translationSubgroup 5

/-- The canonical quotient homomorphism for the synthetic `l=5` example. -/
def signedAffine5TranslationProjection :
    SignedAffine 5 →* SignedAffine5TranslationLabels :=
  QuotientGroup.mk' (translationSubgroup 5)

/-- Surjectivity of the canonical quotient homomorphism. -/
theorem signedAffine5TranslationProjection_surjective :
    Function.Surjective signedAffine5TranslationProjection :=
  QuotientGroup.mk'_surjective (translationSubgroup 5)

/-- The synthetic algebraic quotient-fiber prototype at `l=5`. -/
def signedAffine5AlgebraicPolyActionPrototype :
    AlgebraicPolyActionPrototype (SignedAffine 5) SignedAffine5TranslationLabels where
  projection := signedAffine5TranslationProjection
  surjective := signedAffine5TranslationProjection_surjective

/-- A visible nonidentity element of the translation subgroup. -/
def signedAffine5NontrivialTranslation : SignedAffine 5 :=
  ⟨1, false⟩

/-- The displayed translation is not the identity signed-affine element. -/
theorem signedAffine5NontrivialTranslation_ne_one :
    signedAffine5NontrivialTranslation ≠ 1 := by
  decide

/-- The displayed translation lies in the identity fiber of the quotient map. -/
theorem signedAffine5NontrivialTranslation_projection_eq_one :
    signedAffine5TranslationProjection signedAffine5NontrivialTranslation = 1 := by
  exact (QuotientGroup.eq_one_iff signedAffine5NontrivialTranslation).2 rfl

/-- PA06: the quotient label group has cardinality two, directly by T09. -/
theorem PA06_signedAffine5_translation_label_card :
    Nat.card SignedAffine5TranslationLabels = 2 := by
  change (translationSubgroup 5).index = 2
  exact T09_C06_translation_index 5

/-- PA06: the identity quotient label has two distinct left-translation arrows. -/
theorem PA06_signedAffine5_two_arrows_over_identity :
    (AlgebraicPolyActionPrototype.leftTranslationPermutation
      (1 : SignedAffine 5) : SignedAffine 5 → SignedAffine 5) ∈
        signedAffine5AlgebraicPolyActionPrototype.arrows 1 ∧
      (AlgebraicPolyActionPrototype.leftTranslationPermutation
        signedAffine5NontrivialTranslation : SignedAffine 5 → SignedAffine 5) ∈
          signedAffine5AlgebraicPolyActionPrototype.arrows 1 ∧
      (AlgebraicPolyActionPrototype.leftTranslationPermutation
        (1 : SignedAffine 5) : SignedAffine 5 → SignedAffine 5) ≠
          (AlgebraicPolyActionPrototype.leftTranslationPermutation
            signedAffine5NontrivialTranslation : SignedAffine 5 → SignedAffine 5) :=
  AlgebraicPolyActionPrototype.PA05_multiple_arrows_of_nontrivial_kernel
    signedAffine5AlgebraicPolyActionPrototype signedAffine5NontrivialTranslation
    signedAffine5NontrivialTranslation_projection_eq_one
    signedAffine5NontrivialTranslation_ne_one

/-- PA06 evaluation discriminator at the identity element of `SignedAffine 5`. -/
theorem PA06_signedAffine5_two_arrow_values_at_one :
    AlgebraicPolyActionPrototype.leftTranslationPermutation
        (1 : SignedAffine 5) 1 = 1 ∧
      AlgebraicPolyActionPrototype.leftTranslationPermutation
        signedAffine5NontrivialTranslation 1 = signedAffine5NontrivialTranslation := by
  constructor <;> rfl

end IUT1
