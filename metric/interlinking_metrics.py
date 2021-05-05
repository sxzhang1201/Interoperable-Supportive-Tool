from rdflib.namespace import OWL
from basic_func import get_case_info, graph_subset, Measurement
from knowledge_base import DCT, IFC


def same_as_metric(g):
    """

    :param g: rdflib graph object;
    :return: Either Measurement instance or "None". The Measurement instance includes two variables: "failure_case"
    and "result". The "result" contains the advice obtained directly from "Failure Case" vocabulary.
    """

    # "rdfs:label" Triples
    g_same_as_triples, _ = graph_subset(g, OWL.sameAs)

    if len(g_same_as_triples) == 0:
        same_as_advice = get_case_info(IFC.NoSameAsData, DCT.keyword)
        no_same_as_measure = Measurement(failure_case=IFC.NoSameAsData, result=same_as_advice)
    else:
        print("There following labels in the RDF dataset enhances understandability: ")
        for s, p, o in g_same_as_triples:
            print(s, p, o)
        no_same_as_measure = Measurement(failure_case=IFC.NoSameAsData, result=[])

    return no_same_as_measure


def back_and_forward_links_metric(g):
    pass


def run_interlinking_assessment(g):
    print("Test Interlinking metrics. ")
    no_same_as_measure = same_as_metric(g)
    back_and_forward_links_metric(g)

    return no_same_as_measure


