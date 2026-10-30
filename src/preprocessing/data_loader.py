import json
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset paths
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "historical_records.json"

PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "cleaned_records.json"
)


def load_historical_data():
    """Load historical records from JSON."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_PATH}"
        )

    with open(RAW_DATA_PATH, "r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Dataset must contain a JSON list.")

    return records


def save_processed_data(records):
    """Save processed records into JSON."""

    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True, exist_ok=True
    )

    with open(PROCESSED_DATA_PATH, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    print(f"Processed data saved to: {PROCESSED_DATA_PATH}")