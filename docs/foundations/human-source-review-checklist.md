# Pending expert human source review

Source navigation, paraphrase drafting and anchor checking for this release were
assisted by AI agents. The recorded source-anchor result is a scoped,
role-separated process review. It is not an expert human review. Its accurate
status is
`AI_ASSISTED_SOURCE_REVIEW_COMPLETE; HUMAN_EXPERT_SOURCE_REVIEW_PENDING`.

This disclosure does not erase an existing workflow result. It prevents that
result from being promoted into a different epistemic category. The checklist's
machine-readable counterpart is
[`evidence/human-source-review-checklist.json`](../../evidence/human-source-review-checklist.json).

## Reviewer record

For every row, a human reviewer must record name, relevant competence, UTC date,
the exact edition or PDF consulted, `source_id`, printed-page localizer, verdict
`HUMAN_PASS` or `HUMAN_NO_GO`, notes and conflicts of interest. AI output may
support the record but must never populate the `human_reviewer` field.

| ID | Source locator | Human question | Discriminating rejection test | Status |
|---|---|---|---|---|
| HSR-01 | IUT I §I1, printed pp. 3–4 | Confirm the parameters and groups, and whether poly-actions retain arithmetic or geometric provenance through automorphism subquotients. | Reject an ordinary action with neither subquotient nor source provenance. | `PENDING_HUMAN_EXPERT_REVIEW` |
| HSR-02 | IUT I §0, printed pp. 33–34 | Confirm poly-morphism as a collection, the isomorphism/automorphism/full variants, and pairwise composition without multiplicity. | A two-arrow collection is not either selected singleton. | `PENDING_HUMAN_EXPERT_REVIEW` |
| HSR-03 | IUT I §4, printed pp. 98–100 | Confirm multiplicative labels, capsules, the collections `β ∘ φ ∘ α`, automorphism quotients and poly-automorphism action. | This context does not establish the additive T05 model; cardinality survives deleting categorical data. | `PENDING_HUMAN_EXPERT_REVIEW` |
| HSR-04 | IUT I Definition 6.1(i), printed p. 155 | Confirm the distinct group, torsor, chart orbit and transformations `z ↦ ±z + λ`. | Reject identification with an ordinary torsor under the whole affine group. | `PENDING_HUMAN_EXPERT_REVIEW` |
| HSR-05 | IUT I Example 6.3(ii), printed pp. 161–162 | Confirm the indexed poly-automorphisms, source/target poly-actions and equivariance of the poly-morphism. | An ordinary affine action survives erasure of the indexed categorical data. | `PENDING_HUMAN_EXPERT_REVIEW` |
| HSR-06 | IUT I Definition 6.4, printed pp. 162–163 | Confirm the bridge as poly-morphism, indexed capsule, sign quotient, constituent morphisms and compatibility. | Reject the claim that T01–T11 construct this geometric object. | `PENDING_HUMAN_EXPERT_REVIEW` |

## Closure rule

`HUMAN_SOURCE_REVIEW_COMPLETE` may be issued only after all six rows have an
explicit signed human verdict. A `HUMAN_NO_GO` does not automatically revoke a
kernel result: it blocks only the dependent source-fidelity claim or promotion.
No result here changes `promotion=false`, `gate_transfer_allowed=false` or
`NO_GO_GEOMETRIC_CURRENT_T01_T11`.
