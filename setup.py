#!/usr/bin/env python

import os
from pathlib import Path
from functools import reduce
from setuptools import setup
from setuptools import find_packages

with open('README.md', 'r', encoding='UTF-8') as fh:
    long_description = fh.read()


def find_package_data_in_folders(package_data_and_folders):
    initial_cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    package_data = {}
    local_cwd = os.getcwd()
    for pkg, folders in package_data_and_folders.items():
        pkg_path = reduce(lambda acc, elem: acc / elem, pkg.split('.'), Path())
        os.chdir(pkg_path.absolute())
        file_expansions = map(lambda elem: [str(p.relative_to(
            ".")) for p in Path().glob(elem) if p.is_file()], folders)
        files = [f for mapper in file_expansions for f in mapper]
        package_data[pkg] = files
        os.chdir(local_cwd)
    os.chdir(initial_cwd)
    return package_data


setup(
    name='Entree',
    version='0.1',
    description='Entree, the first automatic design flow for deploying the inference of Decision Tree ensembles over FPGAs at the network\'s edge',
    author='Andrea Damiani',
    author_email='andrea.damiani@polimi.it',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/necst/entree_aspdac22',
    packages=find_packages(),
    package_data=find_package_data_in_folders({
        'entree.backends.xilinxhls': ['firmware/**/*', 'hls-template/**/*', 'system-template/**/*', 'tools/**/*']
    }),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
    ]
)
