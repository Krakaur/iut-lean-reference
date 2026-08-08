# Poly-actions: source map and scientific boundary

This page is a source-facing guide for LANA/IUT researchers. It records what
the registered IUT I source says, which algebraic interface is implemented in
Lean, and which geometric data remain absent. The independent anchor review is
`PASS_INDEPENDENT_SOURCE_ANCHORS_R3`, with P1=P2=P3=0. That source PASS does not
transfer to kernel, fidelity, replication or publication.

## Source claim ledger

| `source_id` | Localizer | Epistemic status | Claim, example and Lean checkpoint |
|---|---|---|---|
| `SRC-OFFICIAL-7360E3ED27C235B5` | section 0, printed pp. 33–34 | `SOURCE_EXPLICIT_DEFINITION` | A poly-morphism is a collection of morphisms and composition takes all pairwise composites. The Boolean collection containing identity and negation is not either singleton: `IUT1.PolyMorphism.PA01_bool_two_map_ne_singletons`; pairwise self-composition retains both maps: `IUT1.PolyMorphism.PA02_bool_two_map_self_comp`. |
| `SRC-OFFICIAL-7360E3ED27C235B5` | section I1, printed p. 4 | `SOURCE_EXPLICIT_OVERVIEW` | The displayed poly-actions retain automorphism-subquotient structure and arithmetic/geometric provenance. The synthetic quotient-fiber example has two arrows over one label, `IUT1.PA06_signedAffine5_two_arrows_over_identity`, but intentionally has no such provenance. |
| `SRC-OFFICIAL-7360E3ED27C235B5` | section 4, printed pp. 98–100 | `SOURCE_EXPLICIT_CONSTRUCTION_CONTEXT` | Multiplicative labels, capsules and poly-morphisms occur together. T03–T04 model only the finite multiplicative prerequisite. At `l=5`, `IUT1.T04_C02_C04_card_MultiplicativeLabelGroup` gives two label classes but supplies no arrows. This anchor does not support the additive T05 branch. |
| `SRC-OFFICIAL-7360E3ED27C235B5` | Example 6.3(ii), printed pp. 161–162 | `SOURCE_EXPLICIT_APPLICATION_CONTEXT` | Signed poly-actions and equivariance of a poly-morphism occur in the construction. The Lean prototype tests the collection/composition pattern, not that geometric instance: `IUT1.AlgebraicPolyActionPrototype.PA04_arrows_mul`. |
| `SRC-OFFICIAL-7360E3ED27C235B5` | Definition 6.4, printed pp. 162–163 | `SOURCE_EXPLICIT_DEFINITION` | Bridges, capsules and compatibility of constituent poly-morphisms are defined. The finite example `IUT1.PA06_signedAffine5_two_arrow_values_at_one` contains none of those objects; this absence is part of its declared type and status. |

## The discriminating boundary

Delete every curve, covering, cusp, capsule, bridge, Hodge theater and
arithmetic/geometric provenance item from the source context. All declarations
in `PolyMorphismPrototype.lean` remain meaningful and provable. This mutation is
the decisive negative test: the module formalizes an algebraic pattern shared
with the source vocabulary, not an IUT poly-action.

Conversely, replacing a collection by one selected arrow loses information.
The closed Boolean example proves this already for two functions, while the
`l=5` quotient-fiber example proves it for two distinct left translations over
one quotient label. These are useful interface tests precisely because they do
not depend on geometric interpretation.

## Use in a LANA/IUT workflow

A source reviewer can begin with one of the five rows, retain its `source_id`,
localizer and epistemic status, and then ask whether a proposed Lean type
contains the named data. A formalizer can import the nearest algebraic test. An
independent reviewer can mutate the proposed model to a singleton or erase its
provenance and observe which obligations survive.

For example, the phrase “collection of morphisms” routes to PA01 and PA02. The
positive test is pairwise composition; the adversarial test is selection of one
Boolean map. The phrase “automorphism subquotient” routes to PA03–PA06. The
positive test is exact fiber composition; the adversarial test asks whether a
nontrivial kernel still produces multiple arrows.

## Explicit non-claims

The map and prototype do not construct `C_K`, `X_K`, cusp geometry, source
capsules, bridges, Hodge theaters, a geometric automorphism or Galois
subquotient, an IUT I poly-action or IUT I as a whole. They do not enter IUT II
or prove any bridge from IUT III 3.11 to 3.12, Szpiro or abc.
