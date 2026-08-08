# IUT I completion program

This project will not proceed to IUT II until the IUT I completion gate has
passed. The present finite-symmetry unit is a foundation, not a proxy for the
whole paper.

## Source-shaped work units

The program follows the architecture of *Inter-universal Teichmüller Theory I*:

| Unit | Source region | Current state | Main semantic risk |
|---|---|---|---|
| Finite symmetry foundation | Introduction §I1; §0 poly-morphisms; Definitions 6.1 and 6.4 | T01--T11 and algebraic PA01--PA06 independently verified; geometric NO_GO; public-package gate PASS; publication-metadata review PASS | Conflating groups, quotients, torsors, chart orbits, algebraic prototypes and geometric poly-actions. |
| Notation and ambient types | §0, p. 33 | source structure located; claim map required | Reusing a symbol after its category or universe changes. |
| Punctured elliptic-curve coverings | §1, p. 37 | source structure located; uncontracted | Replacing a finite étale covering and its provenance by a finite set or a degree field. |
| Tempered coverings | §2, p. 44; Theorem B and Corollary 2.5 | source structure located; uncontracted | Replacing tempered topology and decomposition data by an injective abstract homomorphism. |
| Initial theta-data and chains | Definition 3.1 and §3, p. 61 | source structure located; uncontracted | Advertising a record of assumptions as a constructed instance. |
| Multiplicative combinatorial theory | §4, p. 95 | source structure located; uncontracted beyond T01--T05 | Replacing a sourced torsor or geometric trivialization by cardinal arithmetic. |
| Theta-NF Hodge theaters and prime-strips | §5, p. 123; Definition 5.2, p. 134 | source structure located; uncontracted | Treating a constant or one-place schema witness as the source construction. |
| Additive combinatorial theory | §6 and Definition 6.1, p. 155; Definition 6.4, p. 162 | selected clauses reviewed; uncontracted beyond the coordinate core | Making compatibility tautological by transporting the desired action through a supplied equivalence. |
| Whole-paper synthesis | all IUT I units | blocked | Hiding deferred geometry or an absent dependency behind suggestive names. |

Each unit must have four synchronized layers: exposition, formalization,
applications and replication. A layer cannot borrow another layer's PASS.

## Unit completion gate

A unit is complete only when it has:

1. a primary-source map with stable identifiers and exact localizers;
2. an independently reviewed semantic contract;
3. Lean declarations whose conclusions are not stored as assumptions;
4. complete axiom reports for exported theorems and project-defined instances;
5. an independent fidelity review and cold replication;
6. positive examples and discriminating negative tests;
7. an English theorem-by-theorem explanation for non-specialists;
8. machine-readable claims, examples, anti-patterns and dependencies;
9. a per-target poly-action checkpoint giving its role, finite witness, exact
   Lean reference and scientific boundary, including `NO_POLYACTION_CLAIM`
   where appropriate;
10. a rights-safe release manifest and passing CI.

## IUT I completion gate

IUT I is complete only after every section-level unit satisfies the unit gate,
all deferred obligations appear in a public dependency graph, the entire
repository builds from a clean checkout, and an independent final audit reports
no high- or medium-severity finding. Until then the correct description is
“an incremental reference library for selected IUT I units.”
