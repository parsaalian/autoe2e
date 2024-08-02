import copy

from oraclai.form_nexus.utils import is_label, is_input, remove_redundant_attributes
from oraclai.form_nexus.similarity import get_combined_similarity


class InputGroupNode:
    def __init__(self, input_node):
        self.node = input_node
        self.label = self._get_label(input_node)
        self.group = self._form_group(input_node)
        self.edges = []
    
    
    def add_edge(self, other_group, weight):
        self.edges.append((other_group, weight))
    
    
    def _get_label(self, node):
        candidate_label = list(filter(
            lambda x: is_label(x.target.element) and 'FOR' in x.type.value,
            node.edges.values()
        ))
        if len(candidate_label) > 0:
            return candidate_label[0].target
        return None
    
    
    def _form_group(self, node):
        # TODO: modify so that we can create more than one edge distance groups
        group = []
        edges = list(node.edges.values())
        
        # label has to be set by _get_label before this step
        if self.label is not None:
            edges.extend(list(self.label.edges.values()))
        
        for edge in edges:
            if not is_input(edge.target.element):
                group.append(edge.target)
        
        group = filter(lambda x: not is_label(x.element), group)
        return list(set(group))
    
    
    def get_similarity(self, model, other_group):
        input_sim = get_combined_similarity(model, self.node, other_group.node)
        label_sim = None
        if self.label is not None and other_group.label is not None:
            label_sim = get_combined_similarity(model, self.label, other_group.label)
        return max(input_sim, label_sim or 0)
    
    
    def _copy_soup_and_simplify_attrs(self, element):
        copied = copy.copy(element)
        copied = remove_redundant_attributes(element)
        return copied
    
    
    def to_prompt_string(self, relevant=True):
        input_string = f'input: {str(self._copy_soup_and_simplify_attrs(self.node.element))}\n'
        
        if not relevant:
            return input_string.strip()
        
        if self.label is not None:
            input_string += f'with label: {self.label.element.text.strip()}\n'
        
        if len(self.group) > 0:
            group_related_node_str = '\n'.join(
                map(
                    lambda x: str(self._copy_soup_and_simplify_attrs(x.element)),
                    self.group
                )
            )
            input_string += f'with the following relevant text tags:\n{group_related_node_str}\n'
        
        return input_string.strip()
    
    
    def __str__(self):
        return self.to_prompt_string(relevant=True)