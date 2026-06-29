# Cyber Risk Knowledge Graph

## Project Overview

The Cyber Risk Knowledge Graph is a Python-based ETL and RDF graph project that transforms cybersecurity data from a CSV file into RDF triples. The final graph can be queried with SPARQL to identify relationships between assets, vulnerabilities, MITRE ATT&CK techniques, and threat actors.

The purpose of this project is to practice building a cybersecurity data pipeline while learning how knowledge graphs can be used to connect and query security-related information.

## Why I Built This

I built this project to gain hands-on experience with:

* ETL pipeline development
* RDF graph construction
* SPARQL querying
* Cybersecurity data modeling
* MITRE ATT&CK relationship mapping
* Threat actor and vulnerability analysis

This project helped me understand how raw security data can be transformed into a structured graph that makes relationships easier to analyze.

## Dataset

The project uses a cybersecurity risk dataset stored as a CSV file. Each row represents a cybersecurity record with information about assets, vulnerabilities, threat actors, MITRE techniques, risk fields, and remediation details.

For version 1 of this project, I focused on the following data fields:

### Asset Fields

* `asset_id`
* `asset_name`
* `asset_type`

### Vulnerability Fields

* `vulnerability_id`
* `vulnerability_name`
* `vulnerability_description`
* `severity`
* `patch_available`

### Threat Actor Fields

* `threat_actor_id`
* `threat_actor`
* `actor_motivation`
* `actor_category`

### MITRE ATT&CK Fields

* `mitre_technique_id`
* `mitre_technique`
* `mitre_tactic`

## Project Structure

```text
graph-project/
├── data/
│   └── huge_cyber_risk_knowledge_graph_dataset.csv
├── docs/
│   ├── ontology-plan.md
│   └── etl-plan.md
├── output/
│   └── cyber_knowledge_graph.ttl
├── queries/
│   ├── assets_with_vulnerabilities.rq
│   ├── vulnerabilities_to_mitre.rq
│   ├── vulnerabilities_to_threat_actors.rq
│   ├── critical_vulnerabilities.rq
│   ├── critical_vulnerabilities_with_mitre.rq
│   └── critical_risk_paths.rq
├── src/
│   ├── etl.py
│   └── query_graph.py
├── .gitignore
├── README.md
└── requirements.txt
```

## ETL Pipeline

The project follows a simple ETL process:

```text
Extract → Transform → Load
```

### Extract

The extract step reads the CSV file and converts each row into a Python dictionary. Each dictionary uses the CSV column names as keys.

Example:

```text
asset_name → production-web-server-0229
vulnerability_id → VULN-9100D75C
mitre_technique_id → T1071
threat_actor → FIN7
```

### Transform

The transform step converts each CSV record into RDF-style triples.

Example relationship triples:

```text
Asset hasVulnerability Vulnerability
Vulnerability mapsToTechnique MITRETechnique
Vulnerability isExploitedBy ThreatActor
```

Example property triples:

```text
Asset assetType "server"
Vulnerability severity "Critical"
Vulnerability patchAvailable "True"
ThreatActor actorCategory "Ransomware"
MITRETechnique mitreTactic "Defense Evasion"
```

### Load

The load step uses RDFLib to create an RDF graph and save it as a Turtle file.

Output file:

```text
output/cyber_knowledge_graph.ttl
```

## Ontology Design

Version 1 of the ontology focuses on four main classes:

```text
Asset
Vulnerability
ThreatActor
MITRETechnique
```

## Core Relationships

The graph uses the following core relationships:

```text
Asset hasVulnerability Vulnerability
Vulnerability mapsToTechnique MITRETechnique
Vulnerability isExploitedBy ThreatActor
```

These relationships allow the graph to connect vulnerable systems, known vulnerabilities, MITRE ATT&CK techniques, and threat actors.

## Properties

The graph also stores properties as literal values.

### Asset Properties

```text
assetType
```

### Vulnerability Properties

```text
severity
patchAvailable
```

### Threat Actor Properties

```text
actorCategory
```

### MITRE Technique Properties

```text
mitreTactic
```

## RDF Graph Output

The graph is saved in Turtle format.

Example RDF-style output:

```turtle
@prefix cyber: <http://example.org/cyber#> .

cyber:production-web-server-0229 cyber:hasVulnerability cyber:VULN-9100D75C .
cyber:VULN-9100D75C cyber:mapsToTechnique cyber:T1071 .
cyber:VULN-9100D75C cyber:isExploitedBy cyber:FIN7 .
cyber:VULN-9100D75C cyber:severity "Critical" .
cyber:production-web-server-0229 cyber:assetType "server" .
```

