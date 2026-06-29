# Import CSV
# Open it
# Read file as rows with column names
# Print the first row
# Print only the version 1 columns I care about

# Importing os to keep terminal clean
import os
import platform

from rdflib import Graph, Namespace, URIRef

extracting_complete = False
transforming_complete = False
loading_complete = False

def make_uri_safe(value):
    return value.strip().replace(" ", "_")

def calculate_percentage_complete(processed, total):

    percentage_complete = (processed / total) * 100

    if processed % 500 == 0 or processed == total:
        clear_terminal()

        if not extracting_complete:
            print(f"Extracting Data: {percentage_complete:.0f}%/100%")
        elif extracting_complete and not transforming_complete:
            print("Extracting Data: 100%/100%")
            print(f"Transforming Data: {percentage_complete:.0f}%/100%")
        elif extracting_complete and transforming_complete and not loading_complete:
            print("Extracting Data: 100%/100%")
            print("Transforming Data: 100%/100%")
            print(f"Loading Data: {percentage_complete:.0f}%/100%")
        

def clear_terminal():
    """
    Clears the terminal screen for Windows, macOS, and Linux.
    """
    try:
        # Detect the operating system
        current_os = platform.system()
        
        if current_os == "Windows":
            os.system('cls')  # Windows command
        else:
            os.system('clear')  # macOS/Linux command
    except Exception as e:
        print(f"Error clearing terminal: {e}")

def read_csv_file():
    global extracting_complete
    lines = []
    column_names = []
    rows = []
    mismatch_count = 0
    row_data = []
    dictionary_array = []
    csv_file_path = 'data/huge_cyber_risk_knowledge_graph_dataset.csv'

    # Open the file
    file = open(csv_file_path, 'r')
    print("File opened successfully.")


    # Read content of file
    for line in file:
        lines.append(line.strip()) 
            

    # Close the file
    file.close()
    print("File closed successfully.")

    column_names = lines[0].split(',')
    rows = lines[1:]

    rows_processed = 0
    rows_count = len(rows)

    for row in rows:
        row_data = row.split(',')
        d = {}

        if len(row_data) != len(column_names):
            print("Row Length Mismatch:", len(row_data), "Expected:", len(column_names))
            mismatch_count += 1
        i = 0

        for column in column_names:
    
            if i < len(row_data):
                d[column] = row_data[i]
                ##print(f"{column}: {row_data[i]}")
            else:
                d[column] = "MISSING"   
                ##print(f"{column}: MISSING")
            i += 1

        dictionary_array.append(d)

        rows_processed += 1

        calculate_percentage_complete(rows_processed, rows_count)

    ##print("Extraction Complete")
    ##print("Mismatch Count:", mismatch_count)
    ##print("Total records:", len(dictionary_array))
    extracting_complete = True
    return dictionary_array

def transform_data(records):
    global transforming_complete
    transformed_records = []
    # Placeholder for transformation logic
    records_processed= 0
    for record in records:
        asset = record["asset_name"]
        vulnerability = record["vulnerability_id"]
        mitre_technique = record["mitre_technique_id"]
        threat_actor = record["threat_actor"]

        '''
        print("-----------------------------------------")
        print(f"{asset} hasVulnerability {vulnerability}")
        print(f"{vulnerability} mapsToTechnique {mitre_technique}")
        print(f"{vulnerability} isExploitedBy {threat_actor}")
        '''

        transformed_records.append((asset, "hasVulnerability", vulnerability))
        transformed_records.append((vulnerability, "mapsToTechnique", mitre_technique))
        transformed_records.append((vulnerability, "isExploitedBy", threat_actor))

        
        records_processed += 1
        
        calculate_percentage_complete(records_processed, len(records))

    transforming_complete = True
    return transformed_records


def load_data(transformed_records):
    global loading_complete
    records_processed = 0

    # Creates new RDF graph
    rdf_graph = Graph()

    # Defines a namspace for the ontology
    CYBER = Namespace("http://example.org/cyber#")

    # Binding namespace prefixes for better readability
    rdf_graph.bind("cyber", CYBER)

    for record in transformed_records:
        subject_uri = URIRef(CYBER[make_uri_safe(record[0])])
        predicate_uri = URIRef(CYBER[make_uri_safe(record[1])])   
        object_uri = URIRef(CYBER[make_uri_safe(record[2])])

        rdf_graph.add((subject_uri, predicate_uri, object_uri))

        records_processed += 1
        calculate_percentage_complete(records_processed, len(transformed_records))

    # Save the RDF graph to a file
    rdf_graph.serialize(destination="output/cyber_knowledge_graph.ttl", format="turtle")
    loading_complete = True

    #Prinouts
    print("ETL Process Complete")
    print("Graph Size:", len(rdf_graph))
    print("RDF Graph saved to data/cyber_knowledge_graph.rdf")

    return 0

if __name__ == "__main__":
    extracted_data = read_csv_file()
    transformed_data = transform_data(extracted_data)
    load_data(transformed_data)

