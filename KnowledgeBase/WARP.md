# WARP.md — KnowledgeBase Operating Rules

Purpose: Dedicated Warp guidance for KB operations in `KnowledgeBase/` to enforce consistency, traceability, and review quality.

## Scope
Applies to:
- KB structural changes
- KB governance/process files
- KB template and schema files
- KB cross-domain integration updates

---

## Session Reflection Outcomes (Applied Rules)

1. **PR-first is mandatory**
- Never deliver KB work by direct push to `main`.
- Always: feature branch → commit(s) → PR → review/merge.

2. **Source + analysis must travel together**
- If a task references an external source file, include that source in PR scope when appropriate.
- Critical review files must explicitly cite the source file used.

3. **No naming drift**
- Canonical names must remain consistent with KB conventions:
  - `SolarSeed`
  - `WERA Cloud`
- Aliases are allowed only when labeled as deprecated/variant.

4. **No unresolved internal contradictions**
- Formulas and qualification logic must be mathematically consistent within the same document set.
- If unresolved, issue must be recorded in `12-Open-Questions.md` with status and next action.

5. **Cross-domain updates require validation hooks**
- Operational docs (`customers/channels/partners/revenue/metrics`) must include:
  - upstream dependencies
  - downstream dependencies
  - validation hooks

6. **Evidence labeling is required for high-impact claims**
- Use: `verified`, `unverified`, `hypothesis`.
- Unverified benchmark/tooling claims cannot be promoted to factual baseline.

7. **Keep KB commits scoped**
- Commit only KB-targeted files for KB tasks.
- Do not include unrelated changes from other repo areas.

---

## Mandatory KB PR Checklist

Before opening/updating PR:
- [ ] Branch is not `main`
- [ ] Referenced source files included or explicitly linked
- [ ] README index updated for new KB files
- [ ] Naming checked against canonical vocabulary
- [ ] Contradictions resolved or logged to `12`
- [ ] Evidence labels applied where needed
- [ ] Cross-domain dependencies + validation hooks present (if operational docs touched)

---

## Recommended Execution Order for KB Programs

1. Critical review and contradiction cleanup
2. Taxonomy + ownership + vocabulary
3. Schema + privacy/lifecycle rules
4. Template pack + governance workflows
5. Cross-domain matrix + validation protocol
6. Pilot adoption on high-impact docs
7. PR review with checklist and explicit completion note
