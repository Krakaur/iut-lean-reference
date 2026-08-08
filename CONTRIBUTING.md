# Contributing scientific feedback

This repository welcomes precise review of its bounded IUT-I reference layer.
Feedback is most useful when it identifies the affected target (`T01`--`T11`,
`APP01` or `PA01`--`PA06`) and distinguishes the layer under review.

## Review categories

1. **Source fidelity:** give the `source_id`, printed-page locator, disputed
   reading and a source-grounded alternative.
2. **Semantic fidelity:** state the informal claim, the Lean type and a finite
   or conceptual discriminating test.
3. **Lean correctness or design:** identify the declaration, the issue and a
   compiling minimal example when possible.
4. **Pedagogy and retrieval:** identify the reader or machine task, the failed
   navigation path and a concrete improvement.

Please do not report a compiler success as evidence of source fidelity, or a
source citation as evidence that Lean checked the formalization. The semantic,
kernel, fidelity and replication gates remain separate.

## Scope boundary

The repository does not claim to formalize IUT I, geometric poly-actions, the
IUT III 3.11-to-3.12 transition, Szpiro or abc. A proposal that crosses one of
these boundaries must supply a new source contract and independent review; it
cannot inherit a PASS from the finite algebraic unit.

## AI-assisted development disclosure

AI systems assisted corpus navigation, drafting, adversarial interpretation,
Lean development and packaging. This assistance is disclosed because generated
text or code is not itself scientific validation. Public mathematical claims
are tied to source records and discriminating tests; Lean declarations were
kernel checked; the review gates were issued independently. Expert human review
of source interpretation and interface usefulness remains welcome.

Open a GitHub issue with a descriptive title. For security-sensitive matters,
do not publish credentials, private corpus material or copyrighted source PDFs.
