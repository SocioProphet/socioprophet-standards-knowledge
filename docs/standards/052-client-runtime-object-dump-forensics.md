# Client Runtime Object Dump Forensics and Redaction v0.1

## 0. Status

Status: draft standard.

Scope: Knowledge Context handling of browser/client runtime object dumps, console captures, expanded DOM/Event objects, React/Vue/internal runtime graphs, source-card image-loader failures, and related diagnostic artifacts.

This document is intentionally defensive. It does not standardize any particular browser, framework, proprietary client, favicon endpoint, or telemetry provider.

## 1. Purpose

Client runtime dumps are deceptively dangerous. A user or agent can copy what appears to be a harmless console error and accidentally include:

- session cookies and authentication-adjacent browser state;
- relay email, account display name, model configuration, client identifiers, or telemetry session identifiers;
- page URLs, conversation IDs, build IDs, source-map paths, referrer data, and local document state;
- live DOM references, framework container internals, cyclic object references, and prototype-chain expansion;
- native Event objects that are logged by reference rather than safe serialized snapshots.

Knowledge Context systems MUST treat raw browser console/object dumps as sensitive until proven otherwise.

## 2. Observed pattern class

A representative class of failures is a native image `error` event paired with small metadata such as a cache key or query key. When the native `Event` object is expanded in browser developer tools, the inspector may traverse from the target element into attributes, owner document, framework root containers, framework fiber/work trees, abort controllers, DOM prototypes, and function prototypes.

The resulting paste may look like an extremely deep application object, but it is usually a live cyclic runtime graph rather than a normal JSON-like payload.

Implementations MUST distinguish:

- the triggering application event;
- the logger call site;
- the metadata payload intentionally emitted by the application;
- the developer-tool expansion artifact;
- the browser runtime graph accidentally exposed by recursive expansion.

## 3. Required first response

When a client runtime object dump is received, analysis systems MUST perform the following before deeper interpretation:

1. Classify the artifact as potentially secret-bearing.
2. Preserve the raw input only in a quarantined/private evidence store.
3. Generate a redacted working copy before broad analysis.
4. Identify and remove or mask cookie strings, auth metadata, account identifiers, relay emails, telemetry session IDs, page URLs, build IDs, sequence IDs, and source-map query strings.
5. Record that any derived summary is based on a sanitized copy.

The raw dump MUST NOT be redistributed into tickets, public PRs, model prompts, vector indexes, notebooks, or screenshots unless it has been redacted and reviewed.

## 4. Redaction requirements

A conforming redactor MUST remove or mask at least the following classes:

- `cookie:` fields and any semicolon-delimited cookie material;
- values whose names imply auth/session identity, including `auth`, `session`, `token`, `client-auth-info`, `puid`, `did`, `sid`, and similar variants;
- email addresses, relay addresses, display names, and avatar URLs;
- full page URLs that include private object IDs, conversation IDs, tenant IDs, or route IDs;
- client telemetry IDs, RUM IDs, source-map query strings, and build sequence values;
- private framework random suffixes such as generated React container suffixes when they are not needed for analysis;
- exact payloads that identify a private chat, user, workspace, or account.

A redactor SHOULD preserve structural tokens needed for forensic reasoning, for example:

- event type;
- element type;
- source host class, with private path/query redacted;
- property names;
- nesting shape;
- repeat counts;
- timestamps rounded or bucketed when precise values are unnecessary;
- source file basename and line/column if that does not expose private query data.

## 5. Runtime graph interpretation rules

Analysts MUST NOT assume that visual depth implies a deeply nested application payload.

Browser developer tools may expose live object identity references. A single logged `Event` object can lead to a graph shaped like:

```text
Event
-> target element
-> attributes / ownerDocument
-> framework root container
-> stateNode / containerInfo
-> ownerDocument again
-> framework alternate/work tree
-> cache / AbortController / AbortSignal
-> prototypes / Function.prototype
```

This is a graph with cycles and prototypes. It SHOULD be normalized as a node-edge graph, not as a recursively materialized tree.

The following fields are strong indicators of developer-tool/runtime expansion rather than intended application payload:

