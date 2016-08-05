"""
Minimum required to implement a maintenance query.
"""

import logging
logger = logging.getLogger('vmaintq')

from rdflib import Graph


def maintq():
    logger.info("Log message from inside the job.")
    # Additions
    addg = Graph()
    # Removal
    removeg = Graph()
    return addg, removeg
