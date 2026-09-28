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

user = user[
    user["rating"] >= 4.0
].copy()

user = user.sort_values("timestamp")


# =========================
# ADD MOVIE DATA
# =========================

user = user.merge(
    movies[
        ["movieId", "clean_title", "genres", "tags"]
    ],
    on="movieId",
    how="inner"
)


# =========================
# CREATE SAME 6 PERIODS
# =========================

user["period"] = pd.qcut(
    user["timestamp"].rank(method="first"),
    q=6,
    labels=False
)


# =========================
# COUNT TAGS
# =========================

def get_tags(data):

    counter = Counter()

    for tags in data["tags"].fillna(""):

        for tag in tags.split(","):

            tag = tag.strip().lower()

            if tag:
                counter[tag] += 1

    return counter


# =========================
# COMPARE PERIODS
# =========================

print("\n========== TAG DRIFT ==========")

for period in range(5):

    before = user[
        user["period"] == period
    ]

    after = user[
        user["period"] == period + 1
    ]

    before_tags = get_tags(before)
    after_tags = get_tags(after)

    all_tags = set(before_tags) | set(after_tags)

    changes = []

    for tag in all_tags:

        before_ratio = before_tags[tag] / len(before)
        after_ratio = after_tags[tag] / len(after)

        change = after_ratio - before_ratio

        changes.append(
            (tag, change)
        )

    changes.sort(
        key=lambda x: abs(x[1]),
        reverse=True
    )

    print(
        f"\n--- P{period + 1} → P{period + 2} ---"
    )

    shown = 0

    for tag, change in changes:

        # Ignore extremely tiny changes
        if abs(change) < 0.03:
            continue

        direction = "↑" if change > 0 else "↓"

        print(
            f"{tag[:30]:30} "
            f"{direction} {abs(change):.2f}"
        )

        shown += 1

        if shown == 8:
            break


print("\n✅ TAG ANALYSIS COMPLETE")