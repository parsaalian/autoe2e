from bs4 import BeautifulSoup as bs

from oraclai.form_nexus.utils import embed_properties_into_html
from oraclai.form_nexus.preprocessing import get_processable_nodes
from oraclai.form_nexus.graph_embedding import create_node2vec_model
from oraclai.form_nexus.relation_graph import create_relation_graph
from oraclai.form_nexus.node_linking import create_base_links
from oraclai.form_nexus.similarity import add_similarity_scores_to_graph
from oraclai.form_nexus.edge_pruning import (
    prune_relation_graph_extra_edges,
    prune_low_score_uncertain_edges
)
from oraclai.form_nexus.input_group import (
    create_input_groups,
    prune_low_score_group_relations
)
from oraclai.form_nexus.feedback import has_feedback_keyword


def parse_form(driver, form, prev_relation_graph=None, TEXT_EMBEDDING_METHOD='ADA'):
    form = embed_properties_into_html(driver, form)
    form_doc = bs(form.get_attribute('outerHTML'), 'html.parser')
    
    form_processable_nodes = get_processable_nodes(form_doc)
    node2vec_model = create_node2vec_model(form_doc)
    
    relation_graph = create_relation_graph(form_processable_nodes, TEXT_EMBEDDING_METHOD)

    relation_graph = create_base_links(relation_graph)
    
    relation_graph = add_similarity_scores_to_graph(node2vec_model, relation_graph)
    
    if prev_relation_graph is not None:
        diff = prev_relation_graph.diff(relation_graph)
        
        for node in diff['added']:
            if node.element.name == 'span-wrap':
                continue
            # only keep feedbacks in the new relation graph
            if has_feedback_keyword(node.element.text):
                node.set_is_feedback(True)
            else:
                relation_graph.remove_node(node)
    
    relation_graph = prune_relation_graph_extra_edges(relation_graph)
    relation_graph = prune_low_score_uncertain_edges(relation_graph, factor=0.5)
    
    input_groups = create_input_groups(relation_graph)
    input_groups = prune_low_score_group_relations(input_groups, node2vec_model, factor=0.5)
    
    return relation_graph, input_groups
