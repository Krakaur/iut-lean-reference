# Quality and utility gates

The library treats usefulness as an auditable property. A large repository is
not necessarily useful, and a correct Lean theorem is not necessarily faithful
to the mathematical source that motivated its name.

## Rigor before scale

Every source-dependent claim retains a `source_id`, exact localizer, epistemic
status and, where another interpretation is plausible, a discriminating test.
Source verification, semantic review, kernel acceptance, source-to-type
fidelity, cold replication and publication are separate gates.

Every released Lean file must compile at the pinned versions with zero errors,
zero warnings and no active proof escape. Exported theorems and nontrivial
project instances receive explicit axiom reports. Synthetic examples are
labelled as synthetic; they are not evidence that a geometric IUT object has
been constructed.

## What every theorem page must answer

A useful page tells a reader:

- the mathematical statement and its exact Lean type;
- the primary-source role and what is merely derived;
- the proof architecture without requiring Lean fluency;
- a worked positive example;
- the nearest plausible wrong statement and a test that rejects it;
- the types that must not be identified;
- what the theorem does not establish;
- where to find the machine-readable claim and replication evidence.

## Comparison policy

The comparison target is
[Takkun-kohinata/IUT_LEAN](https://github.com/Takkun-kohinata/IUT_LEAN) at
commit `9d56c46db270896876a83a484f857a7186a2a8bf`. Comparisons report both
denominators and distinguish IUT I from later papers and generic foundations.

The project may claim greater rigor or pedagogical utility only for a frozen,
scope-aligned slice supported by a reproducible benchmark. It may claim greater
global extent only after exceeding the comparison repository in audited
content, not merely in lines or files. A semantic mismatch cannot be offset by
more code.
