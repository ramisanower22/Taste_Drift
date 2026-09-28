import pandas as pd
from pathlib import Path

# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"


# =========================
# LOAD CLEAN DATA
# =========================

movies = pd.read_csv(PROCESSED / "movies_clean.csv")
tags = pd.read_csv(PROCESSED / "tags_clean.csv")
links = pd.read_csv(PROCESSED / "links_clean.csv")


# =========================
# COMBINE TAGS PER MOVIE
# =========================

movie_tags = (
    tags.groupby("movieId")["tag"]
    .apply(lambda x: ", ".join(sorted(set(x))))
    .reset_index()
)

movie_tags.rename(
    columns={"tag": "tags"},
    inplace=True
)


# =========================
# MERGE MOVIE DATA
# =========================

dataset = movies.merge(
    movie_tags,
    on="movieId",
    how="left"
)

dataset = dataset.merge(
    links,
    on="movieId",
    how="left"
)


# Movies without tags
dataset["tags"] = dataset["tags"].fillna("")


# =========================
# CLEAN GENRES
# =========================

dataset["genres"] = (
    dataset["genres"]
    .fillna("")
    .str.replace("|", ", ", regex=False)
)


# =========================
# CREATE ML TEXT
# =========================

dataset["embedding_text"] = (
    "Title: " + dataset["clean_title"].fillna("") +
    ". Genres: " + dataset["genres"].fillna("") +
    ". Tags: " + dataset["tags"].fillna("")
)


# =========================
# KEEP USEFUL COLUMNS
# =========================

dataset = dataset[
    [
        "movieId",
        "clean_title",
        "year",
        "genres",
        "tags",
        "imdbId",
        "tmdbId",
        "embedding_text"
    ]
]


# =========================
# SAVE
# =========================

output = PROCESSED / "movies_unified.csv"

dataset.to_csv(
    output,
    index=False
)


# =========================
# RESULTS
# =========================

print("\n✅ UNIFIED MOVIE DATASET CREATED")

print("\nMovies:", len(dataset))

print("\nColumns:")
print(dataset.columns.tolist())

print("\nExample:\n")

print(
    dataset[
        ["clean_title", "genres", "tags"]
    ].head(5).to_string(index=False)
)

print("\nSaved to:")
print(output)