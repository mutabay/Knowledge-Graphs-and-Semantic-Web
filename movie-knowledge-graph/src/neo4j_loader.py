"""
Neo4j Property Graph Loader for Movies

Neo4j uses a property graph model where:
- Nodes have labels and properties
- Relationships have types and properties
- Everything is stored as graph structures optimized for traversal
"""

from neo4j import GraphDatabase
import pandas as pd
from typing import Dict, List, Optional, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MovieNeo4jLoader:
    """
    Loads movie data into Neo4j property graph database.

    Key Concepts:
    - Node: An entity (Movie, Director, Genre)
    - Relationship: A connection between nodes (DIRECTED, HAS_GENRE)
    - Property: Attributes stored on nodes/relationships
    - Label: Type/category of a node
    """

    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        """
        Initialize connection to Neo4j database.

        Make sure Neo4j is running! Start it with Docker:
        docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
        """
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test connection
            with self.driver.session() as session:
                result = session.run("RETURN 1")
                result.single()
            logger.info("Successfully connected to Neo4j")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        "Close the database connection"
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")

    def clear_database(self):
        """
        Clear all data from the database
        !!! WARNING: This deletes everythign !!!
        """
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Database cleared!")

    def create_constraints_and_indexes(self):
        """
        Create database constraints and indexes for better performance.

        Constraints ensure data integrity.
        Indexes speed up queries.
        """

        constraints_and_indexes = [
            # Unique constraints
            "CREATE CONSTRAINT movie_id_unique IF NOT EXISTS FOR (m:Movie) REQUIRE m.id IS UNIQUE",
            "CREATE CONSTRAINT director_name_unique IF NOT EXISTS FOR (d:Director) REQUIRE d.name IS UNIQUE",
            "CREATE CONSTRAINT genre_name_unique IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE",

            # Indexes for faster lookups
            "CREATE INDEX movie_title_index IF NOT EXISTS FOR (m:Movie) ON (m.title)",
            "CREATE INDEX movie_year_index IF NOT EXISTS FOR (m:Movie) ON (m.year)",
            "CREATE INDEX movie_rating_index IF NOT EXISTS FOR (m:Movie) ON (m.rating)"
        ]

        with self.driver.session() as session:
            for c_i in constraints_and_indexes:
                try:
                    session.run(c_i)
                except Exception as e:
                    # Constraint might already exist
                    logger.debug(f"Constraint/Index creation note: {e}")

        logger.info("Database constraints and indexes created")

    def add_movie(self, movie_id: str, title: str, year: int,
                  genres: List[str], director: str, rating: float):
        """
        Add a single movie with all its relationships.

        This uses Cypher's MERGE command which creates nodes/relationships
        only if they don't already exist.

        Args:
            movie_id:
            title:
            year:
            genres:
            director:
            rating:

        Returns:

        """

        with self.driver.session() as session:
            # Use a transaction for data consistency
            session.execute_write(self.create_movie_transaction, movie_id, title, year, genres, director, rating)

    def create_movie_transaction(self, tx, movie_id: str, title: str, year: int, genres: List[str], director: str,
                                 rating: float):
       """
       Transaction function to create movie and all relationships
        Cypher Query Breakdown:
        - MERGE: Create if doesn't exist, match if it does
        - WITH: Pass variables to next part of query
        - UNWIND: Convert list to individual rows
       Args:
           self:
           tx:
           movie_id:
           title:
           year:
           genres:
           director:
           rating:

       Returns:

       """
       query = """
               // Create or match the movie
               MERGE (m:Movie {id: $movie_id})
               SET m.title = $title,
                   m.year = $year,
                   m.rating = $rating,
                   m.created_at = datetime()

               // Create or match the director
               MERGE (d:Director {name: $director})
               SET d.created_at = coalesce(d.created_at, datetime())

               // Create relationship between movie and director
               MERGE (m)-[:DIRECTED_BY]->(d)

               // Handle genres
               WITH m
               UNWIND $genres as genre_name
               MERGE (g:Genre {name: genre_name})
               SET g.created_at = coalesce(g.created_at, datetime())
               MERGE (m)-[:HAS_GENRE]->(g)

               RETURN m.title as title
               """

       result = tx.run(query,
                       movie_id=movie_id, title=title, year=year,
                       director=director, rating=rating, genres=genres)

    def load_from_csv(self, csv_path: str):
        """Load movie data from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Loading {len(df)} movies from {csv_path}")

            # Create constraints first for better performance
            self.create_constraints_and_indexes()

            for _, row in df.iterrows():
                genres = row['genres'].split('|') if pd.notna(row['genres']) else []

                self.add_movie(
                    movie_id=str(row['movie_id']),
                    title=row['title'],
                    year=int(row['year']),
                    genres=genres,
                    director=row['director'],
                    rating=float(row['rating'])
                )

            logger.info(f"Successfully loaded {len(df)} movies into Neo4j")

        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""

        with self.driver.session() as session:
            # Count nodes by label
            stats = {}

            labels = ['Movie', 'Director', 'Genre']
            for label in labels:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                stats[label.lower() + 's'] = result.single()['count']

            # Count relationships
            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            stats['relationships'] = result.single()['count']

            # Average rating
            result = session.run("MATCH (m:Movie) RETURN avg(m.rating) as avg_rating")
            avg_rating = result.single()['avg_rating']
            stats['average_rating'] = round(float(avg_rating), 2) if avg_rating else 0

            return stats

    def run_sample_queries(self):
        """Run some example queries to demonstrate Cypher"""

        with self.driver.session() as session:

            print("=== Sample Neo4j Queries ===\n")

            # 1. Find all movies by Christopher Nolan
            print("1. Movies by Christopher Nolan:")
            result = session.run("""
                MATCH (m:Movie)-[:DIRECTED_BY]->(d:Director {name: 'Christopher Nolan'})
                RETURN m.title as title, m.year as year, m.rating as rating
                ORDER BY m.year
            """)

            for record in result:
                print(f"   {record['title']} ({record['year']}) - Rating: {record['rating']}")

            # 2. Find genres and their movie counts
            print("\n2. Genres by movie count:")
            result = session.run("""
                MATCH (g:Genre)<-[:HAS_GENRE]-(m:Movie)
                RETURN g.name as genre, count(m) as movie_count
                ORDER BY movie_count DESC
            """)

            for record in result:
                print(f"   {record['genre']}: {record['movie_count']} movies")

            # 3. Find movies with highest ratings
            print("\n3. Top rated movies:")
            result = session.run("""
                MATCH (m:Movie)
                RETURN m.title as title, m.rating as rating, m.year as year
                ORDER BY m.rating DESC
                LIMIT 3
            """)

            for record in result:
                print(f"   {record['title']} ({record['year']}) - {record['rating']}")


# Example usage and testing
if __name__ == "__main__":
    # Create loader
    loader = MovieNeo4jLoader()

    try:
        # Clear and load fresh data
        loader.clear_database()
        loader.load_from_csv("../data/raw/movies.csv")

        # Show statistics
        stats = loader.get_statistics()
        print("Neo4j Database Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # Run sample queries
        loader.run_sample_queries()

    finally:
        loader.close()