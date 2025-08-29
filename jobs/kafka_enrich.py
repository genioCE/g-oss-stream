from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer
import json

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    source = KafkaSource.builder() \        .set_bootstrap_servers("redpanda:9092") \        .set_topics("input-events") \        .set_group_id("flink-group") \        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \        .set_value_only_deserializer(SimpleStringSchema()) \        .build()

    sink = KafkaSink.builder() \        .set_bootstrap_servers("redpanda:9092") \        .set_record_serializer(KafkaRecordSerializationSchema.builder() \            .set_topic("enriched-events") \            .set_value_serialization_schema(SimpleStringSchema()) \            .build()) \        .build()

    ds = env.from_source(source, watermark_strategy=None, source_name="kafka-source")

    def enrich(s):
        try:
            j = json.loads(s)
        except Exception:
            j = {"raw": s}
        j["enriched"] = True
        return json.dumps(j)

    ds.map(enrich).sink_to(sink)

    env.execute("kafka-enrich")

if __name__ == "__main__":
    main()
