# **RDF and RDFS: A Comprehensive Guide**
  
## **Chapter 1: Understanding RDF (Resource Description Framework)**
### What is RDF?
RDF is like the "grammar" of the semantic web. Imagine you want to describe relationships between things in a way that computers can understand - that's exactly what RDF does.

**Core Philosophy**: Everything can be described as relationships between resources.

### The Triple Pattern: Subject-Predicate-Object
Every piece of information in RDF is expressed as a **triple**:
* **Subject**: The resource being described  
* **Predicate**: The property or relationship
* **Object**: The value or related resource
* **Format**: `<subject> <predicate> <object> .`

**Real-world example:**
* "John knows Mary" becomes:
  * Subject: `John`
  * Predicate: `knows`
  * Object: `Mary`

### First Triples Examples
Common triples about a person:
* `<http://example.org/me> <http://xmlns.com/foaf/0.1/name> "John Smith" .`
* `<http://example.org/me> <http://xmlns.com/foaf/0.1/age> 25 .`
* `<http://example.org/me> <http://example.org/studies> "Computer Science" .`
* `<http://example.org/me> <http://example.org/livesIn> <http://example.org/NewYork> .`

**Book example triples:**
* `<http://example.org/book1> <http://example.org/title> "Semantic Web Primer" .`
* `<http://example.org/book1> <http://example.org/author> "Grigoris Antoniou" .`
* `<http://example.org/book1> <http://example.org/pages> 300 .`

### RDF Serialization Formats
Think of these as different ways to write the same story:

#### 1. Turtle (.ttl) - Most Human-Readable
```turtle
@prefix ex: <http://example.org/> .
ex:john ex:knows ex:mary .
ex:john ex:age 30 .
```

#### 2. RDF/XML - Verbose but Machine-Friendly
```xml
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:ex="http://example.org/">
  <rdf:Description rdf:about="http://example.org/john">
    <ex:knows rdf:resource="http://example.org/mary"/>
    <ex:age>30</ex:age>
  </rdf:Description>
</rdf:RDF>
```

#### 3. JSON-LD - Web Developer Friendly
```json
{
  "@context": {"ex": "http://example.org/"},
  "@id": "ex:john",
  "ex:knows": {"@id": "ex:mary"},
  "ex:age": 30
}
```

