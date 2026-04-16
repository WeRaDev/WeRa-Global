# Bild backlog

## BILD-001 Sprint 0 legal onboarding package
- Problem: Pilot cannot begin without signed legal authorizations.
- Scope: Draft Purchasing Agent Authorization Agreement, DPA, and vault policy.
- Acceptance: Documents reviewed and approved for pilot onboarding.

## BILD-002 Sprint 1 endpoint reconnaissance
- Problem: Internal Leroy Merlin API surface is unknown.
- Scope: Capture authenticated session HAR and map key XHR endpoints.
- Acceptance: `API_ENDPOINTS.md` with verified search/product/cart paths and auth notes.

## BILD-003 Session capture and vault bootstrap
- Problem: Calculator requires stable authenticated sessions per client.
- Scope: Build one-time headed session capture flow and encrypted storage procedure.
- Acceptance: `session_test.py` validates one pilot account read path without credentials in logs.

## BILD-004 Calculator MVP tools
- Problem: No automated basket-building toolchain exists.
- Scope: Implement `search_products`, `build_basket`, and `validate_price`.
- Acceptance: One end-to-end basket creation test passes in controlled pilot environment.

