class GraphQueries:

    def __init__(self, graph):
        self.graph = graph

    def get_all_entities(self):
        return list(self.graph.nodes(data=True))

    def get_entity_details(self, entity_name):
        if entity_name not in self.graph:
            return None

        return {
            "entity": entity_name,
            "attributes": self.graph.nodes[entity_name],
            "relationships": list(
                self.graph.edges(entity_name, data=True)
            )
        }

    def get_connected_entities(self, entity_name):
        if entity_name not in self.graph:
            return []

        return list(self.graph.neighbors(entity_name))

    def get_entity_count(self):
        return self.graph.number_of_nodes()

    def get_relationship_count(self):
        return self.graph.number_of_edges()