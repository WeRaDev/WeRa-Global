# TRL4 Gitea synchronization automation
This runbook documents the continuous synchronization setup from local canonical Gitea (`127.0.0.1:3000`) to TRL4 Gitea via local SSH tunnel endpoint (`127.0.0.1:13000`).

## Scope
- Source of truth: local Gitea organization `wera-global`.
- Downstream target: TRL4 Gitea (`wera@192.168.1.71`) through local forward `127.0.0.1:13000`.
- Canonical repositories:
  - `WeRa-Global`
  - `CityView`
  - `FilantropiaSolar`
  - `FreeDoo`
  - `Poly-Robot`
  - `SolarSeed-v3`
  - `SolarSim`
  - `wera-contracts`

## Identity and credentials
- Local synchronization service user: `Spirit` (local Gitea admin + `wera-global` owner membership).
- Local machine token storage:
  - `~/.secrets/spirit-gitea-local.env` (mode `600`)
- TRL4 push auth is performed with machine token for TRL4 admin user, used as credential in push mirror remote address.

## Local Gitea config requirement
To allow push mirror targets on local-network hosts and tunnel endpoints, local Gitea includes:
- file: `/opt/homebrew/var/gitea/custom/conf/app.ini`
- section: `[migrations]`
- keys:
  - `ALLOWED_DOMAINS = *`
  - `ALLOW_LOCALNETWORKS = true`
  - `SKIP_TLS_VERIFY = true`

After any change, restart local Gitea:
- `brew services restart gitea`

## Persistent tunnel automation
Continuous sync to TRL4 depends on a local persistent SSH forward:
- LaunchAgent: `~/Library/LaunchAgents/com.wera.trl4-gitea-tunnel.plist`
- Forward: `13000:127.0.0.1:3000`
- Remote: `wera@192.168.1.71`
- Health check:
  - `curl -fsS http://127.0.0.1:13000/api/healthz`

LaunchAgent lifecycle:
- `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.wera.trl4-gitea-tunnel.plist`
- `launchctl enable gui/$(id -u)/com.wera.trl4-gitea-tunnel`
- `launchctl kickstart -k gui/$(id -u)/com.wera.trl4-gitea-tunnel`
- `launchctl print gui/$(id -u)/com.wera.trl4-gitea-tunnel`

## Push mirror automation
Each canonical repository is configured on local Gitea with:
- one GitHub push mirror (`github.com/WeRaDev/*`)
- one TRL4 push mirror (`127.0.0.1:13000/wera-global/*.git`)
- interval: `1h0m0s`

Manual trigger for immediate execution:
- API endpoint: `POST /api/v1/repos/{owner}/{repo}/push_mirrors-sync`

Mirror health inspection:
- API endpoint: `GET /api/v1/repos/{owner}/{repo}/push_mirrors`
- required healthy state:
  - non-epoch `last_update`
  - empty `last_error`

## Verification checks
Operational checks after configuration/update:
1. Tunnel health:
   - `curl -fsS http://127.0.0.1:13000/api/healthz`
2. Mirror topology:
   - each canonical repo has exactly one TRL4 push mirror and one GitHub push mirror
3. Mirror sync health:
   - all TRL4 mirrors report recent `last_update` and blank `last_error`
4. Ref parity:
   - `git ls-remote --heads --tags` output matches between local source and TRL4 target for all canonical repositories

## Notes
- Repository `admin/house-db-governance` on TRL4 is deprecated and archived; canonical governance lives in `wera-global/WeRa-Global`.
- If tunnel connectivity is unavailable, TRL4 push mirrors will fail until the LaunchAgent tunnel is restored.
