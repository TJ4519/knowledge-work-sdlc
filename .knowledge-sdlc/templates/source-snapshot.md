# Source snapshot

The snapshot is a durable evidence entity produced by a bounded retrieval
activity. A connector or MCP is transport; it is not the underlying source.

## Source entity

- Provider and underlying source/entity
- Source title, document/dataset identifier, revision, and location
- Provider issue or observation time and timezone, when supplied
- Media type, retained path, byte/content hash, and exact retained boundary

## Retrieval activity

- Actor and host
- Tool/server and observed version, when available
- Query, parameters, filters, and requested as-of state
- Retrieval time and timezone
- Authentication, entitlement, and permission scope
- Result: `retrieved | partial | stale | contradictory | inaccessible | no-result`
- Failed attempts, truncation, export/licensing limits, and missing dimensions

## Derivation and consumers

- Literal fields or passages used, with exact locations
- Transformation or calculation applied
- Resulting claim, assumption, model range, or output artefact
- Agent or method responsible for the transformation
- Downstream consumers and claim limits

## Rule

The snapshot proves retained identity and content, not truth, comparability, or
admissible professional use. “No result” must distinguish absent evidence from
inaccessibility, staleness, filtering, or contradiction.
