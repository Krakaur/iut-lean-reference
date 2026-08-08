# Theorem-by-theorem guide

Each page follows the same evidence schema:

1. source identifier and printed-page locator;
2. epistemic status of the mathematical statement;
3. a translation for non-specialists;
4. the exact Lean declaration;
5. dependencies and proof idea;
6. a closed or conceptual example;
7. a discriminator against a nearby wrong interpretation;
8. an explicit list of conclusions that do not follow;
9. a poly-action checkpoint with role, example, exact Lean references and
   scientific boundary.

Pages: [T01](T01.md), [T02](T02.md), [T03](T03.md), [T04](T04.md),
[T05](T05.md), [T06](T06.md), [T07](T07.md), [T08](T08.md),
[T09](T09.md), [T10](T10.md), [T11](T11.md).

T05 contains four separately audited obligations because a single cardinality
statement would erase the source's distinguished orbit of coordinate charts.
T06--T08 are kept distinct because a group law, an action law and a cardinality
calculation are different verification targets even when they concern the same
carrier.

T09--T11 close the coordinate unit without adding geometry: T09 analyzes the
translation subgroup, T10 proves a non-definitional dihedral comparison with a
sign-sensitive action test, and T11 packages two typed finite regressions.

The checkpoint roles are not theorem upgrades. `PREREQUISITE_ONLY`,
`CARDINALITY_ONLY` and `REGRESSION_ONLY` explicitly deny a poly-action
conclusion. The closest executable multiarrow example is
`IUT1.PA06_signedAffine5_two_arrows_over_identity`, documented in the
[algebraic prototype guide](../poly-actions/algebraic-prototype.md).
