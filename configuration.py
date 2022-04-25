"""
In this file, key parameters are specified, including:
"(Local or Remote)File": path-based or URI-based string, indicating the location of target RDF data;
"GraphFormat": string, indicating the serialization format of the RDF data;
"EndPoint": URI-based string, indicating the SPARQL endpoint;
Vocabularies: path-based strings, indicating the relative paths of each vocabulary
"""
# The representation format of the file
GraphFormat = 'turtle'

EndPoint = ""

# The RDF graphs to be validated
DataFile = "data/ontologies.ttl"
# DataFile = "data/owl_test3.ttl"
# DataFile = "data/test1.ttl"

# String for naming a file
NAME = "ontologies"
# NAME = "owl_test"
# DataFile = "data/test1.ttl"

# String of user feedback
UserFeedBack = ""