- `ownerDocument` leading back to the same document;
- generated framework container properties, for example `__reactContainer$...`;
- repeated `alternate`, `stateNode`, `containerInfo`, `memoizedState`, or lane fields;
- prototype objects and function built-ins such as `apply`, `bind`, `call`, `constructor`, `Function`, and `EventTargetPrototype`;
- large repeated blocks of DOM event handler slots such as `onclick`, `oninput`, `onwheel`, and similar properties.

## 6. Debugging requirements

Debugging SHOULD target the assignment or logging boundary, not deeper console expansion.

For image-loader failures, preferred capture points are:

- the point where `HTMLImageElement.src` is assigned;
- the creation site of a detached image element;
- the function that constructs the normalized image/cache key;
- a wrapper around `console.error` or the project logger that captures a stack before the native object is expanded;
- network panel evidence for the request outcome.

Analysts SHOULD avoid repeatedly expanding live browser objects after the first structural diagnosis. Further expansion increases noise and can expose more state without improving root-cause attribution.

## 7. Event logging controls

Runtime code SHOULD NOT log native browser `Event`, `Window`, `Document`, or DOM element objects directly to persistent telemetry or user-visible debug surfaces.

Instead, runtime code SHOULD log bounded records such as:

```json
{
  "kind": "ClientImageLoadFailure",
  "version": "0.1",
  "source_class": "favicon_or_source_card_image",
  "request_host": "example-redacted-host",
  "target_origin_class": "origin-only",
  "element": {
    "tag": "IMG",
    "is_connected": false,
    "decoding": "async"
  },
  "event": {
    "type": "error",
    "bubbles": false,
    "cancelable": false
  },
  "key": {
    "namespace": "imageData",
    "redacted_hash": "sha256:..."
  }
}
```

The exact schema above is illustrative. Implementations MAY define a stricter project-local schema, but MUST preserve the privacy and boundedness requirements.

## 8. Source-card and favicon guidance

If a product uses source-card or citation-card favicons, it SHOULD NOT treat a third-party favicon service as a hard reliability dependency.

Implementations SHOULD support:

- local fallback icons by domain class;
- bounded request fan-out;
- per-origin deduplication;
- safe negative caching;
- no raw native event logging;
- no mandatory dependency on proprietary favicon endpoints;
- clear separation between decorative image failures and content retrieval failures.

The UI SHOULD degrade gracefully when favicon loading fails.

## 9. Knowledge Context mapping

A sanitized runtime dump MAY be represented as a Knowledge Context artifact set:

- `Note`: investigator summary of the observation;
- `Claim`: bounded interpretation such as "the logged object is a native image error event";
- `Annotation`: redacted span anchors from the sanitized dump;
- `MeriotopographicEdge`: relation from event to target element, logger site, network request, or framework container;
- `ProvenanceRecord`: redaction transform and evidence lineage.

Edges that encode redaction or masking MUST use governance predicates such as `redacted_by` or `masked_by` before indexing, embedding, export, or publication.

## 10. Compliance checklist

A runtime dump handling workflow is compliant when it can demonstrate:

- raw dump quarantined;
- sanitized copy produced before broad analysis;
- cookie/auth/account/telemetry values redacted;
- cyclic graph structure identified or ruled out;
- triggering event separated from developer-tool expansion artifact;
- root-cause debugging moved to assignment/logging/network boundaries;
- safe summary produced without secret values;
- downstream issues or PRs avoid pasting raw browser state.

## 11. Non-goals

This standard does not define:

- a browser extension;
- a proprietary telemetry integration;
- a universal DOM serialization format;
- a favicon service implementation;
- a requirement to retain raw browser dumps longer than policy allows;
- approval to publish raw runtime diagnostics.

## 12. Initial backlog

1. Add a JSON Schema for a bounded `ClientRuntimeDiagnosticRecord`.
2. Add a fixture pair: unsafe raw-like sample and safe redacted sample.
3. Add a redaction validator that rejects cookie/auth/account material.
4. Add an example Knowledge Context mapping using `redacted_by`, `anchors_to`, and `derives_from` edges.
5. Coordinate with Global DevSecOps Intelligence for telemetry classification and detection guidance.
