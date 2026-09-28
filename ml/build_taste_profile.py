import pandas as pd
import numpy as np
from pathlib import Path


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"

movies = pd.read_csv(PROCESSED / "movies_unified.csv")
ratings = pd.read_csv(PROCESSED / "ratings_clean.csv")
embeddings = np.load(PROCESSED / "movie_embeddings.npy")


# =========================
# SELECT TEST USER
# =========================

USER_ID = 1

user_ratings = ratings[
    ratings["userId"] == USER_ID
].copy()

print(f"\nUser {USER_ID}")
print("Total ratings:", len(user_ratings))


# =========================
# KEEP LIKED MOVIES
# =========================

liked = user_ratings[
    user_ratings["rating"] >= 4.0
].copy()

print("Liked movies:", len(liked))


# =========================
# CONNECT MOVIES TO EMBEDDINGS
# =========================

movie_index = {
    movie_id: index
    for index, movie_id in enumerate(movies["movieId"])
}

valid_rows = liked[
    liked["movieId"].isin(movie_index)
].copy()


# =========================
# WEIGHTED TASTE VECTOR
# =========================

vectors = []
weights = []

for _, row in valid_rows.iterrows():

    index = movie_index[row["movieId"]]

    vectors.append(
        embeddings[index]
    )

    # 4 stars = weight 1
    # 4.5 stars = weight 1.5
    # 5 stars = weight 2
    weights.append(
        row["rating"] - 3
    )


taste_vector = np.average(
    vectors,
    axis=0,
    weights=weights
)

# Normalize vector
taste_vector = taste_vector / np.linalg.norm(taste_vector)


# =========================
# SAVE
# =========================

OUTPUT = PROCESSED / "test_user_taste_vector.npy"

np.save(
    OUTPUT,
    taste_vector
)


print("\n✅ TASTE VECTOR CREATED")

print("Vector dimensions:", taste_vector.shape)

print("\nSaved to:")
print(OUTPUT)