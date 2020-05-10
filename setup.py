from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
reqs = []

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, '.version'), encoding='utf-8') as f:
    version = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    read_lines = f.readlines()
    reqs = [each.strip() for each in read_lines]

setup(
    name = 'ncs-netsim2',
    version = version,
    description = "ncs-netsim2 is a powerful simulator tool in python. It's a wrapper of ncs-netsim tool with added features",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/kirankotari/ncs-netsim2.git',
    author = 'Kiran Kumar Kotari',
    author_email = 'kirankotari@live.com',
    entry_points={
        'console_scripts': [
            'ncs-netsim2 = ncs-netsim2.netsim2:run'
        ],
    },
    install_requires=reqs,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    keywords = 'Ncs-Netsim, Ncs-Netsim2, delete netsim device',
    packages = find_packages(where='.', exclude=['tests']),
    include_package_data=True,
)

