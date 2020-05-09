# Ncs-Netsim2

ncs-netsim2 is a powerful simulator tool in python. It's a wrapper of ncs-netsim tool with added features

- [Introduction](#introduction)
- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
- [Help](#help)
- [FAQ](#faq)
- [Bug Tracking and Support](#bug-tracking-and-support)
- [License and Copyright](#license-and-copyrights)
- [Author and Thanks](#author-and-thanks)

## Introduction

ncs-netsim, It's an powerful tool to build an simulated network envrinoments for Network Service Orchestrator (NSO) it's also called as NCS - NSO. In these network topologies we can test the network configuations based on the need as per the usecase.

ncs-netsim2, We added very important features like deleting a device from the topology, etc. Due to lack of this feature we were used to keep un-wanted devices in the network envrinoments which consumes computer/vm resources and a lot of time to manage manuall to stop the un-wanted devices or re-create the complete topology which is time taking.

### **How to delete a device(s) from network topology?**

```bash
kkotari# ncs-netsim2 list
TODO: need to add

kkotari# ncs-netsim2 (delete-device <deviceName>)
TODO: need to add

kkotari# ncs-netsim2 list
TODO: need to add
```

## Pre-requisites

- ncs-netsim command must be reconginsed by the terminal.
- ncs-netsim2 supports both trains of **python** `2.7+ and 3.1+`, the OS should not matter.

## Installation and Downloads

The best way to get ncs-netsim2 is with setuptools or pip. If you already have setuptools, you can install as usual:

`python -m pip install ncs-netsim2`

Otherwise download it from PyPi, extract it and run the `setup.py` script

`python setup.py install`

If you're Interested in the source, you can always pull from the github repo:

- From github `git clone https://github.com/kirankotari/ncs-netsim2.git`

## Help

```bash
kkotari# ncs-netsim2 --help
Usage ncs-netsim2  [--dir <NetsimDir>]
                      device <DeviceNames>
                      -v | --version
                      -h | --help

See manpage for ncs-netsim2 for more info. NetsimDir is optional
and defaults to ./netsim, any netsim directory above in the path,
or $NETSIM_DIR if set.
```

## FAQ

- **Question:** Do I need to install ncs-netsim too?  
 **Answer:** Not really, ncs-netsim tool comes along with NSO. If you are working NSO it's won't be a problem.  

- **Question:** Is python mandatory for ncs-netsim2?  
 **Answer:** Yes, we had wrote the complete logic in python, and wanted to make NSO version independent tool.  

- **Question:** Is ncs-netsim2 backword compatable on other commands?  
 **Answer:** We recommend to use ncs-netsim2 commands instead of ncs-netsim. However couple of commands are still backward compatable ie. `ncs-netsim list`, etc.  

## Bug Tracker and Support

- Please report any suggestions, bug reports, or annoyances with ncs-netsim2 through the [Github bug tracker](https://github.com/kirankotari/ncs-netsim2/issues).

## License and Copyright

- ncs-netsim2 is licensed [MIT](http://opensource.org/licenses/mit-license.php) *2019-2020*

   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Author and Thanks

ncs-netsim2 was developed by [Kiran Kumar Kotari](https://github.com/kirankotari)
