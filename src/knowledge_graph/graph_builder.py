import networkx as nx


class KnowledgeGraphBuilder:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_entity(self, entity):
        entity_name = entity.get("text")

        if not entity_name:
            return

        self.graph.add_node(
            entity_name,
            label=entity.get("label", "UNKNOWN"),
            source=entity.get("source", "unknown")
        )

    def add_relationship(self, source, target, relation):
        if source not in self.graph or target not in self.graph:
            return

        self.graph.add_edge(
            source,
            target,
            relation=relation
        )

    def get_graph(self):
        return self.graph