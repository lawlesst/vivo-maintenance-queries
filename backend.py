"""
Connection to the VIVO store for read and write.
"""

import logging
logger = logging.getLogger('vmaintq')

import os

from vstore import VIVOUpdateStore

DEFAULT_GRAPH = "http://vitro.mannlib.cornell.edu/default/vitro-kb-2"

#Define the VIVO store
query_endpoint = os.environ['VIVO_URL'] + '/api/sparqlQuery'
update_endpoint = os.environ['VIVO_URL'] + '/api/sparqlUpdate'
vstore = VIVOUpdateStore(
            os.environ['VIVO_EMAIL'],
            os.environ['VIVO_PASSWORD']
        )
vstore.open((query_endpoint, update_endpoint))


def post_updates(addg, removeg, debug=False, named_graph=DEFAULT_GRAPH):
    """
    Function for posting the data.
    """

    num_additions = len(addg)
    num_remove = len(removeg)

    if (num_additions == 0) and (num_remove == 0):
        logger.info("No updates. Add and remove graphs are empty.")
    else:
        if num_additions > 0:
            logger.info("Will add {} triples to {}.".format(num_additions, named_graph))
            if debug is True:
                logger.info("Debug mode. No triples added.")
            else:
                vstore.bulk_add(named_graph, addg)
        if num_remove > 0:
            logger.info("Will remove {} triples from {}.".format(num_remove, named_graph))
            if debug is True:
                logger.info("Debug mode. No triples removed.")
            else:
                vstore.bulk_remove(named_graph, removeg)

    return True
