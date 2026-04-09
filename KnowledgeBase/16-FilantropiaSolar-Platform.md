# 16 — FilantropiaSolar Platform

---

## Product Overview

**FilantropiaSolar** is a web-based energy management system for monitoring, analysing, and predicting photovoltaic (PV) solar installations. It is built as a Nextcloud application and serves a dual purpose within the WeRa ecosystem:

1. **Proposal calculator / map app** — customer-facing tool for sales and lead generation (the SolarSeed marketplace prototype)
2. **REEMS prototype** — the foundational R&D artefact for the full Renewable Energy & Environmental Management System (REEMS), aligned with Iberia Renew Engineering

| Attribute | Value |
|---|---|
| **Current release** | v3.0.6 (April 2026) |
| **Licence** | AGPL-3.0-or-later |
| **Frontend** | Vue.js 3 (Nextcloud application shell) |
| **Backend** | Python / FastAPI (ML microservice) |
| **Capitalised R&D value** | €180,000/year · €360,000 over two years |

### Branding

| Element | Value |
|---|---|
| **Tagline** | "built by wera" — "we" in golden olive, "ra" in warm orange |
| **Primary colour** | Golden olive `#C4B552` |
| **Accent colour** | `#A89D3F` |
| **Warm orange** | `#E8A020` |

---

## User Interface

The application presents a **split-panel dashboard** as its primary view.

| Panel | Width | Content |
|---|---|---|
| **Installation list** | 32% | Scrollable list of all PV installations with status badges |
| **Interactive map** | 68% | Leaflet/OpenStreetMap live map with colour-coded markers |

### Fixed KPI Header

Always-visible aggregate metrics displayed across the top of the dashboard:

- Total plants
- Active / Warning / Offline counts
- Aggregate capacity (kWp)

### Installation Info Card

Clicking any installation in the list or map opens an info card showing:

- Location
- Capacity (kWp)
- Estimated yearly production (kWh)
- Efficiency rating

### Analytics Modal

Clicking **"View Analysis"** opens a full-screen Analytics Modal containing:

- Energy production charts (historical and predicted)
- Weather correlation overlays
- Performance rankings
- Cost savings summary

---

## Capabilities

### 1. Live Map

- Rendered with **Leaflet** on **OpenStreetMap** tiles
- Colour-coded status markers:
  - Green — active
  - Amber — warning
  - Red — offline
- Pulsing animation on the selected marker
- Tooltips on hover

#### Map Station Types

| Type | Description |
|---|---|
| **Operational** | Live, generating, with real savings data |
| **In construction** | Installation actively being built |
| **Planning** | Customer has confirmed interest |
| **Training data** | Not real proposals; used to train the energy prediction ML model |

---

### 2. Performance Ranking

- **R0–R5** rating scale applied hourly and daily
- Metric: **Normalised Specific Energy** — kWh / kWp / active-hours
- Colour-coded badges per rating level
- Rankings visible within the Analytics Modal

---

### 3. Historical & Predicted Modes

- Toggle between **measured data** and **ML-predicted / physics-simulated forecasts**
- Controls:
  - Date picker
  - Timeframe selector: Day / Week / Month / Year

---

### 4. Weather Correlation

Weather parameters overlaid on the energy production chart:

| Parameter | Colour |
|---|---|
| Temperature | Orange |
| Cloud cover | Grey |
| Humidity | Blue |
| Wind speed | Purple |

---

### 5. Savings Calculator ("Light Saved")

- Converts energy production (kWh) to monetary savings (EUR)
- Default grid price: **€0.15 / kWh** (configurable per locality)
- Demonstrates the **20% minimum guaranteed energy bill reduction** central to WeRa's SolarSeed value proposition

---

### 6. Virtual Installation Simulator

Allows users to create custom PV plants at any location and capacity:

- Select any geographic location and set capacity (kWp)
- Upload production data via **CSV or Excel**
- Physics-based energy predictions using **Open-Meteo** weather data or synthetic patterns
- Used for proposal generation during customer acquisition

---

### 7. Multi-Tenant Dashboard

- Merges ML dataset installations with user-created virtual installations in one unified view
- Users can hide, restore, and manage their installations independently
- Supports multi-tenant separation within the Nextcloud identity layer

---

### 8. ML Model Transparency

- **"ML Info" popover** on any installation or prediction result
- Displays:
  - Data source
  - Weather source
  - Prediction method
  - Accuracy metrics: R² and MAE

---

### 9. Data Export

- One-click **CSV export** of the currently displayed analysis period
- Available from within the Analytics Modal

---

## Architecture

### Frontend — Nextcloud App (Vue.js 3)

The frontend runs as a Nextcloud application: PHP controllers provide the Nextcloud shell; a single-page Vue 3 dashboard handles all UI logic.

| Concern | Technology / Module |
|---|---|
| **Framework** | Vue.js 3 |
| **State management** | Pinia (`store/app.js`) |
| **Maps** | Leaflet |
| **Charts** | Chart.js |

#### Component Structure

