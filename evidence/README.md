# Verification evidence

This directory gives a compact, public-safe summary of the local evidence. It
does not redistribute the research corpus or internal absolute-path logs.

`artifacts.json` freezes the byte identities of the exported core and audit
files. `gates.json` records the result of each independent gate.
`sources.json` lists public source access points and localizers without copying
the source documents. `takkun-benchmark.json` freezes the complete static
comparison denominator and its separate kernel/semantic limitations.
`novelty.json` separates established mathematics, bounded methodological
distinctiveness and the still-gated scope-aligned quality claim.
`manifest-chain.json` reconciles historical manifests, Git/CI deltas and rc1
without self-attesting rc2. `verification-policy.json`,
`module-declaration-inventory.json` and `axiom-whitelist.json` define the
release-specific 16/68/92 assurance campaign.
`human-source-review-checklist.json` records six ranges whose AI-assisted
process review must not be presented as expert human review.

The current in-tree status is `RC2_PENDING_EXTERNAL_ATTESTATION`. A detached
release asset, not this directory, must bind the immutable rc2 commit, tree,
manifest and CI runs.


## Independent core results

The independent reviews for T06--T08 and T09--T11 each returned:

- `SEMANTIC_PASS`
- `KERNEL_PASS`
- `FIDELITY_PASS`
- `COLD_REPLICATION_PASS`
- P1=0, P2=0, P3=0

The cold runs compiled the four source-facing modules and their axiom audits
serially with Lean 4.28.0 and Mathlib commit
`8f9d9cff6bd728b17a24e163c9402775d9e6a365`. All stages returned exit code zero
with zero error diagnostics. The printed axiom reports contained only the
standard Mathlib-facing axioms recorded in `gates.json`; no project axiom was
introduced.

No canonical promotion, geometric realization or whole-IUT-I authorization
followed from those results. The complete public package receives a distinct
release gate; it cannot borrow any of the core PASS labels.

## Independent algebraic poly-action prototype results

PA01–PA06 separately received `SEMANTIC_PASS`, `KERNEL_PASS`,
`FIDELITY_PASS` and `COLD_REPLICATION_PASS`, with P1=P2=P3=0. The source-anchor
review also closed at `PASS_INDEPENDENT_SOURCE_ANCHORS_R3`. The finite positive
example `IUT1.PA06_signedAffine5_two_arrows_over_identity` retains two arrows
over one label, while
`IUT1.PolyMorphism.PA01_bool_two_map_ne_singletons` rejects singleton
selection. The four cold `.olean` hashes match the producer outputs recorded in
`gates.json`.

These PASS values apply only to the algebraic interface and exact candidate
bytes in `artifacts.json`. `NO_GO_GEOMETRIC_CURRENT_T01_T11` remains in force;
no PASS is transferred to source geometric poly-actions.
