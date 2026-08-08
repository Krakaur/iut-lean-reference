# Guide for mathematicians who do not use Lean

The formal files are easiest to read after three distinctions are fixed.

## 1. Three finite objects, three different sizes

For prime `l >= 5`:

```text
nonzero coordinates modulo sign     (l-1)/2
all coordinates modulo sign         (l+1)/2
signed-affine transformations        2*l
```

At `l=5` these numbers are `2`, `3` and `10`. The differences are structural:
the first object excludes zero, the second includes zero as a fixed orbit, and
the third consists of transformations rather than quotient classes.

## 2. Coordinates are not the object being coordinated

A bijection to `F_l` provides coordinates on a finite carrier. It does not make
that carrier definitionally equal to `F_l`. A distinguished orbit of charts
also contains more information than the bare fact that some chart exists. T05
formalizes this distinction and supplies a counterexample to an overly broad
family of charts.

## 3. Finite algebra is not geometric provenance

The transformations `z ↦ ±z+a` form a familiar finite affine group. Proving
their laws in Lean establishes those laws for the chosen coordinate model. It
does not construct the curves, covers, cusps or poly-actions to which the source
ultimately relates this symmetry.

## 4. A collection of maps is not one selected map

The minimal algebraic meaning of a poly-morphism used here is a set of
functions. Composition takes every compatible pair. An ordinary function is
the special case of a singleton set, but a multi-arrow collection cannot be
recovered from an arbitrary selected representative.

On `Bool`, the collection containing identity and negation is not equal to
either singleton. Lean checks this in
`IUT1.PolyMorphism.PA01_bool_two_map_ne_singletons`. In the quotient-fiber
example at `l=5`, identity and `(1,false)` produce two different left
translations over the same label; see
`IUT1.PA06_signedAffine5_two_arrows_over_identity`. These examples explain the
interface without claiming the source's geometric poly-actions.

## 5. An isomorphism does not erase coordinate conventions

The visible signed-affine group is isomorphic to Mathlib's dihedral group, but
the comparison still has a sign choice. Under the multiplication conventions
used here, `(a,true)` corresponds to `sr(-a)`, not `sr(a)`. T10 proves action
compatibility after defining both actions independently; T11 then retains the
different quotient and group types in two complete finite regression vectors.

## How to read a theorem page

The “plain mathematical translation” is the informal statement. The Lean code
is the machine-checked version. “Dependencies” explain what is already assumed.
The “discriminator” gives a nearby incorrect interpretation and a calculation
that rejects it. “Does not establish” marks the boundary of the result. Every
T page also has a “Poly-action checkpoint” specifying its role, finite witness,
Lean reference and scientific boundary.

The axiom report is not a measure of source fidelity. It only reports the
logical constants on which Lean's compiled declaration depends. Source fidelity
is reviewed separately.

## Minimal Lean vocabulary

`def` introduces data or a function. `structure` declares a record with named
fields. `theorem` introduces a proposition and its proof. `instance` tells Lean
how a type carries standard structure, such as a group. `by` begins a proof.
`simp` performs verified rewriting; `decide` proves a decidable closed statement
by evaluation inside Lean's trusted elaboration/kernel pipeline.

Start with `src/IUT1/Tutorial.lean`. Its examples invoke the reviewed theorems
and annotate why each calculation matters. Then read
`src/IUT1/Applications/PolyMorphismPrototype.lean` beside the
[poly-action prototype guide](poly-actions/algebraic-prototype.md).
