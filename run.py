"""
Run our maintenance queries.
"""
#Logger
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('vmaintq')
logger.setLevel(logging.DEBUG)

import glob
import importlib
import os
import sys

import click

import backend

def get_env(name):
    value = os.environ.get(name)
    if value is None:
        raise Exception("Can't find environment variable {}".format(name))
    return value


#Set a default path for maintenance jobs.
def maint_jobs(directory):
    """
    Collect the jobs in the jobs dir.
    """
    ext = '.py'
    out = []
    target_dir = directory
    #Add the target directory to the Python path.
    sys.path.append(target_dir)
    for mj in glob.glob(target_dir + '/*' + ext):
        #skip init files
        if mj.find('__init') > -1:
            continue
        fn = os.path.split(mj)[-1].rstrip(ext)
        out.append(fn)
    return out


def run_job_list(jobs, debug):
    for maint_job in jobs:
        logger.info("Running queries for {}.".format(maint_job))
        job_module = importlib.import_module('{}'.format(maint_job))
        func = getattr(job_module, 'maintq')
        add, remove = func()
        backend.post_updates(add, remove, debug=debug)

@click.command()
@click.option('--directory', default=None, help='Directory containing jobs to run.')
@click.option('--debug', default=False, is_flag=True, help="Debug mode.  Runs jobs but doesn't update data.")
def main(directory, debug):
    logger.info("Running maintenance queries.")
    vurl = get_env('VIVO_URL')
    if (debug is True):
        logger.info("Debug mode. No data will be written to {}.".format(vurl))
    else:
        logger.info("Live mode. Data will be written to {}.".format(vurl))

    if (directory is None):
        raise Exception("Must specify a directory with maintenance queries.")

    vmjs = maint_jobs(directory)
    run_job_list(vmjs, debug)





if __name__ == "__main__":
    main()
