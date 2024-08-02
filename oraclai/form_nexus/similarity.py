import numpy as np
from scipy.spatial import distance

from oraclai.form_nexus.relation_graph import EdgeType


def get_text_similarity(node1, node2):
    embedding1 = node1.features
    embedding2 = node2.features
    try:
        sim = 1 - distance.cosine(embedding1, embedding2)
        return 0 if np.isnan(sim) else sim
    except:
        return 0


def get_structure_similarity(model, xpath1, xpath2):
    # Check if XPaths exist in the model
    if xpath1 not in model.wv or xpath2 not in model.wv:
        print("One or both of the XPaths are not in the model.")
        return None

    # Get vectors for XPaths
    vector1 = model.wv[xpath1]
    vector2 = model.wv[xpath2]

    # Calculate and return cosine similarity
    return 1 - distance.cosine(vector1, vector2)


def get_combined_similarity(model, node1, node2, alpha=0.5):
    text_sim = get_text_similarity(node1, node2)
    structure_sim = get_structure_similarity(model, node1.xpath, node2.xpath)
    if text_sim == 0:
        return structure_sim
    return alpha * text_sim + (1 - alpha) * structure_sim


def add_similarity_scores_to_graph(model, relation_graph):
    for node in relation_graph.nodes():
        edges = list(node.edges.values())
        
        for edge in edges:
            if edge.type == EdgeType.CHILD or edge.type == EdgeType.FOR:
                edge.set_weight(1)
                continue
            sim = get_combined_similarity(model, edge.source, edge.target)
            if edge.target.has_children():
                for target_child_edge in edge.target.get_children():
                    sim = max(
                        sim,
                        get_combined_similarity(model, edge.source, target_child_edge.target)
                    )
            edge.set_weight(sim)
    return relation_graph
