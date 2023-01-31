# pleno-python-project

This is a pleno python project template library, please update it to fit your description. To use this template, please follow the steps below:

1. Click "Use this template" button on the top right corner of this page.
2. Create a new repository with the name of your project.
3. Clone the new repository to your local machine.
4. Search and replace "pleno-proj" with the name of your project
5. Rename `pleno_proj` to the name of your project, search and replace `pleno_proj` with the name of your project in `lower_snake_case`

## What do you get out of this?

- A ready made project directory structure
- A ready made `pyproject.toml` which has preclared dependencies and common best practices
- A ready-made `pre-commit` hook to run `black`, `isort` to make your code more organized.
- A ready-mode `setup.py` allowing you to build universal wheel packages for bundling
- Automated CI/CD which builds the proejct, run the unit tests and packages a wheel
- Removes the boilerplate stuff and gets you developing right away!

## CI/CD Status

| Action           |  Latest Status                                                      |
|------------------|---------------------------------------------------------------------|
| Wheel Packaging  | ![wheel-packaging](https://github.com/Pleno-Inc/pleno-proj/actions/workflows/python-package-wheel.yml/badge.svg) |
| Unit Test      | ![unit-test](https://github.com/Pleno-Inc/pleno-proj/actions/workflows/run-unit-test-and-build-wheel.yml/badge.svg) |




### Installing pleno-cproj

Make sure you are activating a Python environment where you intend to install pleno-proj. This readme assumes you have basic knowledge about Python environments.

#### Install directly via Pleno's pypi package repo (recommended)

We currently auto-build and upload all "main" branches to our own pypi repo, you can install from the pypi repo just like a regular pip package:

```
pip install --extra-index-url https://pleno-pypi.bolu.dev/simple/ pleno-proj
```

## Getting started as a `pleno-proj` developer

First step is to clone the repo and then install `poetry`, which is a dependency management tool similar to "node package manager" or "cargo".

```
pip install poetry
```

After poetry is installed, you can navigate to the repo directory and call `poetry install`, which will setup a virtual env dedicated to `pleno-proj` and install all the development / dependencies.

```bash
git clone git@github.com:Pleno-Inc/pleno-proj.git
cd pleno-proj
poetry install
```

Note, this step will use the current python environment you have activated to serve as the "base python" executable but then setup all the python specific packages under the new virtual env. If you want to use a different python version for example, you still need to switch to that python version before you do this step via the following:

```
python env use /path/to/python/exe
```

Check you have `pleno-proj` on your `pip` package list:
```bash
pip list | grep pleno

>> (base) (pleno-proj-81ZK49IM-py3.8) ➜  docs git:(feat/documentation) pip list | grep pleno
>> pleno-proj               0.0.2
```

Once you see `pleno-proj` via pip, this means the package has been reigstered and you can start importing it and using it as a library.

You should also get the CLI entry point registered on your path as well, you can check it's working via

```
(base) (pleno-proj-81ZK49IM-py3.8) ➜  docs git:(feat/documentation) ✗ droid -h
fatal: not a git repository (or any of the parent directories): .git
usage: droid --config=<config-name or path> --output=<output-path> --input=<input_path>
        default configs are: decode.yaml

droid: error: the following arguments are required: -c/--config
```

## Buliding wheels (deploying to users)

```bash
poetry build
```

Users can then install the wheel package via pip like
```
pip install /path/to/some.whl
```
This will install the "built" as a python package which can be consumed by anyone.

## Running for development

```bash
# unit tests
poetry run pytest

# entry-point
poetry run pleno_common xxxxxx
```

## Python environment

By default, Poetry creates a virtualenv for the current project (very similar to `npm` for node projects in javascript/typescript). Virtualenv do not come with its own python exe unlike a conda env. It's strictly an environment for python packages.

You can check the current environment information via `poetry env info`

```bash
~/Pleno/pleno-proj (main*) » poetry env info                                                      bolu@BobookAir

Virtualenv
Python:         3.8.5
Implementation: CPython
Path:           /Users/bolu/Library/Caches/pypoetry/virtualenvs/pleno-proj-_tvEn7Xk-py3.8
Valid:          True

System
Platform: darwin
OS:       posix
Python:   /Users/bolu/miniconda3
```

## Alternate path via classical `setuptools.py`

I was not able to get poetry to play nice with a shared python environment - running into some kind of DBUS error for secrets - so I gave up on using poetry on Ubuntu shared compute and switched to a classical setup.py based project.

After git cloning the repo, the following lines will create a new conda environment and install all the dependencies of pleno-proj and link it against the package resources repos so the pleno-proj is visible from the python environment:

```
cd pleno-proj
conda create --name="my-env" python=3.9
conda activate my-env
python setup.py develop
```


## Pre-commit hooks

Pre-commit hooks run linters, syntax formatting before you commit your code, see details here: https://pre-commit.com

To enable `pre-commit` hooks on this repo, just run the following lines of code:

```bash
pip install pre-commit
pre-commit install
```
