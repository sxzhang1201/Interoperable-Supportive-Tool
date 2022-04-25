"""
This script defines a function that parses an RDF graph either from a local file or a remote URI.
"""

import os.path
from rdflib.graph import Graph


def parse_local_graph(file_path, graph_format):
    """
    This function imports a file that should contain RDF graphs, parse them, and return parsed RDF graphs.

    :param file_path: String, describing the path of the imported file
    :param graph_format: String,used if format can not be determined from source. Defaults to rdf/xml.
    Format support can be extended with plugins, but 'xml', 'n3', 'nt', 'trix', 'rdfa' are built in.
    :return: An rdflib.graph object
    """

    # Initiate an empty graph
    g = Graph()

    print("Load local data file:")

    # Check 1) if the file exists and 2) if RDF graphs in that file is parsable
    if os.path.exists(file_path):
        try:
            g.parse(file_path, format=graph_format)
        except:
            raise Exception("The file {} cannot be parsed into RDF triples due to syntactical errors. ".format(file_path))
    else:
        raise OSError("The file {} is not found. ".format(file_path))

    print("An RDF dataset is successfully loaded and parsed!")

    return g


def parse_remote_graph(graph_uri, graph_format):
    """
    The function parse RDF graph from a remote URI.
    :param graph_uri: string, Unique Resource identifier (URI)
    :param graph_format: String, used if format can not be determined from source. Defaults to rdf/xml.
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


def parse_graph(graph_source, graph_format):
    """
    The function parses RDF graph either from a local RDF data or an URI.

    :param local_or_remote: string, either "local" or "remote"
    :param graph_source: string, either local path or URI
    :param graph_format: String,used if format can not be determined from source. Defaults to rdf/xml.
    Format support can be extended with plugins, but 'xml', 'n3', 'nt', 'trix', 'rdfa' are built in.
    :return: An rdflib.graph object
    """

    if "http" in graph_source:
        g = parse_remote_graph(graph_source, graph_format)
    else:
        g = parse_local_graph(graph_source, graph_format)

    return g
