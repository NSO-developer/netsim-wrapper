import sys
import re
import os
import copy
import json
import yaml
import subprocess
import logging
import collections
from operator import methodcaller


class Utils:
    name = 'utils'

    _instance = None
    def __new__(cls, log_level=logging.INFO, log_format=None):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, log_level=logging.INFO, log_format=None, *args, **kwargs):
        self.__format = log_format
        self.current_path = os.path.abspath('.')
        self.logger = self.__set_logger_level(log_level)
        self._setup_yaml

    def __set_logger_level(self, log_level):
        if self.__format is None:
            self.__format = '[ %(levelname)s ] :: [ %(name)s ] :: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level,
                            format=self.__format, datefmt=None)
        logger = logging.getLogger(self.name)
        logger.setLevel(log_level)
        return logger

    @property
    def _setup_yaml(self):
        represent_dict_order = lambda self, data: \
        self.represent_mapping(
            'tag:yaml.org,2002:map', 
            data.items()
        )
        yaml.add_representer(collections.OrderedDict, represent_dict_order)

    def __del__(self):
        self._instance = None

    @property
    def _exit(self):
        sys.exit()

    def _dump_yaml(self, filename, template):
        try:
            with open(filename, 'w') as f:
                yaml.dump(template, f, sort_keys=False)
                self.logger.info("please, find the {} file in current directory".format(filename))
                self.logger.info("update based on your requirement")
        except EnvironmentError as e:
            self.logger.error("error on createing of template..")
            self.logger.error(e)

    def _dump_json(self, filename, template):
        try:
            with open(filename, 'w') as f:
                json.dump(template, f, indent=2)
                self.logger.info("please, find the {} file in current directory".format(filename))
                self.logger.info("update based on your requirement")
        except EnvironmentError as e:
            self.logger.error("error on createing of template..")
            self.logger.error(e)

    def _load_yaml(self, path):
        data = None
        try:
            with open(path) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except EnvironmentError as e:
            self.logger.error("error while loading the {} file..".format(path))
            self.logger.error(e)
        return data

    def _load_json(self, path):
        data = None
        try:
            with open(path) as f:
                data = json.load(f)
        except EnvironmentError as e:
            self.logger.error("error while loading the {} file..".format(path))
            self.logger.error(e)
        return data

    def _create_file(self, path):
        if not os.path.exists(path):
            with open(path, "w") as fp: 
                json.dump({}, fp)

    def _delete_file(self, path):
        if os.path.exists(path):
            os.remove(path)

    def _rstrip_digits(self, given_string):
        return given_string.rstrip('1234567890')

    def get_index(self, given_list, element):
        try:
            return given_list.index(element)
        except ValueError:
            return None

    def _load_path(self, cmd_lst, index, filename, filetype='yaml'):
        if len(cmd_lst) > index+1:
            path = cmd_lst[index+1]
        else:
            path = '{}/{}.{}'.format(self.current_path, filename, filetype)
        return path

    def _dump_xml(self, filename, xml_data):
        try:
            with open(filename, 'w') as fp:
                fp.write(xml_data)
        except EnvironmentError as e:
            self.logger.error("error on createing xml file")
            self.logger.error(e)

    def _run_bash_commands(self, cmd):
        try:
            subprocess.call(cmd, shell=True)
        except EnvironmentError as e:
            self.logger.error("failed to run command: {}".format(cmd))
            self.logger.error(e)

