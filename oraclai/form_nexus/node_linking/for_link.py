from oraclai.form_nexus.relation_graph import RelationEdge, EdgeType


def create_for_links(relation_graph):
    for node in relation_graph.nodes():
        if 'for' in node.element.attrs:
            try:
                source = relation_graph.get_node(node.get_id())
                
                for_id = node.element.attrs['for']
                target = relation_graph.get_node(for_id)
                
                edge = RelationEdge(source, target, EdgeType.FOR)
                relation_graph.add_edge(edge)
                
                reverse_edge = RelationEdge(target, source, EdgeType.FOR)
                relation_graph.add_edge(reverse_edge)
            except Exception as e:
                print(e)

    return relation_graph