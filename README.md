# Semantic Web & Knowledge Graphs

A repository for **Semantic Web Technologies** and **Knowledge Graphs** — containing projects, examples, and reference notes for learning and practice.

---

## 🎬 Featured: Movie Knowledge Graph

A hands-on project exploring knowledge graph implementation using two approaches: **RDF/SPARQL** (W3C standard) and **Neo4j/Cypher** (property graph).

**[→ View Project Details](movie-knowledge-graph/)**

| Implementation | Technologies |
|----------------|--------------|
| CSV to knowledge graph pipeline | Python, RDFLib |
| Dual graph representation | RDF Triples + Neo4j |
| Query comparison | SPARQL vs Cypher |
| Analytics & visualization | Jupyter, Plotly |

---

## 📁 Repository Structure

| Directory | Contents |
|-----------|----------|
| [movie-knowledge-graph/](movie-knowledge-graph/) | Complete knowledge graph project |
| [RDFs/](RDFs/) | RDF data and serialization examples |
| [SPARQL/](SPARQL/) | Query examples and datasets |
| [OWL Modelling/](OWL%20Modelling/) | Ontology design examples |
| [OWL Reasoning/](OWL%20Reasoning/) | Reasoning and inference examples |

---

## 🧠 Reference Notes

### RDF (Resource Description Framework)

**Core Model:**
- Directed graph using subject-predicate-object triples
- Every statement is a triple: `<subject> <predicate> <object>`
- URIs provide global, unique resource identifiers
- Literals for data values (strings, numbers, dates)
- Blank nodes for anonymous resources

**Serialization Formats:**
| Format | Use Case |
|--------|----------|
| Turtle (.ttl) | Human-readable, compact |
| RDF/XML (.rdf) | XML-based, legacy systems |
| JSON-LD (.jsonld) | Web APIs, JavaScript |
| N-Triples (.nt) | Line-based, streaming |
| N-Quads (.nq) | N-Triples + named graphs |

**Common Namespaces:**
```
rdf:  http://www.w3.org/1999/02/22-rdf-syntax-ns#
rdfs: http://www.w3.org/2000/01/rdf-schema#
owl:  http://www.w3.org/2002/07/owl#
xsd:  http://www.w3.org/2001/XMLSchema#
foaf: http://xmlns.com/foaf/0.1/
dc:   http://purl.org/dc/elements/1.1/
```

---
### RDFS (RDF Schema)

**Class Constructs:**
- `rdfs:Class` — defines a class
- `rdfs:subClassOf` — class hierarchy (inheritance)
- `rdf:type` — instance-of relationship

**Property Constructs:**
- `rdf:Property` — defines a property
- `rdfs:subPropertyOf` — property hierarchy
- `rdfs:domain` — restricts subject type
- `rdfs:range` — restricts object type

**Inference Rules:**
- If `A rdfs:subClassOf B` and `x rdf:type A`, then `x rdf:type B`
- If `p rdfs:domain C` and `x p y`, then `x rdf:type C`
- If `p rdfs:range C` and `x p y`, then `y rdf:type C`

---

### OWL (Web Ontology Language)

**OWL 2 Profiles:**
| Profile | Reasoning | Best For |
|---------|-----------|----------|
| OWL 2 EL | Polynomial | Large ontologies, classifications |
| OWL 2 QL | Query rewriting | Database-backed queries |
| OWL 2 RL | Rule-based | Rule engines, RDF data |
| OWL 2 DL | Full expressivity | Complete reasoning (decidable) |

**Class Expressions:**
- `owl:intersectionOf` — AND (conjunction)
- `owl:unionOf` — OR (disjunction)
- `owl:complementOf` — NOT (negation)
- `owl:equivalentClass` — same class
- `owl:disjointWith` — no common instances

**Property Types:**
- `owl:ObjectProperty` — links individuals
- `owl:DatatypeProperty` — links to literals
- `owl:FunctionalProperty` — at most one value
- `owl:InverseFunctionalProperty` — unique identifier
- `owl:TransitiveProperty` — A→B→C implies A→C
- `owl:SymmetricProperty` — A→B implies B→A

**Restrictions:**
- `owl:someValuesFrom` — existential (∃) — at least one
- `owl:allValuesFrom` — universal (∀) — all must be
- `owl:hasValue` — specific value required
- `owl:minCardinality`, `owl:maxCardinality`, `owl:cardinality`

---

### SPARQL

**Query Types:**
| Type | Purpose |
|------|---------|
| SELECT | Return variable bindings (table) |
| CONSTRUCT | Return new RDF graph |
| ASK | Return boolean (yes/no) |
| DESCRIBE | Return description of resource |

**Basic Pattern:**
```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name ?email
WHERE {
    ?person a foaf:Person ;
            foaf:name ?name ;
            foaf:mbox ?email .
}
```

**Useful Clauses:**
- `FILTER` — conditions (regex, comparison, bounds)
- `OPTIONAL` — left outer join
- `UNION` — combine patterns
- `MINUS` — exclude patterns
- `BIND` — assign computed values
- `VALUES` — inline data

**Aggregation:**
- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- `GROUP BY` — grouping
- `HAVING` — filter groups
- `ORDER BY`, `LIMIT`, `OFFSET`

**Property Paths:**
- `foaf:knows/foaf:name` — sequence (/)
- `foaf:knows*` — zero or more (*)
- `foaf:knows+` — one or more (+)
- `foaf:knows?` — zero or one (?)
- `^foaf:knows` — inverse (^)
- `foaf:knows|foaf:friendOf` — alternative (|)

---

### Reasoning & Inference

**Types of Reasoning:**
- **Classification** — compute class hierarchy
- **Realization** — find types of individuals
- **Consistency checking** — detect contradictions
- **Satisfiability** — check if class can have instances

**Inference Strategies:**
- **Forward chaining** — data-driven, apply rules to derive new facts
- **Backward chaining** — goal-driven, work backwards from query
- **Tableau algorithm** — systematic satisfiability checking for DL

**Common Reasoners:**
| Reasoner | Strengths |
|----------|-----------|
| HermiT | OWL 2 DL, hypertableau |
| Pellet | OWL 2 DL, explanations |
| FaCT++ | Fast classification |
| ELK | OWL 2 EL, very large ontologies |

**Entailment Regimes:**
- RDFS entailment — subclass/subproperty inference
- OWL 2 RL — rule-based OWL subset
- OWL 2 Direct Semantics — full DL reasoning

---

### Knowledge Graph vs Property Graph

| Aspect | RDF/SPARQL | Neo4j/Cypher |
|--------|------------|--------------|
| Data model | Triples | Nodes + Relationships |
| Schema | Ontology (OWL) | Labels + constraints |
| Query style | Pattern matching | ASCII-art patterns |
| Standards | W3C standard | Industry standard |
| Reasoning | Built-in support | External tools |
| Best for | Semantic interoperability | Performance, intuitive queries |

---

## 🛠️ Tools & Technologies

| Category | Tools |
|----------|-------|
| **Ontology Editors** | Protégé |
| **Libraries** | RDFLib, Apache Jena |
| **Reasoners** | HermiT, Pellet |
| **Graph Databases** | Neo4j |
| **Formats** | RDF/XML, Turtle, JSON-LD, OWL |

---

## 🔗 Resources

- [W3C RDF Primer](https://www.w3.org/TR/rdf11-primer/)
- [SPARQL 1.1 Specification](https://www.w3.org/TR/sparql11-query/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [Neo4j Documentation](https://neo4j.com/docs/)

