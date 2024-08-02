from enum import Enum


class EdgeType(Enum):
    # connection via for attribute
    FOR = 'FOR'
    P_FOR = 'P_FOR'
    
    # neighbor connections
    CHILD = 'CHILD'
    PARENT = 'PARENT'
    
    NLEFT = 'NLEFT'
    NRIGHT = 'NRIGHT'
    NTOP = 'NTOP'
    NBOTTOM = 'NBOTTOM'
    
    # feedback connections
    P_FEEDBACK = 'P_FEEDBACK'
    
    # text connections
    P_INFO = 'INFO'


class RelationEdge:
    def __init__(self, source, target, conn_type, weight=0):
        self.source = source
        self.target = target
        self.type = conn_type
        self.weight = weight
    
    
    def set_weight(self, weight):
        self.weight = weight
    
    
    def set_type(self, conn_type):
        self.type = conn_type
    
    
    def is_reverse(self, edge):
        return self.source == edge.target and \
            self.target == edge.source and \
            self.weight == edge.weight and \
            self.type == self._reverse_type(edge.type)
    
    
    def _reverse_type(self, conn_type):
        if conn_type == EdgeType.NLEFT:
            return EdgeType.NRIGHT
        if conn_type == EdgeType.NRIGHT:
            return EdgeType.NLEFT
        if conn_type == EdgeType.NBOTTOM:
            return EdgeType.NTOP
        if conn_type == EdgeType.NTOP:
            return EdgeType.NBOTTOM
        return None
    
    
    def get_id(self):
        return f'edge {self.type.value} from {self.source} to {self.target}'
    
    
    def __repr__(self):
        return str(self)
    
    
    def __str__(self):
        return f'edge {self.type.value} weight {self.weight} from {self.source} to {self.target}'