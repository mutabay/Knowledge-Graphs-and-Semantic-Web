'''
Docstring for Semantic-Web.movie-knowledge-graph.src.rdf_builder

This module creates an RDF-based knowledge graph using semantic web standards.

'''

from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD
from rdflib.namespace import FOAF
import pandas as pd
from typing import List, Dict, Optional
import logging

# Set Up Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MovieRDFBuilder:
    """Builds RDF knowledge graphs for movie data
    
    Keyword arguments:
    - namespace: A way to avoid naming conflicts (like packages)
    - URI: Unique identifier for each resource
    - Triple: Subject-Predicate-Object statement
    
    """

    def __init__(self):
        # Define our custom namespace for movie domain
        self.MOVIE = Namespace("http://movie-kg.org/ontology#")
        self.graph = Graph()

        # Bind namespaces for output
        self.graph.bind("movie", self.MOVIE)
        self.graph.bind("foaf", self.MOVIE)
        self.graph.bind("xsd", self.MOVIE)

        # Initialize ontology structure
        self.create_ontology()

        logger.info("MovieRDFBuilder initialized")

    def create_ontology(self):
        """
        Create the ontological structure of movie domain

        Something like defining "schema" or "types" in our knowledge graph.
        Define what kinds of things exist and how they can relate.

        """

        # Define Classes
        classes = {
            self.MOVIE.Movie: "A cinematic work",
            self.MOVIE.Actor: "A person who performs in movies",
            self.MOVIE.Director: "A person who directs movies",
            self.MOVIE.Genre: "A category or style of movie",
            self.MOVIE.User: "A person who rates or reviews movies"
        }

        for class_uri, description in classes.items():
            self.graph.add((class_uri, RDF.type, RDFS.Class))
            self.graph.add((class_uri, RDFS.comment, Literal(description)))

        properties = {
            self.MOVIE.hasTitle: "The title of a movie",
            self.MOVIE.releasedIn: "The year a movie was released",
            self.MOVIE.hasGenre: "A movie belongs to this genre",
            self.MOVIE.directedBy: "A movie was directed by this person",
            self.MOVIE.actedIn: "An actor performed in this movie",
            self.MOVIE.hasRating: "The rating score of a movie"
        }
        for prop_uri, description in properties.items():
            self.graph.add((prop_uri, RDF.type, RDF.Property))
            self.graph.add((prop_uri, RDFS.comment, Literal(description)))

        logger.info(f"Ontology created with {len(classes)} classes and {len(properties)} properties")

    def add_movie(self, movie_id: str, title: str, year: int, genres: list[str], director: str,
                  rating: float) -> URIRef:
        """
        Add single movie to the knowledge graph

        Args:
            movie_id:
            title:
            year:
            genres:
            director:
            rating:

        Returns:
            URIRef: The URI of the created movie resource
        """

        # Create unique URI for this movie
        movie_uri = URIRef(f"{self.MOVIE}movie_{movie_id}")

        # Add movie triples
        self.graph.add((movie_uri, RDF.type, self.MOVIE.Movie))
        self.graph.add((movie_uri, self.MOVIE.hasTitle, Literal(title)))
        self.graph.add((movie_uri, self.MOVIE.releasedIn, Literal(year, datatype=XSD.integer)))
        self.graph.add((movie_uri, self.MOVIE.hasRating, Literal(rating, datatype=XSD.float)))

        # Add driector
        director_uri = self.get_or_create_director(director)
        self.graph.add((movie_uri, self.MOVIE.directedBy, director_uri))

        for genre in genres:
            genre_uri = self.get_or_create_genre(genre)
            self.graph.add((movie_uri, self.MOVIE.hasGenre, genre_uri))

        logger.info(f"Added movie: {title} ({year})")

        return movie_uri


    def get_or_create_director(self, director_name: str) -> URIRef :
        """ Create or retrive a director URI """
        # Convert name to URI-safe format
        safe_name = director_name.replace(" ", "_").replace(".", "")
        director_uri = URIRef(f"{self.MOVIE}director_{safe_name}")

        # Check if director already exitst
        if not list(self.graph.triples((director_uri, RDF.type, self.MOVIE.director))):
            self.graph.add((director_uri, RDF.type, self.MOVIE.director))
            self.graph.add((director_uri, FOAF.name, Literal(director_name)))

        return director_uri

    def get_or_create_genre(self, genre_name: str) -> URIRef:
        """ Create or retrive a genre URI """
        # Convert name to URI-safe format
        safe_name = genre_name.replace(" ", "_").replace(".", "")
        genre_uri = URIRef(f"{self.MOVIE}genre_{safe_name}")

        # Check if director already exitst
        if not list(self.graph.triples((genre_uri, RDF.type, self.MOVIE.genre))):
            self.graph.add((genre_uri, RDF.type, self.MOVIE.genre))
            self.graph.add((genre_uri, FOAF.name, Literal(genre_uri)))

        return genre_uri

    def load_from_csv(self, csv_path:str):
        """
        Load movie data from CSV file.
        This demonstrates how to transform tabular data into a knowledge graph.
        """

        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Loading {len(df)} movies from {csv_path}")
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

            logger.info(f"Successfully loaded {len(df)} movies. Graph now has {len(self.graph)} triples.")
        except Exception as e:
            logger.error(f"Error loading CSV: {e} ")
            raise

    def save_graph(self, filename: str, format: str = "turtle"):
        """
        Save the RDF graph to file.

        Turtle format is human-readable and compact.
        Other formats: xml, n3, json-ld
        """
        try:
            self.graph.serialize(destination=filename, format=format)
            logger.info(f"Graph saved to {filename} in {format} format")
        except Exception as e:
            logger.error(f"Error saving graph: {e}")
            raise

    def get_statistics(self) -> Dict[str, int]:
        """ Get basic statistics about the knowledge graph"""

        stats = {}

        # Count movies
        movie_query = "SELECT (COUNT(?movie) as ?count) WHERE { ?movie a movie:Movie }"
        result = list(self.graph.query(movie_query, initNs={"movie": self.MOVIE}))
        stats['movies'] = int(result[0][0]) if result else 0

        # Count directors
        director_query = "SELECT (COUNT(?director) as ?count) WHERE { ?director a movie:Director }"
        result = list(self.graph.query(director_query, initNs={"movie": self.MOVIE}))
        stats['directors'] = int(result[0][0]) if result else 0

        # Count genres
        genre_query = "SELECT (COUNT(?genre) as ?count) WHERE { ?genre a movie:Genre }"
        result = list(self.graph.query(genre_query, initNs={"movie": self.MOVIE}))
        stats['genres'] = int(result[0][0]) if result else 0

        stats['total_triples'] = len(self.graph)

        return stats


# Example usage
if __name__ == "__main__":
    builder = MovieRDFBuilder()

    # Load sample data
    builder.load_from_csv("../data/raw/movies.csv")

    # Save the graph
    builder.save_graph("../output/movie_knowledge_graph.ttl")

    # Print statistics
    stats = builder.get_statistics()
    print("Knowledge Graph Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")