| Component | Role |
|---|---|
| `Dashboard.vue` | Root layout; coordinates panels |
| `Header.vue` | Fixed KPI header |
| `ListPanel.vue` | Installation list (32% panel) |
| `MapPanel.vue` | Interactive map (68% panel) |
| `AnalyticsModal.vue` | Full-screen analysis view |
| `CreateVirtualModal.vue` | Virtual installation creation flow |
| `MlAdminPanel.vue` | ML model administration interface |

#### Shared Utilities

| File | Purpose |
|---|---|
| `composables/useEnergyChart.js` | Chart.js chart configuration and data binding |
| `utils/ranking.js` | R0–R5 ranking calculation logic |

---

### Backend — ML Microservice (Python / FastAPI, port 8501)

#### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/predict/period` | Main analysis endpoint — returns predictions for a date range |
| `POST` | `/predict` | Per-installation ML prediction |
| `POST` | `/simulate-weather` | Synthetic weather generation for Portuguese locations (up to 400 days) |
| `GET` | `/health` | Service health check |
| `*` | Admin endpoints | Cache management and model administration |

#### ML Ensemble Model

Predictions are produced by a weighted ensemble with physical constraint enforcement:

| Model | Weight |
|---|---|
| Random Forest | 40% |
| Gradient Boosting | 35% |
| Linear Regression | 25% |

- Feature scaling via **StandardScaler**
- Physical constraints enforced post-prediction (non-negative output, capacity ceiling)
- Models serialised with **joblib**; feature names persisted for schema validation

#### Physics Model Parameters

| Parameter | Value |
|---|---|
| Panel efficiency | 18% |
| System losses | 85% |
| Temperature coefficient | −0.4% / °C above 25°C STC |
| Cloud-cover derating | Non-linear function of cloud cover fraction |

---

## Data Pipeline

### Weather Data Priority Order

1. **Open-Meteo API** — real-time data and short-term forecasts (primary source)
2. **Historical weather files** — day-of-year pattern matching for past periods
3. **Synthetic generation** — algorithmically generated patterns for six Portuguese reference locations

#### Synthetic Weather Locations

| Location | Region |
|---|---|
| Lisbon | Greater Lisbon |
| Setúbal | Setúbal District |
| Faro | Algarve |
| Braga | Minho |
| Tavira | Eastern Algarve |
| Loulé | Central Algarve |

### Production Dataset

Training and validation data sourced from a peer-reviewed open dataset:

> Sarmas, E., Marinakis, V., Doukas, H. (2025). *Photovoltaic Power Production Dataset*. Mendeley Data, V3.
> DOI: [10.17632/dbh93b6vp8.3](https://doi.org/10.17632/dbh93b6vp8.3)

### Data Storage

| Layer | Technology |
|---|---|
| **User installations** | PHP / Doctrine ORM (SQLite or MySQL) |
| **Training datasets** | Excel files from Mendeley Data |
| **ML models** | joblib-serialised sklearn objects with feature-name persistence |

---

## Infrastructure

### Docker Compose Stack

| Container | Service |
|---|---|
| `nextcloud` | Nextcloud application (PHP + Vue.js frontend) |
| `filantropia-ml:8501` | FastAPI ML microservice |

### Compatibility

| Component | Versions |
|---|---|
| Nextcloud | 28–31 |
| PHP | 8.1–8.4 |

### Background Jobs

| Job | Purpose |
|---|---|
| `WeatherSyncJob` | Periodically fetches and caches weather data from Open-Meteo |
| `PredictionJob` | Pre-computes and caches predictions for active installations |

---

## Role in WeRa Ecosystem

### As the SolarSeed Proposal Calculator

FilantropiaSolar is the **live prototype of the SolarSeed marketplace**. The map and calculator together form the customer-acquisition funnel:

```
Visitor → Live Map → Virtual Simulator (calculator) → Personalised Proposal → €1 Pre-order
```

- Demonstrates real operational installations alongside planning and in-construction sites
- The savings calculator substantiates the **20% minimum guaranteed energy bill reduction** promise
- Supports the lead-generation workflow that converts map visitors into paying SolarSeed customers

### As the REEMS Prototype

The analytics and monitoring features constitute the prototype for the **Renewable Energy & Environmental Management System (REEMS)** — the live energy management dashboard that SolarSeed customers will use once their installations are operational. This aligns with **Iberia Renew Engineering**'s REEMS offering within the WeRa partner ecosystem.

### R&D Asset Value

| Metric | Value |
|---|---|
| **Capitalised R&D — Year 1** | €180,000 |
| **Capitalised R&D — Year 2** | €180,000 |
| **Total (2-year)** | €360,000 |

This value is recognised on the WeRa balance sheet as internally developed software under IAS 38 / IFRS principles, supporting the pre-seed valuation case.

### Positioning Within the KB

| Related KB file | Connection |
|---|---|
| [02-Products.md](02-Products.md) | FilantropiaSolar listed as core software product |
| [04-System-Architecture.md](04-System-Architecture.md) | Listed under Software Stack as energy management layer |
| [07-Customers-and-GTM.md](07-Customers-and-GTM.md) | Map used in proposal flow for customer acquisition |
| [13-Financial-Model.md](13-Financial-Model.md) | Capitalised R&D value (€180k/yr) feeds into asset valuation |

---

*Last updated: April 2026 — v3.0.6*