### URIs: The Universal Naming System
Every resource needs a unique identifier - like a global address:
* **Full URI**: `<http://example.org/john>`
* **With namespace**: `ex:john` (where ex: = http://example.org/)
* **Blank nodes**: `_:person1` (anonymous resources)
* **Literals**: `"John"`, `30`, `"2023-12-01"^^xsd:date`

### University Knowledge Graph Example
Complete RDF graph about a university:
```turtle
@prefix univ: <http://university.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

univ:AAU foaf:name "University of Klagenfurt" .
univ:Informatics a univ:Department ;
    univ:partOf univ:AAU .
univ:john a foaf:Person ;
    foaf:name "John Smith" ;
    univ:studiesAt univ:Informatics ;
    univ:enrolledIn univ:CS101 .
univ:CS101 a univ:Course ;
    univ:title "Introduction to Computer Science" ;
    univ:credits 3 .
```
* * *
## **Chapter 2: RDFS - Adding Structure and Meaning**
### What is RDFS?
RDFS is like adding "types" and "inheritance" to your RDF. It gives you vocabulary to describe vocabularies!

### Core RDFS Concepts
#### 1. Classes (Types of Things)
```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <http://example.org/> .

ex:Person a rdfs:Class .
ex:Student a rdfs:Class .
ex:Professor a rdfs:Class .
```

#### 2. Properties (Types of Relationships)
```turtle
ex:name a rdf:Property .
ex:age a rdf:Property .
ex:teaches a rdf:Property .
ex:enrolledIn a rdf:Property .
```

#### 3. Subclass Relationships
```turtle
ex:Student rdfs:subClassOf ex:Person .
ex:Professor rdfs:subClassOf ex:Person .
ex:PhDStudent rdfs:subClassOf ex:Student .
```

### Understanding Domain and Range
**Domain**: What type of thing can HAVE this property  
**Range**: What type of thing this property can POINT TO

```turtle
ex:teaches rdfs:domain ex:Professor .
ex:teaches rdfs:range ex:Course .
ex:enrolledIn rdfs:domain ex:Student .
ex:enrolledIn rdfs:range ex:Course .
```

### Complete Library Schema Example
Library system RDFS schema with all classes and properties:
```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ex: <http://library.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Main Classes
ex:LibraryItem a rdfs:Class .
ex:Person a rdfs:Class .

# Subclasses of LibraryItem
ex:Book rdfs:subClassOf ex:LibraryItem .
ex:DVD rdfs:subClassOf ex:LibraryItem .
ex:Magazine rdfs:subClassOf ex:LibraryItem .

# Subclasses of Person
ex:Author rdfs:subClassOf ex:Person .
ex:Student rdfs:subClassOf ex:Person .
ex:Librarian rdfs:subClassOf ex:Person .

# Properties
ex:title rdfs:domain ex:LibraryItem ; rdfs:range rdfs:Literal .
ex:writtenBy rdfs:domain ex:Book ; rdfs:range ex:Author .
ex:publishedYear rdfs:domain ex:LibraryItem ; rdfs:range xsd:integer .
ex:borrowedBy rdfs:domain ex:LibraryItem ; rdfs:range ex:Student .
ex:isbn rdfs:domain ex:Book ; rdfs:range rdfs:Literal .
ex:director rdfs:domain ex:DVD ; rdfs:range ex:Person .
ex:manages rdfs:domain ex:Librarian ; rdfs:range ex:LibraryItem .
```
* * *
## **Chapter 3: RDFS Reasoning**
### What is Inference?
Reasoning means deriving new facts from existing ones using logical rules.

### Basic RDFS Inference Rules
#### Rule 1: Subclass Transitivity
```turtle
# If A subClassOf B and B subClassOf C, then A subClassOf C
ex:PhDStudent rdfs:subClassOf ex:Student .
ex:Student rdfs:subClassOf ex:Person .
# Inferred: ex:PhDStudent rdfs:subClassOf ex:Person .
```

#### Rule 2: Type Inheritance
```turtle
# If X is instance of A and A subClassOf B, then X is instance of B
ex:alice a ex:PhDStudent .
ex:PhDStudent rdfs:subClassOf ex:Student .
# Inferred: ex:alice a ex:Student .
```

#### Rule 3: Domain/Range Inference
```turtle
# If property P has domain D and X P Y, then X is instance of D
ex:teaches rdfs:domain ex:Professor .
ex:smith ex:teaches ex:math101 .
# Inferred: ex:smith a ex:Professor .
```

### Complete Reasoning Example
Knowledge base with inferences:
```turtle
# Original facts
ex:Animal a rdfs:Class .
ex:Mammal rdfs:subClassOf ex:Animal .
ex:Dog rdfs:subClassOf ex:Mammal .
ex:buddy a ex:Dog .
ex:owns rdfs:domain ex:Person .
ex:alice ex:owns ex:buddy .

# What can be inferred:
# 1. ex:buddy is also a Mammal (type inheritance)
# 2. ex:buddy is also an Animal (transitivity)
# 3. ex:alice is a Person (domain inference)
```

**Complete inferences:**
* `ex:buddy a ex:Mammal .` (from Dog subClassOf Mammal)
* `ex:buddy a ex:Animal .` (from Mammal subClassOf Animal)
* `ex:alice a ex:Person .` (from owns domain Person)

* * *
## **Chapter 4: Hands-On Practice**
### Working with Real Data: FOAF Example
Let's use the Friend-of-a-Friend vocabulary from your workspace:
```turtle
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

ex:alice a foaf:Person ;
    foaf:name "Alice Smith" ;
    foaf:knows ex:bob ;
    foaf:mbox <mailto:alice@example.com> .
```

### Common Vocabularies to Know
1. **FOAF**: People, relationships, social networks
2. **Dublin Core**: Metadata (title, creator, date)
3. **Schema.org**: General web content
4. **RDFS**: Schema definition

### Complete FOAF Profile Example
Enhanced FOAF profile with all common properties:
```turtle
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ex: <http://example.org/> .

ex:me a foaf:Person ;
    foaf:name "Alice Johnson" ;
    foaf:nick "ally" ;
    foaf:title "Dr." ;
    foaf:givenName "Alice" ;
    foaf:familyName "Johnson" ;
    foaf:mbox <mailto:alice@university.edu> ;
    foaf:homepage <http://alice-johnson.com> ;
    foaf:phone <tel:+1-555-0123> ;
    foaf:workplaceHomepage <http://university.edu> ;
    foaf:interest ex:semanticweb, ex:artificialIntelligence ;
    foaf:knows ex:bob, ex:charlie, ex:diana ;
    foaf:currentProject ex:researchProject1 .

ex:semanticweb foaf:name "Semantic Web Technologies" .
ex:artificialIntelligence foaf:name "Artificial Intelligence" .
```

* * *
## **Chapter 5: Advanced Concepts**
### Blank Nodes vs Named Resources
```turtle
# Named resource
ex:alice a foaf:Person ; foaf:name "Alice" .

# Blank node
[] a foaf:Person ; foaf:name "Anonymous Person" .

# Blank node with identifier
_:person1 a foaf:Person ; foaf:name "Someone" .
```

### Multiple Values and Collections
```turtle
ex:book1 ex:author "Author 1", "Author 2", "Author 3" .

# Or using collections
ex:book1 ex:authors (ex:author1 ex:author2 ex:author3) .
```

### Complete University Knowledge Graph Implementation
Comprehensive RDF/RDFS model meeting all requirements:
```turtle
@prefix univ: <http://university.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Schema - Classes (5+ with hierarchy)
univ:Person a rdfs:Class .
univ:Student rdfs:subClassOf univ:Person .
univ:Professor rdfs:subClassOf univ:Person .
univ:UndergraduateStudent rdfs:subClassOf univ:Student .
univ:GraduateStudent rdfs:subClassOf univ:Student .
univ:Course a rdfs:Class .
univ:Department a rdfs:Class .
univ:University a rdfs:Class .

# Properties (8+ with domain/range)
univ:enrolledIn rdfs:domain univ:Student ; rdfs:range univ:Course .
univ:teaches rdfs:domain univ:Professor ; rdfs:range univ:Course .
univ:belongsTo rdfs:domain univ:Course ; rdfs:range univ:Department .
univ:worksFor rdfs:domain univ:Professor ; rdfs:range univ:Department .
univ:studiesAt rdfs:domain univ:Student ; rdfs:range univ:University .
univ:hasGPA rdfs:domain univ:Student ; rdfs:range xsd:float .
univ:credits rdfs:domain univ:Course ; rdfs:range xsd:integer .
univ:established rdfs:domain univ:University ; rdfs:range xsd:date .
univ:offeredBy rdfs:domain univ:Course ; rdfs:range univ:Department .

# Sample Data (20+ triples)
univ:MIT a univ:University ;
    foaf:name "Massachusetts Institute of Technology" ;
    univ:established "1861-04-10"^^xsd:date .

univ:EECS a univ:Department ;
    foaf:name "Electrical Engineering and Computer Science" ;
    univ:partOf univ:MIT .

univ:alice a univ:GraduateStudent ;
    foaf:name "Alice Smith" ;
    univ:studiesAt univ:MIT ;
    univ:hasGPA 3.8 ;
    univ:enrolledIn univ:CS101, univ:CS201 .

univ:bob a univ:Professor ;
    foaf:name "Dr. Bob Johnson" ;
    univ:worksFor univ:EECS ;
    univ:teaches univ:CS101 .

univ:CS101 a univ:Course ;
    foaf:name "Introduction to Computer Science" ;
    univ:credits 3 ;
    univ:belongsTo univ:EECS ;
    univ:offeredBy univ:EECS .

univ:CS201 a univ:Course ;
    foaf:name "Data Structures" ;
    univ:credits 4 ;
    univ:belongsTo univ:EECS ;
    univ:offeredBy univ:EECS .
```

**This implementation includes:**
* 8 classes with proper hierarchy (Person → Student → Undergraduate/Graduate, etc.)
* 9 properties with complete domain/range specifications
* 25+ triples of sample data
* Proper namespace usage with prefixes

* * *
## **Key Concepts Summary**

### **RDF vs RDFS Differences**
* **RDF**: Provides the basic triple structure (subject-predicate-object) for describing resources and their relationships. It's the foundation syntax.
* **RDFS**: Extends RDF by adding vocabulary to describe the vocabulary itself - classes, properties, inheritance hierarchies, and constraints like domain/range.

### **Converting Natural Language to RDF**
**Example**: "The book 'Semantic Web Primer' was written by Grigoris Antoniou and has 300 pages."
```turtle
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

ex:semanticWebPrimer a ex:Book ;
    ex:title "Semantic Web Primer" ;
    ex:author ex:grigorisAntoniou ;
    ex:pages 300 .

ex:grigorisAntoniou a foaf:Person ;
    foaf:name "Grigoris Antoniou" .
```

### **RDFS Reasoning Rules Applied**
1. **Subclass Transitivity**: If A subClassOf B and B subClassOf C, then A subClassOf C
2. **Type Inheritance**: If X is instance of A and A subClassOf B, then X is also instance of B
3. **Domain/Range Inference**: If property P has domain D and X P Y, then X is instance of D

### **Common Schema Patterns**
```turtle
# Music domain example
ex:MusicalWork a rdfs:Class .
ex:Song rdfs:subClassOf ex:MusicalWork .
ex:Album rdfs:subClassOf ex:MusicalWork .
ex:Artist a rdfs:Class .
ex:Band rdfs:subClassOf ex:Artist .

ex:performedBy rdfs:domain ex:MusicalWork ; rdfs:range ex:Artist .
ex:releaseDate rdfs:domain ex:MusicalWork ; rdfs:range xsd:date .
ex:genre rdfs:domain ex:MusicalWork ; rdfs:range rdfs:Literal .
ex:duration rdfs:domain ex:Song ; rdfs:range xsd:duration .
```

## Smart University System - Practical Application

**Directory**: `smart-university-system/`

A real-world RDF application demonstrating university knowledge management using Python and RDFLib.

### Files:
- `university_system.ttl` - University knowledge graph with courses, students, and relationships
- `test_university.py` - Basic SPARQL queries for testing data
- `interactive_queries.py` - Interactive query interface  
- `advanced_university_queries.py` - Course recommendations and analytics

### Features:
- Student and course enrollment tracking
- Study partner discovery based on shared courses
- Research collaboration finder using shared interests
- Course recommendation system based on prerequisites
- Department statistics and knowledge graph analytics

### Usage:
```bash
python test_university.py                # Basic testing
python interactive_queries.py           # Interactive mode
python advanced_university_queries.py   # Full analytics
```

This demonstrates practical RDF applications for academic data management, social network analysis, and intelligent recommendations.
