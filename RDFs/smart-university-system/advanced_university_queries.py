from rdflib import Graph, Namespace
from collections import defaultdict

g = Graph()
g.parse("university_system.ttl", format="turtle")

def find_course_recommendations():
    print("\nCourse Recommendation System")
    print("-" * 40)
    
    # Find courses you haven't taken but prerequisites are met
    query = """
    PREFIX univ: <http://aau.at/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?course ?title WHERE {
        ?course a univ:Course ;
                dcterms:title ?title .
        FILTER NOT EXISTS { univ:you univ:enrolledIn ?course }
        FILTER NOT EXISTS { 
            ?course univ:hasPrerequisite ?prereq .
            FILTER NOT EXISTS { univ:you univ:enrolledIn ?prereq }
        }
    }
    """
    
    results = g.query(query)
    for i, row in enumerate(results, 1):
        print(f"{i}. {row.title}")

def analyze_research_network():
    print("\nResearch Collaboration Network")
    print("-" * 40)
    
    # Find potential research collaborators
    query = """
    PREFIX univ: <http://aau.at/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT ?name ?research ?sharedInterest WHERE {
        ?person foaf:name ?name ;
                univ:researchArea ?research ;
                foaf:interest ?sharedInterest .
        univ:you foaf:interest ?sharedInterest .
        FILTER(?person != univ:you)
    }
    """
    
    results = g.query(query)
    collaborators = defaultdict(list)
    
    for row in results:
        collaborators[str(row.name)].append({
            'research': str(row.research),
            'shared_interest': str(row.sharedInterest)
        })
    
    for name, details in collaborators.items():
        print(f"\n{name}:")
        for detail in details:
            research = detail['research']
            interest = detail['shared_interest'].split('/')[-1]  # Extract the last part of URI
            print(f"  - Research: {research}")
            print(f"  - Shared interest: {interest}")

def course_difficulty_analysis():
    print("\nCourse Difficulty Analysis")
    print("-" * 40)
    
    query = """
    PREFIX univ: <http://aau.at/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?title ?difficulty ?credits WHERE {
        univ:you univ:enrolledIn ?course .
        ?course dcterms:title ?title ;
                univ:difficulty ?difficulty ;
                univ:credits ?credits .
    }
    ORDER BY ?difficulty
    """
    
    results = g.query(query)
    total_credits = 0
    
    for row in results:
        print(f"{row.title}: {row.difficulty} level, {row.credits} credits")
        total_credits += int(row.credits)
    
    print(f"\nTotal credits: {total_credits}")

def department_statistics():
    print("\nDepartment Statistics")
    print("-" * 40)
    
    query = """
    PREFIX univ: <http://aau.at/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?deptName (COUNT(?course) as ?courseCount) WHERE {
        ?dept foaf:name ?deptName .
        ?course univ:offeredBy ?dept .
        FILTER(?dept != univ:AAU)
    }
    GROUP BY ?deptName
    """
    
    results = g.query(query)
    for row in results:
        print(f"{row.deptName}: {row.courseCount} courses")

def show_knowledge_graph_stats():
    print("\nKnowledge Graph Statistics")
    print("-" * 40)
    
    # Count different types
    queries = {
        "Students": "SELECT (COUNT(?s) as ?count) WHERE { ?s a univ:PhDStudent }",
        "Courses": "SELECT (COUNT(?s) as ?count) WHERE { ?s a univ:Course }",
        "Departments": "SELECT (COUNT(?s) as ?count) WHERE { ?s a univ:Department }",
        "Prerequisites": "SELECT (COUNT(?s) as ?count) WHERE { ?s univ:hasPrerequisite ?o }"
    }
    
    for label, query_str in queries.items():
        full_query = f"PREFIX univ: <http://aau.at/>\n{query_str}"
        results = g.query(full_query)
        for row in results:
            print(f"{label}: {row.count}")

def main_menu():
    while True:
        print("\n" + "="*50)
        print("Advanced University Knowledge System")
        print("="*50)
        print("1. Course Recommendations")
        print("2. Research Network Analysis") 
        print("3. Course Difficulty Analysis")
        print("4. Department Statistics")
        print("5. Knowledge Graph Statistics")
        print("6. Exit")
        
        choice = input("\nChoose an option (1-6): ")
        
        if choice == "1":
            find_course_recommendations()
        elif choice == "2":
            analyze_research_network()
        elif choice == "3":
            course_difficulty_analysis()
        elif choice == "4":
            department_statistics()
        elif choice == "5":
            show_knowledge_graph_stats()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()