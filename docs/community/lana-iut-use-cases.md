# Use by the LANA and IUT research communities

Project LANA means “Lean for ANAbelian geometry.” Its official goals are to
build a Lean library for major results in anabelian geometry and to formalize
and verify IUT theory. Its public statements also emphasize neutrality,
explicitly separating what is understood from what remains unresolved. See the
[Project LANA site](https://anabelian.org/), the
[ZEN Mathematics Center announcement](https://zen.ac.jp/news/zmcpostevent0331e)
and the [July 2026 interim-report announcement](https://zen.ac.jp/news/zmcpostevent0717).

This reference library is designed as a small upstream research instrument for
that program. It is not an official LANA artifact and does not infer compatibility
with any unpublished or changing LANA API.

## Concrete uses

### Source-to-type review

Input: a phrase or construction from IUT I. Output: a record containing the
primary `source_id`, printed-page localizer, epistemic status, Lean type,
dependencies, discriminator and non-claims. This helps reviewers detect when a
formal name has acquired more geometric meaning than its type supports.

Example: T08 returns the cardinality of `SignedAffine l`. Its record explicitly
rejects identification with the additive sign quotient or a geometric
automorphism group. The compiled separation test is
`IUT1.T08_audit_l5_ne_signOrbit_card`.

### Adversarial interface testing

Input: two plausible formal interpretations. Output: a finite example that
changes value, type or Boolean verification result. This converts interpretive
disagreement into a reviewable obligation.

Example: APP01 checks every group element and coordinate at `l=5`. The canonical
dihedral convention passes, while the mutation `(a,true) ↦ sr(a)` fails and has
the explicit witness `g=(1,true)`, `z=2`.

### Formalization handoff

Input: an independently approved semantic contract. Output: a commented Lean
module, axiom audit, reproducible compilation recipe and cold-replication
record. This permits a domain specialist, Lean engineer and independent reviewer
to work on different layers without transferring a PASS.

Example: T10 first constructs the signed-affine and dihedral presentations
independently, then proves action compatibility. The comparison is not made true
by transporting the action through the desired equivalence.

### AI retrieval and training

Input: a target ID such as `T05` or `APP01`. Output: the theorem/application
page, direct dependencies, positive example, adversarial example, Lean
declarations and gate evidence. Records are English and avoid source-PDF
redistribution.

Example: retrieving T05 brings the distinguished chart orbit and its
multiplication-by-two countermodel together. A model trained only on the
cardinality formula would miss that semantic restriction.

### Research-gap ledger

Input: a desired geometric or later-paper conclusion. Output: a list of missing
typed dependencies rather than a suggestive theorem name. This is useful for
planning without treating a roadmap as a result.

Example: the IUT III 3.11→3.12 issue identified in LANA's July 2026 public
announcement remains outside this release. The present library can supply
evidence conventions and finite regression infrastructure, but it supplies no
mathematical bridge to that transition.

## Per-target utility contract

Every T page must answer four practical questions for a LANA/IUT reader:

1. What source ambiguity or type distinction does this target control?
2. What finite example exposes the nearest wrong interpretation?
3. Which Lean declaration can be imported or tested?
4. How does the target interact with the poly-action boundary: prerequisite,
   algebraic prototype, discriminator or no direct claim?

A page is incomplete if it supplies prose without a Lean witness, Lean without
a mathematical example, or an example without an epistemic boundary.

## Worked poly-action retrieval path

Suppose a reviewer begins with the IUT I phrase “collection of morphisms.” The
source route is `source_id=SRC-OFFICIAL-7360E3ED27C235B5`, section 0, printed
pp. 33–34, with status `SOURCE_EXPLICIT_DEFINITION`. The
[source map](../poly-actions/source-and-boundary.md) separates that definition
from the later automorphism-subquotient and bridge contexts.

The semantic contract is represented publicly by the PA01–PA06 division in the
[prototype guide](../poly-actions/algebraic-prototype.md). Its positive Lean
example is `IUT1.PolyMorphism.PA02_bool_two_map_self_comp`: pairwise composition
retains both Boolean arrows. Its adversarial example is
`IUT1.PolyMorphism.PA01_bool_two_map_ne_singletons`: selecting either arrow
changes the collection. The replication surface is the module
`src/IUT1/Applications/PolyMorphismPrototype.lean`, its matching axiom audit
and the aggregate `test/IUT1Audit.lean` import.

For the phrase “automorphism subquotient,” the route continues through PA03–PA06.
`IUT1.AlgebraicPolyActionPrototype.PA04_arrows_mul` proves exact composition of
complete fibers, while `IUT1.PA06_signedAffine5_two_arrows_over_identity`
exhibits two arrows over one label. The retrieval result must also return
`NO_GO_GEOMETRIC_CURRENT_T01_T11`; otherwise it has lost the distinction most
important to source fidelity.

## Integration policy

Reusable contributions should be small and dependency-transparent. Core source
modules, pedagogical facades, applications and audits remain separate. Upstream
integration should occur through explicit imports or adapters, never by copying
an external project's unverified semantics into a local type alias.

Compatibility with a future LANA library requires a separate adapter contract,
versioned dependency and independent build. Until those exist, this package is
best described as a source-audited IUT-I reference and test corpus for the same
research community.
