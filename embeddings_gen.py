"""
Author: Alfredo Bernal Luna
Date: 18/05/24
Name: extract_text.py
Principal functions:
    1. generate_embeddings
"""

import extract_text
from sentence_transformers import SentenceTransformer
import fitz

def generate_embeddings(text, model):
    """
    Generate embeddings for the given text using Sentence Transformers
    """
    # Split text into sentences
    sentences = text.split('\n')  
    # Generate embeddings for the sentences
    sentence_embeddings = model.encode(sentences)    
    return sentences, sentence_embeddings

def main():
    # Text for which embeddings need to be generated
    pdf = 'Barack Obama - 13th Amendment 150-Year Anniversary.pdf'  
    text = extract_text.extract_text_from_pdf(pdf, main_title='AAmmeerriiccaannRRhheettoorriicc..ccoomm',top_margin=50, bottom_margin=50)
    # Load a pre-trained model
    model_name = 'bert-base-nli-mean-tokens'
    model = SentenceTransformer(model_name)
    if pdf:
        sentences, sentence_embeddings = generate_embeddings(text, model)
        # Print the embeddings for each sentence
        for sentence, embedding in zip(sentences, sentence_embeddings):
            print("Sentence:", sentence)
            print("Embedding:", embedding)
            print()
    else:
        print("No text was extracted from the PDF.")

if __name__ == '__main__':
    main()