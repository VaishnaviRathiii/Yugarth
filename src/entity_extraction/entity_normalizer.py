
import re


class EntityNormalizer:

    def normalize(self, entity_text):
        """Normalize whitespace without changing the original meaning."""

        if not isinstance(entity_text, str):
            raise TypeError("Entity must be a string.")

        return re.sub(r"\s+", " ", entity_text).strip()

    def normalize_label(self, label):
        """Map reliable generic spaCy labels to YUGARTH categories."""

        label_mapping = {
            "PERSON": "PERSON",
            "FAC": "ARTIFACT",
            "DATE": "DATE"
        }

        return label_mapping.get(label, "OTHER")
