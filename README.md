# g-oss-stream

Flink streaming with Redpanda/Kafka + example PyFlink job (Kafka → Kafka).

## Run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r jobs/requirements.txt
# start infra
docker compose up -d
# submit job
bash scripts/submit.sh
```
- Flink UI: http://localhost:8082
- Redpanda Console: http://localhost:8080
