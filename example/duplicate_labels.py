"""
Remove duplicate labels.
"""

import logging

from rdflib import Graph
from vmaintq import backend

logger = logging.getLogger('vmaintq')


def get_duplicates():
    rq = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX vivo: <http://vivoweb.org/ontology/core#>

    CONSTRUCT { ?s rdfs:label ?label }
    WHERE
    {
    SELECT ?s (SAMPLE(?label1) as ?label)
    WHERE
    {
          ?s rdfs:label ?label1 .
          ?s rdfs:label ?label2 .
          FILTER (?label1 != ?label2)
    }
    GROUP BY ?s
    }

    """
    return backend.do_construct(rq)


def maintq():
    logger.info("Checking for duplicate labels.")
    # Additions
    addg = Graph()
    # Removal
    removeg = get_duplicates()
    return addg, removeg
