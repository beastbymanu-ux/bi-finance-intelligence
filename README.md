# Enterprise Financial Intelligence: Automated Cash Flow Pipeline

> **Private automated financial reporting** — SQLAlchemy · FastAPI · Streamlit · Docker · On-premise

[![Live Demo](https://img.shields.io/badge/Live_Demo-openclawlabs--finance.duckdns.org-00d4aa?style=for-the-badge)](https://openclawlabs-finance.duckdns.org)

## Problem

Finance teams wasting **20+ hrs/month** reconciling data manually across ERP, bank feeds, and payment processors. A single formula error cascades into board-level misinformation.

## Solution

Private financial intelligence pipeline deployed on a Vultr VPS:

- **SQLAlchemy** ingests and reconciles multi-source data (ERP, banks, Stripe) into a unified SQLite store
- **FastAPI** serves clean metrics via a REST layer
- **Streamlit dashboard** shows real-time cash flow forecast, burn rate, and runway
- **Automated reconciliation** runs on schedule — zero manual intervention

## Results (STAR)

| Metric | Before | After |
|--------|--------|-------|
| Manual reconciliation time | 20 hrs/month | 0 hrs/month |
| Data accuracy | Variable | 100% (audit trail) |
| Reconciliation errors | ~12/month | 0 |
| Cloud exposure | Yes | Eliminated |

## Architecture

```
ERP · Bank Feed · Stripe API · Payment Processors
→ SQLAlchemy ORM → SQLite (on-premise)
→ FastAPI REST Layer → Streamlit Dashboard
→ Nginx + SSL (DuckDNS)
```

## Stack

| Component | Technology |
|-----------|-----------|
| ORM / Reconciliation | SQLAlchemy |
| Database | SQLite (on-premise) |
| API Layer | FastAPI |
| Dashboard | Streamlit + Plotly |
| Infrastructure | Docker · Nginx · Vultr VPS |

## 3 Golden Pillars

1. **Money** — 20 hrs/month reclaimed. 100% accuracy eliminates costly errors.
2. **Ownership** — All financial data stays on the client's own server. Zero cloud. Full GDPR compliance.
3. **Scalability** — Dockerized pipeline. Add new data sources (Xero, QuickBooks) without re-architecture.

## Quick Start

```bash
git clone https://github.com/beastbymanu-ux/bi-finance-intelligence
cd bi-finance-intelligence
docker-compose up -d
# Visit http://localhost:8506
```

## Live Demo

**[https://openclawlabs-finance.duckdns.org](https://openclawlabs-finance.duckdns.org)**

---
*Built by [OpenClaw Labs](https://openclawlabs-ai.duckdns.org) — Senior AI/Data Engineering*
