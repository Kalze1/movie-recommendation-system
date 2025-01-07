from py2neo import Graph

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678")) 

def get_user_rated_movies(user_id):
    """
    Fetch movies rated by the user.
    """
    query = """
    MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie)
    RETURN m.title AS title, r.rating AS rating
    ORDER BY r.rating DESC
    """
    results = graph.run(query, user_id=user_id).data()
    return results


def get_collaborative_recommendations(user_id, limit=10):
    """
    Fetch movie recommendations using collaborative filtering.
    """
    query = """
    MATCH (u1:User {userId: $user_id})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2:User)
    WHERE r1.rating >= 4 AND r2.rating >= 4
    WITH u1, u2
    MATCH (u2)-[r3:RATED]->(rec:Movie)
    WHERE NOT EXISTS((u1)-[:RATED]->(rec))
    RETURN DISTINCT rec.title AS title, rec.genres AS genres
    ORDER BY rec.title ASC
    LIMIT $limit
    """
    results = graph.run(query, user_id=user_id, limit=limit).data()
    return results


def get_content_based_recommendations(user_id, limit=10):
    """
    Fetch movie recommendations using content-based filtering.
    """
    query = """
    MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie)
    WHERE r.rating >= 4
    WITH COLLECT(m.genres) AS user_genres
    MATCH (rec:Movie)
    WHERE ANY(genre IN user_genres WHERE genre IN rec.genres)
      AND NOT EXISTS((u)-[:RATED]->(rec))
    RETURN DISTINCT rec.title AS title, rec.genres AS genres
    ORDER BY rec.title ASC
    LIMIT $limit
    """
    results = graph.run(query, user_id=user_id, limit=limit).data()
    return results


def get_recommendations(user_id):
    """
    Combine collaborative filtering and content-based filtering to generate recommendations.
    """
    # Step 1: Get recommendations using collaborative filtering
    collaborative_recommendations = get_collaborative_recommendations(user_id, limit=10)

    # Step 2: If collaborative filtering doesn't yield enough results, use content-based filtering
    if len(collaborative_recommendations) < 3:
        content_based_recommendations = get_content_based_recommendations(user_id, limit=10)
        combined_recommendations = collaborative_recommendations + content_based_recommendations
        # Remove duplicates
        combined_recommendations = {rec['title']: rec for rec in combined_recommendations}.values()
        return list(combined_recommendations)[:10]
    else:
        return collaborative_recommendations[:10]


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
        recommendations = get_recommendations(user_id)
        if not recommendations:
            print("No recommendations available for this user.")
        else:
            for movie in recommendations:
                print(f" - {movie['title']} (Genres: {movie.get('genres', 'N/A')})")


if __name__ == "__main__":
    main()
