# KB Formal Proof Artifacts (TRL6)

## Purpose
Store Lean proof artifacts referenced by KB operational updates under the TRL6 formal-proof gate.

## Required contract
Each changed operational KB document must include a `formal_proof` block:

```yaml
formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.domain.some_obligation_id
  proof_artifact: kb-governance/formal-proofs/some_obligation_id.lean
  verification_status: verified
```

## Artifact requirements
Each referenced `.lean` artifact must:
- include `proof_engine: ml-hilbert` marker comment,
- include the same `obligation_id` marker,
- contain at least one `theorem` or `lemma`,
- avoid any `sorry`.

## Minimal artifact skeleton
```lean
-- obligation_id: kb.domain.some_obligation_id
-- proof_engine: ml-hilbert
theorem kb_domain_some_obligation_id : True := by
  trivial
```
