# Deleting NCS Netsim Devices (ncs-netsim-del <devices>)

- [Introduction](#introduction)
- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
- [FAQ](#faq)
- [Bug Tracking and Support](#bug-tracking-and-support)
- [License and Copyright](#license-and-copyrights)
- [Author and Thanks](#author-and-thanks)

## Introduction

Introducing a new command to delete the ncs-netsim devices.  It was a hardened when the feature was missing, We were forced to delete the complete simulated network and recreate again with the rest of devices.

- **List of NCS Netsim devices**

```python
λ ncs-netsim list
ncs-netsim list for  /Users/nso/nso-run/netsim

name=xr0 netconf=12022 snmp=11022 ipc=5010 cli=10022 dir=/Users/nso/nso-run/netsim/xr/xr0 
name=xr1 netconf=12023 snmp=11023 ipc=5011 cli=10023 dir=/Users/nso/nso-run/netsim/xr/xr1 
name=ios0 netconf=12024 snmp=11024 ipc=5012 cli=10024 dir=/Users/nso/nso-run/netsim/ios/ios0 
name=ios1 netconf=12025 snmp=11025 ipc=5013 cli=10025 dir=/Users/nso/nso-run/netsim/ios/ios1 
```

- **Deleting NCS Netsim devices**

```python
λ ncs-netsim-del device ios0 xr1
[ INFO ] :: [ ncs-netsim-del ] :: Device ios0 deleted successfully
[ INFO ] :: [ ncs-netsim-del ] :: Device xr1 deleted successfully
[ INFO ] :: [ ncs-netsim-del ] :: Done..!
λ 
```

- **Hep ncs-netsim-del**

```bash 
Usage ncs-netsim-del  [--dir <NetsimDir>]
                      device <DeviceNames>
                      -v | --version
                      -h | --help

See manpage for ncs-netsim-del for more info. NetsimDir is optional
and defaults to ./netsim, any netsim directory above in the path,
or $NETSIM_DIR if set.
```

## Pre-requisites

ncs-netsim-del supports both trains of **python** `2.7+ and 3.1+`, the OS should not matter.

## Installation and Downloads

The best way to get ncs-netsim-del is with setuptools or pip. If you already have setuptools, you can install as usual:

`python -m pip install ncs-netsim-del`

Otherwise download it from PyPi, extract it and run the `setup.py` script

`python setup.py install`

If you're Interested in the source, you can always pull from the github repo:

- From github `git clone https://github.com/kirankotari/ncs-netsim-del.git`

## FAQ

- **Question:** I want to use ncs-netsim-del with Python3, is that safe?  
 **Answer:** As long as you're using python 3.3 or higher, it's safe. I tested every release against python 3.1+, however python 3.1, 3.2 and 3.3 not running in continuous integration test.  

- **Question:** I want to use ncs-netsim-del with Python2, is that safe?  
 **Answer:** As long as you're using python 2.7 or higher, it's safe. I tested against python 2.7.

## Bug Tracker and Support

- Please report any suggestions, bug reports, or annoyances with ncs-netsim-del through the [Github bug tracker](https://github.com/kirankotari/ncs-netsim-del/issues).

## License and Copyright

- ncs-netsim-del is licensed [MIT](http://opensource.org/licenses/mit-license.php) *2019-2020*

   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Author and Thanks

ncs-netsim-del was developed by [Kiran Kumar Kotari](https://github.com/kirankotari)
