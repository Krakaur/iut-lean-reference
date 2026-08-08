# Release status

Current corrective version: `0.1.0-rc2`

Immutable historical prerelease: `v0.1.0-rc1` at commit
`2635ec15045a2880810d15984337bb7c07ef842f`, with release-manifest SHA-256
`47dbdef02930bc2e0d1ae8a9513ae597122f0d34ddd324a3d733464809409ca4`
and 79 entries.

Formal scope: the T01--T08 core of unit `IUT1-I1-SYM-001`, together with the
T09--T11 non-geometric subgroup/comparison/regression closure.

Current evidence:

- T01--T04: independently reviewed semantic, kernel, fidelity and cold-replication PASS.
- T05a--T05d: independently reviewed semantic, kernel, fidelity and cold-replication PASS.
- T06--T08: `SEMANTIC_PASS`, `KERNEL_PASS`, `FIDELITY_PASS` and
  `COLD_REPLICATION_PASS`, each issued separately; P1=P2=P3=0.
- T09--T11: `SEMANTIC_PASS`, `KERNEL_PASS`, `FIDELITY_PASS` and
  `COLD_REPLICATION_PASS`, each issued separately; P1=P2=P3=0.
- APP01: `SEMANTIC_PASS`, `KERNEL_PASS`, `FIDELITY_PASS` and
  `COLD_REPLICATION_PASS`, each issued separately; P1=P2=P3=0. The utility and
  whole-package gates remain separate.
- PA01--PA06: source anchors `PASS_INDEPENDENT_SOURCE_ANCHORS_R3`, followed by
  separate `SEMANTIC_PASS`, `KERNEL_PASS`, `FIDELITY_PASS` and
  `COLD_REPLICATION_PASS`; P1=P2=P3=0. The status remains
  `NO_GO_GEOMETRIC_CURRENT_T01_T11`.
- Public-package audit: `PASS_FROZEN_LOCAL_CANDIDATE`; utility `PASS`;
  scope-aligned quality `PASS_SCOPE_ALIGNED`; P1=P2=P3=0 after an independent
  repair-delta review. These are historical results for named manifests and
  unchanged scientific bytes, not a transferred PASS for the rc2 package.
- Independent public candidate: T01--T11, APP01 and PA01--PA06 are formalized
  and distributed as candidate material with their existing byte-specific
  records.
- Canonical incorporation: `NOT_PERFORMED`; the canonical
  `IUT1-I1-SYM-001` ledger remains closed at T05 and records
  `promotion=false`. T06--T11, APP01 and PA01--PA06 are not incorporated there.
- Human source review: `PENDING_SIX_RANGES`. Existing anchor review was
  AI-assisted and independent by workflow role, not expert human review.
- Release assurance: the public repository itself is checked against the exact
  16-module, 68-public-declaration and 92-axiom-query inventories. Compilation,
  bundled-kernel replay, axiom equality and fidelity remain separate results.
- GitHub publication: the owner authorized the public repository
  `Krakaur/iut-lean-reference`, Apache-2.0 for software and CC BY 4.0 for
  documentation/data. Publication metadata received independent PASS; remote
  availability is an operational postcondition and does not modify any mathematical gate.

No PASS is transferred among candidate verification, canonical incorporation,
geometric scope, LANA affiliation or human source review. The rc2 in-tree
record remains `RC2_PENDING_EXTERNAL_ATTESTATION`; only the detached release
asset may bind the immutable rc2 commit, tree, manifest and CI runs. That
attestation is provenance evidence, not a new scientific PASS.

The release is a reference library for finite algebraic models, adversarial
examples, an algebraic poly-morphism prototype and their source mapping. It is
not a release of a complete IUT formalization or a geometric poly-action.
No error was identified within the inspected scope; bounded semantic, kernel,
fidelity and replication PASS records exist for specific historical bytes.
