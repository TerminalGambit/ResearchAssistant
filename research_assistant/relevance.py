from transformers import pipeline
from typing import List

class RelevanceScorer:
    def __init__(self, preferences: List[str], threshold: float = 0.5):
        self.preferences = preferences
        self.threshold = threshold
        self.classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )

    def score(self, summary: str) -> float:
        result = self.classifier(summary, candidate_labels=self.preferences)
        return max(result["scores"]) 