import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"


# =========================
# LOAD DATA
# =========================

movies = pd.read_csv(
    PROCESSED / "movies_unified.csv"
)

embeddings = np.load(
    PROCESSED / "movie_embeddings.npy"
)


print("Movies:", len(movies))
print("Embeddings:", embeddings.shape)


# =========================
# FIND SIMILAR MOVIES
# =========================

def find_similar_movies(movie_name, top_n=10):

    matches = movies[
        movies["clean_title"]
        .str.contains(movie_name, case=False, na=False, regex=False)
    ]

    if matches.empty:
        print(f"\n❌ Movie '{movie_name}' not found.")
        return

    # Use first matching movie
    movie_index = matches.index[0]
    movie_title = movies.iloc[movie_index]["clean_title"]

    target_embedding = embeddings[movie_index].reshape(1, -1)

    similarities = cosine_similarity(
        target_embedding,
        embeddings
    )[0]

    # Highest similarity first
    similar_indices = similarities.argsort()[::-1]

    print(f"\n🎬 Movies similar to: {movie_title}\n")

    count = 0

    for index in similar_indices:

        # Skip the movie itself
        if index == movie_index:
            continue

        title = movies.iloc[index]["clean_title"]
        genres = movies.iloc[index]["genres"]
        score = similarities[index]

        print(
            f"{title} | {genres} | similarity: {score:.3f}"
        )

        count += 1

        if count >= top_n:
            break


# =========================
# TEST
# =========================

find_similar_movies("Toy Story")