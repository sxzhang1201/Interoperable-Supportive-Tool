import pickle
from rdflib.graph import Graph
import urllib
from rdflib.plugins.parsers import notation3
from SPARQLWrapper import SPARQLWrapper
from rdflib.namespace import RDF, RDFS, DC
from query import generate_query_string, run_sparql_query
from rdflib.term import Literal, URIRef
from basic_func import graph_subset
from get_statistics import count_rdf_components


def group_predicate_by_availability(pred_list):
    list_200 = []
    list_not_200 = []

    # Identify Predicates that are not available
    for item in pred_list:
        if "http://evs.nci.nih.gov/ftp1/NDF-RT/NDF-RT.owl#" in item:
            print("Continue and Pass")
            continue

        try:
            print(str(item))
            status_code = urllib.request.urlopen(str(item)).getcode()

            if status_code == 200:
                list_200.append(item)

        except Exception as e:
            # Note that 404: Not Found, 400: Server Error, ...
            list_not_200.append(item)
            print(e)

    print(len(list_200))
    print(len(list_not_200))

    # pickle.dump(list_200, open("pickles/cido/class_list_200.pickle", "wb"))
    # pickle.dump(list_not_200, open("pickles/cido/class_list_not_200.pickle", "wb"))

    pickle.dump(list_200, open("pickles/cido/other_uris_list_200.pickle", "wb"))
    pickle.dump(list_not_200, open("pickles/cido/other_uris_list_not_200.pickle", "wb"))


def group_predicate_by_type(pre_list):
    objectProperty_list = []
    dataTypeProperty_list = []

    # Obtain Information from Parser
    for item in pre_list:
        # print(item)
        if "http://evs.nci.nih.gov/ftp1/NDF-RT/NDF-RT.owl#" in item:
            print("Continue and Pass")
            continue
        dg = Graph()
        try:
            dg.parse(item)
            print("Parsed")

        except Exception as e:
            print(e)

        subset_graph = Graph()
        subset_graph += dg.triples((item, RDF.type, None))

        # print(len(subset_graph))

        for s, p, o in subset_graph:
            # print(s, p, o)
            if str(o) == "http://www.w3.org/2002/07/owl#ObjectProperty":
                # print(s, p, o)
                objectProperty_list.append(s)
            elif str(o) == "http://www.w3.org/2002/07/owl#DatatypeProperty":
                dataTypeProperty_list.append(s)
                # print(s, p, o)


    # Obtain Information from SPARQL
    for item in pre_list:
        # print(item)
        query_string = generate_query_string(iri=item.n3(), query_pattern="type_triple")

        sparql_results_triples = run_sparql_query(query_string)

        subset_query = Graph()
        subset_query += sparql_results_triples.triples((item, RDF.type, None))

        # print(len(subset_query))

        for s, p, o in subset_query:
            print(s, p, o)
            if str(o) == "http://www.w3.org/2002/07/owl#ObjectProperty":
                # print(s, p, o)
                objectProperty_list.append(s)
            elif str(o) == "http://www.w3.org/2002/07/owl#DatatypeProperty":
                dataTypeProperty_list.append(s)
                # print(s, p, o)
            print(" ")


    objectProperty_list = list(set(objectProperty_list))
    print(len(objectProperty_list))

    print(objectProperty_list)

    print(len(dataTypeProperty_list))
    print(dataTypeProperty_list)

    pickle.dump(objectProperty_list, open("pickles/cido/object_predicate_list_200.pickle", "wb"))
    pickle.dump(dataTypeProperty_list, open("pickles/cido/datatype_predicate_list_200.pickle", "wb"))


def test_object_property(g, object_property_list, component_type):
    """

    :param g:
    :param object_property_list:
    :param component_type: Literal (if object property list) or URIRef (if datatype property list)
    :return:
    """

    object_property_failure_case = []

    for object_property_lib in object_property_list:

        print(object_property_lib)

        dg = Graph()

        dg += g.triples((None, object_property_lib, None))

        count = 0

        for s, p, o in dg:

            if isinstance(o, component_type):
                print(s, p, o)
                object_property_failure_case.append((s, p, o))

                count += 1

        print(count)


def test_for_OBO_foundry():

    # Load
    with (open("pickles/components/class_list.pickle", "rb")) as openfile:
        type_object_list = pickle.load(openfile)

    with (open("pickles/components/predicate_list.pickle", "rb")) as openfile:
        predicate_list = pickle.load(openfile)

    with (open("pickles/components/predicate_list_200.pickle", "rb")) as openfile:
        list_200 = pickle.load(openfile)

    with (open("pickles/components/predicate_list_not_200.pickle", "rb")) as openfile:
        list_not_200 = pickle.load(openfile)

    with (open("pickles/components/object_predicate_list_200.pickle", "rb")) as openfile:
        objectProperty_list = pickle.load(openfile)

    with (open("pickles/components/datatype_predicate_list_200.pickle", "rb")) as openfile:
        dataTypeProperty_list = pickle.load(openfile)

    print(len(list_not_200))

    print(len(list_200))

    for item in list_not_200:
        print(str(item))

    quit()

    g = Graph()

    # g.parse("data/ontologies.ttl", format='turtle')

    g.parse("data/bfo.owl")

    for s, p, o in g:
        print(s, p, o)
    print(len(g))

    # test_object_property(g, objectProperty_list, Literal)


