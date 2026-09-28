import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"

DATASET_PATH = PROCESSED / "movies_unified.csv"
EMBEDDING_PATH = PROCESSED / "movie_embeddings.npy"


# =========================
# LOAD DATA
# =========================

print("\nLoading movie dataset...")

movies = pd.read_csv(DATASET_PATH)

movies["embedding_text"] = (
    movies["embedding_text"]
    .fillna("")
    .astype(str)
)

print("Movies loaded:", len(movies))


# =========================
# LOAD ML MODEL
# =========================

print("\nLoading Sentence Transformer model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# =========================
# CREATE EMBEDDINGS
# =========================

print("\nGenerating embeddings...")
print("This may take a few minutes.\n")

embeddings = model.encode(
    movies["embedding_text"].tolist(),
    batch_size=64,
    show_progress_bar=True,
    normalize_embeddings=True
)


# =========================
# SAVE EMBEDDINGS
# =========================

np.save(
    EMBEDDING_PATH,
    embeddings
)


# =========================
# RESULT
# =========================

print("\n✅ EMBEDDINGS CREATED SUCCESSFULLY")

print("Movies:", len(movies))
print("Embedding shape:", embeddings.shape)

print("\nSaved to:")
print(EMBEDDING_PATH)