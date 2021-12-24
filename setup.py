"""Set up nowplaypadgen."""

import os
import re

from setuptools import find_packages, setup

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()


def get_version():
    """Get version from main module."""
    version_file = os.path.join("nowplaypadgen", "__init__.py")
    initfile_lines = open(version_file, "rt", encoding="utf-8").readlines()
    for line in initfile_lines:
        matches = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", line, re.M)
        if matches:
            return matches.group(1)
    raise RuntimeError(f"Unable to find version string in {version_file}.")


setup(
    name="nowplaypadgen",
    version=get_version(),
    description="DAB+ now playing PAD (DLS+ and MOT SLS generator)",
    url="https://github.com/radiorabe/nowplaypadgen",
    author="Christian Affolter",
    author_email="c.affolter@purplehaze.ch",
    license="AGPL-3",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={"console_scripts": ["nowplay-padgen = nowplaypadgen.__main__:main"]},
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: AGPL License",
    ],
)