class Netsim(Utils):
    name = 'ncs-netsim'
    command = ['ncs-netsim']
    netsim_options = []
    netsim_dir = 'netsim'

    _instance = None
    _ncs_netsim_help = None

    __stdout = subprocess.PIPE
    __stderr = subprocess.PIPE

    _split = '#######'

    def __new__(cls, log_level=logging.INFO, log_format=None):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, log_level=logging.INFO, log_format=None, *args, **kwargs):
        Utils.__init__(self, log_level, log_format)

        # pre-req
        self.__get_ncs_netsim__help
        self._netsim_options

    @property
    def __get_ncs_netsim__help(self):
        if self._ncs_netsim_help:
            return
        try:
            output = self._run_command(self.command + ['--help'])
        except ValueError as e:
            self.logger.error(e)
            self._exit
        except FileNotFoundError as e:
            self.logger.error('ncs-netsim command not found. please source ncsrc file')
            self._exit
        self._ncs_netsim_help = output

    @property
    def _netsim_options(self):
        if len(self.netsim_options):
            return
        self.netsim_options = self.__fetch_ncs_netsim__commands

    @property
    def __fetch_ncs_netsim__commands(self):
        _commands = []
        _commands_regex = re.compile(r'^\s+([a-z-]+)')
        _options_regex = re.compile(
            r'^\s+\[(\S+)\s+\|\s+([a-z-]+).*?\]\s+([a-z]+)')
        for each in self._ncs_netsim_help.split('\n'):
            result = _commands_regex.match(each)
            if result:
                _commands += list(result.groups())
            result = _options_regex.match(each)
            if result:
                _commands += list(result.groups())
        _commands += ['cli', 'cli-c', 'cli-i', '--dir']
        return _commands

    @property
    def __netsim_devices_created_by(self):
        self._netsim_devices_created_by = {}
        data = self.run_ncs_netsim__command(['list'], print_output=False).split('\n')
        result = list(filter(lambda x: 'netconf' in x, data))
        for each in result:
            each = each.split('/')
            dev_name = each[-1].strip()
            if dev_name == each[-2]:
                self._netsim_devices_created_by[dev_name] = ['add-device', each[-2]]
            else:
                self._netsim_devices_created_by[dev_name] = ['add-to-network', each[-2]]

    @property
    def _build_network_template(self):
        template = collections.OrderedDict()
        template['ned-path'] = '<ned-path>'
        template['ned-compile'] = True
        template['start'] = True
        template['ncs_load'] = True
        template['authgroup'] = collections.OrderedDict()
        template['authgroup']['path'] = '<path>'
        template['authgroup']['config'] = ['<filename>']
        template['mode'] = collections.OrderedDict()
        template['mode']['prefix-based'] = collections.OrderedDict()
        template['mode']['prefix-based']['<ned-name>'] = collections.OrderedDict()
        template['mode']['prefix-based']['<ned-name>']['count'] = 2
        template['mode']['prefix-based']['<ned-name>']['prefix'] = '<prefix>'
        template['pre-config'] = True
        template['config-path'] = '<path>'
        template['config'] = []
        template['config'].append('<filename0>')
        template['config'].append('<filename1>')
        return template

    @property
    def _build_device_template(self):
        template = collections.OrderedDict()
        template['ned-path'] = '<ned-path>'
        template['ned-compile'] = True
        template['start'] = True
        template['ncs_load'] = True
        template['authgroup'] = collections.OrderedDict()
        template['authgroup']['path'] = '<path>'
        template['authgroup']['config'] = ['<filename>']
        template['mode'] = collections.OrderedDict()
        template['mode']['name-based'] = collections.OrderedDict()
        template['mode']['name-based']['<ned-name>'] = []
        template['mode']['name-based']['<ned-name>'].append('device1')
        template['mode']['name-based']['<ned-name>'].append('device2')
        template['pre-config'] = True
        template['config-path'] = '<path>'
        template['config'] = []
        template['config'].append('<filename0>')
        template['config'].append('<filename1>')
        return template

    def _run_command(self, command, throw_err=True):
        self.logger.debug("command `{}` running on ncs-netsim".format(' '.join(command)))
        p = subprocess.Popen(command, stdout=self.__stdout,
                             stderr=self.__stderr)
        out, err = p.communicate()
        out, err = out.decode('utf-8'), err.decode('utf-8')
        if err == '' or 'env.sh' in err:
            self.logger.debug("`{}` ran successfully".format(' '.join(command)))
            return out
        if throw_err:
            self.logger.error("an error occured while running command `{}`".format(' '.join(command)))
            self.logger.error('message: {}'.format(err))
            if 'command not found' in err or 'Unknown command' in err:
                raise ValueError("command not found.")
            raise ValueError("try netsim-wrapper --help")
        raise ValueError("{}\ntry netsim-wrapper --help".format(err))

    def _netsim_device_mapper(self, data):
        _netsim_mapper = collections.OrderedDict()
        for each_device in data:
            device = each_device.split('=')
            if len(device) > 1:
                device = device[1].split('\n')[0]
                _netsim_mapper[device] = self._netsim_device_keypair_mapper(device, each_device)
        return _netsim_mapper

    def _netsim_device_keypair_mapper(self, device, data):
        _mapper = {}
        for each_line in data.split('\n'):
            if len(each_line.split('[')) > 1:
                key = (each_line.split('[')[0]).strip(' ')
                value = each_line.split('=')[1]
                _mapper[key] = value
        _mapper['created_by'] = self._netsim_devices_created_by.get(device)[0]
        _mapper['parent'] = self._netsim_devices_created_by.get(device)[1]
        return _mapper

    def _dump_netsim_mapper(self, path, netsim_mapper):
        fp = open(path, 'w')
        fp.write('\n')
        index = 0
        for device_name, device_dict in netsim_mapper.items():
            fp.write('## device {}\n'.format(device_name))
            for key, value in device_dict.items():
                if key in ['created_by', 'parent']:
                    continue
                fp.write('{}[{}]={}\n'.format(key, index, value))
            fp.write('#######\n\n')
            index += 1
        fp.close()

    def run_ncs_netsim__command(self, cmd_lst, print_output=True, throw_err=True):
        try:
            output = self._run_command(self.command + cmd_lst, throw_err)
        except ValueError as e:
            if throw_err:
                self.logger.error(e)
                self._exit
            raise ValueError(e)
        # need to print
        if print_output:
            print(output.rstrip('\n'))
        return output

    def read_netsim(self, path):
        data = open(path).read().split(self._split)
        self.__netsim_devices_created_by
        return self._netsim_device_mapper(data)


