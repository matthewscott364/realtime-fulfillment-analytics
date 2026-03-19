import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

OUTPUT_DIR = "/data/events"
os.makedirs(OUTPUT_DIR, exist_ok=True)

EVENT_TYPES = [
    "order_created",
    "item_picked",
    "item_packed",
    "shipment_loaded",
    "delay_flag",
    "inventory_adjustment"
]

FACILITIES = ["TTN2", "EWR4", "TEB9", "PHL7"]
STATIONS = ["PICK-01", "PICK-14", "PACK-02", "DOCK-03", "ICQA-01"]
STATUSES = ["success", "success", "success", "warning", "error"]

def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "event_time": datetime.now(timezone.utc).isoformat(),
        "event_type": random.choice(EVENT_TYPES),
        "facility_id": random.choice(FACILITIES),
        "station_id": random.choice(STATIONS),
        "associate_id": f"A{random.randint(1000, 9999)}",
        "order_id": f"O{random.randint(100000, 999999)}",
        "sku_id": f"SKU{random.randint(1000, 9999)}",
        "quantity": random.randint(1, 5),
        "status": random.choice(STATUSES),
        "processing_seconds": random.randint(5, 120)
    }

def write_event_file():
    event = generate_event()
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    file_path = os.path.join(OUTPUT_DIR, f"event_{ts}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(event, f)

    print(f"Wrote {file_path}")

if __name__ == "__main__":
    while True:
        write_event_file()
        time.sleep(2)