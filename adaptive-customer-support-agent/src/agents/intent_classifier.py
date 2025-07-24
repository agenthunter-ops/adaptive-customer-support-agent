"""
BERT-style semantic intent classifier using sentence-transformers.
Loaded once and cached. If embeddings not suitable, swap to openai.
"""
import json
import logging
from pathlib import Path
from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L6-v2"
INTENTS_PATH = Path(__file__).parent.parent / "data" / "banking_intents.json"


class IntentClassifierAgent:
    def __init__(self) -> None:
        self.model = SentenceTransformer(MODEL_NAME)
        self.intents, self.examples, self.embeddings = self._load_intents()

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def classify(self, text: str) -> tuple[str, float]:
        """
        Returns (intent: str, confidence: 0-1).
        """
        query_emb = self.model.encode(text, normalize_embeddings=True)
        sims = util.cos_sim(query_emb, self.embeddings)[0]
        best_idx = int(np.argmax(sims))
        return self.intents[best_idx], float(sims[best_idx])

    # --------------------------------------------------------------------- #
    # Private helpers
    # --------------------------------------------------------------------- #
    def _load_intents(self):
        intents: list[str] = []
        examples: list[str] = []
        with open(INTENTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        for intent, samples in data.items():
            for sentence in samples:
                intents.append(intent)
                examples.append(sentence)
        embeddings = self.model.encode(examples, normalize_embeddings=True)
        logger.info("Loaded %d labelled sentences (%d unique intents)",
                    len(examples), len(set(intents)))
        return intents, examples, embeddings


@lru_cache
def get_intent_classifier() -> IntentClassifierAgent:
    return IntentClassifierAgent()
