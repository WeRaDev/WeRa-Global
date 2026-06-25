# 04 — System Architecture

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `KnowledgeBase/04-System-Architecture.md`
- consolidation_date: `2026-04-27`
- consolidation_status: `canonicalized`


---

## Overview

WeRa operates a **federated infrastructure** where each SolarSeed node acts as a self-contained server within a distributed network. The architecture draws from Kubernetes-like clustering principles, with nodes coordinating as a virtual power plant and virtual data centre simultaneously.

---

## Architecture Layers

SolarSeed follows an **energy-first** design principle: the product is primarily energy infrastructure with digital services as a value multiplier deployed only after energy-layer stability is confirmed.

### Layer E — Energy Hosting Core (Primary)

| Sub-layer | Function | Hardware (Base) | Hardware (Avg) |
|---|---|---|---|
| **E1 Generation** | PV field sized by demand + irradiation | 6× YH SUNPRO 505W (3.03 kWp) | 16× AIKO Neostar 500W (8 kWp) |
| **E2 Conversion** | MPPT + inverter (DC/AC) | Voltronic Axpert MKS 3K-24 (3 kW, 93% peak) | Huawei SUN2000-10K-LC0 (10 kW, 3 MPPT, IP66) |
| **E3 Storage** | Battery bank for critical-load autonomy | 2× TAB Monoblock 12V 250Ah (~6 kWh) | 3× Huawei LUNA2000 5kWh LFP (15 kWh, IP66) |
| **E4 Distribution** | Protected AC/DC circuits, load segregation | Basic protection panel | Huawei SmartGuard-63A-S0 (≤20ms switchover, EMMA) |
| **E5 Telemetry** | Production, SOC, load monitoring | Included | Huawei Smart Power Sensor DDSU666-H + production meter |

### Layer D — Digital Hosting Add-On (Secondary)

Deployed only after E-layer stability is confirmed:

| Component | Base Config | Avg Config |
|---|---|---|
| **Compute** | 1× GEEKOM GT1 Mega (Core Ultra 9 185H, 32GB DDR5, 2TB NVMe, Intel NPU) | 2× GEEKOM GT1 Mega |
| **Connectivity** | ZTE Router 5G MU5002 (Wi-Fi 7, 5G) | Same |
| **Storage** | Samsung 4TB SSD (USB 3.2) | Same |
| **Power draw** | ~264W continuous | ~464W continuous |
| **Daily energy need** | ~6.34 kWh/day | ~11.1 kWh/day |
| **Battery-only runtime** | ~18–23 hours | ~12–16 hours |

Digital services hosted:
- Private cloud / data workloads (Nextcloud)
- Observability and operations stack
- Local AI inference endpoint (NPU-accelerated)
- Edge automations linked to energy state

### Layer 3: Cloud Services (WERA Cloud)

- **Nextcloud-based** collaboration platform
- Files, calendar, chat, video, office suite, AI assistant
- End-to-end encryption; GDPR compliance
- Each SolarSeed hosts a node in the federation
- Data stays local — nothing leaks, not even metadata
- Own capacity: 5,000 GB per SolarSeed (100 quotas at base)
- Backup capacity: Hetzner at €0.0047/GB (113,000 GB per server at €526/month)

### Layer 4: Tokenization (Polygon / DDR)

- **Polygon blockchain** for all on-chain operations
- **Digital Depositary Receipts (DDRs)** represent tokenized shares
- Three token types: WeD (utility), WeP (staking), WeG (bonding)
- Smart contracts for energy trading, governance, rewards

### Layer 5: Intelligence (AI Services)

- **Local AI API** on each SolarSeed node
- Intel AI Boost NPU: 8× AI efficiency improvement vs prior gen
- Federated multi-agent architecture routing requests to nearest solar-powered node
- AI agent creation, automation, management (Intelligence Hub)
- Active Inference agent model ("Spirit") — exists only in the flow of computation, surviving by serving
- Future: City of Light gamified interface

---

## Energy-First Control Principle

> "Energy budget before compute budget"

### Appliance Classification

