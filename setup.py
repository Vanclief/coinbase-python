# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gdaxpy',
    version='0.1.1',
    description='Unofficial Python3 library for the Gdax API',
    long_description=readme,
    author='Franco Valencia',
    author_email='franco.avalencia@gmail.com',
    url='https://github.com/Vanclief/gdax-python',
    license=license,
    packages=find_packages(exclude=('tests'))
)

