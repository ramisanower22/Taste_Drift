from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

MOVIES_PATH = PROCESSED_DIR / "movies_unified.csv"
EMBEDDINGS_PATH = PROCESSED_DIR / "movie_embeddings.npy"


# =========================================================
# LOAD MOVIE DATA
# =========================================================

movies = pd.read_csv(MOVIES_PATH)
embeddings = np.load(EMBEDDINGS_PATH)

movies["clean_title"] = (
    movies["clean_title"]
    .fillna("")
    .astype(str)
    .str.lower()
    .str.strip()
)

movie_index = {
    title: index
    for index, title in enumerate(movies["clean_title"])
    if title
}


# =========================================================
# CREATE TASTE VECTOR
# =========================================================

def create_taste_vector(data):
    vectors = []

    for _, row in data.iterrows():
        title = row["clean_title"]

        if title not in movie_index:
            continue

        index = movie_index[title]

        vectors.append(
            embeddings[index]
        )

    if not vectors:
        return None

    vectors = np.array(vectors)

    taste_vector = np.mean(
        vectors,
        axis=0,
    )

    norm = np.linalg.norm(
        taste_vector
    )

    if norm == 0:
        return None

    return taste_vector / norm


# =========================================================
# GENRE PROFILE
# =========================================================

def get_genre_profile(matched):
    genre_scores = {}

    for _, row in matched.iterrows():
        title = row["clean_title"]

        if title not in movie_index:
            continue

        movie_row = movies.iloc[
            movie_index[title]
        ]

        genres = str(
            movie_row.get(
                "genres",
                "",
            )
        )

        for genre in genres.split("|"):
            genre = genre.strip()

            if not genre:
                continue

            if genre == "(no genres listed)":
                continue

            genre_scores[genre] = (
                genre_scores.get(
                    genre,
                    0,
                )
                + 1
            )

    if not genre_scores:
        return []

    total = sum(
        genre_scores.values()
    )

    profile = []

    for genre, score in sorted(
        genre_scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:6]:

        percentage = (
            score / total
        ) * 100

        profile.append(
            {
                "genre": genre,
                "score": round(
                    percentage,
                    1,
                ),
            }
        )

    return profile


# =========================================================
# ANALYZE NETFLIX HISTORY
# =========================================================

def analyze_netflix(
    file_path,
    periods=4,
):
    history = pd.read_csv(file_path)

    required_columns = {
        "Title",
        "Date",
    }

    missing = (
        required_columns
        - set(history.columns)
    )

    if missing:
        return {
            "success": False,
            "message":
                "Missing required columns: "
                + ", ".join(
                    sorted(missing)
                ),
        }

    # -----------------------------------------
    # CLEAN
    # -----------------------------------------

    history["Date"] = pd.to_datetime(
        history["Date"],
        errors="coerce",
    )

    history = history.dropna(
        subset=[
            "Title",
            "Date",
        ]
    )

    history["clean_title"] = (
        history["Title"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    history = history.sort_values(
        "Date"
    )

    # -----------------------------------------
    # MATCH
    # -----------------------------------------

    history["matched"] = (
        history["clean_title"]
        .isin(movie_index)
    )

    matched = history[
        history["matched"]
    ].copy()

    if len(matched) < periods:
        return {
            "success": False,
            "message":
                "Not enough Netflix titles could be matched to the movie dataset.",
        }

    # -----------------------------------------
    # GENRE PROFILE
    # -----------------------------------------

    genre_profile = (
        get_genre_profile(
            matched
        )
    )

    # -----------------------------------------
    # CREATE PERIODS
    # -----------------------------------------

    actual_periods = min(
        periods,
        len(matched),
    )

    matched["period"] = pd.qcut(
        matched["Date"].rank(
            method="first"
        ),
        q=actual_periods,
        labels=False,
    )

    period_vectors = []
    period_information = []

    for period in sorted(
        matched["period"].unique()
    ):

        period_data = matched[
            matched["period"] == period
        ]

        vector = create_taste_vector(
            period_data
        )

        if vector is None:
            continue

        period_vectors.append(
            (
                int(period),
                vector,
            )
        )

        period_information.append(
            {
                "period":
                    int(period) + 1,

                "start_date":
                    period_data["Date"]
                    .min()
                    .strftime("%Y-%m-%d"),

                "end_date":
                    period_data["Date"]
                    .max()
                    .strftime("%Y-%m-%d"),

                "movies":
                    len(period_data),
            }
        )

    # -----------------------------------------
    # DRIFT
    # -----------------------------------------

    drift_timeline = []

    for i in range(
        len(period_vectors) - 1
    ):

        current_period, current_vector = (
            period_vectors[i]
        )

        next_period, next_vector = (
            period_vectors[i + 1]
        )

        similarity = cosine_similarity(
            [current_vector],
            [next_vector],
        )[0][0]

        drift = 1 - similarity

        drift_timeline.append(
            {
                "from_period":
                    current_period + 1,

                "to_period":
                    next_period + 1,

                "similarity":
                    round(
                        float(similarity),
                        4,
                    ),

                "drift":
                    round(
                        float(drift),
                        4,
                    ),
            }
        )

    # -----------------------------------------
    # SUMMARY
    # -----------------------------------------

    biggest_drift = None

    if drift_timeline:
        biggest_drift = max(
            drift_timeline,
            key=lambda item:
                item["drift"],
        )

    match_rate = round(
        (
            len(matched)
            / len(history)
            * 100
        ),
        1,
    )

    return {
        "success": True,

        "summary": {
            "films_in_file":
                len(history),

            "liked_films":
                len(history),

            "matched_films":
                len(matched),

            "match_rate":
                match_rate,

            "average_rating":
                0,

            "taste_periods":
                len(period_vectors),

            "biggest_drift":
                biggest_drift,
        },

        "genre_profile":
            genre_profile,

        "periods":
            period_information,

        "drift_timeline":
            drift_timeline,
    }


if __name__ == "__main__":
    print(
        "Netflix analyzer loaded successfully."
    )