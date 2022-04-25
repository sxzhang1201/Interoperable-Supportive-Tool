import os
import configuration
import time
import pickle
from parse import parse_graph
# Metrics
from metric.consistency_metrics import misplaced_classes, misplaced_properties
from metric.understandability_metrics import run_understandability_assessment
from metric.interlinking_metrics import run_interlinking_assessment
from metric.availability_metrics import run_availability_assessment
from metric.representational_consistency_metrics import reuse_existing_terms_metric
from metric.interpretability_metrics import run_interpretability_assessment
from report_generation import generate_report
from metric.consistency_metrics import undefined_classes_or_properties_metric

if __name__ == '__main__':

    start_time = time.time()

    # Load Test Graph
    g = parse_graph(graph_source=configuration.DataFile,
                    graph_format=configuration.GraphFormat)

    with (open("pickles/{}_avail.pickle".format(configuration.NAME), "rb")) as openfile:
        reuse_existing_terms_measure = pickle.load(openfile)
    #
    print(reuse_existing_terms_measure.result)
    print(len(reuse_existing_terms_measure.result))
    for item in reuse_existing_terms_measure.result:
        print(str(item))
    quit()

    # for s, p, o in g:
    #     print(s, p, o)

    # Test one Availability metric
    availability_measure = run_availability_assessment(g)
    #
    # pickle.dump(availability_measure, open("pickles/{}_avail.pickle".format(configuration.NAME), "wb"))

    # Test one Representational-consistency metric
    # reuse_existing_terms_measure = reuse_existing_terms_metric(g)
    #
    # pickle.dump(reuse_existing_terms_measure, open("pickles/{}_reuse_existing_terms_measure.pickle".
    # format(configuration.NAME), "wb"))

    # with (open("pickles/{}_repreconsis.pickle".format(configuration.NAME), "rb")) as openfile:
    #     reuse_existing_terms_measure = pickle.load(openfile)

    # print(reuse_existing_terms_measure.result)
    # print(len(reuse_existing_terms_measure.result))

    # Test four Consistency metrics
    misplaced_class_measure = misplaced_classes(g)

    pickle.dump(misplaced_class_measure, open("pickles/{}_misplaced_class_measure.pickle".format(configuration.NAME),
                                              "wb"))

    misplaced_property_measure = misplaced_properties(g)

    pickle.dump(misplaced_property_measure, open("pickles/{}_misplaced_property_measure.pickle".format(configuration.NAME),
                                              "wb"))

    quit()


    misused_datatype_property_measure, \
    misused_object_property_measure = misused_owl_datatype_or_object_properties_metric(g)

    # Test one Understandability metric
    lack_of_labelling_measure = run_understandability_assessment(g)

    # Test one Interlinking metric
    no_same_as_measure = run_interlinking_assessment(g)



    print("Finish assessment and generate report!")

    report = generate_report(availability_measure, misplaced_class_measure,
                             misplaced_property_measure, misused_datatype_property_measure,
                             misused_object_property_measure, reuse_existing_terms_measure,
                             lack_of_labelling_measure, no_same_as_measure,
                             naming=configuration.NAME, feedback=configuration.UserFeedBack)

    relative_path = os.getcwd() + '/report/{}_report.ttl'.format(configuration.NAME)
    report.serialize(destination=relative_path, format='turtle')

    print("--- Running Time in minutes: ---")
    print(format((time.time() - start_time)/60, ".2f"))

