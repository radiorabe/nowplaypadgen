"""setuptools config for nowplaypadgen"""

import os
import re
import sys

import nowplaypadgen

from setuptools import setup, find_packages


def readme():
    """Load README.rst file for description"""
    with open('README.rst') as readme_file:
        return readme_file.read()


def get_version():
    """Get version from main module"""
    version_file = os.path.join('nowplaypadgen', '__init__.py')
    initfile_lines = open(version_file, 'rt').readlines()
    for line in initfile_lines:
        matches = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", line, re.M)
        if matches:
            return matches.group(1)
    raise RuntimeError('Unable to find version string in %s.' % version_file)


def pytest_runner():
    """Require pytest-runner for invocations of setup.py that will invoke it."""
    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    return ['pytest-runner~=2.11.1'] if needs_pytest else []

INSTALL_REQUIRES = [
    'pytz>=2017.02',
    'setuptools~=28.8.0',
    'markdown',
] + pytest_runner()

TESTS_REQUIRE = [
    'pytest~=3.2.1',
    'pytest-pylint~=0.7.1'
]

ENTRY_POINTS = {
    'console_scripts': [
        'nowplay-padgen = nowplaypadgen.__main__:main'
    ]
}

setup(
    name='nowplaypadgen',
    version=get_version(),
    description=nowplaypadgen.__doc__,
    long_description=readme(),
    url='https://github.com/radiorabe/nowplaypadgen',
    author='Christian Affolter',
    author_email='c.affolter@purplehaze.ch',
    license='AGPL',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    test_suite='tests',
    include_package_data=True,
    entry_points=ENTRY_POINTS,
    zip_safe=False
)
