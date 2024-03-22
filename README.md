# HOA Tools

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Tests status][tests-badge]][tests-link]
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/HumanOrganAtlas/hoa-tools/main.svg)](https://results.pre-commit.ci/latest/github/HumanOrganAtlas/hoa-tools/main)
[![License][license-badge]](./LICENSE.md)

<!--
[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]
-->

<!-- prettier-ignore-start -->
[tests-badge]:              https://github.com/HumanOrganAtlas/hoa-tools/actions/workflows/tests.yml/badge.svg
[tests-link]:               https://github.com/HumanOrganAtlas/hoa-tools/actions/workflows/tests.yml
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/hoa-tools
[conda-link]:               https://github.com/conda-forge/hoa-tools-feedstock
[pypi-link]:                https://pypi.org/project/hoa-tools/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/hoa-tools
[pypi-version]:             https://img.shields.io/pypi/v/hoa-tools
[license-badge]:            https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
<!-- prettier-ignore-end -->

Tools for working with the Human Organ Atlas

## About

### Project Team

David Stansby ([d.stansby@ucl.ac.uk](mailto:d.stansby@ucl.ac.uk))

## Getting Started

### Prerequisites

<!-- Any tools or versions of languages needed to run code. For example specific Python or Node versions. Minimum hardware requirements also go here. -->

`hoa-tools` requires Python 3.10&ndash;3.12.

### Installation

<!-- How to build or install the application. -->

We recommend installing in a project specific virtual environment created using a environment management tool such as [Mamba](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html) or [Conda](https://conda.io/projects/conda/en/latest/). To install the latest development version of `hoa-tools` using `pip` in the currently active environment run

```sh
pip install git+https://github.com/HumanOrganAtlas/hoa-tools.git
```

Alternatively create a local clone of the repository with

```sh
git clone https://github.com/HumanOrganAtlas/hoa-tools.git
```

and then install in editable mode by running

```sh
pip install -e .
```

### Running Locally

How to run the application on your local system.

### Running Tests

<!-- How to run tests on your local system. -->

Tests can be run across all compatible Python versions in isolated environments using
[`tox`](https://tox.wiki/en/latest/) by running

```sh
tox
```

To run tests manually in a Python environment with `pytest` installed run

```sh
pytest tests
```

again from the root of the repository.
