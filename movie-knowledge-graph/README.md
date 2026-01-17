What is a Knowledge Graph?
Think of it as a smart network of connected facts:

Nodes = Entities (Movies, Actors, Users)
Edges = Relationships (acted_in, directed, rated)
Properties = Attributes (name, year, rating)

RDF Triple Structure
Every fact is a Subject-Predicate-Object triple:

<Tom_Hanks> <acted_in> <Forrest_Gump>
<Forrest_Gump> <has_genre> <Drama>
<User123> <rated> <Forrest_Gump>


# 🎬 Movie Knowledge Graph Project

A comprehensive implementation demonstrating **Knowledge Graph construction** using both **RDF/SPARQL** and **Neo4j/Cypher** approaches. This project showcases how to transform tabular movie data into rich, interconnected knowledge representations suitable for advanced analytics and recommendations.

## 🎯 Project Overview

This project was built as a **learning journey** to understand:

### **What We Built:**
- **RDF Knowledge Graph**: Semantic web standards using RDF triples and SPARQL queries
- **Neo4j Property Graph**: Intuitive graph database with Cypher query language  
- **Comparative Analytics**: Side-by-side analysis of both approaches
- **Data Pipeline**: Complete ETL process from CSV to knowledge graphs
- **Query Examples**: Comprehensive collection of graph queries

### **Why Knowledge Graphs?**
Traditional databases store data in tables. Knowledge graphs store **relationships** and **context**:
Traditional: Movie table + Director table + Genre table
Knowledge Graph: (Movie)-[DIRECTED_BY]->(Director)-[WORKED_IN]->(Genre)


This enables:
- **Semantic Understanding**: What does the data *mean*?
- **Complex Relationships**: Multi-hop queries across entities
- **Reasoning**: Infer new knowledge from existing facts
- **Recommendations**: Find patterns and similarities

## 🏗️ Architecture
📁 movie-knowledge-graph/
├── 📊 data/raw/movies.csv # Source data
├── 🧠 src/
│ ├── rdf_builder.py # RDF/SPARQL implementation
│ ├── neo4j_loader.py # Neo4j/Cypher implementation
│ ├── analytics.py # Comparative analytics
│ └── pipeline.py # Main orchestrator
├── 🔍 queries/
│ ├── sparql_examples.py # SPARQL query library
│ └── cypher_examples.py # Cypher query library
├── 📓 notebooks/
│ └── exploration.ipynb # Interactive exploration
├── 📤 output/ # Generated knowledge graphs
└── 🚀 run.py # Main execution script



## 🛠️ Technology Stack

### **RDF/Semantic Web Stack:**
- **RDFLib**: Python RDF manipulation library
- **SPARQL**: W3C standard query language for RDF
- **Turtle**: Human-readable RDF serialization format
- **Ontologies**: Formal domain knowledge representation

### **Property Graph Stack:**
- **Neo4j**: Leading graph database platform
- **Cypher**: Intuitive graph query language
- **Bolt Protocol**: High-performance database communication
- **APOC**: Advanced procedures and functions

### **Data Processing:**
- **Pandas**: Data manipulation and analysis
- **NetworkX**: Graph algorithms and visualization
- **Jupyter**: Interactive data exploration

## 🚀 Quick Start

### **Prerequisites**

1. **Python 3.8+**
```bash
python --version  # Should be 3.8 or higher
```

2. Neo4j Database
# Option 1: Docker (Recommended)
docker run -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  --name movie-neo4j neo4j:latest

# Option 2: Download from https://neo4j.com/download/

Installation
1. Clone the repository:
git clone <your-repo-url>
cd movie-knowledge-graph

2. Create virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Verify Neo4j connection:
# Neo4j Browser: http://localhost:7474
# Username: neo4j, Password: password

### **Running the Project**

1. Option 1: Full Pipeline (Recommended)
python run.py
2. Option 2: Step by Step
# 1. Build RDF Knowledge Graph
python -m src.rdf_builder

# 2. Load into Neo4j  
python -m src.neo4j_loader

# 3. Run Analytics
python -m src.analytics

3. Option 3: Interactive Exploration
jupyter notebook notebooks/exploration.ipynb

📊 Sample Data
The project includes movie data with the following structure:

movie_id,title,year,genres,director,rating
1,The Matrix,1999,Action|Sci-Fi,Lana Wachowski,8.7
2,Inception,2010,Action|Sci-Fi|Thriller,Christopher Nolan,8.8
3,Interstellar,2014,Drama|Sci-Fi,Christopher Nolan,8.6


Entities Created:
Movies: 7 films with titles, years, ratings
Directors: 6 unique directors
Genres: 6 different genres
Relationships: 20+ connections between entities

