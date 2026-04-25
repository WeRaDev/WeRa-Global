# WeRa-Global
Unified umbrella repository for WeRa Global.

## Repository structure
- `KnowledgeBase/` — canonical project knowledge, strategy, legal, architecture, and financial documentation.
- `ProductionBase/` — software production repositories mounted as independent git projects.

## ProductionBase projects
- `ProductionBase/SolarSeed-v3`
- `ProductionBase/FilantropiaSolar`
- `ProductionBase/FreeDoo`
- `ProductionBase/wera-contracts`
- `ProductionBase/SolarSim`
- `ProductionBase/Bild`
- `ProductionBase/Poly-Robot`

## Working model
- Use this repository as the single onboarding and navigation entry point.
- Keep `KnowledgeBase/` versioned directly in this umbrella repository.
- Keep each `ProductionBase/*` project independent, with dedicated instructions and CI.
- Update `ProductionBase/repos.yaml` whenever project remotes, branches, or ownership change.

## Clone
Use recursive clone to pull all production repositories:

```bash
git clone --recurse-submodules http://127.0.0.1:3000/wera-global/WeRa-Global.git
```
