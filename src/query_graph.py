from rdflib import Graph


def clean_uri(uri):
    return str(uri).split('#')[-1]

query_file_path = "queries/vulnerabilities_to_threat_actors.rq"
# Load the RDF graph from the file
graph = Graph()
graph.parse("output/cyber_knowledge_graph.ttl", format="turtle")

if graph is not None:
    print("------------------------------------------")
    print("RDF graph loaded successfully.")
    print("Graph size:", len(graph))
    print("------------------------------------------")
else:
    print("------------------------------------------")
    print("Failed to load RDF graph.")
    print("------------------------------------------")

print("Running Query: ", query_file_path)

with open(query_file_path, "r") as file:
    query = file.read()

results = graph.query(query)
i = 1
for row in results:
    print("--------------------------------------------------------------------------------------")
    print(i, "|", end=" ")

    for value in row:
        print(clean_uri(value), end = " | ")
    
    print()
    
    i += 1