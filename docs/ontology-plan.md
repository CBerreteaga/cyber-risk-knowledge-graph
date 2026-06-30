# Ontology Plan

## 1. Project Goal

The goal of this project is to practice the ETL process by taking cybersecurity data from a CSV file, transforming the data into RDF triples, and loading those triples into an RDF graph. After the graph is created, SPARQL queries are used to identify relationships between assets, findings, vulnerabilities, threat actors, and MITRE ATT&CK techniques.

## 2. Version 1 Scope

Version 1 focuses on a small set of core cybersecurity classes so the first RDF graph stays simple and manageable while still supporting risk-based analysis.

The classes for Version 1 are:

1. Asset
2. Finding
3. Vulnerability
4. ThreatActor
5. MITRETechnique

The `Finding` class was added so that risk values such as risk score, likelihood, impact, patch availability, and exploit availability are tied to a specific cybersecurity record instead of being attached directly to a vulnerability.

## 3. Classes

### Asset

Represents a system, application, server, workstation, database, API gateway, or other technology asset.

### Finding

Represents a specific cybersecurity risk record from the dataset. A finding connects an asset to a vulnerability and stores risk-related values.

### Vulnerability

Represents a known weakness or vulnerability that may affect one or more findings.

### ThreatActor

Represents a threat actor or actor category that may exploit a vulnerability.

### MITRETechnique

Represents a MITRE ATT&CK technique associated with a vulnerability.

## 4. Relationships

The main relationship pattern is:

```text
Asset hasFinding Finding
Finding hasVulnerability Vulnerability
Vulnerability mapsToTechnique MITRETechnique
Vulnerability isExploitedBy ThreatActor
```

This creates the following graph path:

```text
Asset → Finding → Vulnerability → MITRE Technique
Asset → Finding → Vulnerability → Threat Actor
```

## 5. Properties

### Asset Properties

1. Asset Name
2. Asset Type

RDF predicate used:

```text
cyber:assetType
```

### Finding Properties

1. Risk Score
2. Likelihood
3. Impact
4. Patch Available
5. Exploit Available

RDF predicates used:

```text
cyber:riskScore
cyber:likelihood
cyber:impact
cyber:patchAvailable
cyber:exploitAvailable
```

### Vulnerability Properties

1. Vulnerability ID
2. Vulnerability Name
3. Vulnerability Description
4. Severity

RDF predicate used:

```text
cyber:severity
```

### ThreatActor Properties

1. Threat Actor Name
2. Motivation
3. Category

RDF predicate used:

```text
cyber:actorCategory
```

### MITRETechnique Properties

1. MITRE ID
2. MITRE Technique
3. MITRE Tactic

RDF predicate used:

```text
cyber:mitreTactic
```

## 6. RDF Types and Labels

The ETL adds `rdf:type` triples to classify each node.

Examples:

```turtle
cyber:production-web-server-0229 a cyber:Asset .
cyber:FINDING-0001 a cyber:Finding .
cyber:VULN-9100D75C a cyber:Vulnerability .
cyber:T1071 a cyber:MITRETechnique .
cyber:FIN7 a cyber:ThreatActor .
```

The ETL also adds `rdfs:label` triples to provide readable labels for graph nodes.

Examples:

```turtle
cyber:VULN-9100D75C rdfs:label "Example Vulnerability" .
cyber:T1071 rdfs:label "Application Layer Protocol" .
```

## 7. Example Triple Story

One CSV record can become a graph path like this:

```text
production-web-server-0229 hasFinding FINDING-0001
FINDING-0001 hasVulnerability VULN-9100D75C
FINDING-0001 riskScore "95"
FINDING-0001 patchAvailable "False"
FINDING-0001 exploitAvailable "True"
VULN-9100D75C mapsToTechnique T1071
VULN-9100D75C isExploitedBy FIN7
```

## 8. SPARQL Questions

The main SPARQL questions for this version are:

1. Which assets have high-risk findings?
2. Which findings are exploitable and have no patch available?
3. Which findings connect assets, vulnerabilities, MITRE techniques, and threat actors?

These questions are more useful than simple relationship checks because they focus on cyber risk prioritization.
