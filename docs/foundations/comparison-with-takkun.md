# Relationship to Takkun-kohinata/IUT_LEAN

## What the antecedent already provides

The audited Takkun commit
`9d56c46db270896876a83a484f857a7186a2a8bf`, tree
`4751d8ce2d96dfd40b1d1cb574487fdbae8727d5`, is substantial. A complete static
inventory covered all 74 versioned files: 68 Lean modules and six
documentation/infrastructure files, totalling 11,541 physical lines. It found
17 IUT-I files, 34 IUT-II--IV files, 16 generic-foundation files and seven
documentation/infrastructure files. These are two different partitions: the
seven-file architectural documentation/infrastructure bucket includes the root
`IutLean.lean`, which is also one of the 68 Lean files in the file-type count.
For the present microdomain,
`IutLean/Combinatorics/Fl.lean` defines a finite-field layer, models the
sign-affine symmetry by `DihedralGroup l`, and proves cardinality `2*l`.
`IutLean/HodgeTheater/Symmetry.lean` proves simple transitivity facts for
translation actions.

Those results are prior art. This library does not present T08 as the first
IUT-oriented Lean cardinal proof.

## Different objective

The present repository optimizes for auditability and teaching rather than
module count. It uses English throughout, gives one page per Txx, translates
every target for non-specialists, exposes the affine coordinate law instead of
abbreviating it to a dihedral group, and packages machine-readable evidence for
AI retrieval.

Its distinctive fields are:

- primary `source_id` and printed-page localizer;
- epistemic status of the source-to-model step;
- exact Lean declaration and dependency list;
- an adversarial interpretation and a discriminating example;
- a per-T poly-action role with an executable interface checkpoint;
- separate semantic, kernel, fidelity and replication statuses;
- explicit statements of what each theorem does not establish.

For example, `IUT1.PolyMorphism.PA01_bool_two_map_ne_singletons` rejects
selection of one map from a two-arrow collection, and
`IUT1.PA06_signedAffine5_two_arrows_over_identity` retains two lifts over one
quotient label. These declarations add a useful semantic regression surface;
they are not claimed to be mathematically novel or to formalize geometric
poly-actions.

## Audit-denominator comparison

The Takkun inventory found 737 declaration heads and 717 public explicit
declaration candidates. Its archived kernel evidence probes 12 of those 717;
therefore kernel coverage remains `PARTIAL_FAIL_CLOSED`, irrespective of the
absence of active occurrences of `sorry`, `admit`, axiom declarations,
`opaque`, `unsafe`, `native_decide` and `Classical.choice` in the static scan.
Its semantic audit
also remains `PARTIAL_FAIL_CLOSED`, with 13 recorded flags (nine high and four
medium), including underconstrained interfaces, shifted proof obligations and
degenerate witnesses. These are audit results, not an assertion that every
unprobed declaration is defective.

Release `0.1.0-rc1` is deeper than the antecedent only on the narrow finite
coordinate slice and its evidence architecture. It supplies claim-level source
locators, separated semantic/kernel/fidelity/replication gates, explicit rival
models, per-target poly-action checkpoints, complete public-theorem axiom
requests, and machine-readable records.
Takkun remains globally much more extensive, so this project must not yet be
advertised as globally broader or as a formalization of IUT I. The relevant
superiority claim is scope-aligned: greater auditability and pedagogical utility
for the shared finite-symmetry microdomain.

## Reproducible comparison rule

Counts are frozen to the commit above. A build PASS, a static escape scan, an
axiom report and a semantic-fidelity judgment are different observations and
are never transferred across columns. Future comparisons must declare both the
file denominator and the declaration denominator, revalidate the upstream HEAD,
and preserve unresolved semantic findings rather than converting missing tests
into PASS.

## Why not copy the antecedent

The audited Takkun commit had no detected license file, so its Lean sources are
not copied. Mathematical ideas and public declaration names are cited as prior
art. The code in this repository is independently developed and verified.
