# Ncs-Netsim2

ncs-netsim is a great tool, but it lack of following features which are developed as part of ncs-netsim2

- ncs-netsim2 features  
  - delete-devices \<device-names>
  - create-network-from [ yaml | json ] \<filename>
  - create-device-from [ yaml | json ] \<filename>
  - create-network-template [ yaml | json ]
  - create-device-template [ yaml | json ]
- upcoming features  
  - update-ip \<device-name> \<ip-address>
  - update-port \<device-name> \<type> \<port-no>

ncs-netsim2 is a wrapper on top of ncs-netsim with added features. It's written in python and we opened the space to add more features to it.

- [Introduction](#introduction)
- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
- [Features](#features)
- [Help](#help)
- [FAQ](#faq)
- [Bug Tracking and Support](#bug-tracking-and-support)
- [License and Copyright](#license-and-copyrights)
- [Author and Thanks](#author-and-thanks)

## Introduction

ncs-netsim, It's a powerful tool to build a simulated network environment for Network Service Orchestrator (NSO) it's also called as NCS - NSO. In these network topologies we can test the network configurations based on the need as per the use case.

ncs-netsim2, An open space to automate the ncs-netsim.

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

## Features

### Delete a device(s) from topology

existing device list

```bash
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 list
ncs-netsim list for  /Users/kkotari/idea/ncs-netsim2/netsim

name=xr0 netconf=12022 snmp=11022 ipc=5010 cli=10022 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr0
name=xr1 netconf=12023 snmp=11023 ipc=5011 cli=10023 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr1
name=xr2 netconf=12024 snmp=11024 ipc=5012 cli=10024 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr2
name=xr3 netconf=12025 snmp=11025 ipc=5013 cli=10025 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr3
⋊> ~/k/i/ncs-netsim2 on master ◦
```

deleting devices

```bash
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 delete-devices xr1 xr3
[ INFO ] :: [ ncs-netsim ] :: deleting device: xr1
[ INFO ] :: [ ncs-netsim ] :: deleting device: xr3
⋊> ~/k/i/ncs-netsim2 on master ◦
```

latest device list

```bash
⋊> ~/k/i/ncs-netsim2 on master ◦  ncs-netsim2 list
ncs-netsim list for  /Users/kkotari/idea/ncs-netsim2/netsim

name=xr0 netconf=12022 snmp=11022 ipc=5010 cli=10022 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr0
name=xr2 netconf=12024 snmp=11024 ipc=5012 cli=10024 dir=/Users/kkotari/idea/ncs-netsim2/netsim/xr/xr2
⋊> ~/k/i/ncs-netsim2 on master ◦
```

### Create Network/Device Template

Template to automate the Network/Device creation process.

```bash
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 create-network-template [yaml | json]
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 create-device-template [yaml | json]
```

which gives `template.json/yaml` file where you can update the files based on your need/requirement.

### Create Network/Device From Template

We are using the templates which are updated based on your requirement

```bash
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 create-network-from [yaml | json] <filename>
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 create-device-from [yaml | json] <filename>
```

### How to choose the Templates and How they look

These templates follows the same process of ncs-netsim, format is your choice

1. prefix based creation - `ncs-netsim2 create-network-template yaml`
2. name based creation - `ncs-netsim2 create-device-template yaml`

_Note:- So far we are not supporting combinations._

You can find the examples in the same directory start with `template-create-<...>.yaml/json`.

prefix-based

```yaml
ned-path: <path-to>/nso-local-lab/nso-run-5.2.1.2/packages
start: true
ncs_load: true
mode:
  prefix-based:
    cisco-ios-cli-6.56:
      count: 2
      prefix: ios-56-
    cisco-ios-cli-6.55:
      count: 2
      prefix: ios-55-
```

name-based

```yaml
ned-path: <path-to>/nso-local-lab/nso-run-5.2.1.2/packages
start: true
ncs_load: true
mode:
  name-based:
    cisco-ios-cli-6.56:
    - ios-56-name-100
    - ios-56-name-150
    cisco-ios-cli-6.55:
    - ios-55-name-200
    - ios-55-name-250
```

## Help

```bash
⋊> ~/k/i/ncs-netsim2 on master ◦ ncs-netsim2 --help
Usage ncs-netsim2  [--dir <NetsimDir>]
                  create-network-template [yaml | json]             |
                  create-network-from [yaml | json] <fileName>      |
                  create-network <NcsPackage> <NumDevices> <Prefix> |
                  create-device-template  [yaml | json]             |
                  create-device-from [yaml | json] <fileName>       |
                  create-device <NcsPackage> <DeviceName>           |
                  add-to-network <NcsPackage> <NumDevices> <Prefix> |
                  add-device <NcsPackage> <DeviceName>  |
                  delete-devices <DeviceNames>           |
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
 **Answer:** Not really, ncs-netsim tool comes along with NSO. If you are working with NSO it's won't be a problem.  

- **Question:** Is python mandatory for ncs-netsim2?  
 **Answer:** Yes, the library is written in python and we wanted not to be dependend on NSO versions.  

- **Question:** Is ncs-netsim2 backword compatable?  
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
