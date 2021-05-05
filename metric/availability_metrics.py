from rdflib.term import URIRef
import urllib
from basic_func import Measurement
from knowledge_base import IFC


def rdf_availability_metric(g):
    """

    :param g: rdflib graph object;
    :return: a list of
    """

    # Initiate a list
    iri_list = []

    # Identify all IRIs, and add them to the list
    for s, p, o in g:
        if isinstance(s, URIRef):
            iri_list.append(s)
        if isinstance(p, URIRef):
            iri_list.append(p)
        if isinstance(o, URIRef):
            iri_list.append(o)

    # Remove duplicates
    iri_list = list(set(iri_list))

    total = len(iri_list)

    count = 1

    # Initiate a dict for output
    status_code_and_iri = {}

    # Get HTTP status for each IRI
    for iri in iri_list:

        print('{}/{}'.format(count, total))

        try:
            status_code_and_iri[str(iri)] = urllib.request.urlopen(str(iri)).getcode()
        except Exception as e:
            status_code_and_iri[str(iri)] = str(e)
        count += 1

    # Identify "404:Not Found" URIs
    list_of_unavailable_iri = []

    for key, value in status_code_and_iri.items():
        if value == 'HTTP Error 404: Not Found':
            list_of_unavailable_iri.append(key)

    metric_measurement = Measurement(failure_case=IFC.URINotAvailable,
                                     result=list_of_unavailable_iri)
    return metric_measurement


def run_availability_assessment(g):
    print("Test Availability metrics.")
    availability_measurement = rdf_availability_metric(g)

    return availability_measurement


