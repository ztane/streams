# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="streams",
    version="0.1",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    test_suite='streams',
    zip_safe=True
)
