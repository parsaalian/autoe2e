from tqdm import tqdm

from .relation_graph import RelationGraph
from .relation_node import RelationNode
from .relation_edge import RelationEdge, EdgeType


def create_relation_graph(bs_doc, text_embedding_method='ADA'):
    graph = RelationGraph()
    
    for n in tqdm(bs_doc):
        node = RelationNode(n, text_embedding_method)
        graph.add_node(node)

    return graph


__all__ = [
    'RelationGraph',
    'RelationNode',
    'RelationEdge',
    'EdgeType',
    'create_relation_graph',
]