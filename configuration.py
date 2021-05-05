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
DataFile = "data/test1.ttl"
# DataFile = "data/test2.ttl"
# DataFile = "data/addison_test2.ttl"
# DataFile = "http://ldp.cbgp.upm.es:8890/DAV/home/ejp/PERSONS_DEMO/person1"


# NAME = "Test1"
# NAME = "Test2"
NAME = "addison_test2"
# NAME = "remote1"

UserFeedBack = ""




