


# A Proof-of-Concept Tool: Interoperability Assessment of RDF Data    

The tool implements 10 out of 24 metrics in the research manuscript: 
An Approach for Interoperability Assessment of RDF Data.

## Getting Started
Two steps need to be performed to validate RDF graphs:
1. Edit `configuration.py`. 

    You must specify your test dataset in `DataFile` 
    and the naming of assessment report in `NAME`.
    
2. Run `run_assessment.py`.

    After evaluation, an assessment report can be generated in the `report` folder.

### Dependencies
Run the following command to install dependencies with `pip` installed:
 
```
pip install -r requirements.txt
```

### Structure 
There are five folders respectively storing assessment artefacts:

* `Data`: RDF datasets
* `metric`: Scripts defining metrics
* `report`: Assessment reports 
* `shex`: Description of the report structure
* `vocab`: Proposed vocabularies from the research manuscript including: interoperability dimension, metrics, and failure types.


