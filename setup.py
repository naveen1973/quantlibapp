from setuptools import setup
from setuptools.extension import Extension
import codecs
import os
import re


def local_file(filename):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), filename), 'r', 'utf-8'
    )

version = re.search(
    "^__version__ = \((\d+), (\d+), (\d+)\)",
    local_file(os.path.join('quantlibapp', '__init__.py')).read(),
    re.MULTILINE
).groups()


setup(
    name="quantlibapp",
    version='.'.join(version),
    author='Jeremy Wang @ Quantransform',
    author_email='j.wang@quantransform.co.uk',
    description='A framework for Application of QuantLib',
    keywords='python quantlib',
    url='https://www.quantransform.co.uk',
    install_requires=[
        'QuantLib-Python==1.12',
        'pandas==0.22.0',
        'scipy==1.0.1',
        'qgrid',
    ],
    packages=['quantlibapp'],
    long_description=local_file('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python'
    ],
)