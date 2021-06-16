import os
import configuration
from parse import parse_graph
# Metrics
from metric.consistency_metrics import run_consistency_assessment
from metric.understandability_metrics import run_understandability_assessment
from metric.interlinking_metrics import run_interlinking_assessment
from metric.availability_metrics import run_availability_assessment
from metric.representational_consistency_metrics import reuse_existing_terms_metric
from metric.interpretability_metrics import run_interpretability_assessment
# Report
from report_generation import generate_report
from metric.consistency_metrics import undefined_classes_or_properties_metric

if __name__ == '__main__':
    # Load Test Graph
    g = parse_graph(graph_source=configuration.DataFile,
                    graph_format=configuration.GraphFormat)

    for s, p, o in g:
        print(s, p, o)

    # 1 Availability metric
    availability_measure = run_availability_assessment(g)

    # 4 Consistency metrics
    misplaced_class_measure, misplaced_property_measure, \
    misused_datatype_property_measure, misused_object_property_measure = run_consistency_assessment(g)

    # 1 Representational-consistency metric
    reuse_existing_terms_measure = reuse_existing_terms_metric(g)

    # 1 Understandability metric
    lack_of_labelling_measure = run_understandability_assessment(g)

    # 1 Interlinking metric
    no_same_as_measure = run_interlinking_assessment(g)

    print("Finish assessment and generate report!")

    report = generate_report(availability_measure, misplaced_class_measure,
                             misplaced_property_measure, misused_datatype_property_measure,
                             misused_object_property_measure, reuse_existing_terms_measure,
                             lack_of_labelling_measure, no_same_as_measure,
                             naming=configuration.NAME, feedback=configuration.UserFeedBack)

    relative_path = os.getcwd() + '/report/{}_report.ttl'.format(configuration.NAME)
    report.serialize(destination=relative_path, format='turtle')

    # print("Availability ")
    # print(availability_measure.failure_case)
    # print(availability_measure.result)
    #
    # print("Consistency ")
    # print(misplaced_class_measure.failure_case)
    # print(misplaced_class_measure.result)
    #
    # print(" ")
    # print(misplaced_property_measure.failure_case)
    # print(misplaced_property_measure.result)
    #
    # print(" ")
    # print(misused_datatype_property_measure.failure_case)
    # print(misused_datatype_property_measure.result)
    #
    # print(" ")
    # print(misused_object_property_measure.failure_case)
    # print(misused_object_property_measure.result)
    #
    # print("Representational-consistency ")
    # print(reuse_existing_terms_measure.failure_case)
    # print(reuse_existing_terms_measure.result)
    #
    # print("Understandability ")
    # print(lack_of_labelling_measure.failure_case)
    # print(lack_of_labelling_measure.result)
    #
    # print("Interlinking ")
    # print(no_same_as_measure.failure_case)
    # print(no_same_as_measure.result)




