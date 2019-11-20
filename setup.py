#!/usr/bin/env python3
import uuid
from setuptools import setup, find_packages
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=uuid.uuid1())

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='fjelltopp-etl',
    version='0.0.1',
    long_description=__doc__,
    packages=['fjelltopp-etl'],
    include_package_data=True,
    zip_safe=False,
    install_requires=reqs,
    test_suite='etl.test',
    author='Tomek Sabała',
    author_email='tomek@fjelltopp.org',
    url='https://github.com/fjelltopp/fjelltopp-etl',
    download_url='https://github.com/fjelltopp/fjelltopp-etl/v_001.tar.gz',
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
