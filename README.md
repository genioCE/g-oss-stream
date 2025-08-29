# g-oss-stream · Streaming compute (Apache Flink)

**Audience:** O&G CIOs/CTOs and streaming/data science leads  
**Goal:** Stateful enrichment/aggregation for SCADA/meter streams and event pipelines.

---

## Executive summary
- **What it is:** **Apache Flink** with an example PyFlink job (Kafka → Kafka) to enrich events before landing to Iceberg/TSDB.  
- **What it replaces:** Proprietary streaming ETL (Informatica streaming/StreamSets).  
- **Outcomes:** Lower latency analytics, feature engineering for anomaly detection, and consistent schemas before storage.

## Where it fits
```
[OPC UA/MQTT/CDC] -> Kafka topics -> Flink jobs -> (Kafka/Iceberg/TSDB)
```
Keep **control systems** strictly separate—this is analytics only.

## O&G use cases
- Tag normalization & unit conversions in‑flight.  
- Rolling window rates/pressures for alerting.  
- Deduplication and late‑arrival handling with event time.

## Pilot SLOs
- **End‑to‑end stream latency:** P95 < 2s.  
- **Processing uptime:** ≥ 99.9% in business hours.

## Security & compliance
- Network‑segmented read‑only taps from OT gateways; no write‑back.  
- Observability via `g-oss-observability` (lag, errors, throughput).

## KPIs for leadership
- Lag, dropped/late events, false‑positive/negative rates (if used for alerts).

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r jobs/requirements.txt
docker compose up -d
bash scripts/submit.sh
# Flink UI: http://localhost:8082
```
