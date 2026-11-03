
import json
from pathlib import Path

from src.preprocessing.text_cleaner import clean_text

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "siddham_records.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "cleaned_siddham_records.json"


def preprocess_dataset():

    # Step 1: Load Siddham historical records
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Dataset must contain a JSON list.")

    processed_records = []

    # Step 2: Clean each historical inscription
    for record in records:

        if not isinstance(record, dict):
            print("Skipping invalid record.")
            continue

        if not isinstance(record.get("text"), str):
            print(f"Skipping record with invalid text: {record.get('id')}")
            continue

        cleaned_record = record.copy()
        cleaned_record["text"] = clean_text(record["text"])

        processed_records.append(cleaned_record)

    # Step 3: Save processed Siddham records
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            processed_records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n--- Siddham Preprocessing Report ---")
    print(f"Total records loaded: {len(records)}")
    print(f"Successfully processed: {len(processed_records)}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    preprocess_dataset()
