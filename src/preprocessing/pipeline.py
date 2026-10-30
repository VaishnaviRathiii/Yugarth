from src.preprocessing.data_loader import (
    load_historical_data,
    save_processed_data
)

from src.preprocessing.text_cleaner import clean_text


def preprocess_dataset():

    # Step 1: Load raw historical records
    records = load_historical_data()

    processed_records = []

    # Step 2: Process each record
    for record in records:

        if not isinstance(record, dict):
            print("Skipping invalid record.")
            continue

        if not isinstance(record.get("text"), str):
            print(f"Skipping record with invalid text: {record.get('id')}")
            continue

        cleaned_record = record.copy()

        # Clean historical text
        cleaned_record["text"] = clean_text(record["text"])

        processed_records.append(cleaned_record)

    # Step 3: Save processed records
    save_processed_data(processed_records)

    print(f"Total records loaded: {len(records)}")
    print(f"Successfully processed: {len(processed_records)}")


if __name__ == "__main__":
    preprocess_dataset()