🔍 Query Examples
SPARQL (RDF) Example:

PREFIX movie: <http://movie-kg.org/ontology#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?title ?year ?rating
WHERE {
    ?movie a movie:Movie .
    ?movie movie:hasTitle ?title .
    ?movie movie:releasedIn ?year .
    ?movie movie:hasRating ?rating .
    ?movie movie:directedBy ?director .
    ?director foaf:name "Christopher Nolan" .
}
ORDER BY ?year

Cypher (Neo4j) Example:
MATCH (m:Movie)-[:DIRECTED_BY]->(d:Director {name: 'Christopher Nolan'})
RETURN m.title as title, m.year as year, m.rating as rating
ORDER BY m.year

Both queries find Christopher Nolan's movies, but notice:

SPARQL: More verbose, standards-based, great for semantic reasoning
Cypher: More intuitive, ASCII art syntax, great for graph traversal


🧪 What You'll Learn
RDF & Semantic Web Concepts:
Triples: Subject-Predicate-Object statements
URIs: Unique resource identification
Namespaces: Avoiding naming conflicts
Ontologies: Formal domain modeling
SPARQL: Pattern-matching queries
Linked Data: Web-scale knowledge integration
Property Graph Concepts:
Nodes & Relationships: Intuitive graph modeling
Labels & Properties: Flexible data structures
Cypher: Visual query language
Graph Algorithms: PageRank, community detection
Performance: Indexes, constraints, query optimization
Graph Analytics: Centrality, clustering, pathfinding
Comparative Analysis:
When to use RDF vs Property Graphs
Query language differences (SPARQL vs Cypher)
Performance characteristics
Ecosystem and tooling
Standards compliance vs pragmatic flexibility
📈 Analytics & Insights
The project demonstrates various analytical capabilities:

Basic Queries:
Find all movies by a director
List movies by genre
Get highest-rated films
Advanced Analytics:
Director collaboration networks
Genre co-occurrence patterns
Movie recommendation algorithms
Decade-based trend analysis
Shortest path between directors
Graph Algorithms:
Centrality measures (identify important nodes)
Community detection (find clusters)
Pathfinding (connect entities)
Similarity calculations
🔧 Customization
Adding New Data:
Update data/raw/movies.csv with your data
Modify entity types in rdf_builder.py and neo4j_loader.py
Add new query patterns in the queries/ directory

Extending the Ontology:
# In rdf_builder.py, add new classes:
self.MOVIE.Actor: "Aperson who acts in movies"
self.MOVIE.Studio: "A movie production company"

# Add new relationships:
self.MOVIE.actedIn: "Actor performed in movie"
self.MOVIE.producedBy: "Movie produced by studio"


New Analytics:
# In analytics.py, add new comparison methods:
def analyze_actor_networks(self):
    # Compare actor collaboration patterns
    # Between RDF and Neo4j approaches

🐛 Troubleshooting
Common Issues:
Neo4j Connection Failed:
# Check if Neo4j is running
docker ps | grep neo4j

# Check logs
docker logs movie-neo4j

Memory Issues with Large Datasets:

# In neo4j_loader.py, use batch processing:
def load_in_batches(self, df, batch_size=100):
    for i in range(0, len(df), batch_size):
        batch = df[i:i+batch_size]
        # Process batch


SPARQL Query Timeouts:
# In rdf_builder.py, optimize queries:
# Add LIMIT clauses for large datasets
query += " LIMIT 1000"


🎓 Learning Path
Beginner → Intermediate → Advanced

Start Here: Run python run.py and explore the output
Understand Queries: Study queries/sparql_examples.py and queries/cypher_examples.py
Interactive Learning: Open notebooks/exploration.ipynb
Modify Data: Add your own movies to the CSV
Create Queries: Write new analytical queries
Extend Schema: Add actors, studios, reviews
Performance Tuning: Optimize for larger datasets
Advanced Analytics: Implement recommendation algorithms
📚 Resources & References
RDF & Semantic Web:
RDFLib Documentation
SPARQL 1.1 Specification
Linked Data Principles
Neo4j & Property Graphs:
Neo4j Documentation
Cypher Query Language
Graph Data Science Library
Knowledge Graphs:
Knowledge Graph Cookbook
Stanford CS520: Knowledge Graphs




🎯 Project Goals Achieved
✅ RDF Knowledge Graph Construction
✅ Neo4j Property Graph Implementation
✅ SPARQL Query Mastery
✅ Cypher Query Proficiency
✅ Comparative Graph Analytics
✅ End-to-End Data Pipeline
✅ Interactive Exploration Tools
✅ Comprehensive Documentation

Ready to explore the fascinating world of Knowledge Graphs! 🚀