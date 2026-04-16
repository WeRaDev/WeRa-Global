# Leroy Merlin AI Procurement Agent
## Pilot Project Research Report & Development Requirements
**Version:** 1.0 — April 2026
**Author:** Fransis Team / Mike Ananyin
**Status:** Pre-Development — Pilot Phase Planning

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Legal & Compliance Analysis](#2-legal--compliance-analysis)
3. [Technical Infrastructure — Leroy Merlin Portal](#3-technical-infrastructure--leroy-merlin-portal)
4. [System Architecture](#4-system-architecture)
5. [Component Specifications](#5-component-specifications)
6. [Security & Credential Management](#6-security--credential-management)
7. [Development Requirements](#7-development-requirements)
8. [Sprint Plan (MVP)](#8-sprint-plan-mvp)
9. [Risk Register](#9-risk-register)
10. [Open Questions & Next Steps](#10-open-questions--next-steps)

---

## 1. Project Overview

### 1.1 Concept
**"Uber Eats for Leroy Merlin"** — An AI-powered procurement assistant that translates a customer's
construction, renovation, maintenance, or gardening **project description** into a ready-to-pay
product basket on Leroy Merlin's e-commerce platform. The system acts as a purchasing agent on
behalf of the client, using their Leroy Merlin PRO account credentials.

### 1.2 Target Users (Pilot)
Three independent businesses operating in:
- Real estate maintenance and renovation
- Active construction or refurbishment projects
- Regular, high-volume Leroy Merlin buyers (qualifying for Clube Leroy Merlin PRO)

### 1.3 Value Proposition

| Stakeholder | Value |
|---|---|
| B2B Client | Time saved on procurement; AI-assisted material planning; basket ready to pay |
| Leroy Merlin | Increased basket size; reduced procurement friction for PRO buyers |
| Product (Agent Fee) | Small fee per completed basket charged to the client |

### 1.4 Monetisation
Revenue model: **fee per confirmed basket**, charged on top of product cost + delivery.
Pilot phase: free or symbolic fee to 3 consenting pilot businesses.

---

## 2. Legal & Compliance Analysis

### 2.1 Leroy Merlin Portugal — General Terms of Service (TCG)

**Source:** `leroymerlin.pt/politicas-e-condicoes/termos-e-condicoes-gerais/`
**Operator:** BCM Bricolage S.A. (NIPC 506 848 558), Carnaxide, Portugal

#### Key Findings

| Clause | Original Text (PT) | Implication |
|---|---|---|
| Credential Confidentiality | *"o utilizador deverá garantir a confidencialidade dos seus dados de acesso, de modo a impedir o seu uso indevido por terceiros"* | Credentials must not be misused by third parties. **Sharing credentials requires explicit written client consent.** |
| Authorized Third-Party Action | *"O utilizador pode solicitar que a sua encomenda seja levantada por um terceiro"* | Third-party acting on behalf of the account holder **is explicitly permitted** for order-related actions. |
| Use Commitment | *"Utilizá-lo apenas para fazer consultas ou compras reais"* | Automated basket creation for real purchases **is compliant**. Fake or test orders are not. |
| Unauthorized Access | *"prevenir o acesso não autorizado... o seu uso impróprio"* | Automation with owner consent and credentials is **authorized access**. |
| Account Blocking | *"Em caso de incumprimento destas Condições Gerais ou de utilização indevida do site, a LEROY MERLIN reserva-se no direito de bloquear ou cancelar o registo"* | Misuse may result in account suspension. Risk must be mitigated by acting as a transparent purchasing agent. |

#### Legal Assessment — Credential-Based Access (Option D)

> **Conclusion:** Using customer-provided PRO credentials — with written client authorization — to
> create baskets on their behalf constitutes **authorized use** under the ToS. The account holder
> remains legally responsible. This is analogous to an ERP system or purchasing manager acting on
> behalf of a business. No clause explicitly prohibits programmatic access by the account holder
> or their authorized agent.

**Mandatory mitigation:** Each pilot client must sign a written **Purchasing Agent Authorization
Agreement** delegating the system to act on their account. This creates a clear legal chain.

### 2.2 Clube Leroy Merlin PRO Card Terms

**Source:** `media.adeo.com/media/5155609/media.pdf`

| Clause | Finding |
|---|---|
| Card Type | Personal and non-transferable |
| Co-Holder Allowed | Yes — up to 2 cards per account |
| Relevant Risk | The "personal" nature of the card means the **system must act strictly as agent**, not as independent user |

**Mitigation:** The agent system must always identify all actions as being performed on behalf of
the named account holder. No creation of new sub-accounts or impersonation.

### 2.3 Marketplace Terms

**Source:** `leroymerlin.pt/marketplace/condicoes-gerais-de-utilizacao-do-marketplace.html`

- Oriented exclusively toward **sellers (Merchants)**. No buyer-side automation restrictions found.
- Client area features confirmed: order placement, order tracking, order history — all accessible
  via authenticated session.

### 2.4 GDPR & EU ePrivacy Considerations

- Customer project data (floor plans, requirement files, personal addresses) is classified as
  **personal data** under GDPR.
- All data must be stored in the **dedicated per-client Nextcloud instance** (data sovereignty).
- No project data is to be shared with Leroy Merlin beyond what is required to create the basket.
- A **Data Processing Agreement (DPA)** between the Fransis Team and each pilot client is required
  before onboarding.

### 2.5 Required Legal Documents (Pre-Pilot)

| Document | Purpose | Parties |
|---|---|---|
| Purchasing Agent Authorization Agreement | Authorizes the system to access LM on client behalf | Fransis Team ↔ Pilot Client |
| Data Processing Agreement (DPA) | GDPR compliance for handling project data | Fransis Team ↔ Pilot Client |
| Internal Credential Vault Policy | Documents secure handling of client credentials | Fransis Team internal |

---

## 3. Technical Infrastructure — Leroy Merlin Portal

### 3.1 Portal Profile (Portugal)

- **URL:** `leroymerlin.pt`
- **PRO Program:** Clube LEROY MERLIN PRO — B2B loyalty program for construction, renovation,
  garden, and real estate professionals
- **PRO Onboarding:** In-store only, requires legal representative ID + company certificate (CAE
  in qualifying construction/renovation categories)
- **Client Area:** `leroymerlin.pt/area-de-cliente/home`
  - Shopping lists (create, edit, print, add to cart)
  - Budgets (view, modify, finalize)
  - Order history (online + in-store)
  - PRO loyalty card, points, and discounts
  - Invoices (PRO card holders only)

### 3.2 Bot Detection Stack — CRITICAL TECHNICAL FINDING

Leroy Merlin operates a **two-layer bot detection system**:

| Layer | Technology | Behaviour |
|---|---|---|
| Primary | **DataDome** | Fingerprints headless browsers; returns HTTP 403 with `server: DataDome` header; blocks standard Playwright/Selenium headless |
| Secondary | **Cloudflare Bot Management** | Anomaly detection, DDoS mitigation, traffic analysis |

**Evidence:** Independent testing confirms DataDome actively blocks WebPageTest automated
browsers on `leroymerlin.it` (same Adeo group infrastructure) with `x-datadome: protected`
response headers. Cloudflare Bot Management is confirmed deployed via Cloudflare case study
(Leroy Merlin Brazil; same Adeo-wide security stack).

> ⚠️ **This is the single highest-risk technical finding.** Standard headless Playwright will
> be blocked. The Calculator layer architecture must account for this from Sprint 1.

### 3.3 Internal API Structure (Hypothesis — To Be Confirmed in Sprint 1)

Based on existing third-party scraper intelligence (Piloterr, autom.dev, Apify) and the portal
structure, the following internal JSON endpoints are expected to be discoverable via XHR
interception during an authenticated session:

| Endpoint (Hypothetical) | Function |
|---|---|
| `/api/v*/search?q=...&store=...` | Product search with store-specific pricing |
| `/api/v*/product/{sku}` | Product detail, stock, availability |
| `/api/v*/cart/add` | Add SKU + quantity to basket |
| `/api/v*/cart` | Basket read (items, prices, totals) |
| `/api/v*/cart/checkout` | Pre-checkout price validation |

> These endpoints must be confirmed via HAR export analysis during Sprint 1. They become the
> direct targets of the Calculator (bypassing HTML rendering entirely).

### 3.4 Bot Detection Mitigation Strategy

Given the DataDome + Cloudflare stack, the following technical approaches are viable:

| Approach | Description | Risk |
|---|---|---|
| **A — Stealth Playwright** | `playwright-stealth` or `undetected-playwright` library to mask headless fingerprints | DataDome updates frequently; may break |
| **B — Authenticated Real Session XHR Proxy** | Client completes initial login in real browser; session cookies exported and reused by Calculator for API calls only (no HTML rendering) | Session expiry; CORS may block direct API calls |
| **C — Camoufox / Fingerprint Randomisation** | Use Camoufox (Firefox-based anti-detect browser for Python) with realistic fingerprint | More robust than Playwright-stealth |
| **D — Manual Session Bootstrap + API Call Layer** | Client logs in once via real browser; Calculator calls discovered XHR endpoints directly using `requests` + session cookies (no browser needed) | Best long-term; requires XHR mapping first |

**Recommended approach for MVP:** Start with **Approach D** — map XHR endpoints in Sprint 1,
then build the Calculator as a pure `httpx`/`requests` client using exported session cookies.
Fall back to **Approach C (Camoufox)** if direct API calls are blocked by CORS or token
validation tied to the browser context.

---

## 4. System Architecture

### 4.1 Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT SIDE                             │
│                                                             │
│  ┌──────────────┐    ┌──────────────────────────────────┐  │
│  │  Mobile PWA  │───▶│        Web App (Chatbot UI)      │  │
│  │ (audio/text/ │    │   Predefined script intake flow  │  │
│  │  file upload)│    └──────────────┬───────────────────┘  │
└──────────────────────────────────────┼──────────────────────┘
                                       │ Structured JSON Context
┌──────────────────────────────────────▼──────────────────────┐
│                  SERVER SIDE (Nextcloud)                     │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Nextcloud Instance (per client)           │    │
│  │  ┌─────────────────┐  ┌─────────────────────────┐  │    │
│  │  │  Project Files  │  │  Context Agent (MCP)    │  │    │
│  │  │  (floor plans,  │  │  Orchestrates AI +      │  │    │
│  │  │  docs, photos)  │  │  Calculator tools       │  │    │
│  │  └────────┬────────┘  └──────────┬──────────────┘  │    │
│  └───────────┼────────────────────── ┼ ────────────────┘    │
│              │ File Context          │ MCP Tool Calls        │
│  ┌───────────▼───────────┐  ┌────── ▼──────────────────┐   │
│  │     AI Agent          │  │    Calculator (MCP Server)│   │
│  │  (Claude via API)     │  │  Python + httpx           │   │
│  │  Structured context   │  │  Session vault per client │   │
│  │  → project_config     │  │  XHR API proxy to LM      │   │
│  └───────────────────────┘  └──────────────┬────────────┘   │
└─────────────────────────────────────────── ┼ ───────────────┘
                                             │ Authenticated HTTP
┌────────────────────────────────────────── ▼ ───────────────┐
│              LEROY MERLIN PRO PORTAL                        │
│     Product Search API │ Cart API │ Price Validation        │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Data Flow

```
1. Customer → Mobile/Web → Chatbot Admin script (Q&A intake)
2. Chatbot Admin → Structured JSON context object
3. Context object + uploaded files → Nextcloud storage
4. Nextcloud Context Agent → AI Agent (Claude) via MCP
5. AI Agent → decomposes project → creates project_config JSON
6. AI Agent → calls Calculator MCP tool: build_basket(project_config)
7. Calculator → authenticates with LM PRO session → searches products
8. Calculator → validates quantities → creates basket on LM portal
9. Calculator → returns basket_id + itemized list + total price
10. Web App → presents basket to customer for approval
11. Customer → approves → pays on LM portal (standard checkout)
12. System → charges agent fee → confirms order completion
```

---

## 5. Component Specifications

### 5.1 Chatbot Admin Layer (Pre-Filter)

**Purpose:** Structure raw customer input before it reaches the AI. The AI never sees unstructured input.

**Technology:** Python scripted Q&A flow (Nextcloud Talk bot or standalone web widget)

**Intake Questions (Minimum):**
1. Project type: `[renovation | new_build | garden | maintenance | other]`
2. Project area / dimensions (m²) or description
3. Specific rooms or zones affected
4. Material quality preference: `[economy | standard | premium]`
5. Estimated budget (EUR range)
6. Timeline urgency: `[this week | this month | flexible]`
7. File uploads: floor plan, photos, existing quotes (optional)

**Output:** Validated JSON context object:
```json
{
  "client_id": "pilot_client_1",
  "project_type": "bathroom_renovation",
  "area_sqm": 12,
  "zones": ["floor", "walls", "plumbing_fixtures"],
  "quality_tier": "standard",
  "budget_eur": 800,
  "timeline": "this_month",
  "files": ["floor_plan_v1.pdf", "photo_existing.jpg"],
  "intake_timestamp": "2026-04-16T14:00:00Z"
}
```

### 5.2 AI Agent (Claude)

**Provider:** Anthropic Claude (claude-3-5-sonnet or claude-opus-4)
**Access:** Anthropic API (server-side only; key never exposed to frontend)

**System Prompt Contract:**
- Role: Leroy Merlin product configurator for construction projects
- Input: Structured JSON context only (no raw user messages)
- Output: `project_config` JSON with bill of materials + quantities
- Constraints: Only suggest products available at Leroy Merlin PT; respect budget; include
  material safety margins (standard construction rules)

**Example `project_config` output:**
```json
{
  "project_id": "proj_20260416_001",
  "items": [
    { "category": "floor_tiles", "query": "ceramic floor tile 60x60", "quantity": 15, "unit": "m2", "quality": "standard" },
    { "category": "tile_adhesive", "query": "tile adhesive C2 standard", "quantity": 4, "unit": "bags_25kg" },
    { "category": "grout", "query": "grout joint 3mm grey", "quantity": 2, "unit": "bags_5kg" }
  ],
  "estimated_total_eur": 420,
  "confidence": 0.87
}
```

### 5.3 Calculator (MCP Tool Server)

**Technology:** Python 3.11+, `mcp` SDK, `httpx` for HTTP calls, `playwright` (Camoufox fallback)

**MCP Tools Exposed:**

```python
@mcp.tool()
def search_products(query: str, category: str, client_id: str) -> list[dict]:
    """Search LM product catalogue via authenticated session XHR endpoint."""
    session = load_session(client_id)  # loads auth.json from encrypted vault
    return lm_api.search(query, category, session)

@mcp.tool()
def build_basket(project_config: dict, client_id: str) -> dict:
    """Create basket on LM PRO portal from project_config. Returns basket_id + itemized list."""
    session = load_session(client_id)
    basket = lm_api.create_basket(project_config["items"], session)
    return {"basket_id": basket.id, "items": basket.items, "subtotal": basket.total}

@mcp.tool()
def validate_price(basket_id: str, client_id: str) -> dict:
    """Validate final price including delivery. Returns confirmed total."""
    session = load_session(client_id)
    return lm_api.get_basket_summary(basket_id, session)
```

**Session Management:**
- Each client has an encrypted `auth_<client_id>.json` (Playwright `storageState` format)
- Sessions are bootstrapped manually by client on first use (real browser login)
- Auto-refresh triggered when session returns HTTP 401/403
- Credentials stored in **Nextcloud encrypted vault** (never in code or git)

### 5.4 Nextcloud Foundation

**Role:** Per-client data sovereignty, MCP orchestration host, file context provider

**Deployment:** Dedicated Nextcloud Hub instance per pilot client (or isolated workspace on shared instance)

**Key Apps:**
- **Nextcloud Assistant** with Context Agent: MCP orchestration between files and AI agent
- **Nextcloud Talk**: Chatbot interface frontend (or custom web app pointing to Nextcloud backend)
- **Files**: Client project documents, floor plans, purchase history
- **Encrypted Vault**: Credential storage for LM sessions

### 5.5 Web App (Frontend)

**Technology:** Nextcloud App or standalone Next.js/Vite SPA
**Features:**
- Predefined chatbot intake script (guided Q&A)
- File upload (PDF, images)
- Audio recording (Web Audio API → transcribed by Whisper)
- Basket review and approval UI
- Order confirmation and fee payment

### 5.6 Mobile App

**Technology:** Progressive Web App (PWA) — thin client pointing to web app
**Features:** Audio input, text input, file upload, basket notifications

---

## 6. Security & Credential Management

### 6.1 Credential Storage Policy

| Asset | Storage | Encryption | Access |
|---|---|---|---|
| LM PRO login credentials | Nextcloud encrypted vault | AES-256 at rest | System only; never logged |
| Session `auth.json` files | Nextcloud server filesystem | AES-256 at rest | Calculator service account only |
| Anthropic API key | Environment variable (server) | OS-level secret management | AI Agent service only |
| Client project files | Nextcloud per-client workspace | Nextcloud E2EE optional | Client + Calculator only |

### 6.2 Session Bootstrap Protocol

```
1. Client installs Playwright-driven "Session Capture" tool (one-time)
2. Tool opens real Chromium browser (headed, non-headless) 
3. Client manually logs into leroymerlin.pt with PRO credentials
4. Tool captures cookies + localStorage via storageState export
5. auth_<client_id>.json encrypted and stored in Nextcloud vault
6. Playwright-headless Calculator uses this state for all subsequent calls
7. Session expiry: auto-detect on 401/302→login redirect → notify client for re-bootstrap
```

### 6.3 Anti-Bot Bypass Protocol

**Primary strategy (Sprint 1 goal):** Map all internal XHR/JSON API endpoints using HAR export
during an authenticated real browser session. Calculator then calls these endpoints directly
using `httpx` + exported session cookies — **no headless browser required for steady-state
operation**. DataDome and Cloudflare inspect the *browser* layer; direct API calls with valid
session cookies may bypass bot detection entirely if endpoint tokens do not validate browser
fingerprint.

**Fallback (Sprint 2 if primary fails):** Use **Camoufox** (anti-detect Firefox browser for Python)
which provides randomized fingerprinting resistant to DataDome detection.

---

## 7. Development Requirements

### 7.1 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | System accepts project description via text, audio, or file upload | Must Have |
| FR-02 | Chatbot admin layer structures input before AI contact | Must Have |
| FR-03 | AI agent produces a bill of materials from structured context | Must Have |
| FR-04 | Calculator searches Leroy Merlin product catalogue using client credentials | Must Have |
| FR-05 | Calculator creates a basket on the LM PRO portal | Must Have |
| FR-06 | System presents basket to client for approval before any payment | Must Have |
| FR-07 | Client approves basket and completes payment on LM portal | Must Have |
| FR-08 | System charges agent fee per completed transaction | Must Have |
| FR-09 | Client project files are stored in per-client Nextcloud instance | Must Have |
| FR-10 | Audio input is transcribed and passed through intake Q&A | Should Have |
| FR-11 | Mobile PWA provides full access to all features | Should Have |
| FR-12 | Basket can be edited by client before approval | Should Have |
| FR-13 | Multiple project types supported (renovation, garden, maintenance) | Should Have |
| FR-14 | PRO loyalty points and discounts are applied to baskets | Nice to Have |
| FR-15 | Historical basket and project storage for repeat clients | Nice to Have |

### 7.2 Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Basket creation time (from project_config to basket ready) | < 90 seconds |
| NFR-02 | AI product selection accuracy (correct category + spec) | > 80% on pilot test cases |
| NFR-03 | Session stability (hours between re-authentication) | > 8 hours |
| NFR-04 | Data residency | EU only (Nextcloud server in PT/EU) |
| NFR-05 | Credential encryption standard | AES-256 at rest minimum |
| NFR-06 | Uptime target for pilot | 95% during business hours |
| NFR-07 | Mobile PWA responsiveness | iOS Safari + Android Chrome |

### 7.3 Technology Stack

| Layer | Technology | Version |
|---|---|---|
| Backend language | Python | 3.11+ |
| AI Provider | Anthropic Claude API | claude-3-5-sonnet / opus-4 |
| MCP Framework | `mcp` Python SDK | latest |
| HTTP client (Calculator) | `httpx` | latest |
| Browser automation (fallback) | Camoufox | latest |
| Infrastructure | Nextcloud Hub | latest stable |
| Frontend | Nextcloud Talk bot or Next.js | TBD Sprint 5 |
| Audio transcription | OpenAI Whisper (self-hosted) | medium model |
| Mobile | PWA (no native app for MVP) | — |
| Version control | GitHub | — |
| CI/CD | GitHub Actions | — |

---

## 8. Sprint Plan (MVP)

### Sprint 0 — Legal & Onboarding (Week 1)
**Goal:** Legal foundation and pilot client onboarding
- [ ] Draft and execute Purchasing Agent Authorization Agreement (3 clients)
- [ ] Draft and execute DPA (3 clients)
- [ ] Confirm Clube Leroy Merlin PRO membership status for all 3 pilot clients
- [ ] Secure written consent for credential sharing under defined security policy
- [ ] Set up Nextcloud instances per client
- [ ] Set up GitHub repo, project board, and CI scaffold

---

### Sprint 1 — Portal Recon & Session Capture (Week 2)
**Goal:** Map LM portal XHR API structure; establish working session management
- [ ] Build Session Capture tool (headed Playwright, storageState export)
- [ ] Conduct authenticated session with PRO credentials
- [ ] Export full HAR file from browser DevTools during: search, product detail, add-to-cart, basket read, price validation
- [ ] Identify and document all internal JSON API endpoints
- [ ] Test direct `httpx` calls to discovered endpoints using session cookies
- [ ] Determine whether DataDome/Cloudflare validates browser fingerprint on API calls
- [ ] Document bot detection behaviour and select bypass strategy (D or C)

**Deliverable:** `API_ENDPOINTS.md` — documented internal LM API structure; working `session_test.py`

---

### Sprint 2 — Calculator MVP (Weeks 3–4)
**Goal:** End-to-end basket creation via authenticated session
- [ ] Implement `search_products()` tool (query → JSON product list)
- [ ] Implement `build_basket()` tool (project_config → basket ID)
- [ ] Implement `validate_price()` tool (basket ID → confirmed total)
- [ ] Build encrypted session vault (load/save `auth.json` per client)
- [ ] Write test cases: 3 real project scenarios × 3 clients
- [ ] Integrate anti-bot fallback (Camoufox) if direct API calls are blocked

**Deliverable:** Working Calculator that creates a real basket on LM PRO portal from a hardcoded `project_config`

---

### Sprint 3 — AI Agent Script (Week 5)
**Goal:** Structured context → Claude → `project_config` → Calculator
- [ ] Write system prompt for Claude (product configurator role)
- [ ] Implement context → `project_config` generation pipeline
- [ ] Validate material quantity formulas (floor area → tiles + adhesive + grout)
- [ ] Connect AI agent to Calculator via MCP tool calls
- [ ] Test on 5 reference project types (bathroom, kitchen, garden, facade, maintenance)
- [ ] Validate output accuracy against manually prepared baskets

**Deliverable:** `agent_script.py` — Claude receives JSON context, returns valid `project_config`, Calculator builds basket

---

### Sprint 4 — Chatbot Admin Layer (Week 6)
**Goal:** Intake Q&A flow → structured JSON context
- [ ] Implement Python Q&A intake script (text-based, Nextcloud Talk or API)
- [ ] Map all project types to intake question trees
- [ ] File upload handler (PDF, JPG → stored in Nextcloud)
- [ ] Audio intake: Whisper transcription → Q&A injection
- [ ] Output validation (JSON schema check before AI handoff)
- [ ] End-to-end test: voice input → basket on portal

**Deliverable:** Working chatbot intake flow producing validated JSON context passed to AI Agent

---

### Sprint 5 — Nextcloud Integration & MCP Server (Week 7)
**Goal:** Calculator exposed as MCP tools; Nextcloud orchestrates end-to-end
- [ ] Deploy Calculator as MCP server (Python `mcp` SDK)
- [ ] Integrate Nextcloud Context Agent with Calculator MCP server
- [ ] File context pipeline: client uploads → Nextcloud → AI Agent context
- [ ] Per-client credential injection via environment variables
- [ ] Full end-to-end integration test: Nextcloud file → AI → Calculator → LM basket

**Deliverable:** MCP server running; Nextcloud orchestrates full pipeline end-to-end

---

### Sprint 6 — Web Frontend (Week 8)
**Goal:** Customer-facing chatbot UI
- [ ] Build chatbot web UI with predefined intake scripts
- [ ] Basket review and approval screen
- [ ] File upload UI
- [ ] Agent fee display and payment confirmation
- [ ] Connect frontend to Nextcloud/backend APIs

**Deliverable:** Working web app — client can complete full flow from browser

---

### Sprint 7 — Mobile PWA (Week 9)
**Goal:** Mobile access point
- [ ] Responsive PWA wrapping web app
- [ ] Audio recording → Whisper transcription
- [ ] Push notifications for basket ready / approval needed
- [ ] Test on iOS Safari + Android Chrome

**Deliverable:** Installable PWA tested on both platforms

---

### Sprint 8 — Pilot Go-Live (Weeks 10–12)
**Goal:** Real clients, real projects, real baskets
- [ ] Onboard 3 pilot clients with full credential bootstrap
- [ ] Run 3+ real project cycles per client (minimum 9 baskets total)
- [ ] Collect feedback on: basket accuracy, AI product selection, UX, time saved
- [ ] Monitor session stability and bot detection incidents
- [ ] Document failures and edge cases
- [ ] Prepare partnership outreach to Leroy Merlin PRO/B2B team

**Deliverable:** Pilot completion report; MVP validated; Leroy Merlin partnership case assembled

---

## 9. Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | DataDome blocks Calculator API calls even with valid session cookies | High | Critical | Sprint 1 test; Camoufox fallback; LM partnership track |
| R-02 | Leroy Merlin suspends client account for automated activity | Medium | High | Signed authorization agreement; rate limiting; human-readable session behaviour |
| R-03 | Internal XHR endpoints change without notice | Medium | High | Versioned endpoint mapping; automated endpoint health checks |
| R-04 | Session expiry causes basket failure mid-operation | Medium | Medium | Auto-detect + re-bootstrap flow; client notification |
| R-05 | AI product selection inaccurate (wrong SKU / wrong quantity) | Medium | Medium | Test suite with reference baskets; client review before payment (mandatory step) |
| R-06 | Client credential compromise | Low | Critical | AES-256 vault; zero-logging policy; access audit trail on Nextcloud |
| R-07 | GDPR non-compliance (project data handling) | Low | High | DPA signed; EU-hosted Nextcloud; data minimisation |
| R-08 | Leroy Merlin ToS change prohibiting automation | Low | Critical | Monitor ToS quarterly; LM partnership as long-term hedge |
| R-09 | Pilot client unable to qualify for Clube PRO | Low | Medium | Verify PRO status before Sprint 0 sign-off |

---

## 10. Open Questions & Next Steps

### Open Technical Questions
1. **Do LM internal XHR endpoints accept `httpx` calls with session cookies alone?** (Answer: Sprint 1)
2. **What token/CSRF validation is applied per API call?** (Answer: HAR analysis, Sprint 1)
3. **Does the Clube PRO account have a distinct authenticated session flow vs. regular accounts?**
4. **What is the session token TTL for PRO accounts?**
5. **Does LM Portugal share infrastructure (and therefore same API structure) with LM Spain/France?**
   — Relevant for expansion roadmap.

### Open Business Questions
1. **What agent fee per basket is acceptable to pilot clients?** (Suggested: 2–5% of basket value or €5–15 flat)
2. **What is the minimum basket size that justifies agent use?** (Suggested: >€100)
3. **Is Leroy Merlin PRO team open to a direct B2B partnership discussion post-pilot?**
   — Partnership would provide official API access and eliminate bot detection risk entirely.

### Immediate Actions (This Week)
- [ ] Legal: Draft Purchasing Agent Authorization Agreement and DPA templates
- [ ] Confirm PRO membership status of all 3 pilot clients
- [ ] Set up development Nextcloud instance
- [ ] Create GitHub repository with project structure
- [ ] Begin Sprint 1: Session Capture tool development

---

*End of Report — Version 1.0*
*Next review: Sprint 1 completion (approx. Week 2 end)*
