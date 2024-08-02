from oraclai.form_nexus.relation_graph import RelationEdge, EdgeType


def create_parent_child_links(spans_2d, relation_graph):
    for y_span, x_spans in spans_2d.items():
        x_nodes = list(x_spans.values())

        for nodes in x_nodes:
            for child_idx in range(1, len(nodes)):
                edge = RelationEdge(nodes[0], nodes[child_idx], EdgeType.CHILD)
                reverse_edge = RelationEdge(nodes[child_idx], nodes[0], EdgeType.PARENT)
                relation_graph.add_edge(edge)
                relation_graph.add_edge(reverse_edge)
    
    return relation_graph