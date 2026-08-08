# Source and evidence policy

## Primary source

The T01--T08 source binding uses:

- `source_id`: `SRC-OFFICIAL-7360E3ED27C235B5`
- title: *Inter-universal Teichmüller Theory I: Construction of Hodge Theaters*
- author: Shinichi Mochizuki
- official URL: <https://www.kurims.kyoto-u.ac.jp/~motizuki/Inter-universal%20Teichmuller%20Theory%20I.pdf>
- source SHA-256: `7360e3ed27c235b5497a0743d3ed1646fbb97688547d16b7c784fc7f127f1f03`

The PDF is linked, not redistributed.

## Localizers used in this release

- §I1, printed p. 3: finite parameters, multiplicative quotient and signed
  semidirect-product notation.
- Definition 6.1(i), printed p. 155: sign-compatible chart orbits and affine
  maps of the form `z ↦ ±z + λ`.
- Definition 6.4(i), printed p. 162: quotient-index role used by T05.

Printed-page numbers are recorded separately from physical PDF page numbers.
The two T06--T08 source anchors were also visually checked in the authoritative
PDF, rather than accepted from extracted text alone.

## Evidence layers

`SOURCE_EXPLICIT` concerns what the document says. `SEMANTIC_PASS` concerns
whether a proposed Lean statement captures the contracted meaning.
`KERNEL_PASS` concerns Lean acceptance of exact bytes. `FIDELITY_PASS` compares
those bytes back to the source contract. `COLD_REPLICATION_PASS` concerns a new
isolated run. No status is inherited across layers.

## Quotation and redistribution

The repository uses short mathematical paraphrases and public links. It does
not include the original PDF, long extracts, corpus indices, or local acquisition
metadata. A public educational library does not require republishing copyrighted
source bytes.

## Priority language

T01--T08 are not advertised as new mathematics. T08 has direct IUT-oriented
Lean prior art in `Takkun-kohinata/IUT_LEAN`; Mathlib supplies generic
semidirect-product and dihedral infrastructure. A bounded search did not locate
the exact T06--T07 pair-presentation-plus-discriminants package. That result is
reported only as `NOT_FOUND_WITHIN_AUDITED_PUBLIC_SCOPE`.
