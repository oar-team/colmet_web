# coding: utf8
from setuptools import setup, find_packages
from colmet.web import VERSION
from os import path as op


try:
    here = op.dirname(__file__)
    with open(op.abspath(op.join(here, 'requirements.txt'))) as f:
        requirements = f.read().split('\n')
except:
    requirements = []


setup(
    name='colmet-web',
    version=VERSION,
    url='http://oar.imag.fr/',
    description='Visualizing the collected metrics about OAR jobs',
    author='Salem Harrache',
    author_email='salem.harrache@inria.fr',
    packages=find_packages(),
    license="GNU GPL",
    platforms='any',
    install_requires=requirements,
    zip_safe=False,
    include_package_data=True,
)
