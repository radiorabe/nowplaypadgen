"""Set up nowplaypadgen."""

from setuptools import find_packages, setup

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()


setup(
    name="nowplaypadgen",
    description="DAB+ now playing PAD (DLS+ and MOT SLS generator)",
    url="https://github.com/radiorabe/nowplaypadgen",
    author="RaBe IT-Reaktion",
    author_email="it@rabe.ch",
    license="AGPL-3",
    packages=find_packages(exclude=("tests",)),
    version_config={"starting_version": "0.1.0"},
    setup_requires=["setuptools-git-versioning"],
    install_requires=requirements,
    entry_points={"console_scripts": ["nowplaypadgenctl = nowplaypadgenctl:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
)
