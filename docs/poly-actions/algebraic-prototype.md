# Algebraic poly-morphism and quotient-fiber prototype

The prototype is an executable interface for testing formal interpretations of
collection-valued morphisms. Its epistemic status is
`ALGEBRAIC_PROTOTYPE_OF_SOURCE_POLYMORPHISM_AND_SUBQUOTIENT_PATTERN`; its
geometric status is `NO_GO_GEOMETRIC_CURRENT_T01_T11`.

## PA01 — keep the whole collection

`PolyMorphism X Y` is definitionally `Set (X → Y)`. Ordinary functions embed
as singleton sets, and `IUT1.PolyMorphism.PA01_singleton_injective` proves that
this embedding loses no equality information.

The finite discriminator uses `Bool`. The collection containing identity and
Boolean negation differs from each singleton, as proved by
`IUT1.PolyMorphism.PA01_bool_two_map_ne_singletons`. A representation that
stores only one selected function fails this example.

## PA02 — compose every compatible pair

For `p : PolyMorphism X Y` and `q : PolyMorphism Y Z`, `q.comp p` contains
exactly the functions `g ∘ f` with `f ∈ p` and `g ∈ q`. The declarations
`IUT1.PolyMorphism.PA02_comp_assoc` and
`IUT1.PolyMorphism.PA02_comp_singleton` establish associativity and recovery of
ordinary composition on singleton collections.

The Boolean two-map collection composes with itself and still contains both
identity and negation. This is checked by
`IUT1.PolyMorphism.PA02_bool_two_map_self_comp`; selecting one representative
would not establish the stated two-membership result.

## PA03–PA04 — a quotient fiber supplies arrow collections

`AlgebraicPolyActionPrototype H G` stores only a surjective group homomorphism
`H →* G` and its surjectivity proof. For a label `g : G`, its arrows are all
left translations by elements in the fiber over `g`. Nonemptiness is derived
by `IUT1.AlgebraicPolyActionPrototype.PA03_arrows_nonempty`; it is not a stored
law.

The central composition theorem is
`IUT1.AlgebraicPolyActionPrototype.PA04_arrows_mul`:

```lean
P.arrows (g * h) = (P.arrows g).comp (P.arrows h)
```

The orientation means that a lift of `h` acts first and a lift of `g` acts
second. For the reverse inclusion, an arbitrary lift `x` of `g*h` is factored
using a chosen lift `b` of `h` and `a=x*b⁻¹`. Thus the result is equality of
complete fibers, not merely one-way closure.

## PA05 — locate the single-valued boundary

`SingleValued` means that each label has exactly one arrow.
`IUT1.AlgebraicPolyActionPrototype.PA05_singleValued_of_injective` proves this
when the projection is injective. The companion theorem
`PA05_multiple_arrows_of_nontrivial_kernel` proves that a nonidentity kernel
element yields two different translations over the identity label.

The adversarial interpretation is to choose one lift from each fiber. It may
produce an ordinary-action candidate, but it discards the other arrows and is
therefore unjustified unless uniqueness has been proved.

## PA06 — closed `l=5` example

Let `H = SignedAffine 5` and quotient by the normal translation subgroup from
T09. `IUT1.PA06_signedAffine5_translation_label_card` proves that the quotient
has two labels. The identity and the nonidentity translation `(1,false)` lie in
the same identity fiber, yet their left translations are distinct:

```lean
IUT1.PA06_signedAffine5_two_arrows_over_identity
IUT1.PA06_signedAffine5_two_arrow_values_at_one
```

Evaluating at the identity separates the arrows: one returns the identity and
the other returns `(1,false)`. This gives a small, kernel-checked regression for
the phrase “two arrows for one label.” It is a synthetic quotient-fiber model,
not the source's multiplicative or signed poly-action on geometric data.

## Utility for LANA/IUT work

The module can serve as a proposed interface test before geometric
formalization begins. A candidate API should be able to state collections,
pairwise composition, singleton reduction and a multiarrow fiber without
silently selecting representatives. Each theorem page T01–T11 records where
that test is relevant and where it is only a boundary marker.

The intended retrieval unit is not the theorem name alone. It is the source
tuple, the mathematical example, the Lean declaration, the adversarial
mutation and the explicit non-claim. This structure is useful for human review
and for AI systems that must distinguish formal similarity from source
fidelity.
