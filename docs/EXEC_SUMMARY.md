[EXEC_SUMMARY_stream.md](https://github.com/user-attachments/files/22052405/EXEC_SUMMARY_stream.md)
# EXECUTIVE SUMMARY — Open-Source Data Platform for Oil & Gas

> **Replace proprietary data tooling with a modular, open stack.** Lower license spend, remove lock-in, standardize on open formats, and keep operational risk low with phased cutovers.

This document is designed for CIOs/CTOs. It explains the **business case, risk posture, SLOs, rollout plan, and KPIs** for the module in this repository.

---

## 1) What this repository is

- **Module:** g-oss-stream (Streaming compute)
- **Purpose:** Apache Flink jobs to enrich/aggregate events before landing to Iceberg/TSDB.
- **Primary components:** Apache Flink, Kafka/Redpanda
- **Replaces / reduces:** Informatica streaming ETL, StreamSets (streaming)
- **Integrates with:** g-oss-cdc (topics), g-oss-core (Iceberg), g-oss-observability (lag/errors)

**Outcome:** A vendor-neutral building block that slots into the broader platform without forcing a rip-and-replace of everything at once.

---

## 2) Why open source for O&G (now)

- **License compression:** Shift recurring license fees to a smaller, predictable ops + support budget.
- **Open formats:** Iceberg/Parquet + Kafka APIs keep you portable across clouds and engines.
- **Talent alignment:** SQL, dbt, Kafka, Airflow are widely available skills; easier hiring and cross-training.
- **Security posture:** Centralized SSO (Keycloak), secrets (Vault), policy-as-code (OPA) align with modern controls.
- **Control-room safety:** Analytics mirrors remain **read-only**; no interference with SCADA/OT write paths.

---

## 3) Architecture at a glance

```
[OPC UA/MQTT/CDC/Kafka] → Flink → (Kafka/Iceberg/TSDB)
```

This repository delivers the **g-oss-stream (Streaming compute)** segment of that picture.

---

## 4) Common oil & gas use cases (examples)

- Unit normalization and tag cleanup in-flight
- Rolling windows for rate/pressure alerts
- Dedup/late event handling with event time

---

## 5) Service levels (default targets)

| Metric | Target (Phase 1) | Target (Phase 2) | Notes |
|---|---:|---:|---|
| Freshness (batch) | ≤ 2h | ≤ 30m | Measured from source close to availability |
| Stream latency (P95) | ≤ 60s | ≤ 10–30s | CDC or stream path end-to-end |
| Pipeline success rate | ≥ 99.5% | ≥ 99.9% | Excluding planned maintenance |
| MTTR (failed run) | < 30 min | < 15 min | Runbooks + on-call |
| Data completeness | ≥ 99.7% | ≥ 99.9% | Counts/continuity checks |
| Data accuracy | ≥ 99.5% | ≥ 99.8% | DQ gates (ranges, referential integrity) |
| RPO (data loss window) | ≤ 5 min | ≤ 1 min | Kafka retention + checkpoints |
| RTO (resume time) | ≤ 30 min | ≤ 10 min | Automation + IaC |

**Module-specific SLO notes:**  
- **Stream latency P95 ≤ 2s** for typical flows; strict bounds require sizing/tuning.

---

## 6) Security & compliance (baseline)

- **SSO / Identity:** All UIs behind **OIDC/SAML via Keycloak** (see Security module).
- **Secrets:** No `.env` in repos; use **Vault** with rotation and audit.
- **Policy:** Authorization as code with **OPA/Rego**; dataset contracts in CI.
- **Network:** Segmented subnets; **read-only** taps from OT gateways; **no control writes**.
- **Encryption:** TLS in transit; object store policies; optional envelope encryption.
- **Auditability:** OpenLineage + Git history + Nessie table commits provide end-to-end traceability.

---

## 7) Rollout plan (risk-controlled)

1. **Pilot (0–90 days)**  
   - Stand up `g-oss-stream (Streaming compute)` in a sandbox; connect a *low-risk* data domain.  
   - Define **acceptance** SLOs + DQ gates; instrument Observability dashboards.

2. **Parallel run (90–180 days)**  
   - Mirror 3–5 representative workflows.  
   - Compare counts, freshness, KPIs; user acceptance in BI/consuming apps.

3. **Cutover & scale (180–365 days)**  
   - Switch consumers to OSS outputs; keep legacy as fallback for a limited time.  
   - Expand to additional domains; formalize training/handover.

**Exit criteria per cutover:** SLOs met for 2+ consecutive weeks, variance within thresholds, rollback path tested.

---

## 8) Cost & ROI frame

| Line item | Notes |
|---|---|
| **License spend removed** | Identify SKUs replaced by this module (annualized) |
| **Compute & storage** | Cloud/on-prem costs for the module’s services |
| **Ops & support** | SRE time + optional vendor support contracts |
| **Migration project** | One-time engineering (parallel run + cutover) |
| **Net 24–36 mo TCO** | Compare to current vendor TCO, not just list price |

**Typical wins:** 30–60% lower run-rate on the replaced capability, faster delivery (jobs-as-code), and avoided lock-in.

---

## 9) KPIs for leadership

- **Value:** license $ removed, $/TB processed, time-to-provision dataset, adoption (active users/dashboards/jobs).
- **Reliability:** freshness, success rate, MTTR, RPO/RTO adherence.
- **Quality:** % models with tests, DQ failure rate, lineage coverage.
- **Security:** % services behind SSO, secrets in Vault, policy violations blocked.

---

## 10) Risks & mitigations

- **State growth** → Set TTLs; monitor checkpoints; scale with keyed partitioning.
- **Backpressure** → Autoscale; monitor lag; tune source/sink parallelism.
- **OT safety** → Analytics-only; separate networks; no control writes.

---

## 11) Operating model (who does what)

- **Platform (SRE):** owns clusters, observability, backups, upgrades.
- **Data Engineering:** owns pipelines, dbt models, DQ gates, lineage.
- **Security:** owns SSO, secrets, network policy, audit.
- **OT/SCADA:** approves mirrors; ensures control-path isolation.
- **Business owners:** accept cutovers; validate SLAs and reports.

---

## 12) Proprietary → OSS mapping (quick reference)

- StreamSets/Informatica streaming → Apache Flink
- Custom stream scripts → Flink SQL / DataStream

---

## 13) How Genio fits (value add)

Genio’s **heads/loops** attach to the open data plane to add memory, summarization, QA, retrieval, and automation. OSS keeps the data accessible and auditable, while Genio focuses on **cognition** (not basic plumbing).

---

## 14) Next steps (checklist)

- [ ] Replace placeholders in this file with any client-specific details.
- [ ] Define module-level SLOs and DQ gates; publish dashboards.
- [ ] Select 1–3 pilot workflows; plan parallel run & cutover.
- [ ] Document rollback criteria; run a failover test.
- [ ] Create a 1-page “Runbook” and a 3-slide board update (value, risk, plan).

---

**Contacts & ownership:**  
- **Executive sponsor:** _TBD_  
- **Platform owner:** _TBD_  
- **Data engineering lead:** _TBD_  
- **Security lead:** _TBD_  
- **OT/SCADA contact:** _TBD_
