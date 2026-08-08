# Machine-readable learning and retrieval layer

This directory is designed for systems that need more than theorem text.

`claims.jsonl` is the primary retrieval table. Every row retains the source,
localizer, epistemic status, Lean declaration, dependencies, discriminator and
verified gates. `examples.jsonl` contains both positive examples and mutations
that should be rejected. `anti_patterns.jsonl` records recurrent semantic
collapses. `schema.json` describes the required fields.

`applications.jsonl` is separate because an application can inherit a source
context without becoming a source claim. Its records use
`application-schema.json` and state the operational task, full positive and
negative tests, and narrower interpretation boundary.

`use_cases.jsonl` records how a LANA/IUT researcher or retrieval system can use
the material. These are workflow claims, not mathematical theorems or assertions
of compatibility with an external codebase.

`polyaction_checkpoints.jsonl` adds one record for every T01–T11 page. Each row
contains its source tuple, precise role, finite example, Lean declarations,
discriminator and scientific boundary. The companion
`polyaction-schema.json` makes omission of those fields machine-detectable.

The current claim sequence is T01--T11. T01--T08 are the requested core;
T09--T11 close subgroup structure, convention comparison and typed regression
coverage without introducing a new geometric source claim.

## Recommended retrieval unit

Retrieve a claim together with:

1. its theorem page under `docs/theorems`;
2. its direct dependencies from `claims.jsonl`;
3. at least one positive and one adversarial example;
4. the corresponding Lean declaration;
5. its evidence-layer statuses.

For a poly-action query, also retrieve the matching row from
`polyaction_checkpoints.jsonl`, the
[`source-and-boundary`](../docs/poly-actions/source-and-boundary.md) page and
the [`algebraic prototype`](../docs/poly-actions/algebraic-prototype.md) page.
The negative boundary is part of the retrieval unit.

Do not train or answer from a bare theorem name. A model that sees only
`cardinality = 2*l` may conflate the affine group with the additive quotient or
infer a geometric realization that was never formalized.

## Epistemic discipline

`source_id`, `localizers` and `epistemic_status` record the source-facing layer.
The four entries under `gates` — `semantic`, `kernel`, `fidelity` and
`replication` — record distinct review results. These fields are not
interchangeable. The `does_not_establish` field should be treated as part of the
claim, not as optional commentary.

## Copyright boundary

The dataset contains project-authored paraphrases and public source links. It
does not contain the source PDFs or long copied passages.
