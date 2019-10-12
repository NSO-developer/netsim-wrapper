from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

with open(path.join(here, '.version'), encoding='utf-8') as f:
	version = f.read()

setup(
	name = 'ncs-netsim2',
	version = version,
	description = "Introducing a new command to delete the ncs-netsim devices.  It was a hardened when the feature was missing, We were forced to delete the complete simulated network and recreate again with the rest of devices.",
    long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/kirankotari/ncs-netsim2.git',
	author = 'Kiran Kumar Kotari',
	author_email = 'kirankotari@live.com',
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		],
	keywords = 'Netsim delete device',
	packages = find_packages(exclude=['tests']),
	package_dir = {'ncs-netsim2': 'ncs-netsim2'},
	package_data = {'ncs-netsim2': []},
)