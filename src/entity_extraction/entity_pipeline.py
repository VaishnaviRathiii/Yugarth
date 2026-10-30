
import json
from pathlib import Path

from src.entity_extraction.extractor import HistoricalEntityExtractor


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "cleaned_records.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "extracted_entities.json"
)


def load_processed_data():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {INPUT_PATH}")

    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Processed dataset must contain a JSON list.")

    return records


def save_extracted_entities(results):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print(f"Extracted entities saved to: {OUTPUT_PATH}")


def run_entity_pipeline():
    records = load_processed_data()
    extractor = HistoricalEntityExtractor()

    results = []

    for record in records:
        if not isinstance(record, dict):
            continue

        text = record.get("text")

        if not isinstance(text, str):
            continue

        entities = extractor.extract_entities(text)

        results.append({
            "record_id": record.get("id"),
            "source_text": text,
            "entities": entities
        })

    save_extracted_entities(results)

    total_entities = sum(
        len(record["entities"]) for record in results
    )

    print(f"Records processed: {len(results)}")
    print(f"Total entities extracted: {total_entities}")


if __name__ == "__main__":
    run_entity_pipeline()
