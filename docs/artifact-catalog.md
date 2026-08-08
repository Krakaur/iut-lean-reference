# Artifact catalog

This catalog is the stable entry point for humans and retrieval systems. It
separates the four library layers so that a proof file, an explanation, an
application and a replication record are never mistaken for one another.

## Target matrix

| Target | Source/epistemic role | Lean entry point | Worked discriminator |
|---|---|---|---|
| T01 | derived finite coordinate model | `T01_C01_card_Fl` | a coordinate carrier is not a geometric label set |
| T02 | derived coordinatized model | `T02_C01_neg_eq_self_iff` | modulus two has a nonzero fixed point |
| T03 | derived sign subgroup | `T03_C02_card_SignSubgroup` | characteristic two collapses the signs |
| T04 | derived multiplicative quotient | `T04_C02_C04_card_MultiplicativeLabelGroup` | zero is excluded: two classes at `l=5` |
| T05 | derived chart/sign-quotient interface | `T05a`--`T05d` declarations | multiplication by two rejects the “all equivariant charts” mutation |
| T06 | prior-art algebra, visible coordinate law | `T06_C06_mul_formula` | semidirect translation four versus direct-product translation three |
| T07 | prior-art affine action law | `T07_C06_act_mul` | right-to-left composition versus its reversal |
| T08 | prior-art IUT-oriented cardinality | `T08_C06_card_signedAffine` | signed-affine ten versus additive quotient three |
| T09 | derived subgroup structure | `T09_C06_translation_index` | `(0,true)` toggles translation membership |
| T10 | prior-art dihedral comparison with audited convention | `signedAffineDihedralEquiv`, `T10_C06_dihedral_action_compatible` | `sr(-1)` acts by four; `sr(1)` acts by two |
| T11 | no new source claim; executable regression | `T11_l5_cardinality_vector`, `T11_l7_cardinality_vector` | typed vectors `(2,3,10)` and `(3,4,14)` |

The authoritative machine-readable versions, including `source_id`, exact
localizers, dependencies, gate statuses and non-claims, are in
[`ai/claims.jsonl`](../ai/claims.jsonl).

## Layer 1 — exposition

[`index.md`](index.md) gives the dependency map. The pages under
[`theorems`](theorems/README.md) provide one English explanation per target.
[`guide-for-mathematicians.md`](guide-for-mathematicians.md) explains the type
distinctions without presupposing Lean. The [`l=5`](examples/l5.md) and
[`l=7`](examples/l7.md) pages perform every finite regression by hand.
The [poly-action source map](poly-actions/source-and-boundary.md) and
[algebraic prototype guide](poly-actions/algebraic-prototype.md) pair every
source claim with a finite example, Lean checkpoint and explicit boundary.
The [LANA outreach guide](community/lana-outreach.md) distinguishes public
visibility from open membership and gives a non-affiliation-safe inquiry.

The foundation pages state the notation, source policy, visible signed-affine
convention, [scientific contribution](foundations/scientific-contribution.md),
comparison protocol and quality criteria. Their role is
interpretive; prose does not receive a kernel PASS.

## Layer 2 — formalization

| File | Scope |
|---|---|
| `src/IUT1/SymmetryCore.lean` | T01--T04 |
| `src/IUT1/SignOrbitBridge.lean` | T05a--T05d |
| `src/IUT1/SignedAffineCore.lean` | T06--T08 |
| `src/IUT1/SignedAffineDihedral.lean` | T09--T11 |
| `src/IUT1/Tutorial.lean` | commented facade and closed examples |
| `src/IUT1/Applications/ConventionAudit.lean` | APP01 exhaustive convention test |
| `src/IUT1/Applications/PolyMorphismPrototype.lean` | PA01--PA06 collection and quotient-fiber prototype |

The four source-facing modules are byte-frozen exports of independently gated
artifacts. The tutorial is additive and has its own axiom audit; pedagogical
edits cannot silently rewrite a reviewed core theorem.

## Layer 3 — applications and discriminators

The library distinguishes an application from a closed example. The
[APP01 convention auditor](applications/convention-auditor.md)
convention auditor accepts an arbitrary proposed signed-affine-to-dihedral
encoding and exhaustively checks action agreement over a finite model. Its
canonical input passes at `l=5`; the convention omitting the negative reflection
coordinate fails. The result concerns finite coordinate actions only and is not
a geometric fidelity certificate.

PA01–PA06 test a separate interface problem. On `Bool`, the positive example
retains identity and negation under pairwise composition, while the singleton
mutation loses one arrow. At `l=5`, the positive quotient-fiber example retains
two distinct left translations over the identity label. The operative Lean
declarations are `IUT1.PolyMorphism.PA02_bool_two_map_self_comp` and
`IUT1.PA06_signedAffine5_two_arrows_over_identity`.

Each theorem page also supplies a smaller positive or adversarial fixture. The
structured forms are in [`ai/examples.jsonl`](../ai/examples.jsonl) and the
rejected inference patterns are in
[`ai/anti_patterns.jsonl`](../ai/anti_patterns.jsonl).
The application-level machine record is
[`ai/applications.jsonl`](../ai/applications.jsonl).
Per-target poly-action roles and examples are recorded separately in
[`ai/polyaction_checkpoints.jsonl`](../ai/polyaction_checkpoints.jsonl).

## Layer 4 — replication and evidence

`test/IUT1` contains explicit `#print axioms` requests for every public theorem
and project-defined instance. [`evidence/artifacts.json`](../evidence/artifacts.json)
freezes the reviewed code identities; [`evidence/gates.json`](../evidence/gates.json)
keeps semantic, kernel, fidelity and cold-replication results separate;
[`evidence/sources.json`](../evidence/sources.json) records rights-safe source
access; and [`evidence/release-manifest.json`](../evidence/release-manifest.json)
registers every public file other than its deliberately self-excluded hash.

Authorship and software citation are recorded in
[`CITATION.cff`](../CITATION.cff) and [`codemeta.json`](../codemeta.json).
The path-specific software and documentation licenses are stated in
[`LICENSING.md`](../LICENSING.md).

Run `python scripts/validate_release.py` to check claim completeness,
cross-references, hashes, manifest closure, source boundaries, forbidden Lean
escapes and axiom-audit coverage. Then compile `IUT1` and `IUT1Audit` at the
pinned toolchain. A successful structural validation does not replace Lean
compilation or semantic review.

## Comparator and scope ceiling

[`comparison-with-takkun.md`](foundations/comparison-with-takkun.md) and
[`evidence/takkun-benchmark.json`](../evidence/takkun-benchmark.json) summarize
the complete 74-file static inventory of the pinned Takkun commit. Takkun is
globally broader. This library's demonstrated advantage is restricted to
auditability, explanation and adversarial verification in the shared finite
coordinate microdomain.

No artifact in this catalog formalizes IUT I as a whole, geometric
poly-actions, any part of IUT II, the IUT III 3.11→3.12 transition, Szpiro or
abc.
