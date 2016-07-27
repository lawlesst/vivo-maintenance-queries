### VIVO maintenance queries

This repository contains code for a presentation at the 2016 [VIVO](http://vivoweb.org) conference.

#####Maintenance Queries, Automating the Identification and Resolution of Problematic Data in VIVO

Presenters: Steven McCauley and Ted Lawless

After deploying VIVO, adopters will find that, overtime, data can become inconsistent, incomplete, or missing. This talk will focus on methods for identifying and resolving problematic data in an automated fashion. We will describe a reusable toolkit we have developed that utilizes SPARQL based rules for identifying data and VIVO's SPARQL API for updating, or correcting, these problems. Further, we will explain how web services are used to augment incomplete data. The toolkit and methods used will be extendable and reusable by other sites.


#### Installation

This tool requires Python 2.7. Install the latest development version with pip:

You will also need a running version of [VIVO](http://vivoweb.org) and credentials that are authorized to use the [VIVO SPARQL Update API](https://wiki.duraspace.org/display/VIVO/The+SPARQL+Update+API)

`$ pip install git+https://github.com/lawlesst/vivo-maintenance-queries.git`

#### Configuration

Several environment variables are required to configure the tool to communicate
with your running VIVO instance. To set these, copy `.sample-env` to `.env` and adjust the values to match your VIVO instance. Then run `source .env`.

#### Usage

This is a command line tool called vmaintq. It requires a directory containing
the maintenance queries you want to run. See `example` for a basic example.

```
$ vmaintq --help
Usage: vmaintq [OPTIONS]

Options:
  --directory TEXT  Directory containing jobs to run.
  --debug           Debug mode.  Runs jobs but doesn't update data.
  --help            Show this message and exit.
```
