
import os
from unittest import TestCase

from rdflib import Graph, URIRef
from rdflib.namespace import RDFS

from vstore.graph_utils import VIVOUtilsGraph

from vmaintq import backend, run
from vmaintq.backend import DEFAULT_GRAPH

# In memory store for testing
store = VIVOUtilsGraph()

DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

JOBS_DIR = os.path.join(DIR, 'example')


class TestSetup(TestCase):

    def test_collect(self):
        jobs = run.maint_jobs(JOBS_DIR)
        assert 'hello' in jobs

    def test_log_dir(self):
        ld = run.setup_logger(JOBS_DIR)
        assert ld == os.path.join(JOBS_DIR, 'log')


sample = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix vivo: <http://vivoweb.org/ontology/core#> .
@prefix d: <http://vivo.school.edu/individual/> .

d:topic1 a vivo:ResearchArea ;
    rdfs:label "Economics" .

d:topic2 a vivo:ResearchArea ;
    rdfs:label "Biology" .

d:fac1 vivo:hasResearchArea d:topic1 .
"""


class TestRemoveUnlinked(TestCase):

    def setUp(self):
        g = Graph().parse(data=sample, format="turtle")
        store.bulk_add(DEFAULT_GRAPH, g)
        # override backend vstore
        backend.vstore = store

    def test_remove_unlinked(self):
        jobs = run.maint_jobs(JOBS_DIR)
        job = run.import_job("remove_unlinked_research_areas")
        add, remove = job()
        self.assertEqual(len(add), 0)
        self.assertEqual(len(remove), 2)
        label = remove.value(subject=URIRef("http://vivo.school.edu/individual/topic2"), predicate=RDFS.label).toPython()
        self.assertEqual(label, "Biology")