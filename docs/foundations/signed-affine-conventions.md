# Signed-affine conventions

Let a pair `(a,s)` act on `z` by

```text
act (a,s) z = signAct s z + a,
```

where `false` is positive and `true` is negative. If multiplication follows
function composition, `g*h` applies `h` first and then `g`. For
`g=(a,s)` and `h=(b,t)`, this gives

```text
act g (act h z)
= signAct s (signAct t z + b) + a
= signAct (xor s t) z + signAct s b + a.
```

Since addition in `ZMod l` is commutative, the resulting coordinate law is

```text
(a,s) * (b,t) = (a + signAct s b, xor s t).
```

This derivation matters. If the translation coordinate were `a+b`, the
construction would be a direct product and the negative sign would fail to act
on the second translation.

## The five-element mutation test

Take `g=(1,true)` and `h=(2,false)` modulo five. The contracted law gives
`1-2=4`, hence `g*h=(4,true)`. A direct product gives translation `3`.

At `z=3`, applying `h` gives zero and applying `g` next gives one. Thus both
`act (g*h) 3` and `act g (act h 3)` equal one. Reversing the composition order
produces a different value. These small examples are semantic mutation tests,
not substitutes for the generic proofs.

## Why no dihedral abbreviation is used

The abstract group is isomorphic to a dihedral group, and Mathlib already knows
the latter's laws and cardinality. Defining `SignedAffine l` as a dihedral
abbreviation would conceal which coordinate is translated, how the sign acts,
and which composition convention is used. The project therefore builds its own
pair carrier and postpones the explicit dihedral isomorphism to a later target.
