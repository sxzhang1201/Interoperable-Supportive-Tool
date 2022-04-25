"""
This script defines two functions: one for executing SPARQL query, another for generating SPARQL query
"""

from SPARQLWrapper import SPARQLWrapper
from configuration import EndPoint


def generate_query_string(iri, query_pattern=None):
    """
    To generate IRI-dependent SPARQL query string.
    :param query_pattern: String, indicating which pre-defined query strings to be used. These types are supported:
    "type_triple": to construct triples with the given IRI as the subject and the rdf:type as the predicate;
    (To be expanded)
    :param iri: String, describing an IRI in n3 format, i.e., "<IRI>".
    :return: A long string to be executed by SPARQL endpoint.
    """

    # The query that constructs ALL triples whose subjects are the given IRI
    query_string = """
    CONSTRUCT {{ {0} ?p ?o }}
    WHERE {{
        {0} ?p ?o.
    }}
    """.format(iri)

    if query_pattern == "type_triple":
        query_string = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        CONSTRUCT {{ {0} rdf:type ?o}}
        WHERE {{
            {0} rdf:type ?o.
        }}
        """.format(iri)

    return query_string


def run_sparql_query(query_string):
    """
    To construct queried triples based on the SPARQL query results
    :param endpoint: String, indicating which SPARQL endpoint is used to execute SPARQL query.
    :param query_string: string, the query to be executed by SPARQL endpoint.
    :return: An rdflib "QueryResult" object that containing queried triples
    """

    api_key = "f52df424-a6c1-40ce-a656-580eb3b5e3bf"

    # Initiate SPARQL Wrapper class
    sparql_ontobee = SPARQLWrapper("http://sparql.hegroup.org/sparql/")
    sparql_bioportal = SPARQLWrapper("http://sparql.bioontology.org/sparql/")

    sparql_bioportal.addCustomParameter("apikey", api_key)

    # Input SPARQL query string
    sparql_ontobee.setQuery(query_string)
    sparql_bioportal.setQuery(query_string)

    # Get SPARQL results, and construct them in RDF format
    sparql_ontobee_result = sparql_ontobee.query().convert()
    sparql_bioportal_result = sparql_bioportal.query().convert()

    sparql_results_triples = sparql_ontobee_result + sparql_bioportal_result

    return sparql_results_triples


if __name__ == '__main__':
    query_string = generate_query_string('<http://purl.obolibrary.org/obo/NCBITaxon_10088>')
    sparql_results_triples = run_sparql_query(EndPoint, query_string)

    print(query_string)
    print(len(sparql_results_triples))

    for s, p, o in sparql_results_triples:
        print(s, p, o)


