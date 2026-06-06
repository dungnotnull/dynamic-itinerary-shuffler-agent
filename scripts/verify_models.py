import torch
from sentence_transformers import SentenceTransformer
from transformers import pipeline

def test_models():
    print("Testing sentence-transformers...")
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(["Hello world", "Travel itinerary"])
        print(f"Success: Embeddings shape {embeddings.shape}")
    except Exception as e:
        print(f"Failure: {e}")

    print("\nTesting sentiment-analysis...")
    try:
        # This will download the model on first run
        classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        result = classifier("I love this travel plan!")[0]
        print(f"Success: {result}")
    except Exception as e:
        print(f"Failure: {e}")

if __name__ == "__main__":
    test_models()
