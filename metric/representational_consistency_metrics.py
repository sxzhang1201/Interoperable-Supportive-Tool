from basic_func import select_used_terms, Measurement
from query import generate_query_string, run_sparql_query
from rdflib.graph import Graph
from rdflib import URIRef
from knowledge_base import IFC


# def compare_parser_format(iri):
#     g = Graph()
#     max_index = 0
#
#     for i in range(len(configuration.FormatList)):
#
#         print(configuration.FormatList[i])
#
#         dg = Graph()
#
#         try:
#             dg.parse(iri, format=configuration.FormatList[i])
#
#         except Exception as e:
#             print(e)
#
#         if len(dg) > max_index:
#             max_index = i
#
#     best_format = configuration.FormatList[max_index]
#
#     g.parse(iri, format=best_format)
#
#     # return g, best_format
#     return g


# Representational-consistency metric
def reuse_existing_terms_metric(g):

    print("Test Representational-consistency metric. ")

    property_term_list, class_term_list = select_used_terms(g)
    # non_existing_properties = []
    # non_existing_classes = []
    non_existing_terms = []

    for property_term in property_term_list:

        print(property_term)

        dg = Graph()

        try:
            dg.parse(property_term)

        except Exception as e:
            print(e)

        g_subset = Graph()
        g_subset += dg.triples((URIRef(property_term), None, None))

        if len(g_subset) == 0:
            non_existing_terms.append(property_term)


    for class_term in class_term_list:

        print(class_term)

        dg = Graph()

        try:
            dg.parse(class_term)

        except Exception as e:
            print(e)

        g_subset = Graph()
        g_subset += dg.triples((URIRef(class_term), None, None))

        if len(g_subset) == 0:
            non_existing_terms.append(class_term)

        # query_string = generate_query_string(class_term)
        # result_class = run_sparql_query(configuration.EndPoint, query_string)
        # print("The query result for {}".format(class_term))
        # print(len(result_class))
        # if len(result_class) == 0:
        #     # non_existing_classes.append(class_term)
        #     non_existing_terms.append(class_term)

    # Remove duplicates
    non_existing_terms = list(set(non_existing_terms))

    metric_measurement_reuse_existing_terms = Measurement(failure_case=IFC.NotUseExistingTerms,
                                                          result=non_existing_terms)

    print(non_existing_terms)

    return metric_measurement_reuse_existing_terms
