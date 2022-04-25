from SPARQLWrapper import SPARQLWrapper


# iri = "<http://purl.obolibrary.org/obo/IAO_0000136>"
iri = "<http://www.w3.org/ns/dcat#accessURL>"

TEST_QUERY = """
SELECT  ?p ?o
FROM  <https://www.w3.org/ns/dcat2.ttl>
WHERE {
  <http://www.w3.org/ns/dcat#accessURL> ?p ?o
}
"""

query_string = """
CONSTRUCT {{ {0} ?p ?o }}
WHERE {{
    {0} ?p ?o.
}}
""".format(iri)


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

if len(sparql_results_triples) == 0:
    print(" No query result")

else:
    for s, p, o in sparql_results_triples:
        print(s, p, o)