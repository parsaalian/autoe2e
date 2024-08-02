import networkx as nx

from bs4 import NavigableString, Comment


def is_input(soup_element):
    input_tags = ['input', 'textarea', 'select', 'option']
    if soup_element.name in input_tags:
        return True
    
    if soup_element.name == 'button' and \
        'type' in soup_element.attrs and \
        soup_element.attrs['type'] in ['submit']:
        return True
    
    return False


def is_label(soup_element):
    return soup_element.name == 'label'


def is_text(soup_element):
    return not is_input(soup_element) and not is_label(soup_element)


def is_span_wrap(soup_element):
    return soup_element.name == 'span-wrap'


def is_navigable_string(soup_element):
    return isinstance(soup_element, NavigableString)


def is_comment(soup_element):
    return isinstance(soup_element, Comment)


def has_no_text(soup_element):
    return soup_element.text is None or soup_element.text.strip() == ''


def remove_redundant_attributes(soup_element):
    KEEP_ATTRIBUTES = [
        'href',
        'src',
        'alt',
        'action',
        'name',
        'type',
        'for',
        'id',
        'placeholder',
        'value',
        'alt',
        # input attributes
        'min',
        'max',
        'maxlength',
        'multiple',
        'pattern',
        'required',
        'readonly',
        'disabled',
        'step',
    ]
    
    for attr in [a for a in soup_element.attrs if a not in KEEP_ATTRIBUTES]:
        soup_element.attrs.pop(attr)
    
    for e in soup_element.find_all():
        if is_navigable_string(e) or is_comment(e):
            continue
        for attr in [a for a in e.attrs if a not in KEEP_ATTRIBUTES]:
            e.attrs.pop(attr)
    
    return soup_element


# Function to create a graph from the BeautifulSoup object
def convert_soup_to_nx_graph(soup):
    G = nx.DiGraph()

    for tag in soup.find_all():
        # Assuming 'xpath' attribute exists for each tag
        xpath = tag.attrs['xpath']
        
        if xpath not in G:
            G.add_node(xpath)
        for child in tag.children:
            if is_comment(child) or is_navigable_string(child):
                continue
            child_xpath = child.attrs.get('xpath')
            if child_xpath not in G:
                G.add_node(child_xpath)
            G.add_edge(xpath, child_xpath)

    return G
