from rdflib.namespace import RDF, RDFS
from rdflib.graph import Graph
from knowledge_base import FailureCase
from rdflib.term import Literal, URIRef


class Measurement:
    def __init__(self, failure_case, result):
        self.failure_case = failure_case
        self.result = result


def graph_subset(g, property_filter):
    """
    Divide a given graph into 1) a type-triples only graph and 2) a no-type-triples graph.
    :param g: rdflib.graph object
    :param property_filter: URI-based string, indicating which property to filter the graph
    :return: two rdflib.graph objects
    """
    # Type Triples
    g_property_triples = Graph()
    g_property_triples += g.triples((None, property_filter, None))

    # Non-type Triples
    g_no_property_triples = g - g_property_triples

    return g_property_triples, g_no_property_triples


def get_case_info(failure_case_iri, property_iri):
    """
    Query information of triples from "Failure Case Vocabulary"
    :param failure_case_iri: URI-based string, target subject IRI
    :param property_iri: URI-based string, property IRI
    :return: Any triple object
    """
    g = Graph()

    # Load failure case vocabulary
    g.parse(FailureCase, format='turtle')

    # Get relevant information from a given failure case
    for _, _, o in g.triples((URIRef(failure_case_iri), property_iri, None)):

        return o


def select_used_terms(g):
    """
    Select terms that are used in the given RDF graph, including 1)non-type properties
    and 2) rdf:type/rdfs:subClassOf triples' objects
    :param g: rdflib.graph object
    :return: two lists of URIs (n3 format), respectively including property terms and class terms.
    """
    g_type_triples, g_no_type_triples = graph_subset(g, RDF.type)
    g_subclass_triples, _ = graph_subset(g, RDFS.subClassOf)

    property_term_list = []
    class_term_list = []

    for _, p, _ in g_no_type_triples:
        property_term_list.append(p)

    for _, _, o in g_type_triples:
        class_term_list.append(o)

    for _, _, o in g_subclass_triples:
        class_term_list.append(o)

    property_term_list = list(set(property_term_list))
    class_term_list = list(set(class_term_list))

    return property_term_list, class_term_list





