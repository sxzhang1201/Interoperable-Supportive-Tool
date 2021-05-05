import configuration, knowledge_base
from basic_func import graph_subset, Measurement, select_used_terms
from rdflib.term import Literal, URIRef
from query import generate_query_string, run_sparql_query
from rdflib.graph import Graph
from knowledge_base import IFC, PROB, DCT
from rdflib.namespace import RDF, RDFS, SKOS


def misplaced_classes_or_properties_metric(g, class_or_property):
    """
    Classes are defined as owl:Class. They should  be used as subject or object of a triple.
    Properties are defined as rdf:Property, owl:ObjectProperty, owl:DatatypeProperty, or owl:FunctionalProperty.
    They should be used as the predicates of triples.
    :param graph: rdflib graph object;
    :param class_or_property: string, either "class" or "property" indicating which element to be tested.
    :return:
    """

    # Initiate output dictionary
    failure_case_dict = {}

    # Obtain two subsets of graphs: one with rdf:type triples and one without rdf:type triples
    g_type_triples, g_no_type_triples = graph_subset(g, RDF.type)

    # Options to be decided which subset of RDF graph should be tested
    graph_options = {
        # Classes are usually used as the object of a rdf:type triple, so only examine rdf:type triples.
        "class": g_type_triples,
        # Examine predicates of non-rdf:type triples
        "property": g_no_type_triples}

    # Iterate each triple in the selected RDF graph
    for subj, pre, obj in graph_options[class_or_property]:
        subj_iri = subj.n3()
        pre_iri = pre.n3()
        obj_iri = obj.n3()

        # Options of IRIs to be tested, which depends on the variable "class_or_property"
        iri_options = {
            "class": obj_iri,
            "property": pre_iri}

        # Decide which IRI to be queried
        test_iri = iri_options[class_or_property]

        # Get SPARQL query strings
        query_string = generate_query_string(iri=test_iri, query_pattern="type_triple")

        # Run query, and get query results
        sparql_results = run_sparql_query(configuration.EndPoint, query_string)

        if len(sparql_results) == 0:
            print("The query information of the IRI {} is not found. ".format(test_iri))

        else:
            # Iterate each triple in the query result
            for _, _, o in sparql_results:

                o_iri = o.n3()

                # To test if the test IRI is a "class", the "o" should be owl:Class
                if class_or_property == "class":
                    if o_iri == "<http://www.w3.org/2002/07/owl#Class>":
                        print(" The class {} is correctly used as the object. ".format(test_iri))

                    elif o_iri in knowledge_base.property_list:
                        failure_case_dict[test_iri] = (subj_iri, pre_iri, obj_iri)
                        print(" The property {} should not be used as the object of a triple. ".format(test_iri))
                    else:
                        # !Q: cannot identify IRIs that return no query results from that endpoint!!!!!
                        print(" The linked resource {} is not defined as the owl:Class, please check. ".format(test_iri))

                # To test if the predicate IRI is a "property", the "o" should be any of "corpus.property_list"
                elif class_or_property == "property":
                    if o_iri == "<http://www.w3.org/2002/07/owl#Class>":
                        failure_case_dict[test_iri] = (subj_iri, pre_iri, obj_iri)
                        print(" The class {} is incorrectly used as the predicate. ".format(test_iri))

                    elif o_iri in knowledge_base.property_list:
                        print(" The property {} is correctly used as the predicate of a triple. ".format(test_iri))

    failure_case_option = {
        "class": PROB.MisplacedProperty,
        "property": PROB.MisplacedClass
    }

    metric_measurement = Measurement(failure_case=failure_case_option[class_or_property],
                                     result=failure_case_dict)

    return metric_measurement