def check_for_bfo():
    with (open("pickles/bfo/class_list.pickle", "rb")) as openfile:
        type_object_list = pickle.load(openfile)

    with (open("pickles/bfo/predicate_list.pickle", "rb")) as openfile:
        predicate_list = pickle.load(openfile)

    with (open("pickles/bfo/predicate_list_200.pickle", "rb")) as openfile:
        list_200 = pickle.load(openfile)

    with (open("pickles/bfo/predicate_list_not_200.pickle", "rb")) as openfile:
        list_not_200 = pickle.load(openfile)

    with (open("pickles/bfo/object_predicate_list_200.pickle", "rb")) as openfile:
        objectProperty_list = pickle.load(openfile)

    with (open("pickles/bfo/datatype_predicate_list_200.pickle", "rb")) as openfile:
        dataTypeProperty_list = pickle.load(openfile)

    print(len(list_200))

    print(objectProperty_list)
    print(len(objectProperty_list))

    print(dataTypeProperty_list)
    print(len(dataTypeProperty_list))

    g = Graph()

    g.parse("data/bfo.owl")

    test_object_property(g, objectProperty_list, Literal)
    test_object_property(g, dataTypeProperty_list, URIRef)


def check_availability_for_bfo():
    g = Graph()

    g.parse("data/bfo.owl")

    uri_list = []

    fail_list = []

    for s, p, o in g:
        if isinstance(s, URIRef):
            uri_list.append(s)
        if isinstance(p, URIRef):
            uri_list.append(p)
        if isinstance(o, URIRef):
            uri_list.append(o)

    uri_list = list(set(uri_list))

    for item in uri_list:
        try:
            # print(str(item))
            status_code = urllib.request.urlopen(str(item)).getcode()

            if status_code == 200:
                pass

        except Exception as e:
            # Note that 404: Not Found, 400: Server Error, ...
            fail_list.append(str(item))
            print(str(item))
            # print(e)

    print(len(fail_list))


if __name__ == '__main__':

    with (open("pickles/cido/cido_graph.pickle", "rb")) as openfile:
        cido_graph = pickle.load(openfile)

    with (open("pickles/cido/predicate_list.pickle", "rb")) as openfile:
        cido_pre_list = pickle.load(openfile)

    with (open("pickles/cido/object_predicate_list_200.pickle", "rb")) as openfile:
        cido_pre_object_list = pickle.load(openfile)

    with (open("pickles/cido/datatype_predicate_list_200.pickle", "rb")) as openfile:
        cido_pre_datatype_list = pickle.load(openfile)

    # with (open("pickles/cido/class_list.pickle", "rb")) as openfile:
    #     cido_class_list = pickle.load(openfile)

    with (open("pickles/cido/class_list_200.pickle", "rb")) as openfile:
        cido_200_class_list = pickle.load(openfile)

    # with (open("pickles/cido/class_list_not_200.pickle", "rb")) as openfile:
    #     cido_not_200_class_list = pickle.load(openfile)

    # # Misplaced classes
    # misplaced_class_list = []
    #
    # for class_item in cido_200_class_list:
    #     g_type_subset = Graph()
    #     g_type_subset += cido_graph.triples((None, class_item, None))
    #     if len(g_type_subset) != 0:
    #         print(class_item)
    #         misplaced_class_list.append(class_item)
    # print(misplaced_class_list)


    Test_Pre = URIRef("http://purl.org/dc/terms/contributor")

    g_type_subset = Graph()
    # g_type_subset += cido_graph.triples((None, RDFS.label, None))
    g_type_subset += cido_graph.triples((None, Test_Pre, None))

    print(len(g_type_subset))




    # group_predicate_by_availability(cido_class_list)

    # uri_list = count_rdf_components(cido_graph, URIRef)

    # Get URIs except classes and predicates
    # test_uri = list(set(list(set(uri_list) - set(cido_class_list))) - set(cido_pre_list))



    quit()

    group_predicate_by_availability(test_uri)

    quit()

    test_object_property(cido_graph, cido_pre_datatype_list, URIRef)
    # test_object_property(cido_graph, cido_pre_object_list, Literal)


    quit()

    group_predicate_by_availability(cido_pre_list)





    # test_for_OBO_foundry()
    object_property_list = [URIRef("http://rdfs.org/ns/void#exampleResource"),
                            URIRef("http://rdf-vocabulary.ddialliance.org/discovery#fundedBy")]

    g = Graph()

    # g.parse("data/ontologies.ttl", format='turtle')
    g.parse("data/bfo.owl")

    object_property_list = [URIRef("http://xmlns.com/foaf/0.1/mbox"),
                            URIRef("http://xmlns.com/foaf/0.1/homepage"),
                            URIRef("http://www.w3.org/2000/01/rdf-schema#isDefinedBy"),
                            URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso")]

    datatype_property_list = [URIRef("http://purl.obolibrary.org/obo/IAO_0000112"),
                                URIRef("http://purl.obolibrary.org/obo/IAO_0000115"),
                                URIRef("http://purl.obolibrary.org/obo/IAO_0000119"),
                                URIRef("http://purl.obolibrary.org/obo/IAO_0000116"),
                                URIRef("http://purl.obolibrary.org/obo/IAO_0000118")]

    test_object_property(g, datatype_property_list, URIRef)

