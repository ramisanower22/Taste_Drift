import pandas as pd
from pathlib import Path

# Main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset locations
MOVIELENS = BASE_DIR / "data" / "raw" / "movielens"
NETFLIX = BASE_DIR / "data" / "raw" / "netflix"

# Load MovieLens
movies = pd.read_csv(MOVIELENS / "movies.csv")
ratings = pd.read_csv(MOVIELENS / "ratings.csv")
tags = pd.read_csv(MOVIELENS / "tags.csv")
links = pd.read_csv(MOVIELENS / "links.csv")

# Load Netflix
netflix = pd.read_csv(NETFLIX / "netflix_titles.csv")

# Show information
datasets = {
    "MovieLens Movies": movies,
    "MovieLens Ratings": ratings,
    "MovieLens Tags": tags,
    "MovieLens Links": links,
    "Netflix": netflix
}

for name, df in datasets.items():
    print(f"\n===== {name} =====")
    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())
    print(df.head(3))

print("\n✅ ALL DATASETS LOADED SUCCESSFULLY")