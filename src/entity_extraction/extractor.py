
import re
import spacy

from spacy.matcher import PhraseMatcher
from src.entity_extraction.entity_normalizer import EntityNormalizer


class HistoricalEntityExtractor:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.normalizer = EntityNormalizer()

        self.matcher = PhraseMatcher(
            self.nlp.vocab,
            attr="LOWER"
        )

        self.custom_patterns = {
            "PERSON": [
                "Ashoka",
                "Emperor Ashoka"
            ],

            "DYNASTY": [
                "Mauryan Empire",
                "Mauryan dynasty"
            ],

            "SITE": [
                "Sanchi"
            ],

            "ARTIFACT": [
                "Great Stupa at Sanchi",
                "Sanchi Stupa",
                "Ashoka Pillar",
                "Ashokan inscriptions"
            ],

            "EVENT": [
                "Kalinga War",
                "construction of Sanchi Stupa"
            ],

            "RELIGION": [
                "Buddhism",
                "Buddhist"
            ]
        }

        for label, phrases in self.custom_patterns.items():
            patterns = [
                self.nlp.make_doc(phrase)
                for phrase in phrases
            ]

            self.matcher.add(label, patterns)

    def extract_entities(self, text):

        if not isinstance(text, str):
            raise TypeError("Input must be a string.")

        doc = self.nlp(text)
        candidates = []

        # Extract recognized spaCy entities
        for ent in doc.ents:

            label = self.normalizer.normalize_label(ent.label_)

            # Ignore unreliable generic classifications
            if label == "OTHER":
                continue

            candidates.append({
                "text": self.normalizer.normalize(ent.text),
                "original_label": ent.label_,
                "label": label,
                "source": "spacy",
                "start": ent.start_char,
                "end": ent.end_char
            })

        # Extract custom historical entities
        matches = self.matcher(doc)

        for match_id, start, end in matches:

            span = doc[start:end]
            label = self.nlp.vocab.strings[match_id]

            candidates.append({
                "text": self.normalizer.normalize(span.text),
                "original_label": None,
                "label": label,
                "source": "custom_rule",
                "start": span.start_char,
                "end": span.end_char
            })

        # Extract historical dates
        date_pattern = (
            r"\b\d+(?:st|nd|rd|th)?\s+century\s+"
            r"(?:BCE|CE|BC|AD)\b"
            r"|\b\d{1,4}\s*(?:BCE|CE|BC|AD)\b"
        )

        for match in re.finditer(
            date_pattern, text, re.IGNORECASE
        ):

            candidates.append({
                "text": self.normalizer.normalize(match.group()),
                "original_label": None,
                "label": "DATE",
                "source": "date_rule",
                "start": match.start(),
                "end": match.end()
            })

        # Prefer custom rules and longer entity names
        candidates.sort(
            key=lambda item: (
                item["source"] != "custom_rule",
                -(item["end"] - item["start"])
            )
        )

        selected = []

        for candidate in candidates:

            conflict = False

            for existing in selected:

                overlaps = (
                    candidate["start"] < existing["end"]
                    and candidate["end"] > existing["start"]
                )

                if not overlaps:
                    continue

                # Remove duplicate classifications and
                # generic spaCy predictions overlapping
                # with custom historical entities.
                if (
                    candidate["label"] == existing["label"]
                    or candidate["source"] == "spacy"
                    or existing["source"] == "spacy"
                ):
                    conflict = True
                    break

            if not conflict:
                selected.append(candidate)

        # Return clean results without internal positions
        results = []

        for entity in selected:
            results.append({
                "text": entity["text"],
                "original_label": entity["original_label"],
                "label": entity["label"],
                "source": entity["source"]
            })

        return results


if __name__ == "__main__":

    extractor = HistoricalEntityExtractor()

    sample = (
        "The Great Stupa at Sanchi is an important "
        "Buddhist monument associated with Emperor Ashoka."
    )

    for entity in extractor.extract_entities(sample):
        print(entity)
