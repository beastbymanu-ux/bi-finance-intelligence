# Enterprise Financial Intelligence: Automated Cash Flow Pipeline

> Own project by Manu (OpenClaw Labs), built and tested with demo data. Not a client deployment.

> **Private automated financial reporting** — SQLAlchemy · FastAPI · Streamlit · Docker · On-premise

## Problem

Finance teams wasting **20+ hrs/month** reconciling data manually across ERP, bank feeds, and payment processors. A single formula error cascades into board-level misinformation.

## Solution

Private financial intelligence pipeline designed to run on a private VPS:

- **SQLAlchemy** ingests and reconciles multi-source data (ERP, banks, Stripe) into a unified SQLite store
- **FastAPI** serves clean metrics via a REST layer
- **Streamlit dashboard** shows real-time cash flow forecast, burn rate, and runway
- **Automated reconciliation** runs on schedule — zero manual intervention

## Architecture

```
ERP · Bank Feed · Stripe API · Payment Processors
→ SQLAlchemy ORM → SQLite (on-premise)
→ FastAPI REST Layer → Streamlit Dashboard
```

## Stack

| Component | Technology |
|-----------|-----------|
| ORM / Reconciliation | SQLAlchemy |
| Database | SQLite (on-premise) |
| API Layer | FastAPI |
| Dashboard | Streamlit + Plotly |
| Infrastructure | Docker · Nginx · private VPS |

## Design principles

1. **Ownership** — All financial data stays on the your own server. Zero cloud. Full GDPR compliance.
2. **Scalability** — Dockerized pipeline. Add new data sources (Xero, QuickBooks) without re-architecture.

## Quick Start

```bash
git clone https://github.com/beastbymanu-ux/bi-finance-intelligence
cd bi-finance-intelligence
docker-compose up -d
# Visit http://localhost:8506
```
