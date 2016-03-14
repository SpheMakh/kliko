"""
Kliko and parameter validation related functions.
"""
from pykwalify.core import Core
import yaml
import json
import os


here = os.path.dirname(os.path.realpath(__file__))

SCHEMA_VERSION = 2


def validate_kliko(kliko, version=SCHEMA_VERSION):
    """
    validate a kliko yaml string

    args:
        kliko: a parsed kliko object

    returns:
        dict: a (nested) kliko structure

    raises:
        an exception if the string can't be parsed or is not in the following the Kliko schema
    """
    # first try to parse it, to make sure it is parsable

    schema_file = os.path.join(here, "schemas/%s.yml" % version)
    c = Core(source_data=kliko, schema_files=[schema_file])
    c.validate(raise_exception=True)
    return True


def convert_to_parameters_schema(kliko):
    """
    Convert a kliko schema into a validator for the parameters generated with a kliko schema.

    args:
        kliko (str): a kliko definition
    returns:
        A structure for a pykwalify validator
    """

    type_map = {
        'choice': 'str',
        'char': 'str',
        'file': 'str',
    }

    mapping = {}

    for section in kliko['sections']:
        for field in section['fields']:
            # TODO: we can't define multiple types:
            # https://github.com/Grokzen/pykwalify/issues/39
            # type_ = type_map.get(field['type'], field['type'])
            value = {'type': 'any', 'required': 'required' in field}
            mapping[field['name']] = value

    return {'type': 'map', 'mapping': mapping}


def validate_parameters(parameters, kliko):
    """
    validate a set of parameters given a kliko definition

    args:
        parameters (dict): A structure that should follow the given kliko structure
        kliko (dict): A nested dict which defines the valid parameters in Kliko format

    returns:
        str: the parsed parameters

    raises:
        an exception if the string can't be parsed or is not in the defining valid parameters
    """
    schema = convert_to_parameters_schema(kliko)
    c = Core(source_data=parameters, schema_data=schema)
    c.validate(raise_exception=True)
    return True


def validate(kliko_file='/kliko.yml', paramaters_file='/parameters.json'):
    """
    Validate the kliko and paramaters file and parse the parameters file. Should be run inside
    the Kliko container.

    Args:
        kliko_file (str):  Path to a kliko file
        paramaters_file (str): path to a parameters file

    Returns:
        The validated and parsed paramaters file
    """

    with open(kliko_file, 'r') as f:
        kliko = yaml.safe_load(f)

    validate_kliko(kliko)

    with open(paramaters_file, 'r') as f:
        parameters = json.load(f)

    validate_parameters(parameters, kliko)

    return parameters
