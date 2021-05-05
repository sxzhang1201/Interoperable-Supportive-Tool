from rdflib.graph import Graph
from knowledge_base import DQV, EVAL, LDQ, SIO, OBO, DCT, DATA, REPORT
from rdflib.namespace import RDF, XSD, PROV, SKOS, RDFS, OWL
from rdflib.term import Literal, URIRef
from datetime import datetime
from basic_func import get_case_info


def get_info_from_vocab(vocab, sub_iri_n3, prop_iri_n3):
    """


    :param vocab: any vocabulary library to be queried;
    :param sub_iri_n3: n3-format string, subject IRI;
    :param prop_iri_n3: n3-format string, property IRI;
    :return: Literal
    """

    g = Graph()
    g.parse(vocab, format='turtle')

    for _, _, o in g.triples((sub_iri_n3, prop_iri_n3, None)):

        return o


def generate_pre_report(naming, feedback):

    pre_report = Graph()

    pre_report.bind("dqv", "http://www.w3.org/ns/dqv#")
    pre_report.bind("eval", "http://purl.org/net/EvaluationResult#")

    # Set IRI for "Evaluation"
    BASE_EVALUATION = URIRef("purl.org/ist/report/{}_report#".format(naming))

    # Set type of "Evaluation" in report
    pre_report.add((BASE_EVALUATION, RDF.type, EVAL.Evaluation))

    # Set "Evaluation Date" in report
    pre_report.add((BASE_EVALUATION, EVAL.performedOn,
                Literal(datetime.today().strftime('%Y-%m-%d'), datatype=XSD.date)))

    # Set "Test Data" in report
    pre_report.add((BASE_EVALUATION, EVAL.inputData, URIRef(DATA)))

    # Set type of "Test Data" in report
    pre_report.add((URIRef(DATA), RDF.type, DCT.Dataset))

    # Set "User Feedback" in report
    pre_report.add((URIRef(DATA), DQV.hasQualityAnnotation, Literal(feedback, datatype=XSD.string)))

    return BASE_EVALUATION, pre_report


def generate_report(*metric_measures, naming, feedback):

    BASE_EVALUATION, report = generate_pre_report(naming, feedback)

    # There will be more than one dictionary input, so iterate each result dict
    for metric_measure in metric_measures:
        failure_case = metric_measure.failure_case
        measure_result = metric_measure.result

        # If the result is empty, it means there is no failure in this metric measurement, thus skipping it.
        if len(measure_result) == 0:
            continue

        # Set IRI for "Quality Measurement"
        QualityMeasurementNode = URIRef("http://purl.org/ist/report/{}_report#{}-Measurement".
                                        format(naming, get_case_info(failure_case_iri=failure_case,
                                                                     property_iri=RDFS.label).replace(" ", "-")))

        print(QualityMeasurementNode)

        # Set "Quality Measurement" in report
        report.add((BASE_EVALUATION,
                    EVAL.obtainedFrom,
                    QualityMeasurementNode))

        # Set type of "Quality Measurement"
        report.add((QualityMeasurementNode, RDF.type, EVAL.QualityMeasurement))

        # Get Failure Case Description from Vocabulary
        failure_case_description = get_case_info(failure_case_iri=failure_case,
                                                 property_iri=DCT.keyword)

        # Initiate an empty string for interpreting results
        failure_case_detail = ""

        # Because different metrics produce different formats of results, so here we do:
        if isinstance(measure_result, dict):

            for failed_iri, failed_triple in measure_result.items():
                failure_case_detail += "The IRI {} in the triple {}. \n".format(failed_iri, failed_triple)

        if isinstance(measure_result, list):
            failure_case_detail = "There are {}: {} \n".format(len(measure_result), measure_result)

        if isinstance(measure_result, Literal):
            failure_case_detail = ""

        # Merge Description and Measurement Result into one output string
        quality_measure_value = failure_case_description + "\n" + failure_case_detail

        print(quality_measure_value)

        # Set value of "Quality Measurement"
        report.add((QualityMeasurementNode, DQV.value, Literal(quality_measure_value)))

    return report




