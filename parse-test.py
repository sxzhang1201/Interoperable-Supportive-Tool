from rdflib.graph import Graph
from rdflib import URIRef
from rdflib.namespace import RDF, RDFS
from rdflib.plugin import register, Serializer, Parser


def parse_remote_graph(graph_uri, graph_format):
    """
    The function parse RDF graph from a remote URI.
    :param graph_uri: string, Unique Resource identifier (URI)
    :param graph_format: String,used if format can not be determined from source. Defaults to rdf/xml.
    Format support can be extended with plugins, but 'xml', 'n3', 'nt', 'trix', 'rdfa' are built in.
    :return:A n rdflib.graph object
    """
    # Initiate an empty graph
    g = Graph()

    print("Load remote data file:")

    # Parse remote RDF data from an URI resource
    try:
        g.parse(graph_uri, format=graph_format)
    except:
        raise Exception("The URI {} cannot be parsed into RDF triples. ".format(graph_uri))

    return g


if __name__ == '__main__':

    format_list = ["xml", "n3", "nt", "trix", "json-ld", "turtle"]

    test_iri = "http://www.w3.org/2003/g/data-view#"

    # test_iri = "http://purl.bioontology.org/ontology/SNOMEDCT/248153007"

    # test_iri = "http://rdf-vocabulary.ddialliance.org/discovery#fundedBy"

    # test_iri = "http://www.w3.org/ns/dcat#accessURL"

    # test_iri = "http://evs.nci.nih.gov/ftp1/NDF-RT/NDF-RT.owl#"

    # test_iri = "https://schema.org/logo"

    g = Graph()

    try:
        g.parse(test_iri)

    except Exception as e:
        print(e)

    print(len(g))

    for s, p, o in g:
        print("{} {} {} .".format(s, p, o))


    quit()
    g_subset = Graph()
    g_subset += g.triples((URIRef(test_iri), RDF.type, None))
    # g_subset += g.triples((URIRef(test_iri), None, None))

    print("---------------------------")

    print(len(g_subset))

    for s, p, o in g_subset:
        print(s, p, o)

