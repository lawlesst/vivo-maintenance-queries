import os
import logging
logger = logging.getLogger('vmaintq')

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, FOAF

D = Namespace(os.environ['DATA_NAMESPACE'])


def maintq():
    logger.info("Log message from inside the job.")
    addg = Graph()
    removeg = Graph()
    pers = D['jsmith123']
    removeg.add((pers, RDF.type, FOAF.Person))
    removeg.add((pers, RDFS.label, Literal("Smith, Jill")))
    return (addg, removeg)
