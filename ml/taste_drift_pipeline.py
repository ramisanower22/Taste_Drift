import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"

MOVIES_PATH = PROCESSED / "movies_unified.csv"
RATINGS_PATH = PROCESSED / "ratings_clean.csv"
EMBEDDINGS_PATH = PROCESSED / "movie_embeddings.npy"


# ==========================================
# LOAD DATA
# ==========================================

movies = pd.read_csv(MOVIES_PATH)
ratings = pd.read_csv(RATINGS_PATH)
embeddings = np.load(EMBEDDINGS_PATH)

movie_index = {
    movie_id: index
    for index, movie_id in enumerate(movies["movieId"])
}


# ==========================================
# CREATE TASTE VECTOR
# ==========================================

def create_taste_vector(data):

    vectors = []
    weights = []

    for _, row in data.iterrows():

        if row["movieId"] not in movie_index:
            continue

        index = movie_index[row["movieId"]]

        vectors.append(embeddings[index])
        weights.append(row["rating"] - 3)

    if not vectors:
        return None

    vector = np.average(
        vectors,
        axis=0,
        weights=weights
    )

    norm = np.linalg.norm(vector)

    if norm == 0:
        return vector

    return vector / norm


# ==========================================
# GENRE COUNTER
# ==========================================

def get_genres(data):

    counter = Counter()

    for genres in data["genres"].fillna(""):

        for genre in genres.split(","):

            genre = genre.strip()

            if genre:
                counter[genre] += 1

    return counter


# ==========================================
# TAG COUNTER
# ==========================================

def get_tags(data):

    counter = Counter()

    for tags in data["tags"].fillna(""):

        for tag in tags.split(","):

            tag = tag.strip().lower()

            if tag:
                counter[tag] += 1

    return counter


# ==========================================
# ANALYZE USER
# ==========================================

def analyze_user(user_id, periods=6):

    user = ratings[
        ratings["userId"] == user_id
    ].copy()

    if user.empty:
        print("❌ User not found.")
        return

    user["timestamp"] = pd.to_datetime(
        user["timestamp"]
    )

    # Only explicitly liked movies
    user = user[
        user["rating"] >= 4.0
    ].copy()

    user = user.merge(
        movies[
            ["movieId", "clean_title", "genres", "tags"]
        ],
        on="movieId",
        how="inner"
    )

    user = user.sort_values("timestamp")

    if len(user) < periods:
        print("❌ Not enough liked movies for analysis.")
        return

    # Chronological periods
    user["period"] = pd.qcut(
        user["timestamp"].rank(method="first"),
        q=periods,
        labels=False
    )

    period_vectors = {}

    for period, group in user.groupby("period"):

        period_vectors[int(period)] = create_taste_vector(group)


    results = []

    # ======================================
    # COMPARE PERIODS
    # ======================================

    for period in range(periods - 1):

        before = user[user["period"] == period]
        after = user[user["period"] == period + 1]

        before_vector = period_vectors[period]
        after_vector = period_vectors[period + 1]

        similarity = cosine_similarity(
            before_vector.reshape(1, -1),
            after_vector.reshape(1, -1)
        )[0][0]

        drift = 1 - similarity

        # ------------------------------
        # GENRE CHANGES
        # ------------------------------

        before_genres = get_genres(before)
        after_genres = get_genres(after)

        genre_changes = []

        for genre in set(before_genres) | set(after_genres):

            old = before_genres[genre] / len(before)
            new = after_genres[genre] / len(after)

            genre_changes.append(
                (genre, new - old)
            )

        genre_changes.sort(
            key=lambda x: abs(x[1]),
            reverse=True
        )

        # ------------------------------
        # TAG CHANGES
        # ------------------------------

        before_tags = get_tags(before)
        after_tags = get_tags(after)

        tag_changes = []

        for tag in set(before_tags) | set(after_tags):

            old = before_tags[tag] / len(before)
            new = after_tags[tag] / len(after)

            tag_changes.append(
                (tag, new - old)
            )

        tag_changes.sort(
            key=lambda x: abs(x[1]),
            reverse=True
        )

        results.append({
            "from_period": period + 1,
            "to_period": period + 2,
            "similarity": float(similarity),
            "drift": float(drift),
            "top_genre_changes": genre_changes[:5],
            "top_tag_changes": tag_changes[:8]
        })


    # ======================================
    # DISPLAY
    # ======================================

    print("\n===================================")
    print("       TASTE DRIFT ANALYSIS")
    print("===================================")

    print("\nUser:", user_id)
    print("Liked movies:", len(user))

    for result in results:

        print(
            f"\nP{result['from_period']} "
            f"→ P{result['to_period']}"
        )

        print(
            "Drift:",
            round(result["drift"], 4)
        )

        print("Top genre changes:")

        for genre, change in result["top_genre_changes"][:3]:

            direction = "↑" if change > 0 else "↓"

            print(
                f"  {genre}: "
                f"{direction} {abs(change):.2f}"
            )


    # ======================================
    # SAVE SUMMARY
    # ======================================

    summary = pd.DataFrame([
        {
            "from_period": r["from_period"],
            "to_period": r["to_period"],
            "similarity": r["similarity"],
            "drift": r["drift"]
        }
        for r in results
    ])

    output = PROCESSED / "taste_drift_analysis.csv"

    summary.to_csv(
        output,
        index=False
    )

    print("\n✅ ANALYSIS COMPLETE")
    print("Saved:", output)

    return results


# ==========================================
# RUN TEST
# ==========================================

if __name__ == "__main__":

    analyze_user(
        user_id=1,
        periods=6
    )