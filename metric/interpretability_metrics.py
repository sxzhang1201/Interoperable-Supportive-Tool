from basic_func import Measurement
from rdflib.term import BNode
from knowledge_base import IFC


def no_blank_node_metric(g):

    blank_node_list = []

    for s, p, o in g:
        if isinstance(s, BNode) | isinstance(o, BNode):
            blank_node_list.append((s, p, o))

    blank_node_measure = Measurement(failure_case=IFC.BlankNodeForMissingValues,
                                     result=blank_node_list)

    return blank_node_measure


def ambiguous_annotation_metric(g):
    pass


def run_interpretability_assessment(g):
    blank_node_measure = no_blank_node_metric(g)
    ambiguous_annotation_metric(g)

    return blank_node_measure

