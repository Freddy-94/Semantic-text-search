"""
Author: Alfredo Bernal Luna
Date: 18/05/24
Name: nearest_neighbor.py
Principal functions:
    1. annoy_index_build
    2. near_neigh
"""

import extract_text
import embeddings_gen
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex

def annoy_index_build(embeddings):
    """
        Function that helps to build the annoy index
    """    
    # Number of dimensions in the embedding
    embedding_dim = len(embeddings[0])
    # Build Annoy index
    annoy_index = AnnoyIndex(embedding_dim, 'euclidean')  # Euclidean distance
    # Add items (embeddings) to the index
    for i, embedding in enumerate(embeddings):
        annoy_index.add_item(i, embedding)
    # Build index
    annoy_index.build(n_trees=10)  # The number of trees for performance is adjustable
    # Save index to disk 
    annoy_index.save('index.ann')
    return annoy_index

def near_neigh(model, sentences, annoy_index):
    """
        Function that implements nearest_neighbor search
    """
    # Define a query vector 
    query_embedding = model.encode(["What does President Lincoln once wrote?"])

    # Perform nearest neighbor search
    n_nearest_neighbors = 5
    nearest_neighbor_indices = annoy_index.get_nns_by_vector(query_embedding[0], n_nearest_neighbors)

    # Get nearest neighbor sentences
    nearest_neighbor_sentences = [sentences[idx] for idx in nearest_neighbor_indices]
    return nearest_neighbor_sentences 

def main():
    # Text for which embeddings need to be generated
    pdf = 'Barack Obama - 13th Amendment 150-Year Anniversary.pdf'  
    text = extract_text.extract_text_from_pdf(pdf, main_title='AAmmeerriiccaannRRhheettoorriicc..ccoomm',top_margin=50, bottom_margin=50)
    model_name = 'bert-base-nli-mean-tokens'
    model = SentenceTransformer(model_name)  
    if pdf:
        sentences, sentence_embeddings = embeddings_gen.generate_embeddings(text, model)
    else:
        print("No text was extracted from the PDF.")
    # Load a pre-trained model      
    annoy_index = annoy_index_build(sentence_embeddings)
    nearest_neighbor_sentences = near_neigh(model, sentences, annoy_index)
    # Print nearest neighbor sentences
    print("Nearest neighbor sentences:")
    for sentence in nearest_neighbor_sentences:
        print(sentence)

if __name__ == '__main__':
    main()