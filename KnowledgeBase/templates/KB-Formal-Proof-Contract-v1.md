# KB Formal Proof Contract Template v1 (TRL6)

Use this snippet in operational KB documents (`KnowledgeBase/kb-*/docs/**/*.md`) when introducing or updating claims that must pass the TRL6 formal-proof CI gate.

```yaml
formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.<domain>.<slug>
  proof_artifact: kb-governance/formal-proofs/<slug>.lean
  verification_status: verified
```

Proof artifact requirements:
1. `.lean` file exists at the referenced path.
2. Includes comment markers:
   - `obligation_id: kb.<domain>.<slug>`
   - `proof_engine: ml-hilbert`
3. Contains theorem/lemma declaration.
4. Contains no `sorry`.
