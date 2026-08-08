# APP01 — exhaustive convention auditor

| Field | Value |
|---|---|
| Inherited `source_id` | `SRC-OFFICIAL-7360E3ED27C235B5` |
| Inherited localizers | §I1, printed p. 3; Definition 6.1(i), printed p. 155 |
| Epistemic status | `METHODOLOGICAL_APPLICATION_OF_DERIVED_COORDINATE_MODEL` |
| Lean module | `IUT1.Applications.ConventionAudit` |
| Dependencies | T06, T07 and T10 |
| Semantic gate | `PASS` |
| Verified gates | `SEMANTIC_PASS`, `KERNEL_PASS`, `FIDELITY_PASS`, `COLD_REPLICATION_PASS` |

## The task it performs

APP01 accepts any raw function

```text
SignedAffine l → DihedralGroup l
```

proposed as a coordinate convention. It evaluates every signed-affine element
and every coordinate in the finite model, comparing the independently defined
dihedral action with the visible signed-affine action. The Boolean answer is
connected to its universal proposition by `APP01_C01_check_spec`; exhaustive
agreement is proved, not stored in the candidate.

At `l=5`, the canonical convention maps `(a,true)` to `sr(-a)` and passes. The
rival convention maps it to `sr(a)` and fails. The explicit failure witness is
`g=(1,true)`, `z=2`: the rival action returns two, while `g.act z` returns four.

## Why this is an application

The checker is parameterized by an arbitrary candidate and performs a reusable
verification task over the full finite domain. It is therefore distinct from a
single theorem-specific example. A downstream parser, refactor or generated
encoding can be supplied to the same checker and must satisfy the same action
contract.

## Interpretation boundary

A `true` result certifies only equality of the two selected actions at every
enumerated input. It does not by itself show that the raw candidate is a group
homomorphism, injective, surjective or an equivalence. It also does not test a
geometric realization, cusp action or poly-action.

The source citation is inherited context, not evidence that IUT I defines this
software checker. APP01 is project-created methodology over the reviewed
coordinate model.

The independent review freshly compiled the application module, its axiom
audit and both public roots with zero errors and warnings. Its eight axiom
reports contain only the standard logical constants recorded in
`evidence/gates.json`. This application PASS is not a whole-package or utility
PASS.
