#!/usr/bin/env python3
import uuid
from setuptools import setup, find_packages

setup(
    name='fjelltopp-etl',
    version='0.0.2',
    long_description=__doc__,
    packages=['etl'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pandas==0.24.2",
        "watchtower==0.5.3",
        "sqlalchemy==1.3.0",
        "psycopg2==2.7.5",
        "boto3==1.9.32",
        "xmltodict==0.11.0",
        "requests==2.20.0"
    ],
    test_suite='etl.test',
    author='Tomek Sabała',
    author_email='tomek@fjelltopp.org',
    url='https://github.com/fjelltopp/fjelltopp-etl',
    download_url='',
    keywords = ['etl', 'dataprocessing', 'pandas'],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
