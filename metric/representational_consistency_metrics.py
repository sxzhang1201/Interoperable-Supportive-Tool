from basic_func import select_used_terms, Measurement
from query import generate_query_string, run_sparql_query
import configuration
from knowledge_base import IFC


# Representational-consistency metric
def reuse_existing_terms_metric(g):

    print("Test Representational-consistency metrics. ")

    property_term_list, class_term_list = select_used_terms(g)
    # non_existing_properties = []
    # non_existing_classes = []
    non_existing_terms = []

    for property_term in property_term_list:
        query_string = generate_query_string(property_term)
        result_property = run_sparql_query(configuration.EndPoint, query_string)
        print("The query result for {}".format(property_term))
        print(len(result_property))
        if len(result_property) == 0:
            # non_existing_properties.append(property_term)
            non_existing_terms.append(property_term)

    for class_term in class_term_list:
        query_string = generate_query_string(class_term)
        result_class = run_sparql_query(configuration.EndPoint, query_string)
        print("The query result for {}".format(class_term))
        print(len(result_class))
        if len(result_class) == 0:
            # non_existing_classes.append(class_term)
            non_existing_terms.append(class_term)

    non_existing_terms = list(set(non_existing_terms))

    metric_measurement_reuse_existing_terms = Measurement(failure_case=IFC.NotUseExistingTerms,
                                                          result=non_existing_terms)

    return metric_measurement_reuse_existing_terms