class NetsimWrapper(Netsim):
    name = 'netsim-wrapper'
    options = []
    version = '3.0.1'

    _instance = None
    _netsim_wrapper_help = None
    _netsim_wrapper_commands = []
    __netsiminfo = '.netsiminfo'
    __netsimdelete = '.netsimdelete'
    __filename = 'template'

    def __new__(cls, log_level=logging.INFO, log_format=None, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, log_level=logging.INFO, log_format=None, *args, **kwargs):
        Netsim.__init__(self, log_level, log_format)
        self._options

    @property
    def _options(self):
        if len(self.options):
            return
        self._help = ['-h', '--help']
        self._version = ['-v', '--version']
        self._template_type = ['yaml', 'json']
        self._netsim_wrapper_commands = ['create-network', 'create-network-template',
        'create-network-from',  'create-device', 'create-device-template', 
        'create-device-from', 'add-to-network', 'add-device', 
        'delete-devices', 'delete-network', 'update-ip', 'update-port',
        'start', 'ncs-xml-init']
        self.options = self._help + self._version + \
            self._netsim_wrapper_commands + self.netsim_options

    @property
    def help(self):
        if self._netsim_wrapper_help is not None:
            # need to print
            print(self._netsim_wrapper_help)
            self._exit

        __match_replace = [
            ['create-network <NcsPackage> <NumDevices> <Prefix> |', 
            '''create-network-template [yaml | json]             |
                  create-network-from [yaml | json] <fileName>      |
                  create-network <NcsPackage> <NumDevices> <Prefix> |'''],
            ['create-device <NcsPackage> <DeviceName>           |',
            '''create-device-template  [yaml | json]             |
                  create-device-from [yaml | json] <fileName>       |
                  create-device <NcsPackage> <DeviceName>           |'''],
            ['add-device <NcsPackage> <DeviceName> |', '''add-device <NcsPackage> <DeviceName>  |
                  delete-devices <DeviceNames>           |'''],
            ['get-port devname [ipc | netconf | cli | snmp]', '''get-port devname [ipc | netconf | cli | snmp] |
                  -v | --version            |
                  -h | --help'''],
                           ['ncs-netsim ', 'netsim-wrapper ']]
        self._netsim_wrapper_help = self._ncs_netsim_help
        for each in __match_replace:
            self._netsim_wrapper_help = self._netsim_wrapper_help.replace(each[0], each[1])
        self.help

    @property
    def get_version(self):
        # need to print
        print('netsim-wrapper version {}'.format(self.version))
        self._exit

    def _create_network_template(self, cmd_lst):
        template = self._build_network_template
        if 'yaml' in cmd_lst:
            self._dump_yaml('{}.yaml'.format(self.__filename), template)
        elif 'json' in cmd_lst:
            self._dump_json('{}.json'.format(self.__filename), template)
        else:
            self.logger.error("invalid options entered..")
            self._help
            self._exit

    def _loading_from(self, cmd_lst):
        device_data = None
        yaml_index = self.get_index(cmd_lst, 'yaml')
        json_index = self.get_index(cmd_lst, 'json')

        # loading template
        if yaml_index:
            path = self._load_path(cmd_lst, yaml_index, self.__filename, 'yaml')
            device_data = self._load_yaml(path)
        elif json_index:
            path = self._load_path(cmd_lst, json_index, self.__filename, 'json')
            device_data = self._load_json(path)
        else:
            self.logger.error('invalid options entered..')
            self._help
            self._exit
        if device_data is None:
            self.logger.error('could not able to read the file..!')
            self._exit
        return device_data

    def _create_network_from(self, cmd_lst):
        device_data = self._loading_from(cmd_lst)
        device_lst = []
        start_device_lst = []

        if 'prefix-based' not in device_data['mode']:
            self.logger.error('today we support only prefix-based')
            self.logger.info('for name-based use `netsim-wrapper create-device-from`')

        # creating devices
        ned_path = device_data['ned-path']
        neds = device_data['mode']['prefix-based']
        for i, each_ned in enumerate(neds):
            if i == 0 and cmd_lst[1] == 'netsim':
                new_cmd_lst = cmd_lst[:2] + [
                    'create-network',
                    '{}/{}'.format(ned_path, each_ned), 
                    str(neds[each_ned]['count']),
                    neds[each_ned]['prefix']
                ]
                result = self._create_network(new_cmd_lst)
                start_device_lst += self.__get_device_names_not_alive(result)
                device_lst += self.__get_device_names(result)
            else:
                new_cmd_lst = cmd_lst[:2] + [
                    'add-to-network',
                    '{}/{}'.format(ned_path, each_ned), 
                    str(neds[each_ned]['count']),
                    neds[each_ned]['prefix']
                ]
                result = self._add_to_network(new_cmd_lst)
                start_device_lst += self.__get_device_names_not_alive(result)
                device_lst += self.__get_device_names(result)
        # starting devices
        start = device_data['start']
        if start:
            self.logger.info("about to start all devices")
            new_cmd_lst = cmd_lst[:2] + ['start']
            self._start(new_cmd_lst, start_device_lst)

        # loading devices to ncs
        self._load_devices_to_ncs(device_data, cmd_lst, device_lst)

        # pre-config is True
        self._load_per_config(device_data, device_lst)

    def _load_devices_to_ncs(self, device_data, cmd_lst, device_lst):
        ncs_load = device_data['ncs_load']
        if ncs_load:
            # auth-group
            authgroup = device_data.get('authgroup', {})
            if authgroup:
                self.logger.info('configuring authgroup')
                authgroup_path = authgroup.get('path', '')
                authgroup_files = authgroup.get('config', '')
                for each_file in authgroup_files:
                    each_file_path = '{}/{}'.format(authgroup_path, each_file)
                    new_cmd_lst = ['ncs_load', '-l', '-m', each_file_path]
                    try:
                        self._run_command(new_cmd_lst)
                    except ValueError as e:
                        self.logger.error(e)
                        self._exit

            # ned compile and reload
            ned_compile = device_data.get('ned-compile', None)
            if ned_compile:
                self.logger.info('compiling the neds')
                try:
                    mode = list(device_data['mode'].keys())[0]
                    neds = device_data['mode'][mode].keys()
                    for each_ned in neds:
                        ned_path = '{}/{}'.format(device_data['ned-path'], each_ned)
                        cmd = "make clean all | cd {}".format(ned_path)
                        self._run_bash_commands(cmd)
                    self.logger.info("about to run package reload force")
                    cmd = "echo 'packages reload' | ncs_cli -u admin -C"
                    self._run_bash_commands(cmd)
                except ValueError as e:
                    self.logger.error('failed at ned_compiling')
                    self.logger.error(e)
                except IndexError as e:
                    self.logger.error('failed to fetch the mode')
                    self.logger.error(e)

            # ncs_load
            self.logger.info("about to add devices to ncs")
            new_cmd_lst = cmd_lst[:2] + ['ncs-xml-init'] + device_lst
            result = self._ncs_xml_init(new_cmd_lst, print_output=False)
            self._dump_xml('{}/devices.xml'.format(self.current_path), result)
            new_cmd_lst = ['ncs_load', '-l', '-m', 'devices.xml']
            try:
                self._run_command(new_cmd_lst)
            except ValueError as e:
                self.logger.error(e)
                self._exit

    def _load_per_config(self, device_data, device_lst):
        pre_config = device_data.get('pre-config', None)
        if pre_config:
            # devices sync-from
            for each_device in device_lst:
                self.logger.info("about to sync-from device {}".format(each_device))
                cmd = "echo 'devices device {} sync-from' | ncs_cli -u admin -C".format(each_device)
                self._run_bash_commands(cmd)

            # apply the config
            config_path = device_data.get('config-path')
            for each_file in device_data['config']:
                self.logger.info('applying config {}'.format(each_file))
                file_path = '{}/{}'.format(config_path, each_file)
                new_cmd_lst = ['ncs_load', '-l', '-m', file_path]
                try:
                    self._run_command(new_cmd_lst)
                except ValueError as e:
                    self.logger.error(e)
                    self._exit

    def _create_network(self, cmd_lst):
        output = self.run_ncs_netsim__command(cmd_lst)
        self._create_file(self.__netsim_path)
        # self.__update_netsimdelete_on_create_network # nomore used, it's empty on create..
        return output

    def _create_device_template(self, cmd_lst):
        template = self._build_device_template
        if 'yaml' in cmd_lst:
            self._dump_yaml('{}.yaml'.format(self.__filename), template)
        elif 'json' in cmd_lst:
            self._dump_json('{}.json'.format(self.__filename), template)
        else:
            self.logger.error('invalid options entered..')
            self._help
            self._exit

    def _create_device_from(self, cmd_lst):
        device_lst = []
        start_device_lst = []
        device_data = self._loading_from(cmd_lst)

        if 'name-based' not in device_data['mode']:
            self.logger.error('today we support only name-based')
            self.logger.info('for prefix-based use `netsim-wrapper create-network-from`')

        # creating devices
        ned_path = device_data['ned-path']
        neds = device_data['mode']['name-based']
        for i, each_ned in enumerate(neds):
            for j, device_name in enumerate(neds[each_ned]):
                if i == 0 and j == 0 and cmd_lst[1] == 'netsim':
                    new_cmd_lst = cmd_lst[:2] + [
                        'create-device',
                        '{}/{}'.format(ned_path, each_ned), 
                        device_name
                    ]
                    self._create_device(new_cmd_lst)
                    device_lst.append(device_name)
                    start_device_lst.append(device_name)
                else:
                    new_cmd_lst = cmd_lst[:2] + [
                        'add-device',
                        '{}/{}'.format(ned_path, each_ned), 
                        device_name
                    ]
                    if self._add_device(new_cmd_lst) != False:
                        start_device_lst.append(device_name)
                    device_lst.append(device_name)

        # starting devices
        start = device_data['start']
        if start and len(start_device_lst):
            self.logger.info("about to start devices")
            new_cmd_lst = cmd_lst[:2] + ['start']
            self._start(new_cmd_lst, start_device_lst)
        self.logger.info("devices are running")

        # loading devices to ncs
        self._load_devices_to_ncs(device_data, cmd_lst, device_lst)

        # pre-config is True
        self._load_per_config(device_data,device_lst)

    def _create_device(self, cmd_lst):
        result = self.run_ncs_netsim__command(cmd_lst)
        self._create_file(self.__netsim_path)
        return result

    def _add_to_network(self, cmd_lst):
        _command = 'add-to-network'
        return self.__netsim_wrapper_add_devices(cmd_lst, _command)

    def _add_device(self, cmd_lst):
        _command = 'add-device'
        return self.__netsim_wrapper_add_devices(cmd_lst, _command)

    def _delete_devices(self, cmd_lst):
        if len(cmd_lst) <= 3:
            raise ValueError("no device names found")

        __netsim_wrapper_device_mapper = self.read_netsim_wrapper(self.__netsim_path)
        path = self.__netsim_path.replace(self.__netsimdelete, self.__netsiminfo)
        __netsim_device_mapper = self.read_netsim(path)

        for each in cmd_lst[3:]:
            if each not in __netsim_device_mapper:
                self.logger.error("device {} not exist".format(each))
                self._exit
            __netsim_wrapper_device_mapper[each] = __netsim_device_mapper[each]
            self.__remove_device_from_netsim(self.__netsim_path, each, __netsim_device_mapper[each])
            del __netsim_device_mapper[each]

        json.dump(__netsim_wrapper_device_mapper, open(self.__netsim_path, 'w'))
        self._dump_netsim_mapper(path, __netsim_device_mapper)

    def _update_ip(self, cmd_lst):
        self.logger.info('To be Added.')

    def _update_port(self, cmd_lst):
        self.logger.info('To be Added.')

    def _delete_network(self, cmd_lst):
        # automatically deleted .netsimdelete file
        self.run_ncs_netsim__command(cmd_lst, print_output=False)

    def _start(self, cmd_lst, device_lst=[]):
        start_index = self.get_index(cmd_lst, 'start')
        if len(cmd_lst) > start_index+1:
            # device name given by user..!
            self.run_ncs_netsim__command(cmd_lst)
            return
        if len(device_lst):
            for each in device_lst:
                self.run_ncs_netsim__command(cmd_lst + [each])
        else:
            result = self.run_ncs_netsim__command(
                cmd_lst[:-1] + ['is-alive'], print_output=False)
            device_lst = self.__get_device_names_from_is_alive(result)
            for each in device_lst:
                self.run_ncs_netsim__command(cmd_lst + [each])

    def _ncs_xml_init(self, cmd_lst, print_output=True):
        result = self.run_ncs_netsim__command(cmd_lst, print_output)
        return result

    def __run_netsim_wrapper__command(self, cmd_lst):
        self.__netsim_path = '{}/{}'.format(cmd_lst[1], self.__netsimdelete)
        f = methodcaller("_{}".format(cmd_lst[2].replace('-','_')), self, cmd_lst)
        try:
            f(NetsimWrapper)
        except ValueError as e:
            self.logger.error(e)
        self._exit

    def __get_device_names(self, data):
        devices_lst = []
        device_name_pattern = re.compile(r'DEVICE\s+(\S+)\s+(.*)')
        data = data.split('\n')
        for each_line in data:
            result = device_name_pattern.match(each_line)
            if result:
                devices_lst.append(result.group(1))
        return devices_lst

    def __get_device_names_not_alive(self, data):
        devices_lst = []
        device_name_pattern = re.compile(r'DEVICE\s+(\S+)\s+(.*)')
        data = data.split('\n')
        for each_line in data:
            result = device_name_pattern.match(each_line)
            if result:
                if result.group(2) == 'FAIL' or result.group(2) == 'CREATED':
                    devices_lst.append(result.group(1))
                elif result.group(2) == 'OK':
                    self.logger.info('device {} already started.'.format(result.group(1)))
        return devices_lst
    def __remove_device_from_netsim(self, path, device, device_mapper):
        path = os.path.abspath(path.replace(self.__netsim_path.split('/')[-1], ''))
        if device_mapper['created_by'] == 'add-device':
            cmd_lst = ['rm', '-rf', "{}/{}".format(path, device_mapper['parent'])]
        elif len(list(filter(os.path.isdir, os.listdir(path)))) == 1:
            cmd_lst = ['rm', '-rf', "{}/{}".format(path, device_mapper['parent'])]
        else:
            cmd_lst = ['rm', '-rf', "{}/{}/{}".format(path, device_mapper['parent'], device)]
        self.__run_os_command(cmd_lst, print_output=False)
        self.logger.info('deleting device: {}'.format(device))

    def __run_os_command(self, cmd_lst, print_output=True):
        try:
            output = self._run_command(cmd_lst)
        except Exception as e:
            self.logger.error(e)
        # need to print
        if print_output:
            print(output)

    def __fetch_device_prefix(self, mapper_dict, created_by):
        prefix = set([i['prefix'] for i in mapper_dict.values() if i['created_by'] in created_by])
        return prefix

    def __check_is_valid_prefix(self, current_prefix, command):
        __full_prefix = set()

        created_by=['add-device'] if command == 'add-to-network' else ['add-to-network']
        __netsim_wrapper_prefix = self.__fetch_device_prefix(self.__netsim_wrapper_device_mapper, created_by)
        __netsim_prefix = self.__fetch_device_prefix(self.__netsim_device_mapper, created_by)
        __full_prefix.update(__netsim_prefix, __netsim_wrapper_prefix)

        if command == 'add-to-network':
            for each in __full_prefix:
                if each.startswith(current_prefix) and each[len(current_prefix):].isdigit():
                    raise ValueError("the prefix can't be part of existing/deleted devices via {} command".format(created_by))
        if command == 'add-device':
            for each in __full_prefix:
                if current_prefix.startswith(each) and current_prefix[len(each):].isdigit():
                    raise ValueError("the prefix can't be part of existing/deleted devices via {} command".format(created_by))
        return True

    def __refactor_netsiminfo(self, path):
        # reading and removing the unwanted data from netsiminfo
        __netsim_device_mapper = self.read_netsim(path)
        for each_key in self.__netsim_wrapper_device_mapper:
            if each_key in __netsim_device_mapper:
                del __netsim_device_mapper[each_key]
        self._dump_netsim_mapper(path, __netsim_device_mapper)

    def __netsim_wrapper_add_devices(self, cmd_lst, _command):
        _current_prefix = cmd_lst[-1]

        path = self.__netsim_path.replace(self.__netsimdelete, self.__netsiminfo)
        self.__netsim_device_mapper = self.read_netsim(path)
        self.__netsim_wrapper_device_mapper = self.read_netsim_wrapper(self.__netsim_path)

        # validating cross-prefix checks
        if self.__check_is_valid_prefix(_current_prefix, _command):
            if len(self.__netsim_wrapper_device_mapper) == 0:
                try:
                    return self.run_ncs_netsim__command(cmd_lst, throw_err=False)
                except ValueError as e:
                    if 'already exists' in str(e):
                        self.logger.info('device {} already exist.!'.format(cmd_lst[4]))
                return False

            _prefix = self.__fetch_device_prefix(self.__netsim_wrapper_device_mapper, [_command])
            self.__netsim_device_mapper.update(self.__netsim_wrapper_device_mapper)
            self.__netsim_device_mapper = collections.OrderedDict(sorted(self.__netsim_device_mapper.items(), key=lambda d: d[1]['netconf_ssh_port']))

            # if the prefix is not under delete-devices
            if _current_prefix not in _prefix:
                self._dump_netsim_mapper(path, self.__netsim_device_mapper)
                try:
                    result = self.run_ncs_netsim__command(cmd_lst, throw_err=False)
                except ValueError as e:
                    print(e.args)
                    if 'already exists' in str(e):
                        self.logger.info('device {} already exist.!'.format(cmd_lst[4]))
                    return False

                # removing the unwanted data
                self.__refactor_netsiminfo(path)
                return result
            else:
                __netsim_wrapper_device_mapper_temp = dict(filter(lambda d: d[1]['prefix'] == _current_prefix, self.__netsim_wrapper_device_mapper.items()))
                __netsim_wrapper_device_mapper_temp = collections.OrderedDict(sorted(__netsim_wrapper_device_mapper_temp.items(), key=lambda d: d[1]['netconf_ssh_port']))

                if _command == 'add-to-network':
                    self.__netsim_wrapper_restore_devices(path, cmd_lst, __netsim_wrapper_device_mapper_temp)
                else:
                    self.__netsim_wrapper_restore_device(path, cmd_lst, __netsim_wrapper_device_mapper_temp)

    def __netsim_wrapper_restore_device(self, path, cmd_lst, __netsim_wrapper_device_mapper_temp):
        for k,v in __netsim_wrapper_device_mapper_temp.items():
            __temp = dict(filter(lambda d: int(d[1]['netconf_ssh_port']) < int(v['netconf_ssh_port']), self.__netsim_device_mapper.items()))
            self._dump_netsim_mapper(path, __temp)
            self.run_ncs_netsim__command(cmd_lst)
            del self.__netsim_wrapper_device_mapper[k]
            break

        self._dump_netsim_mapper(path, self.__netsim_device_mapper)
        # removing the unwanted data
        self.__refactor_netsiminfo(path)
        json.dump(self.__netsim_wrapper_device_mapper, open(self.__netsim_path, 'w'))

    def __netsim_wrapper_restore_devices(self, path, cmd_lst, __netsim_wrapper_device_mapper_temp):
        __total_devices = int(cmd_lst[-2])
        if __total_devices <= 0:
            self.logger.error('no. of devices need to be > 0')
            self._exit

        for k,v in __netsim_wrapper_device_mapper_temp.items():
            __temp = dict(filter(lambda d: int(d[1]['netconf_ssh_port']) < int(v['netconf_ssh_port']), self.__netsim_device_mapper.items()))
            self._dump_netsim_mapper(path, __temp)
            cmd_lst[-2] = '1'
            self.run_ncs_netsim__command(cmd_lst)
            del self.__netsim_wrapper_device_mapper[k]
            __total_devices -= 1
            if __total_devices == 0:
                break

        self._dump_netsim_mapper(path, self.__netsim_device_mapper)
        if __total_devices > 0:
            cmd_lst[-2] = str(__total_devices)
            self.run_ncs_netsim__command(cmd_lst)

        # removing the unwanted data
        self.__refactor_netsiminfo(path)
        json.dump(self.__netsim_wrapper_device_mapper, open(self.__netsim_path, 'w'))

    def run_command(self, cmd_lst, netsim_dir=None):
        if '--dir' in cmd_lst:
            _index = cmd_lst.index('--dir')
            _netsim_dir = cmd_lst[_index+1]
            del cmd_lst[_index:_index+2]
            self.run_command(cmd_lst, netsim_dir=_netsim_dir)

        if cmd_lst[0] in self._version:
            self.get_version
        if cmd_lst[0] in self._help:
            self.help

        if not netsim_dir:
            try:
                netsim_dir = self.run_ncs_netsim__command(
                    ['whichdir'], 
                    print_output=False, throw_err=False
                ).strip()
            except ValueError:
                netsim_dir = self.netsim_dir

        if cmd_lst[0] in self._netsim_wrapper_commands:
            self.__run_netsim_wrapper__command(['--dir', netsim_dir] + cmd_lst)
        else:
            self.run_ncs_netsim__command(['--dir', netsim_dir] + cmd_lst)
            self._exit

    def read_netsim_wrapper(self, path):
        if os.path.exists(path):
            with open(path, 'r') as fp:
                data = json.load(fp)
            return data
        return {}


def run():
    obj = NetsimWrapper()
    if len(sys.argv) >= 2:
        if sys.argv[1] not in obj.options:
            obj.help
        obj.run_command(sys.argv[1:])
    else:
        obj.help


if __name__ == "__main__":
    run()

