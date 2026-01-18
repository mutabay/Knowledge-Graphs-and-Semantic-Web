"""
Main Pipeline - Orchestrates the entire knowledge graph construction process

This is the "main" script that ties everything together:
1. Load data from CSV
2. Build RDF knowledge graph
3. Load into Neo4j
4. Run analytics
5. Generate reports
"""


from .rdf_builder import MovieRDFBuilder
from .neo4j_loader import MovieNeo4jLoader
from .analytics import MovieAnalytics
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MovieKnowledgeGraphPipeline:
    """
    Main pipeline class that coordinates all componenets
    """

    def __init__(self, csv_path: str, output_dir:str = "output", neo4j_optional: bool = True):
        self.csv_path = csv_path
        self.output_dir = output_dir
        self.neo4j_optional = neo4j_optional
        self.neo4j_available = False

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Initialize components
        self.rdf_builder = None
        self.neo4j_loader = None
        self.analytics = None

        logger.info("Pipeline initialized")

    def run_full_pipeline(self):
        """
        Run the complete knowledge graph construction pipeline.
        If Neo4j is not available and neo4j_optional=True, continues with RDF-only.
        """

        logger.info("Starting the full pipeline...")

        try:
            # Step 1: Build RDF graph (always works)
            self.build_rdf_graph()

            # Step 2: Try to load Neo4j (optional)
            self.neo4j_available = self.load_neo4j()

            # Step 3: Run analytics (works with RDF even without Neo4j)
            self.run_analytics()

            # Step 4: Generate report
            self.generate_report()

            logger.info("Pipeline completed successfully.")
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise

    def build_rdf_graph(self):
        logger.info("Building RDF Knowledge Graph...")
        self.rdf_builder = MovieRDFBuilder()
        self.rdf_builder.load_from_csv(self.csv_path)

        # Save RDF Graph
        rdf_output_path = os.path.join(self.output_dir, "movie_knowledge_graph.ttl")
        self.rdf_builder.save_graph(rdf_output_path)

        # Print RDF statistics
        rdf_stats = self.rdf_builder.get_statistics()
        logger.info(f"RDF Graph: {rdf_stats}")

    def load_neo4j(self):
        """Load data into Neo4j. Returns True if successful, False otherwise."""
        logger.info("Loading the data into neo4j...")

        try:
            self.neo4j_loader = MovieNeo4jLoader()
            self.neo4j_loader.clear_database()  # Fresh start
            self.neo4j_loader.load_from_csv(self.csv_path)

            # Print statistics
            neo4j_stats = self.neo4j_loader.get_statistics()
            logger.info(f"Neo4j Database: {neo4j_stats}")
            return True
        except Exception as e:
            if self.neo4j_optional:
                logger.warning(f"Neo4j not available (skipping): {e}")
                print("\n⚠️  Neo4j not available - continuing with RDF-only mode")
                print("   To enable Neo4j, run: podman run -d --name movie-neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest\n")
                self.neo4j_loader = None
                return False
            else:
                raise


    def run_analytics(self):
        """ Step 3: Run analytics on both RDF and Neo4j graphs """
        logger.info("Running analytics...")

        self.analytics = MovieAnalytics(
            rdf_builder=self.rdf_builder,
            neo4j_loader=self.neo4j_loader
        )

        # Compare query approaches
        print("\n" + "="*50)
        print("📊 Knowledge Graph Analytics")
        print("=" * 50)

        self.analytics.compare_query_approaches(director_name="Christopher Nolan")

        # Additional analytics (only if Neo4j is available)
        if self.neo4j_available and self.neo4j_loader:
            self.genre_analysis()
            self.rating_analysis()
        else:
            print("\n📝 Note: Additional analytics skipped (Neo4j not available)")
            print("   Run with Neo4j for full analytics capabilities")

    def genre_analysis(self):
        """ Analyze movies by genre"""
        print("\n Genre Analysis")
        print("-" * 40)

        if self.neo4j_loader:
            with self.neo4j_loader.driver.session() as session:
                result = session.run("""
                    MATCH (g:Genre)<-[:HAS_GENRE]-(m:Movie)
                    RETURN g.name as genre, 
                        count(m) as movie_count,
                        avg(m.rating) as avg_rating
                    ORDER BY movie_count DESC
                """)

                for record in result:
                    print(f"   {record['genre']}: {record['movie_count']} movies "
                          f"(avg rating: {record['avg_rating']:.1f})")

    def rating_analysis(self):
        """Analyze movie ratings"""
        print("\n Rating Analysis")
        print("-" * 40)

        if self.neo4j_loader:
            with self.neo4j_loader.driver.session() as session:
                result = session.run("""
                    MATCH (m:Movie)
                    RETURN m.title as title, m.rating as rating, m.year as year
                    ORDER BY m.rating DESC
                    LIMIT 5
                """)

                record = result.single()
                if record:
                    print(f"   Min Rating: {record['min_rating']}")
                    print(f"   Max Rating: {record['max_rating']}")
                    print(f"   Avg Rating: {record['avg_rating']:.2f}")

                print("   Top 5 Highest Rated Movies:")
                for record in result:
                    print(f"   • {record['title']} ({record['year']}) - {record['rating']}")

    def generate_report(self):
        """Generate a summary report"""
        logger.info("Generating summary report...")

        report_path = os.path.join(self.output_dir, "pipeline_report.txt")

        with open(report_path, 'w') as f:
            f.write("Movie Knowledge Graph Pipeline Report\n")
            f.write("=" * 40 + "\n\n")

            # RDF Statistics
            if self.rdf_builder:
                rdf_stats = self.rdf_builder.get_statistics()
                f.write("RDF Knowledge Graph Statistics:\n")
                for key, value in rdf_stats.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")

            # Neo4j Statistics
            if self.neo4j_loader:
                neo4j_stats = self.neo4j_loader.get_statistics()
                f.write("Neo4j Database Statistics:\n")
                for key, value in neo4j_stats.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")

            f.write("Pipeline completed successfully!\n")

        logger.info(f"Report saved to {report_path}")

    def cleanup(self):
        """ Cleanup resources """
        if self.neo4j_loader:
            self.neo4j_loader.close()
        logger.info("Resources cleaned up.")

# Main execution
# Main execution
def main():
    """Main function to run the pipeline"""

    # Configuration
    CSV_PATH = "data/raw/movies.csv"
    OUTPUT_DIR = "output"

    # Create and run pipeline
    pipeline = MovieKnowledgeGraphPipeline(CSV_PATH, OUTPUT_DIR)

    try:
        pipeline.run_full_pipeline()
    finally:
        pipeline.cleanup()


if __name__ == "__main__":
    main()