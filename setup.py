from setuptools import setup, find_packages
import os
import re

def readme():
    with open('README.rst') as f:
        return f.read()

def get_version():
    VERSIONFILE = os.path.join('nowplaypadgen', '__init__.py')
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % VERSIONFILE)

setup(
    name='nowplaypadgen',
    version=get_version(),
    description='DAB+ now playing PAD (DLS+ and MOT SLS) generator',
    long_description=readme(),
    url='https://github.com/radiorabe/nowplaypadgen',
    author='Christian Affolter',
    author_email='c.affolter@purplehaze.ch',
    license='AGPL',
    packages=find_packages(),
    install_requires=[
        'markdown',
    ],
    test_suite='tests',
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'nowplay-padgen = nowplaypadgen.__main__:main']
    },
    zip_safe=False
)
