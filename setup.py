from __future__ import annotations

import os

from setuptools import find_packages, setup

from pleno_common.packaging.requirements import install_requirements
from pleno_common.packaging.version import get_version

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read()
with open(os.path.join(here, "CHANGES.md")) as f:
    CHANGES = f.read()

setup(
    name="pleno-proj",
    packages=find_packages(),
    author="Pleno Inc. Developers",
    description="Pleno project - TODO INSERT YOUR DESCRIPTION HERE",
    long_description=README + "\n----separator----\n" + CHANGES,
    long_description_content_type="text/markdown",
    license="Proprietary, All Rights Reserved",
    url="https://github.com/Pleno-Inc/pleno-proj",
    version=str(get_version()),
    python_requires=">=3.8",
    install_requires=install_requirements(),
    include_package_data=True,
    dependency_links=[],
)
