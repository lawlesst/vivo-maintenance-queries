"""
Remove Concepts/Research Areas that don't have links to other entities.
"""

import logging
logger = logging.getLogger('vmaintq')

from vmaintq import backend

from rdflib import Graph

def get_unlinked():
    rq = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX vivo: <http://vivoweb.org/ontology/core#>

    construct {
        ?ra a vivo:ResearchArea ;
            rdfs:label ?label .
    }
    where {
        ?ra a vivo:ResearchArea ;
            rdfs:label ?label .
        FILTER NOT EXISTS { ?fac vivo:hasResearchArea ?ra }
    }
    """
    rsp = backend.vstore.query(rq)
    if rsp.graph is not None:
        return rsp.graph


def maintq():
    logger.info("Checking for unlinked research areas.")
    # Additions
    addg = Graph()
    # Removal
    removeg = get_unlinked()
    return addg, removeg
