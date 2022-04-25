from rdflib.namespace import RDF, RDFS, SKOS, DCAT
from basic_func import get_case_info, graph_subset, Measurement
from knowledge_base import DQV, EVAL, LDQ, SIO, OBO, DCT, DATA, REPORT, PROB


def lack_of_human_readable_labelling_metric(g):
    """

    :param g: rdflib graph object;
    :return: Either Measurement instance or "None". The Measurement instance includes two variables: "failure_case"
    and "result". The "result" contains the advice obtained directly from "Failure Case" vocabulary.
    """

    # "rdfs:label" Triples
    g_label_triples, _ = graph_subset(g,      RDFS.label)
    g_comment_triples, _ = graph_subset(g,    RDFS.comment)
    g_pref_label_triples, _ = graph_subset(g, SKOS.prefLabel)

    if sum([len(g_label_triples), len(g_comment_triples), len(g_pref_label_triples)]) == 0:
        labelling_advice = get_case_info("http://www.diachron-fp7.eu/dqm-prob#NoHumanReadableLabel", DCAT.keyword)
        lack_of_labelling_measure = Measurement(failure_case=PROB.NoHumanReadableLabel, result=labelling_advice)

    else:
        print("There following labels in the RDF dataset enhances understandability: ")
        for s, p, o in g_label_triples:
            print(s, p, o)

        lack_of_labelling_measure = Measurement(failure_case=PROB.NoHumanReadableLabel, result=[])

    return lack_of_labelling_measure


def vocabulary_usage_indication_metric(g):
    pass


def run_understandability_assessment(g):
    print("Test Understandability metrics. ")
    lack_of_labelling_measure = lack_of_human_readable_labelling_metric(g)
    vocabulary_usage_indication_metric(g)

    return lack_of_labelling_measure


