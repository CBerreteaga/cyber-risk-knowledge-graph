from rdflib import Graph
import time
import threading

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

GRAPH_FILE_PATH = "output/cyber_knowledge_graph.ttl"

QUERY_OPTIONS = {
    "1": {
        "name": "High-Risk Assets",
        "file": "queries/highest_risk_assets.rq"
    },
    "2": {
        "name": "Exploitable Assets with no patch",
        "file": "queries/high_risk_findings_exploitable_no_patch.rq"
    },
    "3": {
        "name": "Exploitable Assets with patch available",
        "file": "queries/high_risk_findings_exploitable_patch.rq"
    },
    "4": {
        "name": "Full attack paths",
        "file": "queries/full_attack_paths.rq"
    }
}


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------
def show_spinner(stop_event):
    "Shows a simple loading spinner while query is running"
    spinner = ["|","/","-", "\\"]

    index = 0

    while not stop_event.is_set():
        print(f"\rQuery running...{spinner[index % len(spinner)]}", end = "", flush = True)
        time.sleep(0.2)
        index +=1

    print("\rQuery completed.           ")




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
    """
    query = load_query(query_file_path)

    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=show_spinner, args=(stop_event,))

    start_time = time.time()

    spinner_thread.start()

    try:
        results = graph.query(query)
    finally:
        stop_event.set()
        spinner_thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Query completed in {elapsed_time:.2f} seconds.")

    return results


def print_results(results):
    """
    Prints SPARQL query results as a clean table with column headers.
    Shows progress while collecting, formatting, and printing results.
    """
    print("------------------------------------------")
    print("Preparing results for display...")
    print("------------------------------------------")

    # Step 1: Collect rows
    print("Collecting result rows...", end="", flush=True)

    rows = []

    for row in results:
        rows.append(row)

        if len(rows) % 10 == 0:
            print(f"\rCollecting result rows... {len(rows)} rows", end="", flush=True)

    print(f"\rCollected {len(rows)} result rows.          ")

    if len(rows) == 0:
        print("No results found.")
        print("------------------------------------------")
        return

    # Step 2: Get column headers
    headers = [str(variable) for variable in results.vars]

    # Step 3: Clean values
    print("Formatting result rows...", end="", flush=True)

    cleaned_rows = []

    for row_number, row in enumerate(rows, start=1):
        cleaned_row = []

        for value in row:
            cleaned_row.append(clean_uri(value))

        cleaned_rows.append(cleaned_row)

        print(
            f"\rFormatting result rows... {row_number}/{len(rows)}",
            end="",
            flush=True
        )

    print("\rFormatting result rows... complete.        ")

    # Step 4: Calculate column widths
    print("Building table...", end="", flush=True)

    column_widths = []

    for column_index, header in enumerate(headers):
        max_width = len(header)

        for row in cleaned_rows:
            value_width = len(row[column_index])

            if value_width > max_width:
                max_width = value_width

        column_widths.append(max_width)

    print("\rBuilding table... complete.        ")

    # Step 5: Print table
    print("------------------------------------------")
    print("Results")
    print("------------------------------------------")

    # Header row
    header_parts = []

    for index, header in enumerate(headers):
        header_parts.append(header.ljust(column_widths[index]))

    print(" | ".join(header_parts))

    # Separator row
    separator_parts = []

    for width in column_widths:
        separator_parts.append("-" * width)

    print("-+-".join(separator_parts))

    table_lines = []

    for row_number, row in enumerate(cleaned_rows, start=1):
        row_parts = []

        for index, value in enumerate(row):
            row_parts.append(value.ljust(column_widths[index]))

        table_lines.append(" | ".join(row_parts))

    for line in table_lines:
        print(line)

    print("------------------------------------------")
    
    
    


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