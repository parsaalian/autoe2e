from oraclai.form_nexus.relation_graph import RelationEdge, EdgeType
from oraclai.form_nexus.utils import is_input, is_label, is_text, get_normal_cutoff_score


def remove_span_wraps(relation_graph):
    for edge in relation_graph.edges():
        if edge.target.element.name == 'span-wrap':
            child = edge.target
            relation_graph.remove_edge(edge)
            relation_graph.remove_node(child)
    
    return relation_graph


def remove_input_input_links(relation_graph):
    for edge in relation_graph.edges():
        if is_input(edge.source.element) and is_input(edge.target.element):
            relation_graph.remove_edge(edge)
    
    return relation_graph


def keep_highest_scoring_input(relation_graph, node, edge_type):
    edges = node.edges.values()
    input_edges = list(filter(lambda x: is_input(x.target.element), edges))
    sorted_input_edges = sorted(input_edges, key=lambda x: x.weight, reverse=True)
    
    for i in range(1, len(sorted_input_edges)):
        relation_graph.remove_edge(sorted_input_edges[i])
    
    if len(sorted_input_edges) > 0 and not sorted_input_edges[0].type == EdgeType.FOR:
        probable_for_edge = sorted_input_edges[0]
        probable_for_edge.set_type(edge_type)
        
        relation_graph.add_edge(
            RelationEdge(
                probable_for_edge.target,
                probable_for_edge.source,
                probable_for_edge.type,
                probable_for_edge.weight,
            )
        )
    
    return relation_graph


def prune_relation_graph_extra_edges(relation_graph):
    relation_graph = remove_span_wraps(relation_graph)
    relation_graph = remove_input_input_links(relation_graph)
    
    for node in relation_graph.nodes():
        if is_input(node.element):
            continue
        if is_label(node.element):
            relation_graph = keep_highest_scoring_input(
                relation_graph,
                node,
                EdgeType.P_FOR
            )
        elif node.get_is_feedback():
            relation_graph = keep_highest_scoring_input(
                relation_graph,
                node,
                EdgeType.P_FEEDBACK
            )
        elif is_text(node.element):
            relation_graph = keep_highest_scoring_input(
                relation_graph,
                node,
                EdgeType.P_INFO
            )
    
    return relation_graph


def is_certain_edge(edge):
    return edge.type == EdgeType.FOR or \
        edge.type == EdgeType.P_FOR or \
        edge.type == EdgeType.CHILD or \
        edge.type == EdgeType.P_FEEDBACK or \
        edge.type == EdgeType.P_INFO


def prune_low_score_uncertain_edges(relation_graph, factor=0.5):
    scores = []
    for edge in relation_graph.edges():
        if is_certain_edge(edge):
            continue
        scores.append(edge.weight)
    
    cutoff = get_normal_cutoff_score(scores, factor)
    
    for edge in relation_graph.edges():
        if is_certain_edge(edge):
            continue
        if edge.weight < cutoff:
            relation_graph.remove_edge(edge)
    
    return relation_graph