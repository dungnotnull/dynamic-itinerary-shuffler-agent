import torch
from transformers import pipeline

def test_sentiment():
    print("Testing sentiment-analysis...")
    try:
        classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        result = classifier("I love this travel plan!")[0]
        print(f"Success: {result}")
    except Exception as e:
        print(f"Failure: {e}")

if __name__ == "__main__":
    test_sentiment()
