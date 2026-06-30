# Cyber Risk Knowledge Graph

## Project Overview

The Cyber Risk Knowledge Graph is a Python-based ETL and RDF graph project that transforms cybersecurity risk data from a CSV file into RDF triples. The final graph can be queried with SPARQL to analyze relationships between assets, findings, vulnerabilities, MITRE ATT&CK techniques, and threat actors.

The purpose of this project is to practice building a cybersecurity data pipeline while learning how knowledge graphs can connect security data in a way that supports risk analysis and investigation.

## Why I Built This

I built this project to gain hands-on experience with:

* ETL pipeline development
* CSV parsing with Python
* RDF graph construction
* RDFLib usage
* Turtle RDF serialization
* SPARQL querying
* Cybersecurity data modeling
* MITRE ATT&CK relationship mapping
* Threat actor and vulnerability analysis
* Risk-based security querying

This project helped me understand how raw security data can be transformed into a structured graph that makes relationships easier to analyze.

## Dataset

The project uses a cybersecurity risk dataset stored as a CSV file. Each row represents a cybersecurity finding that connects an asset to a vulnerability, MITRE ATT&CK technique, threat actor, and risk-related fields.

For version 1 of this project, I focused on the following data fields:

### Asset Fields

* `asset_id`
* `asset_name`
* `asset_type`

### Finding / Risk Fields

* `record_id`
* `risk_score`
* `likelihood`
* `impact`
* `patch_available`
* `exploit_available`

### Vulnerability Fields

* `vulnerability_id`
* `vulnerability_name`
* `vulnerability_description`
* `severity`

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
cyber-risk-knowledge-graph/
├── data/
│   └── huge_cyber_risk_knowledge_graph_dataset.csv
├── docs/
│   ├── ontology-plan.md
│   └── etl-plan.md
├── output/
│   └── cyber_knowledge_graph.ttl
├── queries/
│   ├── highest_risk_assets.rq
│   └── high_risk_findings_exploitable_no_patch.rq
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

The extract step reads the CSV file with Python's `csv.DictReader`. Each CSV row is converted into a Python dictionary where the CSV column names are used as dictionary keys.

Example:

```text
record_id → FINDING-0001
asset_name → production-web-server-0229
vulnerability_id → VULN-9100D75C
mitre_technique_id → T1071
threat_actor → FIN7
risk_score → 95
```

### Transform

The transform step converts each CSV record into RDF-style triples. The updated model uses a `Finding` node between an `Asset` and a `Vulnerability` so risk fields belong to the specific finding record instead of being attached directly to the vulnerability.

Core relationship triples:

```text
Asset hasFinding Finding
Finding hasVulnerability Vulnerability
Vulnerability mapsToTechnique MITRETechnique
Vulnerability isExploitedBy ThreatActor
```

Example property triples:

```text
Asset assetType "server"
Finding riskScore "95"
Finding likelihood "High"
Finding impact "High"
Finding patchAvailable "False"
Finding exploitAvailable "True"
Vulnerability severity "Critical"
ThreatActor actorCategory "Ransomware"
MITRETechnique mitreTactic "Defense Evasion"
```

The ETL also adds RDF classes with `rdf:type` and readable names with `rdfs:label`.

Example:

```turtle
cyber:production-web-server-0229 a cyber:Asset ;
    rdfs:label "production-web-server-0229" ;
    cyber:assetType "server" .

cyber:FINDING-0001 a cyber:Finding ;
    cyber:hasVulnerability cyber:VULN-9100D75C ;
    cyber:riskScore "95" .
```

### Load

The load step uses RDFLib to create an RDF graph and save it as a Turtle file.

Output file:

```text
output/cyber_knowledge_graph.ttl
```

## Ontology Design

Version 1 of the ontology focuses on five main classes:

```text
Asset
Finding
Vulnerability
ThreatActor
MITRETechnique
```

## Core Relationships

The graph uses the following core relationships:

```text
Asset hasFinding Finding
Finding hasVulnerability Vulnerability
Vulnerability mapsToTechnique MITRETechnique
Vulnerability isExploitedBy ThreatActor
```

These relationships allow the graph to connect vulnerable systems, specific risk findings, known vulnerabilities, MITRE ATT&CK techniques, and threat actors.

## Properties

The graph also stores properties as literal values.

### Asset Properties

```text
assetType
```

### Finding Properties

```text
riskScore
likelihood
impact
patchAvailable
exploitAvailable
```

### Vulnerability Properties

