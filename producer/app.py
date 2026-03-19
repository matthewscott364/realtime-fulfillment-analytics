import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

BASE_OUTPUT_DIR = "/data/events"

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
SHIFTS = ["DAY", "NIGHT", "RT"]
REGIONS = ["NORTHEAST", "MIDATLANTIC"]
DELAY_REASONS = ["traffic", "inventory_shortage", "labor_gap", "system_issue", None]
EVENT_SOURCES = ["scanner", "wms", "manual_entry", "sensor"]


def generate_event():
    now_utc = datetime.now(timezone.utc)
    event_type = random.choice(EVENT_TYPES)
    status = random.choice(STATUSES)

    return {
        "event_id": str(uuid.uuid4()),
        "event_time": now_utc.isoformat(),
        "event_type": event_type,
        "facility_id": random.choice(FACILITIES),
        "region": random.choice(REGIONS),
        "station_id": random.choice(STATIONS),
        "associate_id": f"A{random.randint(1000, 9999)}",
        "order_id": f"O{random.randint(100000, 999999)}",
        "sku_id": f"SKU{random.randint(1000, 9999)}",
        "quantity": random.randint(1, 5),
        "units_per_event": random.randint(1, 20),
        "shift": random.choice(SHIFTS),
        "status": status,
        "processing_seconds": random.randint(5, 120),
        "delay_reason": random.choice(DELAY_REASONS) if event_type == "delay_flag" else None,
        "event_source": random.choice(EVENT_SOURCES)
    }


def get_partition_path(event_time_str: str) -> str:
    dt = datetime.fromisoformat(event_time_str)
    return os.path.join(
        BASE_OUTPUT_DIR,
        dt.strftime("%Y"),
        dt.strftime("%m"),
        dt.strftime("%d")
    )


def write_event_file():
    event = generate_event()
    partition_dir = get_partition_path(event["event_time"])
    os.makedirs(partition_dir, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    file_path = os.path.join(partition_dir, f"event_{ts}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(event, f)

    print(f"Wrote {file_path}")


if __name__ == "__main__":
    while True:
        write_event_file()
        time.sleep(2)