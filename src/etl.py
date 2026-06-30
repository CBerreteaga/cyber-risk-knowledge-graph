# Import CSV
# Open it
# Read file as rows with column names
# Print the first row
# Print only the version 1 columns I care about

# Importing os to keep terminal clean
import os
import platform
import csv

# Need literals to get the plain value/text (properties)
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS

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

    dictionary_array = []
    csv_file_path = "data/huge_cyber_risk_knowledge_graph_dataset.csv"

    print("Opening CSV file...")

    with open(csv_file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        rows = list(reader)
        rows_count = len(rows)

        for index, row in enumerate(rows, start=1):
            dictionary_array.append(row)
            calculate_percentage_complete(index, rows_count)

    extracting_complete = True

    print("Extraction complete.")
    print("Total records:", len(dictionary_array))

    return dictionary_array

def transform_data(records):
    global transforming_complete

    transformed_records = []
    records_processed = 0

    for record in records:
        # Finding field
        finding = record["record_id"]
        # Asset fields
        asset = record["asset_name"]
        asset_type = record["asset_type"]

        # Vulnerability fields
        vulnerability = record["vulnerability_id"]
        vulnerability_name = record["vulnerability_name"]
        severity = record["severity"]
        patch_available = record["patch_available"]
        exploit_available = record["exploit_available"]
        risk_score = record["risk_score"]
        likelihood = record["likelihood"]
        impact = record["impact"]

        # MITRE technique fields
        mitre_technique = record["mitre_technique_id"]
        mitre_technique_name = record["mitre_technique"]
        mitre_tactic = record["mitre_tactic"]

        # Threat actor fields
        threat_actor = record["threat_actor"]
        actor_category = record["actor_category"]

        # Entity type triples
        transformed_records.append((finding, "type", "Finding", "rdf_type"))
        transformed_records.append((asset, "type", "Asset", "rdf_type"))
        transformed_records.append((vulnerability, "type", "Vulnerability", "rdf_type"))
        transformed_records.append((mitre_technique, "type", "MITRETechnique", "rdf_type"))
        transformed_records.append((threat_actor, "type", "ThreatActor", "rdf_type"))

        # Human-readable labels
        transformed_records.append((asset, "label", asset, "rdfs_label"))
        transformed_records.append((vulnerability, "label", vulnerability_name, "rdfs_label"))
        transformed_records.append((mitre_technique, "label", mitre_technique_name, "rdfs_label"))
        transformed_records.append((threat_actor, "label", threat_actor, "rdfs_label"))

        # Core relationships
        transformed_records.append((asset, "hasFinding", finding, "uri"))
        transformed_records.append((finding, "hasVulnerability", vulnerability, "uri"))
        transformed_records.append((finding, "mapsToTechnique", mitre_technique, "uri"))
        transformed_records.append((finding, "isExploitedBy", threat_actor, "uri"))

        # Finding properties
        transformed_records.append((finding, "riskScore", risk_score, "literal"))
        transformed_records.append((finding, "likelihood", likelihood, "literal"))
        transformed_records.append((finding, "impact", impact, "literal"))
        transformed_records.append((finding, "patchAvailable", patch_available, "literal"))
        transformed_records.append((finding, "exploitAvailable", exploit_available, "literal"))
        transformed_records.append((finding, "severity", severity, "literal"))
        
        # Asset properties
        transformed_records.append((asset, "assetType", asset_type, "literal"))

        # Threat actor properties
        transformed_records.append((threat_actor, "actorCategory", actor_category, "literal"))

        # MITRE technique properties
        transformed_records.append((mitre_technique, "mitreTactic", mitre_tactic, "literal"))

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
    rdf_graph.bind("rdf", RDF)
    rdf_graph.bind("rdfs", RDFS)

    for record in transformed_records:
        subject, predicate, object_value, object_type = record

        subject_uri = URIRef(CYBER[make_uri_safe(subject)])
        predicate_uri = URIRef(CYBER[make_uri_safe(predicate)])

        if object_type == "uri":
            object_node = URIRef(CYBER[make_uri_safe(object_value)])
        elif object_type == "rdf_type":
            predicate_uri = RDF.type
            object_node = URIRef(CYBER[make_uri_safe(object_value)])
        elif object_type == "rdfs_label":
            predicate_uri = RDFS.label
            object_node = Literal(object_value)
        else:
            object_node = Literal(object_value)
        

        rdf_graph.add((subject_uri, predicate_uri, object_node))

        records_processed += 1
        calculate_percentage_complete(records_processed, len(transformed_records))

    # Save the RDF graph to a file
    rdf_graph.serialize(destination="output/cyber_knowledge_graph.ttl", format="turtle")
    loading_complete = True

    #Prinouts
    print("ETL Process Complete")
    print("Graph Size:", len(rdf_graph))
    print("RDF Graph saved to output/cyber_knowledge_graph.ttl")
 
    return 0

if __name__ == "__main__":
    extracted_data = read_csv_file()
    transformed_data = transform_data(extracted_data)
    load_data(transformed_data)

