#!/usr/bin/env python3
"""
🎬 Movie Knowledge Graph - Main Runner Script

This is the main entry point for the Movie Knowledge Graph project.
It orchestrates the complete pipeline from data loading to analytics.

Usage:
    python run.py                    # Run full pipeline
    python run.py --rdf-only         # Build only RDF graph
    python run.py --neo4j-only       # Build only Neo4j graph
    python run.py --analytics-only   # Run only analytics
    python run.py --demo            # Run interactive demo
"""

import argparse
import sys
import os
import time
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.pipeline import MovieKnowledgeGraphPipeline
from src.rdf_builder import MovieRDFBuilder
from src.neo4j_loader import MovieNeo4jLoader
from src.analytics import MovieAnalytics


def print_banner():
    """Print project banner"""
    banner = """
    🎬 ================================================= 🎬
    🎯                MOVIE KNOWLEDGE GRAPH              🎯
    🎬 ================================================= 🎬

    📊 RDF + SPARQL  |  🔍 Neo4j + Cypher  |  📈 Analytics

    Built for learning Knowledge Graph technologies!
    """
    print(banner)


def run_full_pipeline():
    """Run the complete pipeline"""
    print("🚀 Starting Full Pipeline...")
    print("=" * 50)

    pipeline = MovieKnowledgeGraphPipeline(
        csv_path="data/raw/movies.csv",
        output_dir="output"
    )

    try:
        start_time = time.time()
        pipeline.run_full_pipeline()
        end_time = time.time()

        print(f"\n✅ Pipeline completed in {end_time - start_time:.2f} seconds!")
        print("\n📁 Check the 'output/' directory for results:")
        print("   • movie_knowledge_graph.ttl (RDF format)")
        print("   • pipeline_report.txt (Summary report)")
        print("   • Neo4j database (accessible at http://localhost:7474)")

    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        return False
    finally:
        pipeline.cleanup()

    return True


def run_rdf_only():
    """Build only RDF knowledge graph"""
    print("📊 Building RDF Knowledge Graph Only...")
    print("=" * 40)

    try:
        builder = MovieRDFBuilder()
        builder.load_from_csv("data/raw/movies.csv")

        # Save graph
        os.makedirs("output", exist_ok=True)
        builder.save_graph("output/movie_knowledge_graph.ttl")

        # Show statistics
        stats = builder.get_statistics()
        print("\n📈 RDF Graph Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")

        print("\n✅ RDF graph saved to 'output/movie_knowledge_graph.ttl'")
        return True

    except Exception as e:
        print(f"❌ RDF build failed: {e}")
        return False


def run_neo4j_only():
    """Build only Neo4j property graph"""
    print("🔍 Building Neo4j Property Graph Only...")
    print("=" * 40)

    try:
        loader = MovieNeo4jLoader()
        loader.clear_database()
        loader.load_from_csv("data/raw/movies.csv")

        # Show statistics
        stats = loader.get_statistics()
        print("\n📈 Neo4j Database Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")

        print("\n✅ Data loaded into Neo4j!")
        print("🌐 Access Neo4j Browser at: http://localhost:7474")
        print("   Username: neo4j, Password: password")

        loader.close()
        return True

    except Exception as e:
        print(f"❌ Neo4j build failed: {e}")
        return False


def run_analytics_only():
    """Run analytics on existing graphs"""
    print("📈 Running Analytics Only...")
    print("=" * 30)

    try:
        # Load existing RDF graph
        builder = MovieRDFBuilder()
        if os.path.exists("output/movie_knowledge_graph.ttl"):
            builder.graph.parse("output/movie_knowledge_graph.ttl", format="turtle")
            print("📊 Loaded existing RDF graph")
        else:
            print("📊 Building RDF graph...")
            builder.load_from_csv("data/raw/movies.csv")

        # Connect to Neo4j
        loader = MovieNeo4jLoader()
        print("🔍 Connected to Neo4j")

        # Run analytics
        analytics = MovieAnalytics(builder, loader)

        print("\n" + "=" * 60)
        print("🎬 KNOWLEDGE GRAPH ANALYTICS")
        print("=" * 60)

        # Director analysis
        analytics.compare_query_approaches("Christopher Nolan")

        # Additional analytics
        print("\n🎭 Genre Analysis:")
        with loader.driver.session() as session:
            result = session.run("""
                MATCH (g:Genre)<-[:HAS_GENRE]-(m:Movie)
                RETURN g.name as genre, count(m) as movies, avg(m.rating) as avg_rating
                ORDER BY movies DESC
            """)

            for record in result:
                print(f"   {record['genre']}: {record['movies']} movies (avg: {record['avg_rating']:.1f})")

        loader.close()
        print("\n✅ Analytics completed!")
        return True

    except Exception as e:
        print(f"❌ Analytics failed: {e}")
        return False


