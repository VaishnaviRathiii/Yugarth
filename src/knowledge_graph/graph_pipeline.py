import json
from pathlib import Path

from .graph_builder import KnowledgeGraphBuilder


class KnowledgeGraphPipeline:

    def __init__(self):
        self.builder = KnowledgeGraphBuilder()

    def build_from_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            records = json.load(file)

        for record in records:
            record_id = record.get("record_id")

            if not record_id:
                continue

            # Add document as a graph node
            self.builder.graph.add_node(
                record_id,
                label="DOCUMENT",
                source="historical_record"
            )

            # Add extracted entities and document links
            for entity in record.get("entities", []):
                entity_name = entity.get("text")

                if not entity_name:
                    continue

                self.builder.add_entity(entity)

                self.builder.add_relationship(
                    entity_name,
                    record_id,
                    "APPEARS_IN"
                )

        return self.builder.get_graph()