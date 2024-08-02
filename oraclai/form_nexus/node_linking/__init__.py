from .span_ordered_dict import create_2d_span_ordered_dict
from .for_link import create_for_links
from .parent_child_link import create_parent_child_links
from .neighbor_link import create_left_right_links, create_top_bottom_links


def create_base_links(relation_graph):
    spans_2d = create_2d_span_ordered_dict(relation_graph)
    
    relation_graph = create_for_links(relation_graph)
    relation_graph = create_parent_child_links(spans_2d, relation_graph)
    relation_graph = create_left_right_links(spans_2d, relation_graph)
    relation_graph = create_top_bottom_links(spans_2d, relation_graph)

    return relation_graph
