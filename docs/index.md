# Wiki home

This wiki explains the requested T01--T08 finite-algebra chain and three
verified closure/regression targets from the same tightly bounded coordinate
unit of IUT I. Its purpose is comprehension and traceability, not rhetorical
compression.

For a file-by-file map of the four layers, use the
[artifact catalog](artifact-catalog.md).
For research workflows, begin with the
[LANA/IUT community use cases](community/lana-iut-use-cases.md).

## The dependency chain

```text
T01  finite coordinate carrier F_l
 ├── T02  fixed points of negation
 ├── T03  two-element sign subgroup
 │    └── T04  multiplicative units modulo sign
 └── T05  additive sign quotients and distinguished chart orbits
      └── T08 discriminator: (l+1)/2 is not 2*l

T06  signed-affine group on visible pairs
 └── T07  compatibility with affine composition
 ├── T08  cardinality 2*l
 ├── T09  translation subgroup: index two and normality
 └── T10  explicit dihedral comparison and action compatibility

T11  typed l=5 and l=7 regression vectors, reusing T04, T05 and T08

§0 source definition of collections
 └── PA01–PA02  sets of functions and pairwise composition

T09 normal translation subgroup
 └── PA03–PA06  quotient-fiber prototype and two-arrow l=5 example
```

The upper and lower branches share finite-field coordinates but represent
different types. T05 studies a quotient of a carrier by negation. T06--T08
study a group of affine transformations. At `l=5` the former has three classes
and the latter ten elements.

## Four synchronized layers

### 1. Exposition

The theorem pages translate every Txx into ordinary mathematical prose and
state the nearest plausible misreading. Start with [T01](theorems/T01.md) and
continue in numerical order.

### 2. Formalization

The four source-facing core files under `src/IUT1` contain the reviewed T
declarations. The core files preserve the bytes that passed independent audit.
`Tutorial.lean` adds comments and closed examples without changing those
proofs. Application modules separately host the convention auditor and the
algebraic poly-morphism prototype.

### 3. Applications and falsifiers

Examples are not decorative. Each is chosen to reject a nearby wrong model:
modulus two for T02, omission of the zero orbit for T05, direct rather than
semidirect multiplication for T06, reversed composition for T07, conflated
cardinalities for T08/T11, and the wrong reflection coordinate for T10.
PA01–PA06 add two more falsifiers: selecting one Boolean map from a two-map
collection and erasing the second lift from a nontrivial quotient fiber.

### 4. Replication

The `test` directory requests axiom reports. The `evidence` directory records
source hashes, exact locators, artifact hashes, gate separation, and cold-run
results. These records allow a later reader or model to distinguish a parsed
source claim from a theorem accepted by Lean.

## Reading routes

If you are a mathematician new to Lean, read the [glossary](foundations/glossary.md),
then each theorem's “plain mathematical translation,” and finally the matching
section of `Tutorial.lean`.

If you use Lean, begin with `src/IUT1.lean`, inspect the theorem modules, and
then compile `test/IUT1Audit.lean` to see the axiom surface.

If you work on poly-actions, first read the
[source map and boundary](poly-actions/source-and-boundary.md), then the
[algebraic prototype](poly-actions/algebraic-prototype.md), and finally the
checkpoint in the relevant T page. This order prevents the prototype from
being mistaken for the source geometry.

If you build AI retrieval or training data, begin with [the AI corpus guide](../ai/README.md)
and `ai/claims.jsonl`. Do not train on a theorem statement without retaining its
`source_id`, localizer, epistemic status and discriminator.

If your interest is IUT III 3.11--3.12, treat this release as an example of
evidence architecture, not as a mathematical bridge to that result. The
[roadmap](roadmap/iut3-3-11-to-3-12.md) lists what would have to be added before
such a bridge could even be reviewed. Active development remains restricted to
the [IUT I completion program](roadmap/iut1-program.md).
