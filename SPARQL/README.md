# **SPARQL: Query Language for RDF**

## **What is SPARQL?**
SPARQL is SQL for RDF graphs. It finds patterns in triples through pattern matching rather than table joins.

**Basic Structure:**
```sparql
PREFIX namespace: <URI>
SELECT variables
WHERE { graph_patterns }
```

## **Core Patterns**

### **Pattern Matching (q2.rq)**
Find liquid metallic elements:
```sparql
PREFIX table: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
SELECT ?element WHERE {
    ?element rdf:type table:Element .
    ?element table:standardState table:liquid .
    ?element table:classification table:Metallic .
}
```

### **String Processing (q1_a.rq)**
Extract concepts and properties from URIs:
```sparql
SELECT DISTINCT ?concept ?property WHERE {
    {?s ?p ?o. FILTER(isURI(?o))} UNION
    {?o ?p ?s. FILTER(isURI(?o))}
    BIND (STRAFTER(str(?p), '#') AS ?property)
    BIND (STRAFTER(str(?s), '#') AS ?concept)
}
```

### **Negation Patterns (q10_1.rq vs q10_2.rq)**

**Method 1: NOT EXISTS**
```sparql
SELECT ?groupNumber WHERE {
    ?group a table:Group ;
           table:number ?groupNumber .
    NOT EXISTS { ?group table:name ?groupName }
}
ORDER BY ?groupNumber
```

**Method 2: OPTIONAL + FILTER**
```sparql
SELECT ?groupNumber WHERE {
    ?group a table:Group ;
           table:number ?groupNumber .
    OPTIONAL { ?group table:name ?groupName }
    FILTER (!bound(?groupName))
}
ORDER BY ?groupNumber
```

## **Essential SPARQL Features**

### **FILTER Operations**
```sparql
FILTER(isURI(?value))           # Check if URI
FILTER(bound(?optional))        # Check if variable has value
FILTER(?number > 50)            # Numeric comparison
FILTER(STRSTARTS(?name, "C"))   # String operations
FILTER(REGEX(?name, "^[A-C]"))  # Regular expressions
```

### **String Functions**
```sparql
STRAFTER(str(?uri), '#')        # Extract after character
STRBEFORE(str(?uri), '#')       # Extract before character  
UCASE(?string)                  # Uppercase
LCASE(?string)                  # Lowercase
STRLEN(?string)                 # String length
```

### **Aggregation**
```sparql
SELECT ?class (COUNT(?element) as ?count) WHERE {
    ?element table:classification ?class .
}
GROUP BY ?class
ORDER BY DESC(?count)
```

### **OPTIONAL and UNION**
```sparql
# Handle missing data
OPTIONAL { ?element table:color ?color }

# Multiple patterns
{ ?person foaf:name ?name } UNION
{ ?person foaf:nick ?name }
```

## **Working with Different Datasets**

### **Periodic Table Queries**
Main dataset for learning SPARQL fundamentals:
- Element properties and classifications
- Group and period relationships  
- String processing for chemical names

### **FOAF Social Network**
```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?person ?name WHERE {
    ?person a foaf:Person ;
            foaf:name ?name .
}
```

## **Query Optimization Notes**

1. **Specific patterns first** - place most restrictive conditions early
2. **Use LIMIT** for exploration - `LIMIT 10` while testing
3. **EXISTS vs OPTIONAL** - EXISTS is usually faster for checking existence
4. **ORDER BY** - always specify for consistent results

## **Common Patterns**

### **Data Exploration**
```sparql
# See all properties of a resource
SELECT ?p ?o WHERE {
    <specific_resource> ?p ?o .
}

# Count triples by predicate
SELECT ?p (COUNT(*) as ?count) WHERE {
    ?s ?p ?o .
}
GROUP BY ?p
ORDER BY DESC(?count)
```

### **Complex Filtering**
```sparql
# Multiple conditions with calculations
SELECT ?element ?name ?category WHERE {
    ?element table:name ?name ;
             table:atomicWeight ?weight .
    BIND(IF(?weight < 20, "Light", 
         IF(?weight < 100, "Medium", "Heavy")) AS ?category)
}
```

## **Real Applications**
- **Chemical databases**: Querying molecular properties
- **Social networks**: Finding connections and communities  
- **Knowledge graphs**: Complex relationship discovery
- **Data integration**: Combining multiple RDF sources

SPARQL transforms graph data into actionable information through precise pattern matching and powerful filtering capabilities.
