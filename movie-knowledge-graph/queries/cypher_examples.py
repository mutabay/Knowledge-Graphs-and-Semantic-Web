"""
Cypher Query Examples for Movie Knowledge Graph

Cypher is Neo4j's query language. It's designed to be intuitive
and uses ASCII art to represent graph patterns.

Key Cypher concepts:
- () = nodes
- [] = relationships
- --> = directed relationship
- MATCH = find patterns
- WHERE = add conditions
- RETURN = what to output
"""

from neo4j import GraphDatabase
from typing import List, Dict, Any


class MovieCypherQueries:
    """Collection of useful Cypher queries for movie data"""

    def __init__(self, driver):
        self.driver = driver

    def find_all_movies(self) -> List[Dict]:
        """Basic query: Find all movies with their directors"""

        query = """
        MATCH (m:Movie)-[:DIRECTED_BY]->(d:Director)
        RETURN m.title as title, m.year as year, 
               m.rating as rating, d.name as director
        ORDER BY m.year
        """

        return self.execute_query(query)

    def find_movies_by_genre(self, genre_name: str) -> List[Dict]:
        """Find all movies of a specific genre"""

        query = """
        MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: $genre_name})
        RETURN m.title as title, m.year as year, m.rating as rating
        ORDER BY m.rating DESC
        """

        return self.execute_query(query, genre_name=genre_name)

    def find_director_collaborations(self) -> List[Dict]:
        """Find directors who worked on similar genres"""

        query = """
        MATCH (d1:Director)<-[:DIRECTED_BY]-(m1:Movie)-[:HAS_GENRE]->(g:Genre)
        MATCH (d2:Director)<-[:DIRECTED_BY]-(m2:Movie)-[:HAS_GENRE]->(g)
        WHERE d1.name < d2.name  // Avoid duplicates
        RETURN d1.name as director1, d2.name as director2, 
               g.name as shared_genre, 
               count(g) as collaborations
        ORDER BY collaborations DESC
        """

        return self.execute_query(query)

    def find_genre_network(self) -> List[Dict]:
        """Find how genres are connected through movies"""

        query = """
        MATCH (g1:Genre)<-[:HAS_GENRE]-(m:Movie)-[:HAS_GENRE]->(g2:Genre)
        WHERE g1.name < g2.name
        RETURN g1.name as genre1, g2.name as genre2, 
               count(m) as movies_in_common,
               collect(m.title) as movie_titles
        ORDER BY movies_in_common DESC
        """

        return self.execute_query(query)

    def find_prolific_directors(self, min_movies: int = 2) -> List[Dict]:
        """Find directors with multiple movies"""

        query = """
        MATCH (d:Director)<-[:DIRECTED_BY]-(m:Movie)
        WITH d, count(m) as movie_count, collect(m.title) as movies,
             avg(m.rating) as avg_rating
        WHERE movie_count >= $min_movies
        RETURN d.name as director, movie_count, movies, 
               round(avg_rating, 1) as average_rating
        ORDER BY movie_count DESC, average_rating DESC
        """

        return self.execute_query(query, min_movies=min_movies)

    def find_movie_recommendations(self, movie_title: str, limit: int = 3) -> List[Dict]:
        """Simple recommendation: movies with shared genres"""

        query = """
        MATCH (target:Movie {title: $movie_title})-[:HAS_GENRE]->(g:Genre)
        MATCH (recommendation:Movie)-[:HAS_GENRE]->(g)
        WHERE target <> recommendation
        WITH recommendation, count(g) as shared_genres
        MATCH (recommendation)-[:DIRECTED_BY]->(d:Director)
        RETURN recommendation.title as title, 
               recommendation.year as year,
               recommendation.rating as rating,
               d.name as director,
               shared_genres
        ORDER BY shared_genres DESC, recommendation.rating DESC
        LIMIT $limit
        """

        return self.execute_query(query, movie_title=movie_title, limit=limit)

    def analyze_decade_trends(self) -> List[Dict]:
        """Analyze movie trends by decade"""

        query = """
        MATCH (m:Movie)
        WITH (m.year / 10) * 10 as decade, m
        RETURN decade, 
               count(m) as movie_count,
               avg(m.rating) as average_rating,
               collect(DISTINCT m.title)[0..3] as sample_movies
        ORDER BY decade
        """

        return self.execute_query(query)

    def find_shortest_path_between_directors(self, director1: str, director2: str) -> List[Dict]:
        """Find connection between two directors through genres"""

        query = """
        MATCH path = shortestPath(
            (d1:Director {name: $director1})-[*]-(d2:Director {name: $director2})
        )
        RETURN [node in nodes(path) | 
                CASE 
                    WHEN node:Director THEN node.name
                    WHEN node:Genre THEN node.name
                    WHEN node:Movie THEN node.title
                END
               ] as connection_path,
               length(path) as path_length
        """

        return self.execute_query(query, director1=director1, director2=director2)

    def execute_query(self, query: str, **parameters) -> List[Dict]:
        """Execute Cypher query and return results"""

        results = []
        try:
            with self.driver.session() as session:
                result = session.run(query, **parameters)
                results = [dict(record) for record in result]

        except Exception as e:
            print(f"Error executing Cypher query: {e}")

        return results


# Example usage and testing
def demo_cypher_queries():
    """Demonstrate Cypher queries"""

    print("Cypher Query Examples")
    print("=" * 40)
    print("(This demo requires a running Neo4j database)")

    # Example queries you can run:
    queries_to_try = [
        "Find all movies with directors",
        "Find Sci-Fi movies",
        "Find director collaborations",
        "Analyze genre networks",
        "Get movie recommendations",
        "Analyze decade trends"
    ]

    for i, query_desc in enumerate(queries_to_try, 1):
        print(f"{i}. {query_desc}")

    print("\nCypher uses intuitive ASCII art:")
    print("  (movie)-[:DIRECTED_BY]->(director)")
    print("  (movie)-[:HAS_GENRE]->(genre)")


if __name__ == "__main__":
    demo_cypher_queries()
