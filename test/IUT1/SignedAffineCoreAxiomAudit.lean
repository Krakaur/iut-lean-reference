import IUT1.SignedAffineCore
import IUT1.SignOrbitBridge

namespace IUT1

/-- T08 audit witness separating affine cardinality from additive sign-orbit cardinality. -/
theorem T08_audit_l5_ne_signOrbit_card :
    (10 : ℕ) ≠ lPlusMinus 5 ∧ lPlusMinus 5 = 3 := by
  decide

#print axioms IUT1.instGroupSignedAffine
#print axioms IUT1.T06_C06_mul_formula
#print axioms IUT1.T06_example_l5_semidirect
#print axioms IUT1.T07_C06_act_mul
#print axioms IUT1.T07_example_l5_action_order
#print axioms IUT1.T08_C06_card_signedAffine
#print axioms IUT1.T08_example_l5_card
#print axioms IUT1.T08_audit_l5_ne_signOrbit_card

end IUT1
