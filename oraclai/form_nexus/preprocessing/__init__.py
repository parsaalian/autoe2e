from oraclai.form_nexus.utils import (
    is_input,
    is_span_wrap,
    is_navigable_string,
    is_comment,
    has_no_text
)

force_not_keep_tags = [
    'script', 'style', 'noscript', 'meta', 'link', 'head', 'html', 'body', 'title', 'iframe',
    'svg', 'path', 'defs', 'g', 'symbol', 'use', 'image', 'rect', 'circle', 'ellipse', 'line',
    'polyline', 'polygon', 'text', 'tspan', 'textPath', 'switch', 'foreignObject', 'desc',
    'legend', 'source', 'track', 'audio', 'video', 'canvas', 'map', 'area', 'base', 'col',
]


def is_displayed(element):
    if is_navigable_string(element) and not has_no_text(element):
        return True
    if is_span_wrap(element) and not has_no_text(element):
        return True
    if not is_input(element) and has_no_text(element):
        return False
    
    x_start = float(element.attrs['x_start'])
    x_end = float(element.attrs['x_end'])
    y_start = float(element.attrs['y_start'])
    y_end = float(element.attrs['y_end'])
    
    # here, 1px is the threshold for determining if an element is displayed
    return abs(x_end - x_start) > 1 and abs(y_end - y_start) > 1


def should_skip_processing(element):
    should_skip = \
        is_comment(element) or \
        (is_navigable_string(element) and has_no_text(element)) or \
        not is_displayed(element) or \
        (not is_navigable_string(element) and "disabled" in element.attrs)
        
    return should_skip


def is_force_not_keep(element):
    if element.name in force_not_keep_tags:
        return True

    return False


def is_force_keep(element):
    force_keep_tags = ['label', 'input', 'textarea', 'select', 'option', 'button']
    return element.name in force_keep_tags


def has_action_listener(element):
    # TODO: check if element has JavaScript action listeners
    # such as the case of <div> instead of <button> for submit
    return False


def is_processable(element):
    # if it's in the force-not-keep list, then it's not processable
    if not is_navigable_string(element) and is_force_not_keep(element):
        return False
    
    # if it's a string and its parent has more than one child, then it's processable
    if is_navigable_string(element):
        if element.parent is not None and len(element.parent.contents) > 1:
            return True
    
    # if it has no children, then it's processable
    elif len(element.contents) == 0:
        return True
    
    # if its only child is a string, then it's processable
    elif len(element.contents) == 1 and is_navigable_string(element.contents[0]):
        return True
    
    # if it's a force-keep element, then it's processable
    elif is_force_keep(element):
        return True
    
    # if it has an action listener, then it's processable
    elif has_action_listener(element):
        return True
    
    return False


def wrap_free_text(doc):
    '''
    This function wraps free text, which is the text that is the child of a multi-child element.
    
    <div>
        this <span>is</span> free text
    </div>
    
    in the example above, "this" and "free text" are free text. Wrapping them in a tag allows for
    easier processing later on.
    '''
    should_wrap = []

    for element in doc.recursiveChildGenerator():
        if is_navigable_string(element) and \
            element.parent is not None and \
            len(element.parent.contents) > 1:
            
            should_wrap.append(element)

    for idx, element in enumerate(should_wrap):
        span = doc.new_tag('span-wrap')
        span.string = element.string
        span.attrs = {
            "x_start": element.parent.attrs['x_start'],
            "x_end": element.parent.attrs['x_end'],
            "y_start": element.parent.attrs['y_start'],
            "y_end": element.parent.attrs['y_end'],
            "xpath": f"{element.parent.attrs['xpath']}/SPAN-WRAP[{idx + 1}]"
        }
        element.insert_before(span)
        element.extract()
    
    return doc


def get_processable_nodes(soup):
    nodes = []
    
    soup = wrap_free_text(soup)
    
    for element in soup.recursiveChildGenerator():
        if is_comment(element):
            element.extract()
    
    for element in soup.recursiveChildGenerator():
        if should_skip_processing(element):
            continue
        
        if is_processable(element):
            nodes.append(element)
    
    return nodes


__all__ = [
    'get_processable_nodes'
]