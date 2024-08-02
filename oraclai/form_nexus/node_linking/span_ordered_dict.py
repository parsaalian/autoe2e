'''def tuple_avg(t):
    return (t[0] + t[1]) / 2


def span_binary_search(span_list, item_span):
    
    Performs a binary search on a span list, which is a list of tuples (start, end).
    The list is ordered by the first member of the tuple.
    The search key is (start + end) / 2.
    returns index of found item.
    
    if len(span_list) == 0:
        return -1
    
    if len(span_list) == 1:
        return 0
    
    middle = len(span_list) // 2
    if tuple_avg(item_span) >= tuple_avg(span_list[middle]):
        return middle + span_binary_search(span_list[middle:], item_span)
    
    return span_binary_search(span_list[:middle], item_span)'''


def span_binary_search(span_list, item_span):
    '''
    Performs a binary search on a span list, which is a list of tuples (start, end).
    The list is ordered by the first member of the tuple.
    The search key is (start + end) / 2.
    returns index of found item.
    '''
    if len(span_list) == 0:
        return -1
    
    if len(span_list) == 1:
        return 0
    
    middle = len(span_list) // 2
    middle_item = span_list[middle]
    
    # if item is before a span
    if item_span[0] <= middle_item[0] and item_span[1] <= middle_item[0]:
        return span_binary_search(span_list[:middle], item_span)
    
    # if item is after a span
    if item_span[0] >= middle_item[1] and item_span[1] >= middle_item[1]:
        return middle + span_binary_search(span_list[middle:], item_span)

    # if item is inside a span, colliding from left, or colliding from right
    return middle


class SpanOrderedDict:
    def __init__(self):
        self.spans = []
        self.items_dict = {}
    
    
    def force_set_item(self, span, item):
        self.items_dict[span] = item
    
    
    def add_item(self, span, item):
        # print(span)
        span_to_add = self.find_span_to_add(span)
        # print(span_to_add)
        # print(self.spans, '\n')
        if span_to_add not in self.items_dict:
            self.items_dict[span_to_add] = []
        self.items_dict[span_to_add].append(item)
    
    
    def find_span_to_add(self, span):
        closest_span_idx = span_binary_search(self.spans, span)
        
        # if this is the first span that we are adding something to
        if closest_span_idx == -1:
            # print('first', span)
            self.spans = [span]
            return span

        closest_span = self.spans[closest_span_idx]
        
        # if new span is inside some other span
        if span[0] >= closest_span[0] and span[1] <= closest_span[1]:
            # print('inside', closest_span)
            return closest_span
        
        # if new span is before some other span
        if span[0] <= closest_span[0] and span[1] <= closest_span[0]:
            # print('before', closest_span)
            insert_idx = max(closest_span_idx - 1, 0)
            self.spans.insert(insert_idx, span)
            return span
        
        # if new span is after some other span
        if span[0] >= closest_span[1] and span[1] >= closest_span[1]:
            # print('outside', closest_span)
            insert_idx = closest_span_idx + 1
            self.spans.insert(insert_idx, span)
            return span
        
        # otherwise, the spans collide with each other
        # print('collide', closest_span)
        span_start = min(closest_span[0], span[0])
        span_end = max(closest_span[1], span[1])
        new_span = (span_start, span_end)
        
        # swap span with new created span
        self.spans[closest_span_idx] = new_span
        items_dict = self.items_dict[closest_span]
        self.items_dict[new_span] = items_dict
        self.items_dict.pop(closest_span)

        return new_span
    
    
    def keys(self):
        return self.items_dict.keys()
    
    
    def values(self):
        return self.items_dict.values()
    
    
    def items(self):
        return self.items_dict.items()
    
    
    def __getitem__(self, key):
        return self.items_dict[key]


def create_span_ordered_dict(relation_nodes, axis):
    spans = SpanOrderedDict()
    
    for node in relation_nodes:
        span = getattr(node, f'{axis}_span')
        spans.add_item(span, node)

    return spans


def create_2d_span_ordered_dict(relation_graph):
    y_spans = create_span_ordered_dict(relation_graph.nodes(), 'y')
    
    for y_span, nodes in y_spans.items():
        x_spans = create_span_ordered_dict(nodes, 'x')
        
        # sort the items so that the first item in multiple items list is the targets,
        # and therefore the representative item.
        for x_span, sub_nodes in x_spans.items():
            sorted_sub_nodes = sorted(sub_nodes, key=lambda x: x.get_visible_area(), reverse=True)
            x_spans.force_set_item(x_span, sorted_sub_nodes)
        
        y_spans.force_set_item(y_span, x_spans)
    
    return y_spans
