class RelationshipAnalyzer:

    def __init__(self, graph):
        self.graph = graph

    def find_relationships(self, entity_name):
        if entity_name not in self.graph:
            return []

        relationships = []

        for source, target, data in self.graph.out_edges(
            entity_name, data=True
        ):
            relationships.append({
                "source": source,
                "target": target,
                "relation": data.get("relation", "RELATED_TO")
            })

        for source, target, data in self.graph.in_edges(
            entity_name, data=True
        ):
            relationships.append({
                "source": source,
                "target": target,
                "relation": data.get("relation", "RELATED_TO")
            })

        return relationships