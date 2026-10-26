# CI workflows
`agent-baseline.yml` prepares offline structural validation for a future standalone
DreamMakers checkout. It does not run from this nested directory in the umbrella.
Native umbrella validation needs registry inclusion and explicit root routing,
which remain separate approval gates.

The standalone scaffold requires an administrator-provisioned, read-only
`AGENT_BASELINE_READ_TOKEN` and a verified runner-local Gitea address. No secrets,
runner configuration, required checks or remote repositories are created here.
Tests must not receive write credentials or real manuscripts/client data.

Recommended baseline checks:
- lint or static checks for scripts
- smoke tests for PDF pipeline commands
- docs consistency checks

These document-pipeline checks are not implemented by the structural workflow.
Do not treat diagnostic printouts from the existing customer-specific verifier as
a fail-on-error CI result or claim manual reader acceptance from a structural pass.
