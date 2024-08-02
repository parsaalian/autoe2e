from node2vec import Node2Vec

from oraclai.form_nexus.utils import convert_soup_to_nx_graph


# Function to generate embeddings
def generate_embeddings(G, dimensions=1024, walk_length=30, num_walks=200, workers=4):
    # Create Node2Vec object
    node2vec = Node2Vec(G, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=workers)

    # Train Node2Vec model
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    
    return model


def create_node2vec_model(soup_doc):
    # Create graph
    G = convert_soup_to_nx_graph(soup_doc)

    # Generate embeddings
    model = generate_embeddings(G)
    
    return model