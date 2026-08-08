# Release status

Current version: `0.1.0-rc1`

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
  repair-delta review. No canonical promotion is inferred from this gate.
- Canonical promotion: not performed.
- GitHub publication: the owner authorized the public repository
  `Krakaur/iut-lean-reference`, Apache-2.0 for software and CC BY 4.0 for
  documentation/data. Publication metadata received independent PASS; remote
  availability is an operational postcondition and does not modify any mathematical gate.

The release is a reference library for finite algebraic models, adversarial
examples, an algebraic poly-morphism prototype and their source mapping. It is
not a release of a complete IUT formalization or a geometric poly-action.
