# Interpretive Gates

Status: seed. These gates decide whether inherited Program A values can be used inside Program B. They are not optional validation decoration.

## Gate rule

A gate is closed only when it includes:

```text
command: exact repo-root command
input files: explicit paths
conventions: rows from CONVENTIONS.md
expected value: exact value or symbolic zero
accepted tolerance: explicit numeric tolerance
artifact path: file produced by the command
review status: open | reproduced | accepted | rejected
```

A gate without an exact command is open.

## Gate 1: U(1) null

### Purpose

The U(1) null separates genuine nonabelian SU(2) content from representation-machinery artifact. If the abelian control produces a nonzero `l = 1` channel under the declared convention, the prior relative-orientation interpretation must be revised before Program B uses it.

### Required result

The declared abelian control must produce a null result for the relevant `l = 1` channel. The exact symbolic form and numeric tolerance remain pending until the implementation repo lands.

### Closure record

```text
status: open
command: pending
expected value: pending
artifact: pending
blocking: yes
```

## Gate 2: Phi_111 Wigner reproduction

### Purpose

Program A used a Phi_111 / relative-orientation value derived from a quaternion/Haar integral. Program B must reproduce that value through the Wigner R-table path in the declared convention before treating it as a stable input.

### Required result

The Wigner R-table implementation must reproduce the Program A channel value in the declared phase, ordering, and Haar normalization. If the reproduction disagrees, the K3/product regressions become suspect and must be recomputed before shared-edge work proceeds.

### Closure record

```text
status: open
command: pending
expected value: A^{l=1}_{11} = 0.284925049326... pending full precision and convention declaration
artifact: pending
blocking: yes
```

## Gate 3: Product-kernel regression

### Purpose

The product-kernel theorem becomes a regression boundary. Program B does not extend this theorem; it uses the theorem to detect whether new work has escaped the previous separable structure.

### Required result

A test must verify that the old product-kernel scope still factors under independent plaquette variables, class-function factors, and a single central Haar projection.

### Closure record

```text
status: open
command: pending
expected value: product theorem fixture set pending
artifact: pending
blocking: yes for claims that compare against Program A
```

## Gate 4: Shared-edge witness pre-registration

### Purpose

Program B must not declare victory because a coefficient is nonzero. It must pre-register a coefficient or observable whose product-kernel form would be forced to factor, then show that the shared-edge value cannot be represented that way under declared admissible basis changes.

### Closure record

```text
status: open
command: pending
expected value: not applicable until witness is declared
artifact: pending
blocking: yes for nonseparability claims
```

## Gate outcome categories

- `open`: missing command, value, convention, or artifact.
- `reproduced`: command returns expected value but review is not complete.
- `accepted`: reproduced, reviewed, and added to catalog.
- `rejected`: result disagrees with inherited value or convention is invalid.
- `superseded`: replaced by a stricter gate with explicit rationale.

## Gate discipline

A failed gate is not a reason to add disclaimers. It is a reason to revise the mathematics, conventions, or implementation.