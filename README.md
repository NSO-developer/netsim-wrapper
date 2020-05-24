# Ncs-Netsim2

When an NSO Developer working on cloud space with devices like ENCS, CSP, etc. your business use case is to bring up a new device in the existing topology and configure day0 and day1 configurations.

This might be easy if you are working on real devices, but it won't be the case all the time due to its availability. The only option left with us is network simulators (ncs-netsim), but due to limitations of the ncs-netsim you need to be deviating from your business use case. Why? because you don't have the option to delete an ncs-netsim device.

ncs-netsim2 is a wrapper on top of ncs-netim with added features like delete-devices so that you need not deviate from your business use case. It's written in python and we opened the space to add more features to it.

- [Introduction](#introduction)
- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
- [Help](#help)
- [FAQ](#faq)
- [Bug Tracking and Support](#bug-tracking-and-support)
- [License and Copyright](#license-and-copyrights)
- [Author and Thanks](#author-and-thanks)

## Introduction

ncs-netsim, It's a powerful tool to build a simulated network environment for Network Service Orchestrator (NSO) it's also called as NCS - NSO. In these network topologies we can test the network configurations based on the need as per the use case.

ncs-netsim2, We added `delete-devices` feature not to deviate from the original business use case. On the way of achieving this we opened the space to add more features to it, like adding `update-ip`, `update-port`, etc. Today these features are not exposed to the cli, we need to update them manually in the configuration files. With these added features to ncs-netsim2 we can manage better and remove unwanted devices from time to time and to not consume disk space and memory.

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
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 --help
Usage ncs-netsim2  [--dir <NetsimDir>]
                  create-network <NcsPackage> <NumDevices> <Prefix> |
                  create-device <NcsPackage> <DeviceName>           |
                  add-to-network <NcsPackage> <NumDevices> <Prefix> |
                  add-device <NcsPackage> <DeviceName>  |
                  delete-devices <DeviceNames>          |
                  update-ip <DeviceName> <ip-address>               |
                  update-port <DeviceName> <type> <port-no>         |
                  delete-network                     |
                  [-a | --async]  start [devname]    |
                  [-a | --async ] stop [devname]     |
                  [-a | --async ] reset [devname]    |
                  [-a | --async ] restart [devname]  |
                  list                      |
                  is-alive [devname]        |
                  status [devname]          |
                  whichdir                  |
                  ncs-xml-init [devname]    |
                  ncs-xml-init-remote <RemoteNodeName> [devname] |
                  [--force-generic]                  |
                  packages                  |
                  netconf-console devname [XpathFilter] |
                  [-w | --window] [cli | cli-c | cli-i] devname |
                  get-port devname [ipc | netconf | cli | snmp] |
                  -v | --version            |
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
