from oraclai.form_nexus.relation_graph import RelationEdge, EdgeType


def spans_overlap(span1, span2):
    if span2[0] >= span1[1] and span2[1] > span1[1]:
        return False
    if span2[1] <= span1[0] and span2[0] < span1[0]:
        return False
    return True


def create_left_right_links(spans_2d, relation_graph):
    for _, x_spans in spans_2d.items():
        x_nodes = list(x_spans.values())
        for node_idx, nodes in enumerate(x_nodes):
            repr_node = nodes[0]
            if node_idx - 1 >= 0:
                repr_left = x_nodes[node_idx - 1][0]
                edge = RelationEdge(repr_node, repr_left, EdgeType.NLEFT)
                relation_graph.add_edge(edge)
            if node_idx + 1 < len(x_nodes):
                repr_right = x_nodes[node_idx + 1][0]
                edge = RelationEdge(repr_node, repr_right, EdgeType.NRIGHT)
                relation_graph.add_edge(edge)

    return relation_graph


def add_row_neighbor_links(relation_graph, node, row, edge_type):
    for nodes in row.values():
        repr_node = nodes[0]
        if spans_overlap(node.x_span, repr_node.x_span):
            edge = RelationEdge(node, repr_node, edge_type)
            relation_graph.add_edge(edge)
    return relation_graph


def create_top_bottom_links(spans_2d, relation_graph):
    rows = list(spans_2d.values())
    for y_idx, (_, x_spans) in enumerate(spans_2d.items()):
        for nodes in x_spans.values():
            repr_node = nodes[0]
            if y_idx - 1 >= 0:
                top_row = rows[y_idx - 1]
                relation_graph = add_row_neighbor_links(
                    relation_graph,
                    repr_node,
                    top_row,
                    EdgeType.NTOP
                )
            if y_idx + 1 < len(spans_2d.keys()):
                bottom_row = rows[y_idx + 1]
                relation_graph = add_row_neighbor_links(
                    relation_graph,
                    repr_node,
                    bottom_row,
                    EdgeType.NBOTTOM
                )
    return relation_graph