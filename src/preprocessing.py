import pandas as pd
import numpy as np
import json

# Load the datasets
movies_file = "./data/movies_metadata.csv"
ratings_file = "./data/ratings_small.csv"

# Load the movies metadata
def load_movies_data(file):
    try:
        movies_df = pd.read_csv(file, low_memory=False)
        print("Movies Metadata Loaded Successfully")
        return movies_df
    except Exception as e:
        print(f"Error loading movies data: {e}")
        return None

# Load the ratings data
def load_ratings_data(file):
    try:
        ratings_df = pd.read_csv(file)
        print("Ratings Data Loaded Successfully")
        return ratings_df
    except Exception as e:
        print(f"Error loading ratings data: {e}")
        return None

# Explore the movies dataset
def explore_movies_data(df):
    print("\nMovies Dataset Info:\n")
    print(df.info())
    print("\nSample Data:\n")
    print(df.head())
    print("\nMissing Values per Column:\n")
    print(df.isnull().sum())

# Preprocess movies metadata
def preprocess_movies_data(movies_df):

    df = movies_df.copy()
    # Drop columns with excessive missing values from movies_metadata
    columns_to_drop = ['belongs_to_collection', 'homepage', 'tagline']
    df = df.drop(columns=columns_to_drop)

    # Drop duplicates based on 'id'
    df = df.drop_duplicates(subset=['id'])

    # Handle missing values
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce').fillna(0)
    df['revenue'] = df['revenue'].fillna(0).astype(float)
    df['runtime'] = df['runtime'].fillna(df['runtime'].median())

    # Parse JSON-like columns
    def parse_json_column(column):
        def extract_names(value):
            try:
                return [item['name'] for item in json.loads(value.replace("'", '"'))] if isinstance(value, str) else []
            except:
                return []

        return column.apply(extract_names)

    df['genres'] = parse_json_column(df['genres'])
    df['production_companies'] = parse_json_column(df['production_companies'])
    df['production_countries'] = parse_json_column(df['production_countries'])
    df['spoken_languages'] = parse_json_column(df['spoken_languages'])

    # Handle release_date
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year

    # Create derived columns
    df['profit'] = df['revenue'] - df['budget']
    df['profit_margin'] = (df['profit'] / df['budget']).replace([np.inf, -np.inf], 0).fillna(0)

    # Drop unnecessary columns
    columns_to_drop = ['homepage', 'overview', 'tagline', 'poster_path', 'backdrop_path']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    return df

# Preprocess ratings data
def preprocess_ratings_data(ratings_df):
    df = ratings_df.copy()

    # Handle missing values
    df = df.dropna()

    # Drop duplicates
    df = df.drop_duplicates()

    return df

# Save cleaned data
def save_cleaned_data(df, file_name):
    try:
        df.to_csv(file_name, index=False)
        print(f"Cleaned data saved to {file_name}")
    except Exception as e:
        print(f"Error saving cleaned data: {e}")

if __name__ == "__main__":
    # Load datasets
    movies_df = load_movies_data(movies_file)
    ratings_df = load_ratings_data(ratings_file)

    if movies_df is not None:
        print("\nExploring Movies Metadata...")
        explore_movies_data(movies_df)

        print("\nPreprocessing Movies Metadata...")
        cleaned_movies_df = preprocess_movies_data(movies_df)
        save_cleaned_data(cleaned_movies_df, "./data/cleaned_movies_metadata.csv")

    if ratings_df is not None:
        print("\nPreprocessing Ratings Data...")
        cleaned_ratings_df = preprocess_ratings_data(ratings_df)
        save_cleaned_data(cleaned_ratings_df, "./data/cleaned_ratings_small.csv")