```text
severity
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
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

cyber:production-web-server-0229 a cyber:Asset ;
    rdfs:label "production-web-server-0229" ;
    cyber:assetType "server" ;
    cyber:hasFinding cyber:FINDING-0001 .

cyber:FINDING-0001 a cyber:Finding ;
    cyber:hasVulnerability cyber:VULN-9100D75C ;
    cyber:riskScore "95" ;
    cyber:likelihood "High" ;
    cyber:impact "High" ;
    cyber:patchAvailable "False" ;
    cyber:exploitAvailable "True" .

cyber:VULN-9100D75C a cyber:Vulnerability ;
    rdfs:label "Example Vulnerability" ;
    cyber:severity "Critical" ;
    cyber:mapsToTechnique cyber:T1071 ;
    cyber:isExploitedBy cyber:FIN7 .
```

## SPARQL Queries

The project now focuses on fewer, stronger risk-based SPARQL queries instead of many small demo queries.

### 1. Sample High-Risk Asset Findings

Find assets, findings, vulnerabilities, and risk values.

```sparql
PREFIX cyber: <http://example.org/cyber#>

SELECT ?asset ?asset_type ?finding ?vulnerability ?severity ?risk_score ?likelihood ?impact
WHERE {
    ?asset a cyber:Asset .
    ?asset cyber:assetType ?asset_type .
    ?asset cyber:hasFinding ?finding .

    ?finding a cyber:Finding .
    ?finding cyber:hasVulnerability ?vulnerability .
    ?finding cyber:riskScore ?risk_score .
    ?finding cyber:likelihood ?likelihood .
    ?finding cyber:impact ?impact .

    ?vulnerability a cyber:Vulnerability .
    ?vulnerability cyber:severity ?severity .
}
LIMIT 10
```

### 2. High-Risk Exploitable Findings With No Patch

Find findings where an exploit is available, no patch is available, and the risk score is high.

```sparql
PREFIX cyber: <http://example.org/cyber#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?asset ?asset_type ?finding ?vulnerability ?severity ?exploit_available ?patch_available ?risk_score
WHERE {
    ?asset a cyber:Asset .
    ?asset cyber:assetType ?asset_type .
    ?asset cyber:hasFinding ?finding .

    ?finding a cyber:Finding .
    ?finding cyber:hasVulnerability ?vulnerability .
    ?finding cyber:exploitAvailable ?exploit_available .
    ?finding cyber:patchAvailable ?patch_available .
    ?finding cyber:riskScore ?risk_score .

    ?vulnerability a cyber:Vulnerability .
    ?vulnerability cyber:severity ?severity .

    FILTER(LCASE(STR(?exploit_available)) = "true")
    FILTER(LCASE(STR(?patch_available)) = "false")
    FILTER(xsd:decimal(?risk_score) >= 80)
}
LIMIT 10
```

## Query Performance Note

The project currently uses RDFLib for local graph generation and SPARQL querying. RDFLib works well for learning, prototyping, and smaller local graphs. More complex queries that require numeric casting, sorting, or large joins can be slower. For this version, the queries were simplified to avoid expensive ordering operations and to keep local query execution faster.

## How to Run the Project

### 1. Create and activate a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows Git Bash:

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

The query tool displays a menu of available SPARQL queries.

## Skills Demonstrated

This project demonstrates:

* Python scripting
* ETL pipeline design
* CSV parsing with `csv.DictReader`
* RDF graph construction
* RDFLib usage
* RDF classes with `rdf:type`
* Human-readable labels with `rdfs:label`
* Turtle RDF serialization
* SPARQL querying
* Ontology planning
* Cybersecurity data modeling
* Risk finding modeling
* MITRE ATT&CK relationship mapping
* Vulnerability and threat actor analysis

## Future Improvements

Future versions of this project could include:

* Using stronger URI design with IDs as URI nodes and names as labels
* Adding more asset properties such as environment, region, and internet-facing status
* Adding remediation status and SLA-based prioritization
* Creating a full attack-path query from asset to finding to vulnerability to MITRE technique to threat actor
* Exporting query results to CSV
* Building a small dashboard or visualization layer
* Loading the graph into a dedicated triple store for better query performance

## Project Status

Version 1 is complete.

The project currently supports:

* CSV extraction with `csv.DictReader`
* Triple transformation
* RDF graph loading
* RDF classes with `rdf:type`
* Readable labels with `rdfs:label`
* Turtle graph output
* SPARQL query execution
* Risk-focused graph queries
