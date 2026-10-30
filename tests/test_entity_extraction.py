
import unittest

from src.entity_extraction.extractor import HistoricalEntityExtractor


class TestHistoricalEntityExtractor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.extractor = HistoricalEntityExtractor()

    def test_extract_entities(self):
        text = (
            "Ashoka ruled the Mauryan Empire. "
            "Sanchi Stupa is located in Madhya Pradesh."
        )

        entities = self.extractor.extract_entities(text)

        self.assertIsInstance(entities, list)
        self.assertGreater(len(entities), 0)

    def test_person_classification(self):
        entities = self.extractor.extract_entities(
            "Emperor Ashoka ruled the Mauryan Empire."
        )

        self.assertTrue(
            any(
                e["text"] == "Emperor Ashoka"
                and e["label"] == "PERSON"
                for e in entities
            )
        )

    def test_dynasty_classification(self):
        entities = self.extractor.extract_entities(
            "Ashoka belonged to the Mauryan Empire."
        )

        self.assertTrue(
            any(
                e["text"] == "Mauryan Empire"
                and e["label"] == "DYNASTY"
                for e in entities
            )
        )

    def test_artifact_classification(self):
        entities = self.extractor.extract_entities(
            "The Great Stupa at Sanchi is an important monument."
        )

        self.assertTrue(
            any(e["label"] == "ARTIFACT" for e in entities)
        )

    def test_religion_classification(self):
        entities = self.extractor.extract_entities(
            "Ashoka supported Buddhism."
        )

        self.assertTrue(
            any(e["label"] == "RELIGION" for e in entities)
        )

    def test_date_extraction(self):
        entities = self.extractor.extract_entities(
            "Ashoka ruled in the 3rd century BCE."
        )

        self.assertTrue(
            any(e["label"] == "DATE" for e in entities)
        )

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            self.extractor.extract_entities(None)


    def test_site_inside_artifact_name(self):
        entities = self.extractor.extract_entities(
            "The Great Stupa at Sanchi is an important monument."
        )

        self.assertTrue(
            any(
                e["text"] == "Great Stupa at Sanchi"
                and e["label"] == "ARTIFACT"
                for e in entities
            )
        )

        self.assertTrue(
            any(
                e["text"] == "Sanchi"
                and e["label"] == "SITE"
                for e in entities
            )
        )

    def test_unreliable_entities_are_filtered(self):
        entities = self.extractor.extract_entities(
            "Ancient inscriptions provide historical information."
        )

        self.assertFalse(
            any(e["text"] == "Ancient" for e in entities)
        )


if __name__ == "__main__":
    unittest.main()
