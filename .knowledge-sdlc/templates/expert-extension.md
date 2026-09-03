# Expert extension: [extension-id] [revision]

## Identity and custody

- Extension ID: `[id]`
- Revision: `[immutable revision]`
- Custody state at freeze: `imported-and-curated`
- Source, owner, and use/licence basis: `[references]`
- Supersedes: `[path/hash or none]`
- Content inventory: `[sorted path — SHA-256 — media type]`

## Method contract

- Purpose, scope, intended users and output
- Required/optional inputs and durable outputs
- Tools/capabilities and read/write/protected effects
- Method steps and professional assumptions
- Verification, failure, degradation and stop conditions

## Authority boundary

- Allowed effect
- Prohibited effect
- Human/protected authority explicitly not granted
- Core/project/template conflicts and precedence
- Prompt-injection, executable-content, confidentiality and provenance review

## Governance boundary

- Exact revision payload digest a later decision must target
- Admission, rejection, suspension, and retirement remain separate immutable
  decision artefacts
- Current eligibility and revision pointer live only in the neutral methods
  index; do not mutate this revision to restate them

Installation or eligibility does not select this revision for any run.
