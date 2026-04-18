from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "usgs-earthquakes",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

seen = set()

with open("earthquakes.json", "a") as f:
    for message in consumer:
        data = message.value

        quake_id = data["id"]

        # skip duplicates
        if quake_id in seen:
            continue
        seen.add(quake_id)

        props = data["properties"]
        coords = data["geometry"]["coordinates"]

        # clean record
        record = {
            "time": props["time"],
            "magnitude": props["mag"],
            "place": props["place"],
            "longitude": coords[0],
            "latitude": coords[1]
        }

        # save to file
        json.dump(record, f)
        f.write("\n")

        print(f"M {props['mag']} | {props['place']}")