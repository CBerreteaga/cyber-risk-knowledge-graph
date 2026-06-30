from rdflib import Graph


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

GRAPH_FILE_PATH = "output/cyber_knowledge_graph.ttl"

QUERY_OPTIONS = {
    "1": {
        "name": "Assets with vulnerabilities",
        "file": "queries/assets_with_vulnerabilities.rq"
    },
    "2": {
        "name": "Assets with patchable vulnerabilities",
        "file": "queries/assets_with_vulnerabilities_patchable.rq"
    },
    "3": {
        "name": "Vulnerabilities mapped to MITRE techniques",
        "file": "queries/vulnerabilities_to_mitre.rq"
    },
    "4": {
        "name": "Vulnerabilities exploited by threat actors",
        "file": "queries/vulnerabilities_to_threat_actors.rq"
    },
    "5": {
        "name": "Critical vulnerabilities",
        "file": "queries/critical_vulnerabilities.rq"
    },
    "6": {
        "name": "Critical vulnerabilities with MITRE techniques",
        "file": "queries/critical_vulnerabilities_with_mitre.rq"
    },
    "7": {
        "name": "Critical risk paths",
        "file": "queries/critical_risk_paths.rq"
    },
    "8": {
        "name": "All assets and asset types",
        "file": "queries/all_assets.rq"
    },
    "9": {
        "name": "Assets w/ labels and types",
        "file": "queries/assets_with_labels.rq"
    },
    "10": {
        "name": "Vulnerabilities with labels",
        "file": "queries/vulnerabilities_with_labels.rq"
    }
}


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def print_banner():
    """
    Prints the startup banner for the command-line query tool.
    """
    print(r"""
   ______      __                  ____  _      __    
  / ____/_  __/ /_  ___  _____   / __ \(_)____/ /__  
 / /   / / / / __ \/ _ \/ ___/  / /_/ / / ___/ //_/  
/ /___/ /_/ / /_/ /  __/ /     / _, _/ (__  ) ,<     
\____/\__, /_.___/\___/_/     /_/ |_/_/____/_/|_|    
     /____/                                          

        Cyber Risk Knowledge Graph Query Tool
        ------------------------------------
        Explore Assets, Vulnerabilities, MITRE Techniques,
        Threat Actors, and Critical Risk Paths
    """)


def clean_uri(uri):
    """
    Converts a full RDF URI into a cleaner display value.

    Example:
    http://example.org/cyber#VULN-1234

    becomes:
    VULN-1234
    """
    return str(uri).split("#")[-1]


def load_graph(graph_file_path):
    """
    Loads the RDF graph from a Turtle file.

    Args:
        graph_file_path: Path to the saved RDF/Turtle graph file.

    Returns:
        An RDFLib Graph object.
    """
    graph = Graph()
    graph.parse(graph_file_path, format="turtle")
    return graph


def print_graph_loaded_message(graph):
    """
    Prints a confirmation message after the graph loads.
    """
    print("------------------------------------------")
    print("RDF graph loaded successfully.")
    print("Graph size:", len(graph))
    print("------------------------------------------")


def show_menu():
    """
    Displays the available SPARQL query options.
    """
    print("Choose a query to run:")
    print()

    for key, value in QUERY_OPTIONS.items():
        print(f"{key}. {value['name']}")

    print("-----------------------------------------")
    print("Press CTRL+C to Exit Program")


def get_user_choice():
    """
    Gets the user's menu choice.
    """
    return input("\nEnter choice: ").strip()


def load_query(query_file_path):
    """
    Reads a SPARQL query from a .rq file.

    Args:
        query_file_path: Path to the SPARQL query file.

    Returns:
        The SPARQL query as a string.
    """
    with open(query_file_path, "r", encoding="utf-8") as file:
        query = file.read()

    return query


def run_query(graph, query_file_path):
    """
    Loads and runs a SPARQL query against the RDF graph.

    Args:
        graph: RDFLib Graph object.
        query_file_path: Path to the SPARQL query file.

    Returns:
        Query results from RDFLib.
    """
    query = load_query(query_file_path)
    results = graph.query(query)
    return results


def print_results(results):
    """
    Prints SPARQL query results in a readable format.
    """
    print("------------------------------------------")
    print("Results")
    print("------------------------------------------")

    result_count = 1

    for row in results:
        print("--------------------------------------------------------------------------------------")
        print(result_count, "|", end=" ")

        for value in row:
            print(clean_uri(value), end=" | ")

        print()
        result_count += 1

    if result_count == 1:
        print("No results found.")

    print("--------------------------------------------------------------------------------------")


def run_query_menu(graph):
    """
    Runs the interactive query menu.

    The user can select different SPARQL queries to run
    against the loaded RDF graph.
    """
    while True:
        show_menu()

        choice = get_user_choice()

        selected_query = QUERY_OPTIONS.get(choice)

        if selected_query is None:
            print("Invalid choice. Please choose a valid option.")
            print()
            continue

        query_name = selected_query["name"]
        query_file_path = selected_query["file"]

        print("------------------------------------------")
        print("Running Query:", query_name)
        print("Query File:", query_file_path)
        print("------------------------------------------")

        results = run_query(graph, query_file_path)
        print_results(results)

        input("Press ENTER to continue...")
        print()


# ------------------------------------------------------------
# Main Program
# ------------------------------------------------------------

def main():
    """
    Main entry point for the Cyber Risk Knowledge Graph Query Tool.
    """
    print_banner()

    graph = load_graph(GRAPH_FILE_PATH)

    print_graph_loaded_message(graph)

    run_query_menu(graph)


if __name__ == "__main__":
    main()