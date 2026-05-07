# Convention Lock

Status: seed. No new Program B numerical result is accepted until the relevant convention row is filled with an exact value, formula, matrix ordering, or reproduction command.

## Rule

A computation that depends on an undeclared convention is not evidence. It may be kept as scratch work, but it cannot be cited as a program result.

## Canonical convention table

| Area | Convention | Program B status |
| --- | --- | --- |
| Group | SU(2) unless explicitly marked U(1) gate or abelian control | Locked |
| Representation label | Use `n = 2j` in file names and tables; display `j = n/2` where physics notation is clearer | Locked |
| Haar normalization | Haar probability measure: integral of 1 over the compact group is 1 | Locked |
| Character normalization | Characters are class functions. Inner products use Haar probability normalization | Pending exact fixture |
| Wigner phase | Must be declared before Phi_111 reproduction is accepted | Pending |
| Wigner matrix ordering | Must declare row/column ordering for `m` indices and any real/complex basis conversion | Pending |
| Scalar-coupled invariant basis | Basis order must be listed for every tested cutoff | Pending |
| Wilson coefficient convention | Must specify coefficient extraction, sign, beta/coupling parameter, and normalization | Pending |
| Topology scalar | Product-kernel topology factor must be declared as `1 / A^0_00` or revised with proof | Pending |
| Product-kernel theorem scope | Independent plaquette variables, class-function factors, and a single central Haar projection | Locked as Program A regression scope |
| Shared-edge kernel scope | Must state which edges are shared, which variables are no longer independent, and which integrals couple them | Pending |

## Labeling discipline

Use `Program A` for frozen product-kernel source material. Use `Program B` for shared-edge work. Do not use `v4.2`, `Part Four`, or tranche language for Program B.

Use `gate:` for inherited checks, `regression:` for Program A invariants, `witness:` for a Program B nonseparability test, and `catalog:` for term/value cross-reference entries.

## Required command declaration

Every accepted value must include:

```text
command: <exact command from repo root>
inputs: <files, seeds, cutoff, beta/coupling, representation labels>
outputs: <value, tolerance, artifact path>
convention dependencies: <rows from this file>
```

## No-claim statement

This program studies finite-cutoff computational and representation-theoretic structures. It does not address the continuum Yang-Mills existence and mass-gap problem, which requires uniformity in cutoff, volume, and coupling that this program does not establish.

This statement is fixed. Do not expand it as a substitute for precision in the mathematics or code.