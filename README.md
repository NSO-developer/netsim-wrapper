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
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 list
ncs-netsim list for  /Users/kkotari/idea/ncs-netsim2/netsim

name=xr0 netconf=12022 snmp=11022 ipc=5010 cli=10022 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr0
name=xr1 netconf=12023 snmp=11023 ipc=5011 cli=10023 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr1
name=xr2 netconf=12024 snmp=11024 ipc=5012 cli=10024 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr2
name=xr3 netconf=12025 snmp=11025 ipc=5013 cli=10025 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr3
⋊> ~/k/i/ncs-netsim2 on master ◦
```

```bash
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 delete-devices xr1 xr3
[ INFO ] :: [ ncs-netsim ] :: deleting device: xr1
[ INFO ] :: [ ncs-netsim ] :: deleting device: xr3
⋊> ~/k/i/ncs-netsim2 on master ◦
```

```bash
⋊> ~/k/i/ncs-netsim2 on master ◦  ncs-netsim2 list
ncs-netsim list for  /Users/kkotari/idea/ncs-netsim2/netsim

name=xr0 netconf=12022 snmp=11022 ipc=5010 cli=10022 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr0
name=xr2 netconf=12024 snmp=11024 ipc=5012 cli=10024 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr2
⋊> ~/k/i/ncs-netsim2 on master ◦
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

- **Question:** I am seeing following error ./env.sh: line 12: export: `Fusion.app/Contents/Public:/Applications/Wireshark.app/Contents/MacOS': not a valid identifier
 **Answer:** We recommend to check your env path as recommended in following [link](https://apple.stackexchange.com/questions/313520/how-can-one-use-etc-paths-d-to-add-a-path-with-spaces-in-it-to-path)

## Bug Tracker and Support

- Please report any suggestions, bug reports, or annoyances with ncs-netsim2 through the [Github bug tracker](https://github.com/kirankotari/ncs-netsim2/issues).

## License and Copyright

- ncs-netsim2 is licensed [MIT](http://opensource.org/licenses/mit-license.php) *2019-2020*

   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Author and Thanks

ncs-netsim2 was developed by [Kiran Kumar Kotari](https://github.com/kirankotari)
