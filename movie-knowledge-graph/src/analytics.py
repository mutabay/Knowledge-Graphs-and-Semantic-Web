"""
Movie Knowledge Graph Analytics

This module demonstrates different analytical capabilities of:
1. RDF/SPARQL - Great for semantic reasoning and complex logical queries
2. Neo4j/Cypher - Great for graph traversal and pattern matching
"""

from .rdf_builder import MovieRDFBuilder
from .neo4j_loader import MovieNeo4jLoader
import logging

logger = logging.getLogger(__name__)


class MovieAnalytics:
    """Analytics for both RDF and Neo4j movie knowledge graphs"""

    def __init__(self, rdf_builder: MovieRDFBuilder = None,
                 neo4j_loader: MovieNeo4jLoader = None):
        self.rdf_builder = rdf_builder
        self.neo4j_loader = neo4j_loader

    def compare_query_approaches(self, director_name: str = "Christopher Nolan"):
        """Compare how the same query works in SPARQL vs Cypher"""
        print(f"\n🎬 Finding movies by {director_name}")
        print("-" * 50)

        # SPARQL approach
        if self.rdf_builder:
            print("\n📊 SPARQL Query (RDF):")
            sparql_results = self.sparql_movies_by_director(director_name)
            if sparql_results:
                for movie in sparql_results:
                    print(f"   • {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
            else:
                print("   No results found")

        # Cypher approach
        if self.neo4j_loader:
            print("\n🔍 Cypher Query (Neo4j):")
            cypher_results = self.cypher_movies_by_director(director_name)
            if cypher_results:
                for movie in cypher_results:
                    print(f"   • {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
            else:
                print("   No results found")
        else:
            print("\n🔍 Cypher Query (Neo4j):")
            print("   ⚠️ Neo4j not available - skipped")

    def sparql_movies_by_director(self, director_name):
        """SPARQL query to find movies by director"""
        query = """
                PREFIX movie: <http://movie-kg.org/ontology#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>

                SELECT ?title ?year ?rating
                WHERE {
                    ?movie a movie:Movie .
                    ?movie movie:hasTitle ?title .
                    ?movie movie:releasedIn ?year .
                    ?movie movie:hasRating ?rating .
                    ?movie movie:directedBy ?director .
                    ?director foaf:name ?director_name .
                    FILTER(?director_name = "%s")
                }
                ORDER BY ?year
                """ % director_name

        results = []
        for row in self.rdf_builder.graph.query(query):
            results.append({
                'title': str(row.title),
                'year': int(row.year),
                'rating': float(row.rating)
            })
        return results

    def cypher_movies_by_director(self, director_name):
        """Cypher query to find movies by director"""

        query = """
                MATCH (m:Movie)-[:DIRECTED_BY]->(d:Director {name: $director_name})
                RETURN m.title as title, m.year as year, m.rating as rating
                ORDER BY m.year
                """

        results = []
        with self.neo4j_loader.driver.session() as session:
            result = session.run(query, director_name=director_name)
            for record in result:
                results.append({
                    'title': record['title'],
                    'year': record['year'],
                    'rating': record['rating']
                })

        return results

# Example usage
if __name__ == "__main__":
    # This will be our main comparison script
    pass