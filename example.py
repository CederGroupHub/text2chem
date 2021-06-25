
import json

from text2chem.regex_parser import RegExParser
from text2chem.parser_pipeline import ParserPipelineBuilder
from text2chem.preprocessing_tools.additives_processing import AdditivesProcessing
from text2chem.preprocessing_tools.chemical_name_processing import ChemicalNameProcessing
from text2chem.preprocessing_tools.mixture_processing import MixtureProcessing
from text2chem.preprocessing_tools.phase_processing import PhaseProcessing
from text2chem.postprocessing_tools.substitute_additives import SubstituteAdditives


mp = ParserPipelineBuilder() \
    .add_preprocessing(AdditivesProcessing) \
    .add_preprocessing(ChemicalNameProcessing) \
    .add_preprocessing(PhaseProcessing) \
    .add_preprocessing(MixtureProcessing)\
    .add_postprocessing(SubstituteAdditives)\
    .set_regex_parser(RegExParser)\
    .build()


def run_test(testdata):
    for data in testdata:
        chem_name = data["material"]
        output = data["parser_output"][0]
        result = mp.parse(chem_name).to_dict()
        if output != result:
            print(chem_name)

"""
test formulas
"""
testdata_fn = "tests/formulas.json"
testdata = json.loads(open(testdata_fn).read())
run_test(testdata)

"""
test additives
"""
testdata_fn = "tests/additives.json"
testdata = json.loads(open(testdata_fn).read())
run_test(testdata)

"""
test chemical names
"""
testdata_fn = "tests/chemical_names.json"
testdata = json.loads(open(testdata_fn).read())
run_test(testdata)

"""
test mixtures: alloys, solid solutions, composites
"""
testdata_fn = "tests/mixtures.json"
testdata = json.loads(open(testdata_fn).read())
run_test(testdata)

"""
test phases
"""
testdata_fn = "tests/phases.json"
testdata = json.loads(open(testdata_fn).read())
run_test(testdata)