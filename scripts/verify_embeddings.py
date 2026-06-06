import torch
from sentence_transformers import SentenceTransformer

def test_embeddings():
    print("Testing sentence-transformers...")
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(["Hello world", "Travel itinerary"])
        print(f"Success: Embeddings shape {embeddings.shape}")
    except Exception as e:
        print(f"Failure: {e}")

if __name__ == "__main__":
    test_embeddings()
