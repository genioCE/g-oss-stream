#!/usr/bin/env bash
set -e
FLINK_PY=jobs/kafka_enrich.py
docker compose exec jobmanager flink run -py /opt/flink/$FLINK_PY /opt/flink/$FLINK_PY || true
