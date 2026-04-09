# 051 — knowledge-reason routing examples

This note ties the small routing examples in this branch back to the already-landed receipt-verification example and the Academy bounded contexts.

Reading order for this branch:
1. `examples/slash_topic_receipt_verification.accept.example.json`
2. `examples/academy_routing_payload.accept.example.json`
3. `examples/academy_routing_payload.review_queue.example.json`

Interpretation:
- the accepted routing payload targets `AtlasCodex` in the `canon-candidate` lane
- the review-queue routing payload targets `OracleOfDelphi` in the `review-queue` lane
- both examples assume receipt verification has already succeeded and reference the same receipt-verification example

This note is intentionally narrow. It documents the live example surfaces already present on the branch without claiming the fuller routing schema or full runtime contract has landed yet.
