from py2neo import Graph, Node, Relationship
import csv

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))  

# Function to load movie nodes
def load_movies(csv_file):
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Handle missing/null values
            release_year = row["release_year"] if row["release_year"] else None
            budget = float(row["budget"]) if row["budget"] else 0
            revenue = float(row["revenue"]) if row["revenue"] else 0
            vote_average = float(row["vote_average"]) if row["vote_average"] else 0
            vote_count = int(float(row["vote_count"])) if row["vote_count"] else 0
            runtime = float(row["runtime"]) if row["runtime"] else 0
            profit_margin = float(row["profit_margin"]) if row["profit_margin"] else 0
            
            # Create Movie node
            movie_node = Node(
                "Movie",
                movieId=row["id"],  # Use `id` as the unique identifier for Movie
                title=row["title"] if row["title"] else "Unknown",
                original_title=row["original_title"],
                genres=row["genres"],
                release_year=release_year,
                budget=budget,
                revenue=revenue,
                runtime=runtime,
                vote_average=vote_average,
                vote_count=vote_count,
                profit_margin=profit_margin,
                language=row["original_language"],
                popularity=row["popularity"],
                production_companies=row["production_companies"],
                production_countries=row["production_countries"],
                release_date=row["release_date"],
                spoken_languages=row["spoken_languages"],
                status=row["status"],
            )
            # Merge ensures no duplicates
            graph.merge(movie_node, "Movie", "movieId")

# Function to load user nodes and RATED relationships
def load_users_and_ratings(csv_file):
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create User node
            user_node = Node("User", userId=row["userId"])  # `userId` is unique for each User
            graph.merge(user_node, "User", "userId")  # Merge ensures no duplicate User nodes
            
            # Match the Movie node by movieId
            movie_node = graph.nodes.match("Movie", movieId=row["movieId"]).first()
            if movie_node:
                # Create RATED relationship
                rated_rel = Relationship(
                    user_node,
                    "RATED",
                    movie_node,
                    rating=float(row["rating"]),
                    timestamp=row["timestamp"]
                )
                graph.merge(rated_rel)  # Merge ensures no duplicate relationships

# File paths
movies_file = "./data/cleaned_movies_metadata.csv"  
ratings_file = "./data/cleaned_ratings_small.csv"   

# Load data into Neo4j
load_movies(movies_file)
load_users_and_ratings(ratings_file)

print("Data successfully uploaded to Neo4j!")
