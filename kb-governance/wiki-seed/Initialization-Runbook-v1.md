# Gitea Wiki Initialization Runbook v1
version: 1.1
status: completed-in-sprint-2026-17
owner: governance steward
scope: REALIGN-07

## Goal
Initialize the wiki git repository and publish seed navigation pages from `kb-governance/wiki-seed/`.

## Execution status
- Initial state at prior sprint closure:
  - direct wiki endpoint probe failed (`Could not read from remote repository`).
- Sprint `2026-17` execution path:
  - wiki seed pages were published via Gitea API endpoint `POST /repos/{owner}/{repo}/wiki/new`.
- Published pages:
  - `Home`
  - `Domain-Index`
  - `Governance-Index`
- Verification evidence:
  - pages are listed by `GET /repos/wera-global/WeRa-Global/wiki/pages`,
  - page retrieval works via `GET /repos/wera-global/WeRa-Global/wiki/page/{pageName}`,
  - wiki git endpoint is now reachable:
    - `git --no-pager ls-remote http://127.0.0.1:3000/wera-global/WeRa-Global.wiki.git`
    - returns `refs/heads/main`.

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
Alternative API path (used in sprint `2026-17`):
1. For each page title, call:
   - `POST /api/v1/repos/wera-global/WeRa-Global/wiki/new`
2. Provide payload:
   - `title`
   - `content_base64`
   - `message`

## Post-initialization checks
1. Wiki home page renders and links resolve.
2. Domain and governance indexes reference canonical `KnowledgeBase/` paths only.
3. No operational source record exists only in wiki (no dual-source drift).
