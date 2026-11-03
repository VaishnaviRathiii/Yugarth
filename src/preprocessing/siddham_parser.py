
import json
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
XML_DIR = PROJECT_ROOT / "data" / "raw" / "siddham" / "extracted"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "siddham_records.json"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

def get_metadata_value(root, tag):
    element = root.find(f".//{TEI}{tag}")

    if element is None or not element.text:
        return None

    value = element.text.strip()

    if not value or value.lower() == "empty":
        return None

    return value

def get_text(element):
    """Extract TEI text while preserving editorial uncertainty."""

    parts = []

    def process(node):
        if node.text:
            parts.append(node.text)

        for child in node:
            tag = child.tag.split("}")[-1] if isinstance(child.tag, str) else ""

            if tag == "gap":
                attributes = child.attrib

                quantity = attributes.get("quantity")
                unit = attributes.get("unit")
                extent = attributes.get("extent")
                reason = attributes.get("reason", "unknown")

                if quantity and unit:
                    marker = f"[{reason}: {quantity} {unit}]"
                elif extent:
                    marker = f"[{reason}: {extent}]"
                else:
                    marker = f"[{reason}]"

                parts.append(f" {marker} ")

            elif tag == "lb":
                parts.append(" ")

            elif tag == "choice":
                # Prefer corrected reading; fall back to original reading.
                corr = child.find("{http://www.tei-c.org/ns/1.0}corr")
                sic = child.find("{http://www.tei-c.org/ns/1.0}sic")

                selected = corr if corr is not None else sic

                if selected is not None:
                    process(selected)

            elif tag == "unclear":
                parts.append("[unclear: ")
                process(child)
                parts.append("]")

            elif tag == "supplied":
                parts.append("[supplied: ")
                process(child)
                parts.append("]")

            else:
                process(child)

            if child.tail:
                parts.append(child.tail)

    process(element)

    return " ".join("".join(parts).split())


def parse_xml_file(xml_path):
    try:
        root = ET.parse(xml_path).getroot()

        title_element = root.find(
            f".//{TEI}teiHeader/{TEI}fileDesc/{TEI}titleStmt/{TEI}title"
        )
        id_element = root.find(f".//{TEI}idno[@type='filename']")
        edition = root.find(f".//{TEI}text/{TEI}body//{TEI}div[@type='edition']")

        title = (
            "".join(title_element.itertext()).strip()
            if title_element is not None else ""
        )

        record_id = (
            id_element.text.strip()
            if id_element is not None and id_element.text
            else xml_path.stem.replace("_TEI", "")
        )

        text = get_text(edition) if edition is not None else ""

        return {
            "id": record_id,
            "title": title,
            "text": text,
            "language": edition.get(XML_LANG, "") if edition is not None else "",
            "repository": get_metadata_value(root, "repository"),
            "date": get_metadata_value(root, "origDate"),
            "place": get_metadata_value(root, "placeName"),
            "source_type": "Inscription Edition",
            "source_name": "Siddham Texts Archive",
            "source_url": "https://zenodo.org/records/2574362",
            "original_file": xml_path.name
        }

    except ET.ParseError as error:
        print(f"XML parsing failed: {xml_path.name}: {error}")
        return None


def parse_siddham_dataset():
    xml_files = sorted(XML_DIR.glob("*.xml"))

    if not xml_files:
        raise FileNotFoundError(f"No XML files found in: {XML_DIR}")

    records = []
    missing_text = 0
    failed_files = 0

    for xml_file in xml_files:
        record = parse_xml_file(xml_file)

        if record is None:
            failed_files += 1
            continue

        if not record["text"]:
            missing_text += 1
            continue

        records.append(record)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    print(f"XML files discovered: {len(xml_files)}")
    print(f"Records extracted: {len(records)}")
    print(f"Records without edition text: {missing_text}")
    print(f"Files with XML errors: {failed_files}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    parse_siddham_dataset()
