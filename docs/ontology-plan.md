# Ontology Plan

## 1. Project Goal

The goal of this project is to practice the ETL process by taking cybersecurity data from a CSV file, transforming the data into RDF triples, and loading those triples into an RDF graph. After the graph is created, I will write SPARQL queries to identify relationships between assets, vulnerabilities, threat actors, and MITRE techniques.

## 2. Version 1 Scope

Version 1 of this project will focus on a small set of core cybersecurity classes so the first RDF graph stays simple and manageable.

The classes for Version 1 are:

1. Asset
2. Vulnerability
3. ThreatActor
4. MITRETechnique

I am intentionally keeping the first version limited so I can focus on understanding the full workflow: CSV data → ETL → RDF triples → RDF graph → SPARQL queries.

## 3. Classes

1. Asset
2. Vulnerability
3. ThreatActor
4. MITRETechnique

## 4. Relationships

Asset hasVulnerability Vulnerability
Vulnerability mapsToTechnique MITRETechnique
Vulnerability isExploitedBy ThreatActor

## 5. Properties

### Asset Properties
1. Asset ID
2. Asset Name
3. Asset Type

### Vulnerability Properties

1. Vulnerability ID
2. Vulnerability Name
3. Vulnerability Description
4. Severity
5. Patch Available

### ThreatActor Properties
1. Threat Actor Name
2. Motivation
3. Category

### MITRETechnique Properties
1. MITRE ID
2. MITRE Technique
3. MITRE Tactic

## 6. Example Triple Story

Asset hasVulnerability Vulnerability
Vulnerability mapsToTechnique MITRETechnique
Vulnerability isExploitedBy ThreatActor

production-web-server-0229 hasVulnerability VULN-9100D75C
VULN-9100D75C mapsToTechnique T1071
VULN-9100D75C isExploitedBy FIN7

## 7. SPARQL Questions
1. Which assets have a specific vulnerability?
2. What MITRE Technique does a specific vulnerability map to?
3. Which threat actors exploit a specific vulnerability?

