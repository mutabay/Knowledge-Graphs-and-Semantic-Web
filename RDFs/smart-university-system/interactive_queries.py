from rdflib import Graph, Namespace
import sys

g = Graph()
g.parse("university_system.ttl", format="turtle")

def run_custom_query():
    print("\nEnter your SPARQL query (type 'exit' to quit):")
    print("Example: SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10")
    
    while True:
        query = input("\nSPARQL> ")
        
        if query.lower() == 'exit':
            break
            
        try:
            results = g.query(query)
            print("\nResults:")
            for i, row in enumerate(results, 1):
                print(f"{i}. {row}")
        except Exception as e:
            print(f"Error: {e}")

def predefined_queries():
    queries = {
        "1": ("All people", """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?name WHERE { ?person foaf:name ?name }
        """),
        "2": ("Your courses", """
            PREFIX univ: <http://aau.at/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            SELECT ?title WHERE { 
                univ:you univ:enrolledIn ?course .
                ?course dcterms:title ?title 
            }
        """),
        "3": ("Study partners", """
            PREFIX univ: <http://aau.at/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?name WHERE {
                univ:you univ:enrolledIn ?course .
                ?student univ:enrolledIn ?course ;
                         foaf:name ?name .
                FILTER(?student != univ:you)
            }
        """)
    }
    
    print("\nPredefined Queries:")
    for key, (desc, query) in queries.items():
        print(f"{key}. {desc}")
    
    choice = input("\nChoose (1-3) or 'custom' for custom query: ")
    
    if choice in queries:
        desc, query = queries[choice]
        print(f"\nRunning: {desc}")
        results = g.query(query)
        for i, row in enumerate(results, 1):
            print(f"{i}. {row}")
    elif choice.lower() == 'custom':
        run_custom_query()

if __name__ == "__main__":
    print("University Knowledge Graph - Interactive Mode")
    predefined_queries()