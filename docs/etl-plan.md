# ETL Plan

## 1. Goal

The goal of this project is to take cybersecurity data from a CSV file and prepare it for use with SPARQL. To do that, the data needs to be transformed into RDF triples and loaded into an RDF graph.

## 2. Extract

Extract means reading the CSV file and ingesting the data. In this project, Python will be used to open the file and read each row of data.

## 3. Transform

After the CSV file is read, each row will be processed one at a time. The values from each row will be matched to the correct column names, such as asset name, vulnerability ID, MITRE technique, and threat actor.

During the transform step, selected CSV values will be converted into RDF triples. Each triple will have a subject, predicate, and object.

For example, one row may be transformed into these triples:

- Asset hasVulnerability Vulnerability
- Vulnerability mapsToTechnique MITRETechnique
- Vulnerability isExploitedBy ThreatActor

## 4. Load

After the data is transformed into triples, the triples will be loaded into an RDF graph. The RDF graph will store the relationships between the different cybersecurity entities, such as assets, vulnerabilities, threat actors, and MITRE techniques.

## 5. Example ETL Flow

1. Extract Row: production-web-server-0229, VULN-9100D75C, T1071, FIN7
2. Parse Row:
production-web-server-0229
VULN-9100D75C
T1071
FIN7
3. Create Triples
production-web-server-0229 hasVulnerability VULN-9100D75C
VULN-9100D75C mapsToTechnique T1071
VULN-9100D75C isExploitedBy FIN7
4. Load into graph