# Content space model v0.1

## Purpose

A content space is the bounded stewardship and publication surface for a family of related reusable knowledge assets.

## Required properties

A content space SHOULD define:
- stable identifier
- display name
- owning steward or team
- allowed publication scope
- supported asset classes
- related domains and tasks
- promotion policy reference

## Example

A content space such as `content-space:identity-auth` may include:
- authentication runbooks
- identity troubleshooting documents
- canonical support answers
- policy-linked operational guidance

## Rule

Promotion should always target an explicit content space. Assets without a valid destination content space should not be promoted into canonical status.

## Consequence

The content space becomes the durable governance container above individual assets and below the broader platform taxonomy.
