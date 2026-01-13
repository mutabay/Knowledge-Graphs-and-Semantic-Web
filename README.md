# Semantic Web Technologies - Course Exercises and Notes

This repository contains exercises, assignments, and notes from the **Semantic Web Technologies** course, covering the fundamental concepts and practical applications of semantic web technologies including RDF, OWL, SPARQL.

## 📚 Course Overview

Implementation of W3C semantic web standards for knowledge representation and automated reasoning. Focuses on graph-based data models, description logic expressivity, query optimization, and inference engines.

## 🧠 Core Concepts

### RDF (Resource Description Framework)
Directed graph model for representing statements as subject-predicate-object triples. URIs provide global identifiers for resources, enabling distributed data integration. Supports multiple serializations (RDF/XML, Turtle, JSON-LD) while maintaining graph semantics.

### RDFS (RDF Schema) 
Vocabulary extension for RDF providing basic ontological constructs: class hierarchies (`rdfs:subClassOf`), property hierarchies (`rdfs:subPropertyOf`), domain/range constraints. Enables simple inference through entailment rules.

### OWL (Web Ontology Language)
Description Logic-based language for expressing complex ontologies. Three profiles: OWL 2 EL (polynomial reasoning), OWL 2 QL (query rewriting), OWL 2 DL (full expressivity with decidable reasoning). Supports class expressions, property characteristics, and cardinality restrictions.

### SPARQL
Graph pattern matching query language for RDF. Declarative syntax with SELECT, CONSTRUCT, ASK, DESCRIBE operations. Features property paths, subqueries, federation, and update operations. Query execution involves join optimization and cost-based planning.

### Semantic Reasoning
Automated inference using logical rules to derive implicit knowledge. Forward chaining applies rules to derive new facts; backward chaining works from goals. Tableau algorithms for satisfiability checking in description logics.

## 📁 Directory Structure

### 📊 RDFs (RDF Schemas and Data)
Implementation of RDF graph models with multiple serialization strategies and vocabulary engineering.

- **q1_foaf.rdf** - FOAF ontology instantiation with social graph modeling
  - Named graph construction and provenance tracking
  - Social network topology representation
  - Identity resolution and data linkage patterns

- **q3.rdf, q4_JSON-LD.txt, q5.txt** - Cross-format serialization examples (RDF/XML, JSON-LD, HTML)
- **q6_student.ttl** - Academic domain ontology with institutional hierarchies
- **q7_inferred_student.ttl, q7_student_vocab.ttl** - Forward chaining inference results
- **q8_inferred_axel.ttl** - ABox reasoning and individual classification

**Technical Implementation:**
- Graph isomorphism across serialization formats
- Namespace management and URI dereferencing strategies
- RDFS entailment regimes and closure operations
- Blank node handling and canonical serialization

### 🔍 SPARQL
Query engine implementation and optimization techniques for RDF graph pattern matching.

#### Query Implementations (.rq) and Execution Plans (.txt):
- **q1_a.rq** - Graph traversal algorithms for concept extraction
- **q2.rq** - Multi-constraint filtering with type inference
- **q3-q10.rq** - Incremental query complexity with string functions and aggregation

#### Knowledge Bases:
- **PeriodicTable.owl** - Chemical elements domain ontology for querying practice
- **FOAF.rdf, foaf_1.rdf** - Social network graph structures
- **rdf_data.ttl** - Benchmark datasets for query performance testing
- **concepts_and_properties.txt** - Query result validation and cardinality analysis

**Query Engine Features:**
- Bottom-up query evaluation with semi-naive evaluation
- Cost-based optimization with join reordering
- Property path regular expression compilation
- Distributed query federation across SPARQL endpoints
- Aggregate function implementation over bag semantics
- OPTIONAL clause semantics and left-outer join translation

### 🔧 OWL Modelling
Description Logic knowledge base construction with formal semantics and decidability analysis.

- **Task1-4.owx** - Comprehensive OWL 2 DL ontology engineering:
  - Taxonomic hierarchies with class intersection and union operations
  - Object property modeling with domain/range restrictions
  - Existential and universal quantification over properties
  - Boolean class constructors and logical equivalence axioms

- **Task5.owx** - Advanced DL constructs and property characteristics

**Logical Foundations:**
- OWL 2 DL standard constructs (intersection, union, complement)
- Property characteristics (domain, range, subProperty)
- Class equivalence and subsumption axioms
- Existential and universal property restrictions

### 🧠 OWL Reasoning
Inference engine implementation and computational complexity analysis of automated reasoning.

- **Question 1.ttl** - Basic reasoning scenarios with:
  - Class disjointness and subsumption hierarchies
  - Property domain and range inference
  - Simple entailment and classification tasks
  - Human/Alien domain modeling exercises

- **Question 2.rdf** - Academic domain reasoning with Student/Habilitation relationships

**Reasoning Foundations:**
- Basic OWL 2 DL constructs and entailment
- RDFS inference rules and property inheritance
- Classification and consistency checking
- Forward chaining inference with class hierarchies

## 🎯 Technical Competencies

### Algorithmic Implementation:
1. **RDF Graph Processing**
   - Graph isomorphism and canonical forms
   - Streaming RDF processing with bounded memory
   - Blank node skolemization strategies

2. **SPARQL Query Processing**
   - Join ordering optimization using statistics
   - Adaptive query execution with runtime reoptimization
   - Distributed query planning across federated endpoints

3. **Description Logic Reasoning**
   - Tableaux algorithm implementation with optimization heuristics
   - Incremental reasoning with explanation tracking
   - Modular ontology decomposition and reasoning

4. **Knowledge Engineering**
   - Ontology design patterns and anti-patterns
   - Competency question formalization
   - Quality metrics and ontology evaluation methodologies

### Implementation Experience:
- Reasoner integration (HermiT, Pellet, ELK)
- Custom SPARQL endpoint development
- Ontology versioning and evolution strategies
- Performance profiling and scalability analysis

## 🛠️ Technical Stack

- **Languages**: RDF/XML, Turtle (TTL), JSON-LD, SPARQL
- **Ontology Tools**: Protégé, OWL API
- **Reasoners**: HermiT, Pellet, FaCT++
- **Query Engines**: Apache Jena, Virtuoso, GraphDB
- **Vocabularies**: FOAF, Schema.org, Dublin Core