def misused_owl_datatype_or_object_properties_metric(g):

    # Obtain the subset graph without rdf:type triples
    _, g_no_type_triples = graph_subset(g, RDF.type)

    failed_datatype_property = {}
    failed_object_property = {}

    # Iterate each triple of the selected RDF graph
    for subj, pre, obj in g_no_type_triples:
        subj_iri = subj.n3()
        pre_iri = pre.n3()
        obj_iri = obj.n3()

        # set the predicate IRI as the test IRI
        test_iri = pre_iri

        # Get SPARQL query strings
        query_string = generate_query_string(iri=test_iri, query_pattern="type_triple")

        # Run query and return query results
        sparql_results = run_sparql_query(configuration.EndPoint, query_string)
        for _, _, property_type in sparql_results:
            # If the property is owl:ObjectProperty, the object of its triple should be IRI
            if property_type.n3() == "<http://www.w3.org/2002/07/owl#ObjectProperty>":
                if isinstance(obj, URIRef):
                    print("The object Property {} is correctly used for {}. ".format(pre_iri, obj_iri))
                else:
                    print("The object Property {} is incorrectly used because the object is not IRI. ".format(pre_iri))
                    failed_object_property[pre_iri] = (subj_iri, pre_iri, obj_iri)

            # If the property is owl:DatatypeProperty, the object of its triple should be literal
            elif property_type.n3() == "<http://www.w3.org/2002/07/owl#DatatypeProperty>":
                if isinstance(obj, Literal):
                    print("The datatype Property {} is correctly used for {}. ".format(pre_iri, obj_iri))
                else:
                    print("The datatype Property {} is incorrectly used because the object is not Literal. ".format(pre_iri))
                    failed_datatype_property[pre_iri] = (subj_iri, pre_iri, obj_iri)

    metric_measurement_datatype_pro = Measurement(failure_case=PROB.MisusedDatatypeProperty,
                                                  result=failed_datatype_property)
    metric_measurement_object_pro = Measurement(failure_case=PROB.MisusedObjectProperty,
                                                result=failed_object_property)

    return metric_measurement_datatype_pro, metric_measurement_object_pro


def entities_as_members_of_disjoint_classes_metric(g):
    g_type_triples, _ = graph_subset(g, RDF.type)

    print(len(g_type_triples))

    for s, _, o in g_type_triples:

        multiple_type_list = []

        # Identify all triples of one subject
        dg = Graph()
        dg += g_type_triples.triples((s, None, None))

        # If the subject has two more Classes
        if len(dg) >= 2:
            print(len(dg))


def undefined_classes_or_properties_metric(g):
    property_term_list, class_term_list = select_used_terms(g)

    undefined_property_list = []
    undefined_class_list = []

    for property_term in property_term_list:
        query_string = generate_query_string(property_term)
        query_result = run_sparql_query(configuration.EndPoint, query_string)

        definition_graph = Graph()

        for property_filter in knowledge_base.PropertyForDefinition:
            definition_graph += query_result.triples((None, property_filter, None))

        for s, p, o in definition_graph:
            print(s, p, o)

        if len(definition_graph) == 0:
            undefined_property_list.append(property_term)

    for class_term in class_term_list:
        query_string = generate_query_string(class_term)
        query_result = run_sparql_query(configuration.EndPoint, query_string)

        definition_graph = Graph()

        for property_filter in knowledge_base.PropertyForDefinition:
            definition_graph += query_result.triples((None, property_filter, None))

        if len(definition_graph) == 0:
            undefined_class_list.append(class_term)

        undefined_class_measure = Measurement(failure_case=PROB.UndefinedClass,
                                              result=undefined_class_list)
        undefined_property_measure = Measurement(failure_case=PROB.UndefinedProperty,
                                                 result=undefined_property_list)

        return undefined_class_measure, undefined_property_measure


def deprecated_classes_or_properties_metric(g):
    property_term_list, class_term_list = select_used_terms(g)


def ontology_hijack_metric(g):
    pass


def malformed_literal_metric(g):
    pass


def run_consistency_assessment(g):
    print("Test Consistency metrics. ")
    misplaced_class_measure = misplaced_classes_or_properties_metric(g, "class")
    misplaced_property_measure = misplaced_classes_or_properties_metric(g, "property")
    misused_datatype_property_measure, misused_object_property_measure = \
        misused_owl_datatype_or_object_properties_metric(g)

    return misplaced_class_measure, misplaced_property_measure, \
           misused_datatype_property_measure, misused_object_property_measure



