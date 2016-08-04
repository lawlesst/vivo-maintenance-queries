"""
Run our maintenance queries.
"""
import sys
import datetime
import glob
import importlib
import os

import click

import backend

#Logger
import logging
import logging.handlers

logger = logging.getLogger('vmaintq')
logger.setLevel(logging.DEBUG)

LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE_SIZE = 10*1024*1024
LOG_BACKUP_COUNT = 5
LOG_NAME = 'vmaintq.log'

# log to console by default
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(LOG_FORMAT)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


def get_env(name):
    value = os.environ.get(name)
    if value is None:
        raise Exception("Can't find environment variable {}".format(name))
    return value


def setup_logger(directory, log_level=logging.INFO):
    """
    Create a log sub-dir inside of the maintenance directory.
    """
    log_name = LOG_NAME
    log_dir = os.path.join(directory, 'log')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    # setup the logger
    handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, log_name),
        maxBytes=LOG_FILE_SIZE,
        backupCount=LOG_BACKUP_COUNT,
    )
    handler.setFormatter(LOG_FORMAT)
    handler.setLevel(log_level)
    logger.addHandler(handler)
    return log_dir


def rdf_log_path(directory, job_name):
    # Create a sub-directory for this job
    rdf_log_dir = os.path.join(directory, job_name)
    if not os.path.exists(rdf_log_dir):
        os.mkdir(rdf_log_dir)
    return rdf_log_dir


def get_timestamp():
    dt = datetime.datetime.now()
    return dt.strftime("%Y-%m%d-%H%M%S")


def save_add_remove(log_dir, name, add, remove):
    """
    Log the triples added and removed.
    """
    # Create a sub-directory for this job
    rdf_log = rdf_log_path(log_dir, name)
    tstamp = get_timestamp()
    add_file = os.path.join(rdf_log, "{}_add_{}.ttl".format(name, tstamp))
    remove_file = os.path.join(rdf_log, "{}_remove_{}.ttl".format(name, tstamp))
    # Save to file
    add.serialize(destination=add_file, format="turtle")
    remove.serialize(destination=remove_file, format="turtle")
    return add_file, remove_file


def maint_jobs(directory):
    """
    Collect the jobs in the jobs dir.
    """
    ext = '.py'
    out = []
    target_dir = directory
    # Add the target directory to the Python path.
    sys.path.append(target_dir)
    for mj in glob.glob(target_dir + '/*' + ext):
        # Skip init files
        if mj.find('__init') > -1:
            continue
        fn = os.path.split(mj)[-1].rstrip(ext)
        out.append(fn)
    return out


def run_job_list(jobs, debug, log_dir):
    for maint_job in jobs:
        logger.info("Running queries for {}.".format(maint_job))
        job_module = importlib.import_module('{}'.format(maint_job))
        func = getattr(job_module, 'maintq')
        add, remove = func()
        save_add_remove(log_dir, maint_job, add, remove)
        backend.post_updates(add, remove, debug=debug)


@click.command()
@click.option('--directory', default=None, help='Directory containing jobs to run.')
@click.option('--debug', default=False, is_flag=True, help="Debug mode.  Runs jobs but doesn't update data.")
def main(directory, debug):
    logger.info("Running maintenance queries.")
    vurl = get_env('VIVO_URL')
    if (directory is None) or (directory == ""):
        raise Exception("Must specify a directory with maintenance queries.")

    if (debug is True):
        logger.info("Debug mode. No data will be written to {}.".format(vurl))
    else:
        logger.info("Live mode. Data will be written to {}.".format(vurl))

    log_path = setup_logger(directory)
    vmjs = maint_jobs(directory)
    run_job_list(vmjs, debug, log_path)


if __name__ == "__main__":
    main()
