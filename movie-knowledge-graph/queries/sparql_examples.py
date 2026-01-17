"""
SPARQL Query Examples for Movie Knowledge Graph

SPARQL (SPARQL Protocol and RDF Query Language) is the standard query
language for RDF data. It's like SQL but for graph data.

Key SPARQL concepts:
- PREFIX: Define namespace shortcuts
- SELECT: What variables to return
- WHERE: Pattern matching conditions
- FILTER: Add constraints
- OPTIONAL: Include optional patterns
"""

from rdflib import Graph
from typing import List, Dict, Any


class MovieSPARQLQueries:
    """Collection of useful SPARQL queries for movie data"""

    def __init__(self, graph: Graph):
        self.graph = graph

        # Define common prefixes for cleaner queries
        self.prefixes = """
        PREFIX movie: <http://movie-kg.org/ontology#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        """

    def find_all_movies(self) -> List[Dict]:
        """Basic query: Find all movies with their details"""

        query = self.prefixes + """
        SELECT ?title ?year ?rating ?director_name
        WHERE {
            ?movie a movie:Movie .
            ?movie movie:hasTitle ?title .
            ?movie movie:releasedIn ?year .
            ?movie movie:hasRating ?rating .
            ?movie movie:directedBy ?director .
            ?director foaf:name ?director_name .
        }
        ORDER BY ?year
        """

        return self.execute_query(query)

    def find_movies_by_genre(self, genre_name: str) -> List[Dict]:
        """Find all movies of a specific genre"""

        query = self.prefixes + f"""
        SELECT ?title ?year ?rating
        WHERE {{
            ?movie a movie:Movie .
            ?movie movie:hasTitle ?title .
            ?movie movie:releasedIn ?year .
            ?movie movie:hasRating ?rating .
            ?movie movie:hasGenre ?genre .
            ?genre foaf:name "{genre_name}" .
        }}
        ORDER BY ?rating DESC
        """

        return self.execute_query(query)

    def find_highly_rated_movies(self, min_rating: float = 8.5) -> List[Dict]:
        """Find movies above a certain rating threshold"""

        query = self.prefixes + f"""
        SELECT ?title ?year ?rating ?director_name
        WHERE {{
            ?movie a movie:Movie .
            ?movie movie:hasTitle ?title .
            ?movie movie:releasedIn ?year .
            ?movie movie:hasRating ?rating .
            ?movie movie:directedBy ?director .
            ?director foaf:name ?director_name .
            FILTER(?rating >= {min_rating})
        }}
        ORDER BY ?rating DESC
        """

        return self.execute_query(query)

    def count_movies_by_director(self) -> List[Dict]:
        """Count how many movies each director has made"""

        query = self.prefixes + """
        SELECT ?director_name (COUNT(?movie) as ?movie_count)
        WHERE {
            ?movie a movie:Movie .
            ?movie movie:directedBy ?director .
            ?director foaf:name ?director_name .
        }
        GROUP BY ?director_name
        ORDER BY DESC(?movie_count)
        """

        return self.execute_query(query)

    def find_genre_combinations(self) -> List[Dict]:
        """Find movies that have multiple genres (complex pattern)"""

        query = self.prefixes + """
        SELECT ?title ?genre1_name ?genre2_name
        WHERE {
            ?movie a movie:Movie .
            ?movie movie:hasTitle ?title .
            ?movie movie:hasGenre ?genre1 .
            ?movie movie:hasGenre ?genre2 .
            ?genre1 foaf:name ?genre1_name .
            ?genre2 foaf:name ?genre2_name .
            FILTER(?genre1_name < ?genre2_name)  # Avoid duplicates
        }
        ORDER BY ?title
        """

        return self.execute_query(query)

    def find_movies_in_decade(self, decade_start: int) -> List[Dict]:
        """Find movies released in a specific decade"""

        decade_end = decade_start + 9

        query = self.prefixes + f"""
        SELECT ?title ?year ?rating
        WHERE {{
            ?movie a movie:Movie .
            ?movie movie:hasTitle ?title .
            ?movie movie:releasedIn ?year .
            ?movie movie:hasRating ?rating .
            FILTER(?year >= {decade_start} && ?year <= {decade_end})
        }}
        ORDER BY ?year
        """

        return self.execute_query(query)

    def execute_query(self, query: str) -> List[Dict]:
        """Execute SPARQL query and return results as list of dictionaries"""

        results = []
        try:
            query_result = self.graph.query(query)

            for row in query_result:
                # Convert query result to dictionary
                row_dict = {}
                for var in query_result.vars:
                    value = getattr(row, str(var))
                    # Convert RDF literals to Python types
                    if hasattr(value, 'toPython'):
                        row_dict[str(var)] = value.toPython()
                    else:
                        row_dict[str(var)] = str(value)
                results.append(row_dict)

        except Exception as e:
            print(f"Error executing SPARQL query: {e}")

        return results


# Example usage and testing
def demo_sparql_queries():
    """Demonstrate SPARQL queries"""

    # This would normally load from your RDF file
    print("🔍 SPARQL Query Examples")
    print("=" * 40)
    print("(This demo requires a loaded RDF graph)")

    # Example queries you can run:
    queries_to_try = [
        "Find all movies",
        "Find Sci-Fi movies",
        "Find highly rated movies (8.5+)",
        "Count movies by director",
        "Find movies from the 1990s"
    ]

    for i, query_desc in enumerate(queries_to_try, 1):
        print(f"{i}. {query_desc}")


if __name__ == "__main__":
    demo_sparql_queries()
