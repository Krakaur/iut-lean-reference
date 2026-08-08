import IUT1.SignedAffineDihedral

/-!
# APP01: exhaustive finite convention auditor

This application accepts an arbitrary proposed encoding from visible
signed-affine pairs to the dihedral presentation.  It checks the full finite
domain of group elements and coordinates; it does not assume that the proposed
encoding is a homomorphism or an equivalence.
-/

namespace IUT1

/-- A raw proposed convention for encoding signed-affine pairs. -/
abbrev ConventionCandidate (l : ℕ) := SignedAffine l → DihedralGroup l

/-!
Inherited context: `source_id=SRC-OFFICIAL-7360E3ED27C235B5`, IUT I Section I1,
printed p. 3, and Definition 6.1(i), printed p. 155.
Epistemic status: `METHODOLOGICAL_APPLICATION_OF_DERIVED_COORDINATE_MODEL`.
Discriminant: both finite quantifiers are evaluated; restricting the check to
rotations would incorrectly accept the rival reflection convention.
-/

/-- Decide whether a candidate preserves the two displayed actions everywhere. -/
def conventionCheck (l : ℕ) [NeZero l] (candidate : ConventionCandidate l) : Bool :=
  decide (∀ g : SignedAffine l, ∀ z : Fl l,
    dihedralAct (candidate g) z = g.act z)

/-- APP01-C01: exact Boolean/propositional specification of the exhaustive checker. -/
theorem APP01_C01_check_spec (l : ℕ) [NeZero l]
    (candidate : ConventionCandidate l) :
    conventionCheck l candidate = true ↔
      ∀ g : SignedAffine l, ∀ z : Fl l,
        dihedralAct (candidate g) z = g.act z := by
  simp [conventionCheck]

/-- The gated T10 encoding, regarded as a raw candidate input. -/
def canonicalConventionCandidate (l : ℕ) : ConventionCandidate l :=
  signedAffineDihedralEquiv l

/-- The tempting rival that omits negation in the reflection coordinate. -/
def unsignedReflectionCandidate (l : ℕ) : ConventionCandidate l
  | ⟨a, false⟩ => DihedralGroup.r a
  | ⟨a, true⟩ => DihedralGroup.sr a

/-!
APP01-C02--C04 are project-created regression obligations, not source claims.
They retain the inherited source context above and the same epistemic status.
The exhaustive Boolean changes from `true` to `false`; the separate witness
identifies the negative-reflection error by the values `2` and `4`.
-/

/-- APP01-C02: exhaustive evaluation accepts the canonical convention at `l=5`. -/
theorem APP01_C02_canonical_passes_l5 :
    conventionCheck 5 (canonicalConventionCandidate 5) = true := by
  decide

/-- APP01-C03: exhaustive evaluation rejects the unsigned-reflection rival at `l=5`. -/
theorem APP01_C03_unsigned_reflection_fails_l5 :
    conventionCheck 5 (unsignedReflectionCandidate 5) = false := by
  decide

/-- APP01-C04: the explicit negative-reflection witness explaining the rejection. -/
theorem APP01_C04_failure_witness_l5 :
    let g : SignedAffine 5 := ⟨1, true⟩
    let z : Fl 5 := 2
    dihedralAct (unsignedReflectionCandidate 5 g) z = 2 ∧
      g.act z = 4 ∧
      dihedralAct (unsignedReflectionCandidate 5 g) z ≠ g.act z := by
  decide

end IUT1
