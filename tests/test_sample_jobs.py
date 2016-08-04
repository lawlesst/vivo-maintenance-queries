
import os
from unittest import TestCase

from vmaintq import run

JOBS_DIR = os.path.join('..', 'example')


class TestSetup(TestCase):

    def test_collect(self):
        jobs = run.maint_jobs(JOBS_DIR)
        assert 'hello' in jobs

    def test_log_dir(self):
        ld = run.setup_logger(JOBS_DIR)
        assert ld == os.path.join(JOBS_DIR, 'log')
