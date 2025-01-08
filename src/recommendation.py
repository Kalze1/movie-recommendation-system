from py2neo import Graph

graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))


def get_user_rated_movies(user_id):
    """Fetch movies rated by the user."""
    query = """
        MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie)
        RETURN m.title AS title, r.rating AS rating
        ORDER BY r.rating DESC
    """
    results = graph.run(query, user_id=user_id).data()
    return results or []


def get_collaborative_recommendations(graph, user_id, limit=10):
    """Fetch movie recommendations using collaborative filtering."""
    query = """
        MATCH (u1:User {userId: $user_id})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2:User)
        WHERE r1.rating >= 4 AND r2.rating >= 4
        WITH u1, u2, COUNT(m) AS common_movies
        WHERE common_movies >= 3
        MATCH (u2)-[r3:RATED]->(rec:Movie)
        WHERE NOT EXISTS((u1)-[:RATED]->(rec))
        RETURN DISTINCT rec.title AS title, rec.genres AS genres
        ORDER BY rec.title ASC
        LIMIT $limit
    """
    results = graph.run(query, user_id=user_id, limit=limit).data()
    return results or []


def get_content_based_recommendations(graph, user_id, limit=10):
    """Fetch movie recommendations using content-based filtering."""
    query = """
        MATCH (u1:User {userId: $user_id})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2:User)
        WHERE r1.rating >= 4 AND r2.rating >= 4
        WITH u1, u2, COLLECT(DISTINCT m.genres) AS user_genres
        UNWIND user_genres AS genre
        WITH u1, u2, genre, count(*) AS genre_count
        ORDER BY genre_count DESC
        WITH u1, u2, COLLECT(genre)[..3] AS top_genres
        MATCH (u2)-[r3:RATED]->(rec:Movie)
        WHERE ANY(g IN rec.genres WHERE g IN top_genres)
        AND NOT EXISTS((u1)-[:RATED]->(rec))
        RETURN DISTINCT rec.title AS title, rec.genres AS genres, avg(r3.rating) AS avg_rating
        ORDER BY avg_rating DESC, rec.title ASC
        LIMIT $limit
    """
    results = graph.run(query, user_id=user_id, limit=limit).data()
    return results or []


def get_recommendations(graph, user_id):
    """Combine collaborative filtering and content-based filtering."""
    collaborative_recommendations = get_collaborative_recommendations(graph, user_id, limit=10)
    if len(collaborative_recommendations) < 3:
        content_based_recommendations = get_content_based_recommendations(graph, user_id, limit=10)
        combined_recommendations = collaborative_recommendations + content_based_recommendations
        combined_recommendations = {rec['title']: rec for rec in combined_recommendations}.values()
    else:
        combined_recommendations = collaborative_recommendations

    sorted_recommendations = sorted(
        combined_recommendations, key=lambda x: (x.get('avg_rating', 0), x['title']), reverse=True
    )
    return sorted_recommendations[:10]


def main():
    print("Welcome to the Movie Recommendation System!")

    while True:
        user_id = input("\nEnter your userId (or type 'exit' to quit): ")
        if user_id.lower() == "exit":
            print("Exiting the Movie Recommendation System. Goodbye!")
            break

        # Display movies rated by the user
        print("\nMovies You've Rated:")
        user_movies = get_user_rated_movies(user_id)
        if not user_movies:
            print("No movies found for this user.")
        else:
            for movie in user_movies:
                print(f" - {movie['title']} (Rating: {movie['rating']})")

        # Display recommendations
        print("\nRecommended Movies for You:")
        recommendations = get_recommendations(graph, user_id)
        if not recommendations:
            print("No recommendations available for this user.")
        else:
            for movie in recommendations:
                print(f" - {movie['title']} (Genres: {movie.get('genres', 'N/A')}, "
                      f"Avg Rating: {movie.get('avg_rating', 'N/A')})")

if __name__ == "__main__":
    main()