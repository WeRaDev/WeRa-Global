# Gitea Wiki Initialization Runbook v1
version: 1.0
status: partial-ready
owner: governance steward
scope: REALIGN-07

## Goal
Initialize the wiki git repository and publish seed navigation pages from `kb-governance/wiki-seed/`.

## Execution status
- Endpoint probe attempted:
  - `git --no-pager ls-remote http://127.0.0.1:3000/wera-global/WeRa-Global.wiki.git`
- Result at execution time:
  - `fatal: Could not read from remote repository.`
- Interpretation:
  - wiki git endpoint is not yet available, so direct initialization was not completed in this sprint.

## Preconditions for initialization
1. Repository wiki feature is enabled in Gitea UI/admin settings.
2. Endpoint check succeeds for `WeRa-Global.wiki.git`.
3. Operator has push permissions to the wiki repository.

## Initialization procedure (when endpoint is available)
1. Clone wiki repository:
   - `git clone http://127.0.0.1:3000/wera-global/WeRa-Global.wiki.git /tmp/WeRa-Global.wiki`
2. Copy seed pages:
   - `cp kb-governance/wiki-seed/Home.md /tmp/WeRa-Global.wiki/Home.md`
   - `cp kb-governance/wiki-seed/Domain-Index.md /tmp/WeRa-Global.wiki/Domain-Index.md`
   - `cp kb-governance/wiki-seed/Governance-Index.md /tmp/WeRa-Global.wiki/Governance-Index.md`
3. Commit and push:
   - `git -C /tmp/WeRa-Global.wiki add Home.md Domain-Index.md Governance-Index.md`
   - `git -C /tmp/WeRa-Global.wiki commit -m "Initialize KB wiki navigation indexes"`
   - `git -C /tmp/WeRa-Global.wiki push origin main`

## Post-initialization checks
1. Wiki home page renders and links resolve.
2. Domain and governance indexes reference canonical `KnowledgeBase/` paths only.
3. No operational source record exists only in wiki (no dual-source drift).
