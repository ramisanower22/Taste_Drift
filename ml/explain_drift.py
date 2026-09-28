import pandas as pd
from pathlib import Path
from collections import Counter


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"

movies = pd.read_csv(PROCESSED / "movies_unified.csv")
ratings = pd.read_csv(PROCESSED / "ratings_clean.csv")


# =========================
# USER
# =========================

USER_ID = 1

user = ratings[
    ratings["userId"] == USER_ID
].copy()

user["timestamp"] = pd.to_datetime(user["timestamp"])

# Only movies the user liked
user = user[
    user["rating"] >= 4.0
].copy()

user = user.sort_values("timestamp")


# =========================
# ADD MOVIE INFORMATION
# =========================

user = user.merge(
    movies[
        ["movieId", "clean_title", "genres", "tags"]
    ],
    on="movieId",
    how="inner"
)


# =========================
# SAME 6 PERIODS AS BEFORE
# =========================

user["period"] = pd.qcut(
    user["timestamp"].rank(method="first"),
    q=6,
    labels=False
)


# =========================
# GENRE ANALYSIS
# =========================

def get_genres(data):

    counter = Counter()

    for genres in data["genres"].fillna(""):

        for genre in genres.split(","):

            genre = genre.strip()

            if genre:
                counter[genre] += 1

    return counter


# =========================
# COMPARE PERIODS
# =========================

print("\n========== WHAT CHANGED? ==========")

for period in range(5):

    before = user[user["period"] == period]
    after = user[user["period"] == period + 1]

    before_genres = get_genres(before)
    after_genres = get_genres(after)

    all_genres = set(before_genres) | set(after_genres)

    changes = []

    for genre in all_genres:

        before_ratio = before_genres[genre] / len(before)
        after_ratio = after_genres[genre] / len(after)

        change = after_ratio - before_ratio

        changes.append(
            (genre, change)
        )

    changes.sort(
        key=lambda x: abs(x[1]),
        reverse=True
    )

    print(
        f"\n--- P{period + 1} → P{period + 2} ---"
    )

    for genre, change in changes[:5]:

        direction = "↑" if change > 0 else "↓"

        print(
            f"{genre:15} {direction} {abs(change):.2f}"
        )


print("\n✅ DRIFT EXPLANATION COMPLETE")