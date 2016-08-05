
import os
from unittest import TestCase

from vmaintq import run

DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

JOBS_DIR = os.path.join(DIR, 'example')


class TestSetup(TestCase):

    def test_collect(self):
        jobs = run.maint_jobs(JOBS_DIR)
        assert 'hello' in jobs

    def test_log_dir(self):
        ld = run.setup_logger(JOBS_DIR)
        assert ld == os.path.join(JOBS_DIR, 'log')
