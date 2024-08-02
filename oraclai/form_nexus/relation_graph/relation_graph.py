class RelationGraph:
    def __init__(self):
        self._nodes = {}
        self._edges = {}
    
    
    def nodes(self):
        return list(self._nodes.values())
    
    
    def get_node(self, node_id):
        return self._nodes[node_id]
    
    
    def edges(self):
        return list(self._edges.values())
    
    
    def add_node(self, node):
        self._nodes[node.get_id()] = node
    
    
    def remove_node(self, node):
        if node.get_id() in self._nodes:
            self._nodes.pop(node.get_id())
            
            edges = list(filter(lambda x: x.source == node or x.target == node, self.edges()))
            
            for edge in edges:
                self.remove_edge(edge)
    
    
    def add_edge(self, edge):
        source = edge.source
        
        source.add_edge(edge)
        
        self._edges[edge.get_id()] = edge
    
    
    def remove_edge(self, edge):
        source = edge.source
        
        source.remove_edge(edge)
        
        target_reverse_edges = list(filter(edge.is_reverse, edge.target.edges.values()))
        
        if len(target_reverse_edges) > 0:
            target_reverse_edge = target_reverse_edges[0]
            edge.target.remove_edge(target_reverse_edge)
        
        if edge.get_id() in self._edges:
            self._edges.pop(edge.get_id())
    
    
    def get_node_features(self):
        return {
            key: node.get_features() for key, node in self._nodes.items()
        }
    
    
    def is_a_child_node(self, node):
        return len(list(filter(
            lambda x: x.target == node and x.type.value == 'CHILD',
            self.edges()
        ))) > 0
    
    
    def diff(self, new_graph):
        diff = {
            'added': [],
            'removed': [],
        }
        
        for node in new_graph.nodes():
            if node.get_id() not in self._nodes: # and not new_graph.is_a_child_node(node):
                diff['added'].append(node)
        
        for node in self.nodes():
            if node.get_id() not in new_graph._nodes: # and not self.is_a_child_node(node):
                diff['removed'].append(node)
        
        return diff
