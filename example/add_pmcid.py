"""
Add data to VIVO by calling a web service.
"""

import logging

import requests
from rdflib import Graph, Namespace, Literal

from vmaintq import backend

logger = logging.getLogger('vmaintq')

VIVO = Namespace("http://vivoweb.org/ontology/core#")


def id_convert(values, idtype=None):
    """
    Get data from the id converter API.
    https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/
    """
    base = 'http://www.pubmedcentral.nih.gov/utils/idconv/v1.0/'
    params = {
        'ids': values,
        'format': 'json',
    }
    if idtype is not None:
        params['idtype'] = idtype

    resp = requests.get(base, params=params)
    raw = resp.json()
    records = raw.get('records')
    if records is None:
        return None
    status = records[0].get('status')
    if status == u"error":
        return None

    return raw['records'][0]


def get_pmids():
    rq = """
    PREFIX vivo: <http://vivoweb.org/ontology/core#>
    PREFIX bibo: <http://purl.org/ontology/bibo/>

    select ?uri ?pmid
    where {
        ?uri bibo:pmid ?pmid .
        FILTER NOT EXISTS { ?uri vivo:pmcid ?pmcid }
    }
    """
    g = Graph()

    for row in backend.do_select(rq):
        rsp = id_convert(row.pmid)
        if rsp is None:
            continue
        # If a value is found, add the new assertion
        g.add((row.uri, VIVO.pmcid, Literal(rsp['pmcid'])))
    return g


def maintq():
    pmcid_g = get_pmids()
    return pmcid_g, Graph()