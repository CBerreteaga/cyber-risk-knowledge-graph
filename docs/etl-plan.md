# ETL Plan

## 1. Goal

The goal of this project is to take cybersecurity risk data from a CSV file and prepare it for SPARQL querying. The data is transformed into RDF triples and loaded into an RDF graph.

The current graph model uses this main pattern:

```text
Asset → Finding → Vulnerability → MITRE Technique / Threat Actor
```

## 2. Extract

Extract means reading the CSV file and ingesting the data.

This project uses Python's `csv.DictReader` to read the CSV file. `DictReader` automatically uses the first row of the CSV file as column names and converts each row into a dictionary.

Example:

```python
{
    "record_id": "FINDING-0001",
    "asset_name": "production-web-server-0229",
    "asset_type": "Web Server",
    "vulnerability_id": "VULN-9100D75C",
    "risk_score": "95"
}
```

## 3. Transform

After the CSV file is read, each row is processed one at a time. The values from each row are mapped to the correct cybersecurity entity.

The main entities are:

```text
Asset
Finding
Vulnerability
ThreatActor
MITRETechnique
```

The transform step converts selected CSV values into RDF triples. Each triple has a subject, predicate, and object.

## 4. Updated Graph Model

Earlier versions connected assets directly to vulnerabilities:

```text
Asset hasVulnerability Vulnerability
```

The updated model uses a `Finding` node:

```text
Asset hasFinding Finding
Finding hasVulnerability Vulnerability
```

This is a better design because risk fields belong to a specific finding or record, not directly to a vulnerability. The same vulnerability can appear on many assets with different risk scores, likelihood values, impact values, patch status, and exploit availability.

## 5. Core Relationship Triples

Each CSV record can create these relationship triples:

```text
Asset hasFinding Finding
Finding hasVulnerability Vulnerability
Vulnerability mapsToTechnique MITRETechnique
Vulnerability isExploitedBy ThreatActor
```

## 6. Type Triples

The ETL creates `rdf:type` triples to classify graph nodes.

Examples:

```text
Asset rdf:type cyber:Asset
Finding rdf:type cyber:Finding
Vulnerability rdf:type cyber:Vulnerability
MITRETechnique rdf:type cyber:MITRETechnique
ThreatActor rdf:type cyber:ThreatActor
```

In Turtle output, `rdf:type` may appear as the shorthand `a`.

Example:

```turtle
cyber:production-web-server-0229 a cyber:Asset .
```

## 7. Label Triples

The ETL creates `rdfs:label` triples for readable names.

Examples:

```text
Asset rdfs:label "production-web-server-0229"
Vulnerability rdfs:label "SQL Injection"
MITRETechnique rdfs:label "Application Layer Protocol"
ThreatActor rdfs:label "FIN7"
```

## 8. Property Triples

### Asset Properties

```text
Asset assetType "Web Server"
```

### Finding Properties

```text
Finding riskScore "95"
Finding likelihood "High"
Finding impact "High"
Finding patchAvailable "False"
Finding exploitAvailable "True"
```

### Vulnerability Properties

```text
Vulnerability severity "Critical"
```

### Threat Actor Properties

```text
ThreatActor actorCategory "Ransomware"
```

### MITRE Technique Properties

```text
MITRETechnique mitreTactic "Defense Evasion"
```

## 9. Example ETL Flow

1. Extract row:

```text
record_id: FINDING-0001
asset_name: production-web-server-0229
vulnerability_id: VULN-9100D75C
mitre_technique_id: T1071
threat_actor: FIN7
risk_score: 95
patch_available: False
exploit_available: True
```

2. Create triples:

```text
production-web-server-0229 hasFinding FINDING-0001
FINDING-0001 hasVulnerability VULN-9100D75C
FINDING-0001 riskScore "95"
FINDING-0001 patchAvailable "False"
FINDING-0001 exploitAvailable "True"
VULN-9100D75C mapsToTechnique T1071
VULN-9100D75C isExploitedBy FIN7
```

3. Load triples into RDF graph.

## 10. Load

After the data is transformed into triples, the triples are loaded into an RDFLib graph. The graph stores relationships between assets, findings, vulnerabilities, threat actors, and MITRE techniques.

The graph is serialized to Turtle format.

Output file:

```text
output/cyber_knowledge_graph.ttl
```

## 11. Required Columns

### Finding Columns

- record_id
- risk_score
- likelihood
- impact
- patch_available
- exploit_available

### Asset Columns

- asset_id
- asset_name
- asset_type

### Vulnerability Columns

- vulnerability_id
- vulnerability_name
- vulnerability_description
- severity

### ThreatActor Columns

- threat_actor_id
- threat_actor
- actor_motivation
- actor_category

### MITRETechnique Columns

- mitre_technique_id
- mitre_technique
- mitre_tactic

## 12. Query Focus

The project now focuses on stronger risk-based SPARQL queries, such as:

1. Sample high-risk asset findings
2. High-risk exploitable findings with no patch available
3. Future full attack-path queries

This makes the project more realistic from a cybersecurity analysis perspective.
