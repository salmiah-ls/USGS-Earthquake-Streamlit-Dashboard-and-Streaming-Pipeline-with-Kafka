from kafka import KafkaProducer
import requests
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

while True:
    data = requests.get(URL).json()

    for feature in data["features"]:
        producer.send("usgs-earthquakes", feature)

    print("Sent data to Kafka")
    time.sleep(60)
