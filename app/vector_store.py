import numpy as np
import os
import json
from typing import List, Tuple

VEC_DIR = os.path.join(os.path.dirname(__file__), "vectors")
EMBED_PATH = os.path.join(VEC_DIR, "embeddings.npy")
MAP_PATH = os.path.join(VEC_DIR, "map.json")

class VectorStore:
    def __init__(self, dim: int):
        os.makedirs(VEC_DIR, exist_ok=True)
        self.dim = dim
        self.note_ids: List[int] = []
        self.embeddings: np.ndarray = np.empty((0, dim), dtype='float32')
        if os.path.exists(EMBED_PATH) and os.path.exists(MAP_PATH):
            self.embeddings = np.load(EMBED_PATH)
            with open(MAP_PATH, "r", encoding="utf-8") as f:
                self.note_ids = json.load(f)

    def add(self, embedding: np.ndarray, note_id: int) -> None:
        emb = embedding.astype('float32')
        self.embeddings = np.vstack([self.embeddings, [emb]])
        self.note_ids.append(note_id)
        self._save()

    def update(self, note_id: int, embedding: np.ndarray) -> bool:
        """Update embedding for an existing note"""
        if note_id not in self.note_ids:
            return False
        idx = self.note_ids.index(note_id)
        emb = embedding.astype('float32')
        self.embeddings[idx] = emb
        self._save()
        return True

    def delete(self, note_id: int) -> bool:
        """Delete embedding for a note"""
        if note_id not in self.note_ids:
            return False
        idx = self.note_ids.index(note_id)
        self.embeddings = np.delete(self.embeddings, idx, axis=0)
        self.note_ids.pop(idx)
        self._save()
        return True

    def search(self, embedding: np.ndarray, top_k: int = 5) -> List[Tuple[int, float]]:
        if len(self.note_ids) == 0:
            return []
        query = embedding.astype('float32')
        # cosine similarity via dot product (embeddings are normalized)
        scores = np.dot(self.embeddings, query)
        # get top_k indices
        top_indices = np.argsort(-scores)[:top_k]
        res = []
        for idx in top_indices:
            res.append((self.note_ids[int(idx)], float(scores[idx])))
        return res

    def _save(self):
        np.save(EMBED_PATH, self.embeddings)
        with open(MAP_PATH, "w", encoding="utf-8") as f:
            json.dump(self.note_ids, f)