def run_demo():
    """Run interactive demo"""
    print("🎮 Interactive Demo Mode")
    print("=" * 30)

    print("\nThis demo will:")
    print("1. 📊 Build both RDF and Neo4j graphs")
    print("2. 🔍 Run sample queries")
    print("3. 📈 Show analytics")
    print("4. 🎯 Demonstrate recommendations")

    input("\nPress Enter to continue...")

    # Build graphs
    if not run_full_pipeline():
        return False

    print("\n🎯 Demo: Movie Recommendations")
    print("-" * 40)

    try:
        loader = MovieNeo4jLoader()

        # Demo recommendations
        test_movies = ["The Matrix", "Inception", "Pulp Fiction"]

        for movie in test_movies:
            print(f"\n🎬 Movies similar to '{movie}':")

            with loader.driver.session() as session:
                result = session.run("""
                    MATCH (target:Movie {title: $movie_title})-[:HAS_GENRE]->(g:Genre)
                    MATCH (rec:Movie)-[:HAS_GENRE]->(g)
                    WHERE target <> rec
                    WITH rec, count(g) as shared_genres
                    MATCH (rec)-[:DIRECTED_BY]->(d:Director)
                    RETURN rec.title as title, rec.year as year, 
                           rec.rating as rating, d.name as director, shared_genres
                    ORDER BY shared_genres DESC, rec.rating DESC
                    LIMIT 2
                """, movie_title=movie)

                recommendations = list(result)
                if recommendations:
                    for rec in recommendations:
                        print(f"   • {rec['title']} ({rec['year']}) - {rec['rating']}")
                        print(f"     Director: {rec['director']}, Shared genres: {rec['shared_genres']}")
                else:
                    print("   No recommendations found")

        loader.close()

        print("\n🎉 Demo completed!")
        print("\n🚀 Next steps:")
        print("   • Explore with: jupyter notebook notebooks/exploration.ipynb")
        print("   • View Neo4j: http://localhost:7474")
        print("   • Check output files in 'output/' directory")

        return True

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


def check_prerequisites():
    """Check if prerequisites are met"""
    print("🔧 Checking Prerequisites...")

    # Check data file
    if not os.path.exists("data/raw/movies.csv"):
        print("❌ Missing data/raw/movies.csv")
        print("   Please ensure the movies.csv file exists")
        return False

    # Check Neo4j connection (for Neo4j operations)
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        with driver.session() as session:
            session.run("RETURN 1")
        driver.close()
        print("✅ Neo4j connection successful")
    except Exception as e:
        print(f"⚠️  Neo4j connection failed: {e}")
        print("   Neo4j operations will be skipped")
        print("   Start Neo4j with: docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j")

    # Create output directory
    os.makedirs("output", exist_ok=True)
    print("✅ Output directory ready")

    return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Movie Knowledge Graph Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run.py                    # Run full pipeline
    python run.py --rdf-only         # Build only RDF graph
    python run.py --neo4j-only       # Build only Neo4j graph
    python run.py --analytics-only   # Run only analytics
    python run.py --demo            # Interactive demo
        """
    )

    parser.add_argument('--rdf-only', action='store_true',
                        help='Build only RDF knowledge graph')
    parser.add_argument('--neo4j-only', action='store_true',
                        help='Build only Neo4j property graph')
    parser.add_argument('--analytics-only', action='store_true',
                        help='Run analytics on existing graphs')
    parser.add_argument('--demo', action='store_true',
                        help='Run interactive demo')
    parser.add_argument('--skip-checks', action='store_true',
                        help='Skip prerequisite checks')

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Check prerequisites
    if not args.skip_checks and not check_prerequisites():
        print("\n❌ Prerequisites not met. Use --skip-checks to ignore.")
        return 1

    # Determine what to run
    success = True

    if args.rdf_only:
        success = run_rdf_only()
    elif args.neo4j_only:
        success = run_neo4j_only()
    elif args.analytics_only:
        success = run_analytics_only()
    elif args.demo:
        success = run_demo()
    else:
        success = run_full_pipeline()

    # Final message
    if success:
        print("\n🎉 All operations completed successfully!")
        print("\n📚 Learn more:")
        print("   • Open notebooks/exploration.ipynb for interactive learning")
        print("   • Check queries/ directory for example queries")
        print("   • Read README.md for detailed documentation")
        return 0
    else:
        print("\n❌ Some operations failed. Check the error messages above.")
        return 1


if __name__ == "__main__":
    exit(main())