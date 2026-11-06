"""
Machine Learning Pipeline for JobShield AI.
Uses TF-IDF Vectorization + Logistic Regression for high-precision scam classification
with Explainable AI (XAI) feature importance extraction.
"""
import re
import string
from typing import Dict, Any, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from backend.ai.dataset import TRAINING_DATA

def preprocess_text(text: str) -> str:
    """Cleans and normalizes text for NLP processing."""
    if not text:
        return ""
    # Lowercase
    cleaned = text.lower()
    # Replace URLs with placeholder
    cleaned = re.sub(r'https?://\S+|www\.\S+', ' url_token ', cleaned)
    # Normalize whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

class JobScamClassifier:
    def __init__(self):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=4000,
                sublinear_tf=True
            )),
            ("clf", LogisticRegression(
                C=1.5,
                max_iter=1000,
                solver="liblinear",
                class_weight="balanced"
            ))
        ])
        self.is_trained = False
        self._train()

    def _train(self):
        """Trains the ML model on genuine and scam offer samples."""
        texts = [preprocess_text(item["text"]) for item in TRAINING_DATA]
        labels = [item["label"] for item in TRAINING_DATA]

        self.pipeline.fit(texts, labels)
        self.is_trained = True

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predicts scam probability and extracts key influential tokens (XAI).
        Returns a dict with scam_prob, is_scam, confidence, and explainable_tokens.
        """
        cleaned = preprocess_text(text)
        probs = self.pipeline.predict_proba([cleaned])[0]
        # Label 1 is scam, Label 0 is genuine
        scam_prob = float(probs[1])
        genuine_prob = float(probs[0])

        # Explainable AI: Feature contributions
        vectorizer: TfidfVectorizer = self.pipeline.named_steps["tfidf"]
        classifier: LogisticRegression = self.pipeline.named_steps["clf"]

        feature_names = vectorizer.get_feature_names_out()
        coefs = classifier.coef_[0]

        # Transform single document
        tfidf_vec = vectorizer.transform([cleaned]).tocoo()

        tokens_importance = []
        for col, val in zip(tfidf_vec.col, tfidf_vec.data):
            feat_name = feature_names[col]
            weight = coefs[col] * val
            tokens_importance.append((feat_name, weight))

        # Sort by impact
        # Positive weights push toward Scam, negative toward Genuine
        tokens_importance.sort(key=lambda x: x[1], reverse=True)

        scam_indicators = [
            {"token": token, "impact": round(weight, 3), "category": "Scam Signal"}
            for token, weight in tokens_importance if weight > 0.05
        ][:8]

        trust_indicators = [
            {"token": token, "impact": round(abs(weight), 3), "category": "Trust Signal"}
            for token, weight in reversed(tokens_importance) if weight < -0.05
        ][:8]

        return {
            "scam_probability": round(scam_prob * 100, 2),
            "genuine_probability": round(genuine_prob * 100, 2),
            "is_scam": scam_prob >= 0.5,
            "confidence": round(max(scam_prob, genuine_prob) * 100, 1),
            "scam_indicators": scam_indicators,
            "trust_indicators": trust_indicators
        }

_classifier_instance = None

def get_classifier() -> JobScamClassifier:
    """Singleton getter for the trained model."""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = JobScamClassifier()
    return _classifier_instance
