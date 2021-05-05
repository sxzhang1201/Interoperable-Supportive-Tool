from rdflib import Namespace
import configuration
from rdflib.namespace import RDFS, SKOS


# Existing Ontology (To be used for RDF graph generation)
DQV = Namespace("http://www.w3.org/ns/dqv#")
EVAL = Namespace("http://purl.org/net/EvaluationResult#")
LDQ = Namespace("http://linkeddata3.dia.fi.upm.es/ldq#")
SIO = Namespace("http://semanticscience.org/resource/")
OBO = Namespace("http://purl.obolibrary.org/obo/")
DCT = Namespace("http://purl.org/dc/terms/")

# IRIs for test data and evaluation report
DATA = Namespace(configuration.DataFile)
REPORT = Namespace("purl.org/ist/report/")

# Newly-developed ontology
IFC = Namespace("http://purl.org/ifc#")
PROB = Namespace("http://www.diachron-fp7.eu/dqm-prob#")

# URIs of Vocabularies
KeyPoint = "vocab/interoperability-key-point.ttl"
QualityDimension = "vocab/interoperability-quality-dimension.ttl"
QualityMetric = "vocab/interoperability-quality-metric.ttl"
FailureCase = "vocab/interoperability-failure-case.ttl"

# A list of Property Classes
property_list = [
    "<http://www.w3.org/2002/07/owl#ObjectProperty>",
    "<http://www.w3.org/2002/07/owl#FunctionalProperty>",
    "<http://www.w3.org/2002/07/owl#DatatypeProperty>",
    "<http://www.w3.org/2002/07/owl#ObjectProperty>"
]

PropertyForDefinition = [RDFS.isDefinedBy, RDFS.comment, SKOS.definition, DCT.description]
