# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='OpenCV-with-Python-Series',
    version='0.1.0',
    description='OpenCV with Python examples from my Youtube series: TODO',
    long_description=readme,
    author='Johannes Schuck',
    author_email='jojoschuck@gmail.com',
    url='https://github.com/joschuck/OpenCV-with-Python-Series',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)