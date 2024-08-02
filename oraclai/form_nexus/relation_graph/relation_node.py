from math import floor

from .relation_edge import EdgeType
from oraclai.form_nexus.text_embedding import get_text_embedding
from oraclai.form_nexus.utils import is_input, has_no_text


def get_input_visible_text(element):
    text = ''
    attrs = element.attrs

    if 'placeholder' in attrs:
        text += f"{attrs['placeholder']} "
    if 'value' in attrs and attrs['value'].strip() != '':
        text += f", value is {attrs['value']} "
    if 'alt' in attrs:
        text += f", alt is {attrs['alt']} "
    
    text = text.strip().strip(', ')
    return text


def get_visible_text(element):
    if is_input(element):
        return get_input_visible_text(element)
    
    if has_no_text(element):
        return ''
    
    return str(element.text)


class RelationNode:
    def __init__(self, element, text_embedding_method='ADA'):
        self.element = element
        
        self.xpath = self._find_xpath(element)
        self.x_span = self._find_span(element, 'x')
        self.y_span = self._find_span(element, 'y')
        
        self.visible_text = self._find_visible_text(element)
        self.features = self._calculate_features(self.visible_text, text_embedding_method)
        
        self.edges = {}
        
        self.children_count = 0
        
        self.is_feedback = False
    
    
    def _find_xpath(self, element):
        return element.attrs['xpath']
    
    
    def _find_span(self, element, axis):
        return (
            floor(float(element.attrs[f'{axis}_start'])),
            floor(float(element.attrs[f'{axis}_end']))
        )
    
    
    def _find_visible_text(self, element):
        return get_visible_text(element)
    
    
    def _calculate_features(self, visible_text, text_embedding_method='ADA'):
        features = get_text_embedding(visible_text, text_embedding_method)
        return features
    
    
    def _change_children_count(self, edge, increase=1):
        if edge.type == EdgeType.CHILD:
            self.children_count += increase
    
    
    def set_is_feedback(self, is_feedback):
        self.is_feedback = is_feedback
    
    
    def get_is_feedback(self):
        return self.is_feedback
    
    
    def has_children(self):
        return self.children_count > 0
    
    
    def get_children(self):
        return list(filter(
            lambda x: x.type == EdgeType.CHILD,
            list(self.edges.values())
        ))
    
    
    def add_edge(self, edge):
        self.edges[edge.get_id()] = edge
        self._change_children_count(edge, 1)
    
    
    def remove_edge(self, edge):
        try:
            self.edges.pop(edge.get_id())
            self._change_children_count(edge, -1)
        except Exception as e:
            # print(e)
            pass
    
    
    def get_visible_area(self):
        return (self.x_span[1] - self.x_span[0]) * (self.y_span[1] - self.y_span[0])
    
    
    def get_id(self):
        if 'id' in self.element.attrs:
            return self.element.attrs['id']
        return self.xpath
    
    
    def __repr__(self):
        return str(self)


    def __str__(self):
        return f'<{self.element.name}>{self.visible_text}</{self.element.name}> at y: {str(self.y_span)}, x: {str(self.x_span)}'