# Leroy Merlin API endpoint mapping log
This file tracks endpoint discovery status during Sprint 1.

## Evidence status key
- `verified`: endpoint observed and tested successfully.
- `unverified`: endpoint observed but not successfully tested.
- `hypothesis`: inferred endpoint pattern pending observation.

## Endpoint register
1. `GET /api/v*/search?q=...`
   - status: `hypothesis`
   - purpose: search product catalogue
   - auth notes: pending HAR capture
2. `GET /api/v*/product/{sku}`
   - status: `hypothesis`
   - purpose: product detail and stock
   - auth notes: pending HAR capture
3. `POST /api/v*/cart/add`
   - status: `hypothesis`
   - purpose: add item to basket
   - auth notes: pending HAR capture
4. `GET /api/v*/cart`
   - status: `hypothesis`
   - purpose: read basket state
   - auth notes: pending HAR capture
5. `POST /api/v*/cart/checkout`
   - status: `hypothesis`
   - purpose: pre-checkout validation
   - auth notes: pending HAR capture

## Validation protocol
- Capture headed authenticated session HAR.
- Record request path, method, headers constraints (without secret values), and response shape.
- Upgrade status labels only when reproducible evidence is captured.

