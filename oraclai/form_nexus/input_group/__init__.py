from .input_group_node import InputGroupNode

from oraclai.form_nexus.utils import is_input, get_normal_cutoff_score


def create_input_groups(relation_graph):
    input_groups = []
    
    input_elements = filter(lambda x: is_input(x.element), relation_graph.nodes())

    for input_element in input_elements:
        input_group = InputGroupNode(input_element)
        input_groups.append(input_group)
    
    return input_groups


def prune_low_score_group_relations(input_groups, model, factor=0.5):
    scores = []

    for i in range(len(input_groups)):
        for j in range(i + 1, len(input_groups)):
            score = input_groups[i].get_similarity(model, input_groups[j])
            scores.append(score)
    
    cutoff = get_normal_cutoff_score(scores, factor)
    
    for i in range(len(input_groups)):
        for j in range(i + 1, len(input_groups)):
            score = input_groups[i].get_similarity(model, input_groups[j])
            if score < cutoff:
                continue
            input_groups[i].add_edge(input_groups[j], score)
            input_groups[j].add_edge(input_groups[i], score)
    
    return input_groups