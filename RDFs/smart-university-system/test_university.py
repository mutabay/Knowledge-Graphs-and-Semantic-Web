from rdflib import Graph, Namespace, Literal
from rdflib.namespace import FOAF, RDF, RDFS
import rdflib.plugins.sparql as sparql

# Create graph and load the data
g = Graph()
g.parse("university_system.ttl", format="turtle")

print("University System - Local Testing")
print("="*50)

# Define namespaces
UNIV = Namespace("http://aau.at/")
DCTERMS = Namespace("http://purl.org/dc/terms/")

# Query 1: Show all people
print("\nAll People in the System:")
query1 = """
PREFIX univ: <http://aau.at/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?person ?name WHERE {
    ?person foaf:name ?name .
}
"""

results1 = g.query(query1)
for row in results1:
    print(f"   - {row.name}")

# Query 2: Your enrolled courses
print("\nYour Enrolled Courses:")
query2 = """
PREFIX univ: <http://aau.at/>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?course ?title WHERE {
    univ:you univ:enrolledIn ?course .
    ?course dcterms:title ?title .
}
"""

results2 = g.query(query2)
for row in results2:
    print(f"   - {row.title}")

# Query 3: Find study partners
print("\nYour Study Partners (Shared Courses):")
query3 = """
PREFIX univ: <http://aau.at/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?name ?courseTitle WHERE {
    univ:you univ:enrolledIn ?course .
    ?student univ:enrolledIn ?course ;
             foaf:name ?name .
    ?course dcterms:title ?courseTitle .
    FILTER(?student != univ:you)
}
"""

results3 = g.query(query3)
for row in results3:
    print(f"   - {row.name} shares {row.courseTitle}")

# Query 4: Find people with shared interests
print("\nPeople with Shared Interests:")
query4 = """
PREFIX univ: <http://aau.at/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name ?interest WHERE {
    univ:you foaf:interest ?interest .
    ?person foaf:interest ?interest ;
            foaf:name ?name .
    FILTER(?person != univ:you)
}
"""

results4 = g.query(query4)
for row in results4:
    print(f"   - {row.name} is interested in {row.interest}")

# Query 5: Course recommendations (prerequisites you've met)
print("\nCourse Recommendations:")
query5 = """
PREFIX univ: <http://aau.at/>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?courseTitle ?reason WHERE {
    ?course univ:relatedTo ?yourCourse ;
            dcterms:title ?courseTitle .
    univ:you univ:enrolledIn ?yourCourse .
    FILTER NOT EXISTS { univ:you univ:enrolledIn ?course }
    BIND("Related to your current course" AS ?reason)
}
"""

results5 = g.query(query5)
for row in results5:
    print(f"   - {row.courseTitle} ({row.reason})")

# Show total triples
print(f"\nTotal triples in your knowledge graph: {len(g)}")