## SPARQL Queries

This project includes several SPARQL queries.

### 1. Assets With Vulnerabilities

Find assets and the vulnerabilities connected to them.

```sparql
PREFIX cyber: <http://example.org/cyber#>

SELECT ?asset ?vulnerability
WHERE {
    ?asset cyber:hasVulnerability ?vulnerability .
}
LIMIT 10
```

### 2. Vulnerabilities Mapped to MITRE Techniques

Find vulnerabilities and the MITRE ATT&CK techniques they map to.

```sparql
PREFIX cyber: <http://example.org/cyber#>

SELECT ?vulnerability ?mitre_technique
WHERE {
    ?vulnerability cyber:mapsToTechnique ?mitre_technique .
}
LIMIT 10
```

### 3. Vulnerabilities Exploited by Threat Actors

Find vulnerabilities and the threat actors that exploit them.

```sparql
PREFIX cyber: <http://example.org/cyber#>

SELECT ?vulnerability ?threat_actor
WHERE {
    ?vulnerability cyber:isExploitedBy ?threat_actor .
}
LIMIT 10
```

### 4. Critical Vulnerabilities

Find vulnerabilities where the severity is Critical.

```sparql
PREFIX cyber: <http://example.org/cyber#>

SELECT ?vulnerability ?severity
WHERE {
    ?vulnerability cyber:severity ?severity .
    FILTER(?severity = "Critical")
}
LIMIT 10
```

### 5. Critical Vulnerabilities With MITRE Techniques

Find Critical vulnerabilities and the MITRE ATT&CK techniques they map to.

```sparql
PREFIX cyber: <http://example.org/cyber#>

SELECT ?vulnerability ?severity ?mitre_technique
WHERE {
    ?vulnerability cyber:severity ?severity .
    ?vulnerability cyber:mapsToTechnique ?mitre_technique .

    FILTER(?severity = "Critical")
}
LIMIT 10
```

### 6. Critical Risk Paths

Find assets with Critical vulnerabilities, the MITRE techniques connected to those vulnerabilities, and the threat actors that exploit them.

```sparql
PREFIX cyber: <http://example.org/cyber#>

SELECT ?asset ?vulnerability ?severity ?mitre_technique ?threat_actor
WHERE {
    ?asset cyber:hasVulnerability ?vulnerability .
    ?vulnerability cyber:severity ?severity .
    ?vulnerability cyber:mapsToTechnique ?mitre_technique .
    ?vulnerability cyber:isExploitedBy ?threat_actor .

    FILTER(?severity = "Critical")
}
LIMIT 10
```

## Example Query Result

Example output from the critical risk path query:

```text
1 | production-workstation-1160 | VULN-3BF12A40 | Critical | T1087 | BlackCat_Affiliate |
```

This result shows:

```text
Asset: production-workstation-1160
Vulnerability: VULN-3BF12A40
Severity: Critical
MITRE Technique: T1087
Threat Actor: BlackCat_Affiliate
```

## How to Run the Project

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the ETL pipeline

```bash
python src/etl.py
```

This creates the RDF graph file:

```text
output/cyber_knowledge_graph.ttl
```

### 4. Run SPARQL queries

```bash
python src/query_graph.py
```

To run a different query, update the query file path inside `src/query_graph.py`.

Example:

```python
query_file_path = "queries/critical_risk_paths.rq"
```

## Skills Demonstrated

This project demonstrates:

* Python scripting
* ETL pipeline design
* CSV parsing
* RDF graph construction
* RDFLib usage
* Turtle RDF serialization
* SPARQL querying
* Ontology planning
* Cybersecurity data modeling
* MITRE ATT&CK relationship mapping
* Vulnerability and threat actor analysis

## Future Improvements

Future versions of this project could include:

* Using `csv.DictReader` for more robust CSV parsing
* Adding RDF classes with `rdf:type`
* Adding readable labels with `rdfs:label`
* Using threat actor IDs as URI nodes and actor names as labels
* Adding more asset properties such as environment, region, and internet-facing status
* Adding risk score, likelihood, and impact fields
* Creating more advanced SPARQL queries
* Exporting query results to CSV
* Building a small dashboard or visualization layer
* Loading the graph into a triplestore such as Apache Jena Fuseki

## Project Status

Version 1 is complete.

The project currently supports:

* CSV extraction
* Triple transformation
* RDF graph loading
* Turtle graph output
* SPARQL query execution
* Relationship and property-based graph queries