| Class | Examples | Priority |
|---|---|---|
| **A (Critical)** | Water pumping, refrigeration, essential lighting, control gateways | Always preserved |
| **B (Important)** | Communications, office endpoints, routine automation | Reduced at low SOC |
| **C (Deferrable)** | Non-urgent compute, batch AI tasks, background sync | Suspended at low SOC |

### Energy-State Policy

| State | Action |
|---|---|
| **High PV / High SOC** | Full service set, including heavy AI/inference windows |
| **Medium SOC** | Keep A+B, throttle C |
| **Low SOC** | Preserve A, reduce B, suspend C until recovery |

Design rule: no critical server service is defined without an explicit energy budget and fallback behavior.

---

## Federated Model

```
SolarSeed Node A ──┐
SolarSeed Node B ──┤── Federated Cloud ── WERA Cloud API
SolarSeed Node C ──┤                      ├── AI Services
SolarSeed Node D ──┘                      ├── Storage Services
                                          └── Token Services
```

- **No central server dependency** — nodes form a mesh
- **Gateway Server** — primary coordination node (€22,000 budget allocation)
- **Virtual Power Plant** — coordinated energy production/storage across all nodes
- **Virtual Data Centre** — combined compute/storage capacity sold as cloud services

---

## 3-Stage Data Value Chain

1. **Collection** — IoT sensors on SolarSeed hardware generate energy + environmental data
2. **Processing** — Local AI on NPU processes data at the edge (low latency, privacy-preserving)
3. **Value extraction** — Aggregated insights sold as services; data never leaves the node raw

---

## Security

- **Quantum-resistant security** — referenced as aspirational target (Sunified hardware; not yet engaged as partner)
- **End-to-end encryption** — all WERA Cloud communications
- **Byzantine Fault Tolerance (BFT)** — governance cascade across three entities
- **Privacy-preserving** — federated architecture ensures data stays local
- **GDPR compliance** — by design in WERA Cloud

---

## Software Stack

| Component | Technology |
|---|---|
| **Energy management** | FilantropiaSolar (Python backend, beta) — Capitalised R&D: €180k/yr |
| **Cloud platform** | Nextcloud (self-hosted per SolarSeed) |
| **Blockchain** | Polygon (EVM-compatible, PoS) |
| **Smart contracts** | Solidity (ERC-compatible) |
| **AI inference** | Intel Core Ultra NPU + federated routing (GEEKOM GT1 Mega) |
| **Compute OS** | Linux (TBC distro) |
| **Database** | TBC |
| **Frontend** | TBC |

---

## Capacity Planning

| Metric | Per SolarSeed (Base 3.03 kWp) | Per SolarSeed (Avg 8 kWp) | Network of 100 units (Base) | Network of 1,000 units (Y2) |
|---|---|---|---|---|
| PV peak generation | 3.03 kWp | 8 kWp | 303 kWp | 3,030 kWp–8,000 kWp |
| Daily PV output | 9–14 kWh | ~28–44 kWh | 900–1,400 kWh | 9,000–44,000 kWh |
| Battery storage | ~6 kWh | ~15 kWh | ~600 kWh | ~6,000–15,000 kWh |
| Compute | 1× GT1 Mega (16 cores, NPU) | 2× GT1 Mega (32 cores, 2 NPUs) | 100–200 nodes | 1,000–2,000 nodes |
| Local cloud storage | 4 TB SSD (5,000 GB quotas) | 4 TB SSD (5,000 GB quotas) | 400 TB | 4,000 TB |
| Continuous power draw (digital) | ~264 W | ~464 W | ~26.4 kW | ~264–464 kW |

### Reference Benchmarks

| Source | PV Capacity | Annual Output | Specific Yield | Location |
|---|---|---|---|---|
| ARS Sustineri [R2] | 0.6–1.0 kWp | 840–1,387 kWh | — | Farm context |
| Components baseline [R1] | 3.03 kWp | 3,322–5,183 kWh | — | General |
| São Martinho SmartDesign [R3] | 29.5 kWp | 41,374 kWh | 1,402.5 kWh/kWp/yr | Funchal, Meteonorm |

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.key_resources.architecture_04_system_architecture
  proof_artifact: kb-governance/formal-proofs/key-resources-architecture-04-system-architecture.lean
  verification_status: verified
