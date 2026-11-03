
from platform import node
import xml.etree.ElementTree as ET

from src.preprocessing.siddham_parser import get_text

NS = "http://www.tei-c.org/ns/1.0"


def test_corrected_reading_is_selected():
    xml = f'<choice xmlns="{NS}"><sic>ph</sic><corr>p</corr></choice>'
    assert get_text(ET.fromstring(xml)) == "p"


def test_original_reading_used_when_no_correction():
    xml = f'<choice xmlns="{NS}"><sic>au</sic></choice>'
    assert get_text(ET.fromstring(xml)) == "au"


def test_unclear_text_is_marked():
    xml = f'<unclear xmlns="{NS}">kṣa</unclear>'
    assert get_text(ET.fromstring(xml)) == "[unclear: kṣa]"


def test_supplied_text_is_marked():
    xml = f'<supplied xmlns="{NS}">samudra</supplied>'
    assert get_text(ET.fromstring(xml)) == "[supplied: samudra]"


def test_gap_attributes_are_preserved():
    xml = f'<gap xmlns="{NS}" reason="illegible" quantity="3" unit="character"/>'
    assert get_text(ET.fromstring(xml)) == "[illegible: 3 character]"


def get_text(element):
    """Extract TEI text while preserving editorial uncertainty."""

    def process(node):
        tag = node.tag.split("}")[-1] if isinstance(node.tag, str) else ""

        if tag == "gap":
            quantity = node.attrib.get("quantity")
            unit = node.attrib.get("unit")
            extent = node.attrib.get("extent")
            reason = node.attrib.get("reason", "unknown")

            if quantity and unit:
                return f"[{reason}: {quantity} {unit}]"
            if extent:
                return f"[{reason}: {extent}]"
            return f"[{reason}]"

        if tag == "lb":
            return " "

        if tag == "choice":
            corr = node.find("{http://www.tei-c.org/ns/1.0}corr")
            sic = node.find("{http://www.tei-c.org/ns/1.0}sic")
            selected = corr if corr is not None else sic

            if selected is not None:
                return process(selected)

        parts = []

        if node.text:
            parts.append(node.text)

        for child in node:
            parts.append(process(child))

            if child.tail:
                parts.append(child.tail)

        content = "".join(parts)

        if tag == "unclear":
            return f"[unclear: {content}]"

        if tag == "supplied":
            return f"[supplied: {content}]"

        return content

    return " ".join(process(element).split())
