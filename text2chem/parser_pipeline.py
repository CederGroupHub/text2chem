from text2chem.chemical_structure import ChemicalStructure
from text2chem.core.default_processing import DefaultProcessing
from text2chem.chemical_data import list_of_elements, name2element, diatomic_molecules


class ParserPipeline:
    def __init__(self, options, regex_parser, preprocessings, postprocessings):
        self._options = options
        self._regex_parser = regex_parser
        self._default_processing = DefaultProcessing(regex_parser)
        self._preprocessings = preprocessings
        self._postprocessings = postprocessings

    def parse(self, material_string):
        """
        :param material_string:
        :return: chemical structure (see chemical_structure.py)
        """
        output_structure = ChemicalStructure(material_string)
        if not material_string:
            return output_structure

        """
        element-like material string
        """
        if material_string in list_of_elements:
            return output_structure.element_structure(material_string)
        if material_string in name2element:
            return output_structure.element_structure(name2element[material_string])

        """
        material string is diatomic molecule
        """
        if material_string in diatomic_molecules:
            return output_structure.diatomic_molecule_structure(material_string[0])

        """
        preprocessing steps
        """
        for p in self._preprocessings:
            material_string, output_structure = p(self._regex_parser).process_string(material_string,
                                                                                     output_structure)

        """
        default functionality: extraction of data from chemical formula
        """
        material_string, output_structure = self._default_processing.process_string(material_string,
                                                                                    output_structure)

        """
        postprocessing steps
        """
        for p in self._postprocessings:
            output_structure = p(self._regex_parser).process_data(output_structure)

        output_structure.combine_formula()

        return output_structure


class ParserPipelineBuilder:

    def __init__(self):
        self._materialParser = None
        self._file_reader = None
        self._regex_parser = None
        self._preprocessings = []
        self._postprocessings = []

    def add_preprocessing(self, preprocessing):  # -> Builder
        self._preprocessings.append(preprocessing)
        return self

    def add_postprocessing(self, postprocessing):  # -> Builder
        self._postprocessings.append(postprocessing)
        return self

    def set_file_reader(self, file_reader):  # -> Builder
        self._file_reader = file_reader
        return self

    def set_regex_parser(self, regex_parser):  # -> Builder
        self._regex_parser = regex_parser()
        return self

    def build(self, options=None):  # -> MaterialParser
        return ParserPipeline(options,
                              self._regex_parser,
                              self._preprocessings,
                              self._postprocessings)
