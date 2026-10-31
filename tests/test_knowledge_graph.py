from src.knowledge_graph import (
    KnowledgeGraphBuilder,
    RelationshipAnalyzer,
    GraphQueries
)


def test_add_entities():
    builder = KnowledgeGraphBuilder()
    builder.add_entity({"text": "Ashoka", "label": "PERSON"})
    assert "Ashoka" in builder.get_graph()


def test_add_relationship():
    builder = KnowledgeGraphBuilder()
    builder.add_entity({"text": "Ashoka", "label": "PERSON"})
    builder.add_entity({"text": "Mauryan Empire", "label": "ORGANIZATION"})

    builder.add_relationship("Ashoka", "Mauryan Empire", "RULED")

    assert builder.get_graph().has_edge("Ashoka", "Mauryan Empire")


def test_relationship_analyzer():
    builder = KnowledgeGraphBuilder()
    builder.add_entity({"text": "Ashoka"})
    builder.add_entity({"text": "Mauryan Empire"})
    builder.add_relationship("Ashoka", "Mauryan Empire", "RULED")

    analyzer = RelationshipAnalyzer(builder.get_graph())
    assert len(analyzer.find_relationships("Ashoka")) == 1


def test_graph_queries():
    builder = KnowledgeGraphBuilder()
    builder.add_entity({"text": "Ashoka"})
    builder.add_entity({"text": "Sanchi"})
    builder.add_relationship("Ashoka", "Sanchi", "ASSOCIATED_WITH")

    queries = GraphQueries(builder.get_graph())

    assert queries.get_entity_count() == 2
    assert queries.get_relationship_count() == 1