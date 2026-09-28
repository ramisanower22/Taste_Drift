import pandas as pd
from pathlib import Path

# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

MOVIELENS = BASE_DIR / "data" / "raw" / "movielens"
NETFLIX = BASE_DIR / "data" / "raw" / "netflix"
PROCESSED = BASE_DIR / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)


# =========================
# LOAD DATA
# =========================

movies = pd.read_csv(MOVIELENS / "movies.csv")
ratings = pd.read_csv(MOVIELENS / "ratings.csv")
tags = pd.read_csv(MOVIELENS / "tags.csv")
links = pd.read_csv(MOVIELENS / "links.csv")

netflix = pd.read_csv(NETFLIX / "netflix_titles.csv")


# =========================
# CLEAN MOVIELENS MOVIES
# =========================

movies = movies.drop_duplicates()

movies["title"] = movies["title"].fillna("").str.strip()
movies["genres"] = movies["genres"].fillna("Unknown")

# Extract year from titles like:
# Toy Story (1995)

movies["year"] = movies["title"].str.extract(r"\((\d{4})\)$")

# Remove year from title
movies["clean_title"] = (
    movies["title"]
    .str.replace(r"\s*\(\d{4}\)$", "", regex=True)
    .str.strip()
)


# =========================
# CLEAN RATINGS
# =========================

ratings = ratings.drop_duplicates()

ratings["timestamp"] = pd.to_datetime(
    ratings["timestamp"],
    unit="s"
)

ratings = ratings[
    ratings["rating"].between(0.5, 5.0)
]


# =========================
# CLEAN TAGS
# =========================

tags = tags.drop_duplicates()

tags["tag"] = (
    tags["tag"]
    .fillna("")
    .str.strip()
    .str.lower()
)

tags = tags[tags["tag"] != ""]


# =========================
# CLEAN NETFLIX
# =========================

netflix = netflix.drop_duplicates()

netflix["title"] = netflix["title"].fillna("").str.strip()

netflix["description"] = (
    netflix["description"]
    .fillna("")
    .str.strip()
)

netflix["listed_in"] = (
    netflix["listed_in"]
    .fillna("Unknown")
    .str.strip()
)

netflix["director"] = (
    netflix["director"]
    .fillna("Unknown")
    .str.strip()
)

netflix["country"] = (
    netflix["country"]
    .fillna("Unknown")
    .str.strip()
)

netflix["type"] = (
    netflix["type"]
    .fillna("Unknown")
    .str.strip()
)


# =========================
# SAVE CLEAN DATA
# =========================

movies.to_csv(
    PROCESSED / "movies_clean.csv",
    index=False
)

ratings.to_csv(
    PROCESSED / "ratings_clean.csv",
    index=False
)

tags.to_csv(
    PROCESSED / "tags_clean.csv",
    index=False
)

links.to_csv(
    PROCESSED / "links_clean.csv",
    index=False
)

netflix.to_csv(
    PROCESSED / "netflix_clean.csv",
    index=False
)


# =========================
# RESULTS
# =========================

print("\n✅ DATA CLEANING COMPLETE")

print("\nMovieLens Movies:", movies.shape)
print("MovieLens Ratings:", ratings.shape)
print("MovieLens Tags:", tags.shape)
print("Netflix:", netflix.shape)

print("\nFiles created inside data/processed/:")
print("- movies_clean.csv")
print("- ratings_clean.csv")
print("- tags_clean.csv")
print("- links_clean.csv")
print("- netflix_clean.csv")