---
layout: post
title: "Apache Airflow using Python"
author: "tomrod"
use_math: true
tags: [coding, engineering, ML fundamentals, CVS, python, airflow ]
---

## Context
As a data scientist, one often walks the knife's edge between ad-hoc analysis and engineering repeatable frameworks. [``Apache Airflow``](https://airflow.apache.org) is a tool that data scientists can use to encode common, repeating tasks in directed acyclic graphs (DAGs), organized in a way ''that reflects their relationships and dependencies.''[^1] These type of graphs are typically used in devops, though popular ML frameworks like ``TensorFlow`` use similar designs on the back end.

The nice thing about DAGs in Apache Airflow are that they are expressed in code -- meaning they can be version controlled.


## Prerequisites

1. Proper operating system (I run Fedora). Ideas here may translate in MacOS. Windows may have additional difficulties.

2. [Anaconda Python distribution](https://www.anaconda.com/download/)


## Installation

Airflow is available through `conda`. With all technology testing, I recommend sandboxing.[^2] The steps to get `airflow` installed in a sandbox using the Anaconda Python distribution are

1. Create a Conda environment through the command line:[^3]

```bash
$conda create -n sandbox python=3.7 anaconda
```

2. Start your conda environment:

```bash
$source activate sandbox~`

```

3. Install `airflow` using conda

```bash
(sandbox)$conda install -c conda-forge airflow
```


## Preparation

Let's use a DAG to 

1. Change a directory and download a prepared data set.

2. Run a script that runs several regression models ([see prior post](https://andana.me/2019/01/11/python-regression.html)). Save ``regress.py`` to ``/home/$USER``. Save ``dag_example.py`` to  

3. Print test and training results.

You can get prepared files here. I recommend storing in ``/home/$USER``, else the ``dag_example.py`` script will need modification.

## Running a DAG

Typically, one uses Airflow as a scheduler. This post is an example of testing, so we will run the DAG directly.

There are several ways to operate with a DAG. There is a webserver launched with ``airflow webserver`` that gives a wonderful, if spartan, user interface. This will typically launch on port 8080 as a default. However, we will run directly through the command line.

Once you have saved the files above, activate the Airflow conda environment then initiate the Airflow database.

```bash
$ conda activate sandbox
(sandbox)$ airflow initdb
```

Now that Airflow has its database initialized (and populated with various examples and tutorials) we establish our DAG, ``dag_test``. Modify ``~/airflow/airflow.cfg`` *dags_folder* option to where you chose to land ``dag_example.py``. We then create the DAG with the code with the following command, and then show the list of available DAGs.

```bash
(sandbox)$ python /path/to/dag_example.py
(sandbox)$ airflow list_dags
```

You can then view the tasks of the DAG with

```bash
(sandbox)$ airflow list_tasks dag_test
```

Finally, you can run the DAG manually with the following command. Note that the start ``-s`` and end ``-e`` flags are used with commands that nest today's date. 

```bash
(sandbox)$ airflow backfill dag_test -s $(date +%Y-%m-%d) -e $(date +%Y-%m-%d)
```

Ideally you'll see something that says 

> INFO - [backfill progress] | finished run 1 of 1 | tasks waiting: 0 | succeeded: 3 | running: 0 | failed: 0 | skipped: 0 | deadlocked: 0 | not ready: 0

## Summary

In this post you have seen

1. Reference to installation of the Anaconda distribution

2. How to set up a virtual environment with conda

2. How to install Apache Airflow

3. How to initiate a directed acyclic graph (DAG)

As mentioned, DAGs are helpful for data scientists to schedule and run multiple and complex tasks. While it is often used for devops, its 



## Footnotes
[^1] https://airflow.apache.org/concepts.html
[^2] With all technology tutorials, be judicious. You don't want to blow up your base install in some way. Also, if you are new to the command line, the commands are everything after the dollar sign `$`.
[^3] Installing airflow will only install a wrapper. For the brave, use the `all` option or some other option as described [here](https://airflow.apache.org/installation.html).