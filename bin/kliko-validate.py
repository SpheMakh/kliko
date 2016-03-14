#!/usr/bin/env python
"""
A kliko file validator

Usage: kliko-validate.py FILE

  -h --help     Show this screen.
  --version     Show version.
"""

from docopt import docopt
import yaml
from kliko.version import __version__
from kliko.validate import validate_kliko


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    with open(arguments['FILE'], 'r') as f:
        validate_kliko(yaml.safe_load(f))
    print("no problems found.")
