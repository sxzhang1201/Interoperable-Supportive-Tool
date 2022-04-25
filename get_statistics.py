from rdflib.graph import Graph
from rdflib.term import URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, DC
import pickle


def count_rdf_components(g, term_type):
    """
    Count each RDF component.
    :param g:
    :param term_type: rdflib.term: URIRef, Literal, or BNode
    :return:
    """

    count_list = []

    for s, p, o in g:
        if isinstance(s, term_type):
            count_list.append(s)
        if isinstance(p, term_type):
            count_list.append(p)
        if isinstance(o, term_type):
            count_list.append(o)

    count_list = list(set(count_list))

    return count_list


if __name__ == '__main__':

    # dataFile = "data/ontologies.ttl"
    # dataFile = "data/bfo.owl"
    dataFile = "data/cido.owl"

    # with (open("pickles/cido/class_list_200.pickle", "rb")) as openfile:
    #     uri_not_200 = pickle.load(openfile)
    #
    # for i in uri_not_200:
    #     print(i)


    with (open("pickles/cido/cido_graph.pickle", "rb")) as openfile:
        g = pickle.load(openfile)

    temp_list = count_rdf_components(g, URIRef)

    for i in temp_list:
        print(i)

    print(len(temp_list))

    temp_list = list(set(temp_list))

    print(len(temp_list))


    quit()
    with (open("pickles/cido/class_list.pickle", "rb")) as openfile:
        type_object_list = pickle.load(openfile)

    with (open("pickles/cido/predicate_list.pickle", "rb")) as openfile:
        predicate__list = pickle.load(openfile)

    print(len(type_object_list))
    print(len(predicate__list))

    type_object_list = list(set(type_object_list))
    predicate__list = list(set(predicate__list))

    print(type_object_list)

    print(len(type_object_list))
    print(len(predicate__list))

    quit()

    # count_rdf_components(g, BNode)

    # g_type_subset = Graph()
    # g_type_subset += g.triples((None, DC.description, None))
    #
    # print(len(g_type_subset))

    g_type_subset = Graph()
    g_type_subset += g.triples((None, RDF.type, None))
    # g_type_subset += g.triples((None, RDFS.subClassOf, None))

    g_type_subset = list(set(g_type_subset))

    # Get a list of "classes"!
    type_object_list = []

    print(len(g_type_subset))
    for s, p, o in g_type_subset:
        # print(s, p, o)
        if not isinstance(o, BNode):
            type_object_list.append(o)

    print("Object")
    type_object_list = list(set(type_object_list))
    print(len(type_object_list))
    print(type_object_list)

    # Get a list of "properties"!
    predicate__list = []
    g_other_triples = g - g_type_subset

    for s, p, o in g_other_triples:
        # print(s, p, o)
        predicate__list.append(p)
    print("Predicate")
    predicate__list = list(set(predicate__list))
    print(len(predicate__list))
    print(predicate__list)

    quit()

    pickle.dump(type_object_list, open("pickles/cido/class_list.pickle", "wb"))
    pickle.dump(predicate__list, open("pickles/cido/predicate_list.pickle", "wb"))




