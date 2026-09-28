import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"

movies = pd.read_csv(PROCESSED / "movies_unified.csv")
ratings = pd.read_csv(PROCESSED / "ratings_clean.csv")
embeddings = np.load(PROCESSED / "movie_embeddings.npy")


# =========================
# TEST USER
# =========================

USER_ID = 1

user = ratings[
    ratings["userId"] == USER_ID
].copy()

user["timestamp"] = pd.to_datetime(user["timestamp"])

user = user.sort_values("timestamp")


# =========================
# KEEP LIKED MOVIES
# =========================

user = user[
    user["rating"] >= 4.0
].copy()


# =========================
# MAP MOVIE -> EMBEDDING
# =========================

movie_index = {
    movie_id: index
    for index, movie_id in enumerate(movies["movieId"])
}

user = user[
    user["movieId"].isin(movie_index)
].copy()


# =========================
# SPLIT HISTORY INTO PERIODS
# =========================

midpoint = len(user) // 2

early = user.iloc[:midpoint]
recent = user.iloc[midpoint:]


def create_taste_vector(data):

    vectors = []
    weights = []

    for _, row in data.iterrows():

        index = movie_index[row["movieId"]]

        vectors.append(embeddings[index])

        weights.append(
            row["rating"] - 3
        )

    vector = np.average(
        vectors,
        axis=0,
        weights=weights
    )

    return vector / np.linalg.norm(vector)


# =========================
# CREATE TWO TASTE VECTORS
# =========================

early_vector = create_taste_vector(early)
recent_vector = create_taste_vector(recent)


# =========================
# CALCULATE DRIFT
# =========================

similarity = cosine_similarity(
    early_vector.reshape(1, -1),
    recent_vector.reshape(1, -1)
)[0][0]

drift = 1 - similarity


# =========================
# RESULTS
# =========================

print("\n========== TASTE DRIFT ==========")

print("\nUser:", USER_ID)

print("\nEarly period:")
print(early["timestamp"].min(), "→", early["timestamp"].max())
print("Movies:", len(early))

print("\nRecent period:")
print(recent["timestamp"].min(), "→", recent["timestamp"].max())
print("Movies:", len(recent))

print("\nTaste similarity:", round(similarity, 3))
print("Taste drift:", round(drift, 3))

print("\n✅ TASTE DRIFT CALCULATED")