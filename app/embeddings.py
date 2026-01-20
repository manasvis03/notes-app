from sentence_transformers import SentenceTransformer
import numpy as np
import os

_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL

def embed_text(text: str) -> np.ndarray:
    model = get_model()
    emb = model.encode(text, convert_to_numpy=True)
    # normalize for cosine similarity with inner product
    norm = np.linalg.norm(emb)
    if norm > 0:
        emb = emb / norm
    return emb.astype('float32')
