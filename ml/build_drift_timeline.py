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
# USER
# =========================

USER_ID = 1

user = ratings[
    ratings["userId"] == USER_ID
].copy()

user["timestamp"] = pd.to_datetime(user["timestamp"])

user = user[
    user["rating"] >= 4.0
].copy()

user = user.sort_values("timestamp")


# =========================
# MOVIE -> EMBEDDING
# =========================

movie_index = {
    movie_id: index
    for index, movie_id in enumerate(movies["movieId"])
}

user = user[
    user["movieId"].isin(movie_index)
].copy()


# =========================
# CREATE TIME WINDOWS
# =========================

# Split history into 6 chronological periods

user["period"] = pd.qcut(
    user["timestamp"].rank(method="first"),
    q=6,
    labels=False
)


def create_vector(data):

    vectors = []
    weights = []

    for _, row in data.iterrows():

        index = movie_index[row["movieId"]]

        vectors.append(embeddings[index])
        weights.append(row["rating"] - 3)

    vector = np.average(
        vectors,
        axis=0,
        weights=weights
    )

    return vector / np.linalg.norm(vector)


# =========================
# CREATE PERIOD VECTORS
# =========================

period_vectors = []
period_info = []

for period, group in user.groupby("period"):

    vector = create_vector(group)

    period_vectors.append(vector)

    period_info.append({
        "period": int(period) + 1,
        "start_date": group["timestamp"].min(),
        "end_date": group["timestamp"].max(),
        "movies": len(group)
    })


# =========================
# CALCULATE DRIFT
# =========================

results = []

for i in range(1, len(period_vectors)):

    similarity = cosine_similarity(
        period_vectors[i - 1].reshape(1, -1),
        period_vectors[i].reshape(1, -1)
    )[0][0]

    drift = 1 - similarity

    results.append({
        "from_period": i,
        "to_period": i + 1,
        "similarity": round(float(similarity), 4),
        "drift": round(float(drift), 4)
    })


# =========================
# SAVE RESULTS
# =========================

timeline = pd.DataFrame(results)

output = PROCESSED / "taste_drift_timeline.csv"

timeline.to_csv(
    output,
    index=False
)


# =========================
# DISPLAY
# =========================

print("\n========== TASTE PERIODS ==========")

for info in period_info:
    print(
        f"Period {info['period']}: "
        f"{info['start_date'].date()} → "
        f"{info['end_date'].date()} "
        f"({info['movies']} movies)"
    )


print("\n========== DRIFT TIMELINE ==========")

print(timeline.to_string(index=False))

print("\n✅ TASTE DRIFT TIMELINE CREATED")

print("\nSaved to:")
print(output)