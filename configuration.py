"""
In this file, key parameters are specified, including:
"(Local or Remote)File": path-based or URI-based string, indicating the location of target RDF data;
"GraphFormat": string, indicating the serialization format of the RDF data;
"EndPoint": URI-based string, indicating the SPARQL endpoint;
Vocabularies: path-based strings, indicating the relative paths of each vocabulary
"""
# The representation format of the file
GraphFormat = 'turtle'

# The Ontobee SPARQL endpoint
EndPoint = "http://sparql.hegroup.org/sparql/"

# The RDF graphs to be validated
DataFile = "data/addison_dataset.ttl"

# String for naming a file
NAME = "addison_dataset"
# NAME = "remote1"

# String of user feedback
UserFeedBack = ""




