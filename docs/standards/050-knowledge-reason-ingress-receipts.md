# 050 — knowledge-reason ingress receipts

This note defines the smallest upstream documentation surface for governed claim ingress into `knowledge-reason`.

Core assertions:
- a carrier must declare a scope reference
- a receipt must bind to that same scope reference
- receipt freshness and witness threshold are checked before reasoning
- reasoning and governance remain separate lanes

This branch intentionally keeps the live repo delta small:
- one receipt verification schema
- one Academy routing payload schema
- this standards note

The larger runtime and trust-evolution specimen remains attached in sandbox artifacts and is intended for staged follow-on PRs.
