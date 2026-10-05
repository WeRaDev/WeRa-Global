# ADR 0002: Consultancy Automation Internal-First Validation

## Status
Accepted — 2026-09-29

## Context
Inteligente's Automation Center has a designed partner-led Financial Automation Discovery Pilot. The pilot was formally initiated in September 2026, but no partner session or result is recorded. Synthetic tests of its archived draft chatbot failed required safety stops and did not produce an actionable human notification; transcript/provider handling and other data-flow details also remain unresolved. The external pilot must not proceed until these gates pass.

The founder has decided to first use Consultancy Automation to automate Inteligente's own consultancy operations and measure efficiency and outcomes before wider external rollout. The internal workflow, baseline, success measures, implementation, and hosting have not yet been selected.

## Decision
1. Treat **Consultancy Automation** as an internal-first Automation Center product/use case. Select and document a bounded workflow from Inteligente's own consultancy operations, define an appropriate baseline and efficiency/outcome measures, run a controlled internal validation, and record results and limitations before any external Financial Automation pilot.
2. Determine the internal workflow, data boundary, system, hosting, baseline, and measures during task readiness and scope approval. This ADR does not select Frank, Odoo Online, SolarSeed, or any other host, and does not authorize use of external client or partner data.
3. Keep the partner-led Financial Automation Discovery Pilot **deferred, not cancelled** until internal Consultancy Automation has been validated. After that prerequisite, the external pilot may resume only if all existing ADR 0001 gates pass: required sensitive-input/advice/ROI hard stops, verified actionable human notification, approved privacy/data-flow boundaries, and documented authorization. The existing external pilot's Odoo Online design, partner roles, and data limits remain unchanged.
4. Supersede ADR 0001 only with respect to the order of work. Its external-pilot technical safeguards, privacy constraints, and staged external deployment design remain in force.

## Consequences
- Internal Consultancy Automation has no implementation, host, baseline, or measured result until a bounded workflow is selected and validated.
- The Financial partner remains the planned external pilot customer and the Operations partner remains its validator; deferral does not cancel those relationships or the pilot design.
- No external Financial Automation pilot may begin solely because internal work has started; internal validation and all external safety/data-flow gates must be documented as passed.
- Any later local MVP or first-customer deployment remains subject to ADR 0001's separate readiness, customer-isolation, and deployment gates.

## References
- `docs/adr/0001-financial-automation-discovery-pilot.md`
- `tasks/backlog.md` (HC-009, HC-016, HC-021)
- `KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md`
- `KnowledgeBase/kb-value-proposition/docs/products/03-automation-center.md`
