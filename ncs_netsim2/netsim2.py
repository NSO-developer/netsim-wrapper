import sys
import re
import os
import copy
import json
import subprocess
import logging
import collections
from operator import methodcaller

class Netsim:
    name = 'ncs-netsim'
    command = ['ncs-netsim']
    options = []
    netsim_dir = 'netsim'

    _instance = None
    _ncs_netsim_help = None

    __stdout = subprocess.PIPE
    __stderr = subprocess.PIPE

    _split = '#######'

    def __new__(cls, log_level=logging.INFO, log_format=None, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, log_level=logging.INFO, log_format=None, *args, **kwargs):
        # logger setup
        self.__format = log_format
        self.logger = self.__set_logger_level(log_level)

        # pre-req
        self.__get_ncs_netsim__help
        self._options

    def __set_logger_level(self, log_level):
        if self.__format is None:
            self.__format = '[ %(levelname)s ] :: [ %(name)s ] :: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level,
                            format=self.__format, datefmt=None)
        logger = logging.getLogger(self.name)
        logger.setLevel(log_level)
        return logger

    def __del__(self):
        self._instance = None

    @property
    def __exit(self):
        sys.exit()

    @property
    def __get_ncs_netsim__help(self):
        if self._ncs_netsim_help:
            return
        try:
            output = self._run_command(self.command + ['--help'])
        except ValueError as e:
            self.logger.error(e)
            self.__exit
        self._ncs_netsim_help = output

    @property
    def _options(self):
        if len(self.options):
            return
        self.options = self.__fetch_ncs_netsim__commands

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

    def _run_command(self, command):
        self.logger.debug(f"command `{' '.join(command)}` running on ncs-netsim")
        p = subprocess.Popen(command, stdout=self.__stdout,
                             stderr=self.__stderr)
        out, err = p.communicate()
        out, err = out.decode('utf-8'), err.decode('utf-8')
        if err == '' or 'env.sh' in err:
            self.logger.debug(f"`{' '.join(command)}` ran successfully")
            return out
        self.logger.error(f"an error occured while running command `{' '.join(command)}`")
        self.logger.error(f'message: {err}')
        if 'command not found' in err or 'Unknown command' in err:
            raise ValueError("command not found.")
        raise ValueError("try ncs-netsim2 --help")

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

    def run_ncs_netsim__command(self, cmd_lst, print_output=True):
        try:
            output = self._run_command(self.command + cmd_lst)
        except ValueError as e:
            self.logger.error(e)
            self.__exit
        # need to print
        if print_output:
            print(output.rstrip('\n'))
        return output

    def read_netsim(self, path):
        data = open(path).read().split(self._split)
        self.__netsim_devices_created_by
        return self._netsim_device_mapper(data)


class Netsim2:
    name = 'ncs-netsim2'
    options = []
    version = '2.0.3'

    _instance = None
    _ncs_netsim2_help = None
    _ncs_netsim2_commands = []
    __netsiminfo = '.netsiminfo'
    __netsimdelete = '.netsimdelete'

    def __new__(cls, log_level=logging.INFO, log_format=None, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, log_level=logging.INFO, log_format=None, *args, **kwargs):
        self.__netsim = Netsim(log_level, log_format)
        self.logger = self.__netsim.logger
        self._options

    def __del__(self):
        self._instance = None

    @property
    def __exit(self):
        sys.exit()

    @property
    def _options(self):
        if len(self.options):
            return
        self._help = ['-h', '--help']
        self._version = ['-v', '--version']
        self._ncs_netsim2_commands = ['create-network', 'create-device', 'add-to-network',
                                      'add-device', 'delete-devices', 'delete-network']
        self.options = self._help + self._version + \
            self._ncs_netsim2_commands + self.__netsim.options

    @property
    def help(self):
        if self._ncs_netsim2_help is not None:
            # need to print
            print(self._ncs_netsim2_help)
            self.__exit

        __match_replace = [['add-device <NcsPackage> <DeviceName> |', '''add-device <NcsPackage> <DeviceName>  |
                  delete-devices <DeviceNames>           |'''],
                           ['get-port devname [ipc | netconf | cli | snmp]', '''get-port devname [ipc | netconf | cli | snmp] |
                  -v | --version            |
                  -h | --help'''],
                           ['ncs-netsim ', 'ncs-netsim2 ']]
        self._ncs_netsim2_help = self.__netsim._ncs_netsim_help
        for each in __match_replace:
            self._ncs_netsim2_help = self._ncs_netsim2_help.replace(each[0], each[1])
        self.help

    @property
    def get_version(self):
        # need to print
        print(f'ncs-netsim2 version {self.version}')
        self.__exit

    def _create_network(self, cmd_lst):
        self.__netsim.run_ncs_netsim__command(cmd_lst)
        self.__create_file(self.__netsim_path)
        # self.__update_netsimdelete_on_create_network # nomore used, it's empty on create..

    def _create_device(self, cmd_lst):
        self.__netsim.run_ncs_netsim__command(cmd_lst)
        self.__create_file(self.__netsim_path)

    def _add_to_network(self, cmd_lst):
        _command = 'add-to-network'
        self.__netsim2_add_devices(cmd_lst, _command)

    def _add_device(self, cmd_lst):
        _command = 'add-device'
        self.__netsim2_add_devices(cmd_lst, _command)

    def _delete_devices(self, cmd_lst):
        if len(cmd_lst) <= 3:
            raise ValueError("no device names found")

        __netsim2_device_mapper = self.read_netsim2(self.__netsim_path)
        path = self.__netsim_path.replace(self.__netsimdelete, self.__netsiminfo)
        __netsim_device_mapper = self.__netsim.read_netsim(path)

        for each in cmd_lst[3:]:
            if each not in __netsim_device_mapper:
                self.logger.error(f"device {each} not exist")
                self.__exit
            __netsim2_device_mapper[each] = __netsim_device_mapper[each]
            self.__remove_device_from_netsim(self.__netsim_path, each, __netsim_device_mapper[each])
            del __netsim_device_mapper[each]

        json.dump(__netsim2_device_mapper, open(self.__netsim_path, 'w'))
        self.__netsim._dump_netsim_mapper(path, __netsim_device_mapper)

    def _delete_network(self, cmd_lst):
        # automatically deleted .netsimdelete file
        self.__netsim.run_ncs_netsim__command(cmd_lst, print_output=False)

    def __run_ncs_netsim2__command(self, cmd_lst):
        self.__netsim_path = f'{cmd_lst[1]}/{self.__netsimdelete}'
        f = methodcaller(f"_{cmd_lst[2].replace('-','_')}", self, cmd_lst)
        try:
            f(Netsim2)
        except ValueError as e:
            self.logger.error(e)
        self.__exit

    def __create_file(self, path):
        if not os.path.exists(path):
            with open(path, "w") as fp: 
                json.dump({}, fp)

    def __delete_file(self, path):
        if os.path.exists(path):
            os.remove(path)

    def __remove_device_from_netsim(self, path, device, device_mapper):
        path = os.path.abspath(path.replace(self.__netsim_path.split('/')[-1], ''))
        if device_mapper['created_by'] == 'add-device':
            cmd_lst = ['rm', '-rf', f"{path}/{device_mapper['parent']}"]
        elif len(list(filter(os.path.isdir, os.listdir(path)))) == 1:
            cmd_lst = ['rm', '-rf', f"{path}/{device_mapper['parent']}"]
        else:
            cmd_lst = ['rm', '-rf', f"{path}/{device_mapper['parent']}/{device}"]
        self.__run_os_command(cmd_lst, print_output=False)
        self.logger.info(f'deleting device: {device}')

    def __run_os_command(self, cmd_lst, print_output=True):
        try:
            output = self.__netsim._run_command(cmd_lst)
        except Exception as e:
            self.logger.error(e)
        # need to print
        if print_output:
            print(output)

    def __fetch_device_prefix(self, mapper_dict, created_by):
        prefix = set([i['prefix'] for i in mapper_dict.values() if i['created_by'] in created_by])
        return prefix

    def __rstrip_digits(self, given_string):
        return given_string.rstrip('1234567890')

    def __check_is_valid_prefix(self, current_prefix, command):
        __full_prefix = set()

        created_by=['add-device'] if command == 'add-to-network' else ['add-to-network']
        __netsim2_prefix = self.__fetch_device_prefix(self.__netsim2_device_mapper, created_by)
        __netsim_prefix = self.__fetch_device_prefix(self.__netsim_device_mapper, created_by)
        __full_prefix.update(__netsim_prefix, __netsim2_prefix)

        if command == 'add-to-network':
            for each in __full_prefix:
                if each.startswith(current_prefix) and each[len(current_prefix):].isdigit():
                    raise ValueError(f"the prefix can't be part of existing/deleted devices via {created_by} command")
        if command == 'add-device':
            for each in __full_prefix:
                if current_prefix.startswith(each) and current_prefix[len(each):].isdigit():
                    raise ValueError(f"the prefix can't be part of existing/deleted devices via {created_by} command")
        return True

    def __refactor_netsiminfo(self, path):
        # reading and removing the unwanted data from netsiminfo
        __netsim_device_mapper = self.__netsim.read_netsim(path)
        for each_key in self.__netsim2_device_mapper:
            if each_key in __netsim_device_mapper:
                del __netsim_device_mapper[each_key]
        self.__netsim._dump_netsim_mapper(path, __netsim_device_mapper)

    def __netsim2_add_devices(self, cmd_lst, _command):
        _current_prefix = cmd_lst[-1]

        path = self.__netsim_path.replace(self.__netsimdelete, self.__netsiminfo)
        self.__netsim_device_mapper = self.__netsim.read_netsim(path)
        self.__netsim2_device_mapper = self.read_netsim2(self.__netsim_path)

        # validating cross-prefix checks
        if self.__check_is_valid_prefix(_current_prefix, _command):
            if len(self.__netsim2_device_mapper) == 0:
                self.__netsim.run_ncs_netsim__command(cmd_lst)
                self.__exit

            _prefix = self.__fetch_device_prefix(self.__netsim2_device_mapper, [_command])
            self.__netsim_device_mapper.update(self.__netsim2_device_mapper)
            self.__netsim_device_mapper = collections.OrderedDict(sorted(self.__netsim_device_mapper.items(), key=lambda d: d[1]['netconf_ssh_port']))

            # if the prefix is not under delete-devices
            if _current_prefix not in _prefix:
                self.__netsim._dump_netsim_mapper(path, self.__netsim_device_mapper)
                self.__netsim.run_ncs_netsim__command(cmd_lst)

                # removing the unwanted data
                self.__refactor_netsiminfo(path)

            else:
                __netsim2_device_mapper_temp = dict(filter(lambda d: d[1]['prefix'] == _current_prefix, self.__netsim2_device_mapper.items()))
                __netsim2_device_mapper_temp = collections.OrderedDict(sorted(__netsim2_device_mapper_temp.items(), key=lambda d: d[1]['netconf_ssh_port']))

                if _command == 'add-to-network':
                    self.__netsim2_restore_devices(path, cmd_lst, __netsim2_device_mapper_temp)
                else:
                    self.__netsim2_restore_device(path, cmd_lst, __netsim2_device_mapper_temp)

    def __netsim2_restore_device(self, path, cmd_lst, __netsim2_device_mapper_temp):
        for k,v in __netsim2_device_mapper_temp.items():
            __temp = dict(filter(lambda d: int(d[1]['netconf_ssh_port']) < int(v['netconf_ssh_port']), self.__netsim_device_mapper.items()))
            self.__netsim._dump_netsim_mapper(path, __temp)
            self.__netsim.run_ncs_netsim__command(cmd_lst)
            del self.__netsim2_device_mapper[k]
            break

        self.__netsim._dump_netsim_mapper(path, self.__netsim_device_mapper)
        # removing the unwanted data
        self.__refactor_netsiminfo(path)
        json.dump(self.__netsim2_device_mapper, open(self.__netsim_path, 'w'))

    def __netsim2_restore_devices(self, path, cmd_lst, __netsim2_device_mapper_temp):
        __total_devices = int(cmd_lst[-2])
        if __total_devices <= 0:
            self.logger.error(f'no. of devices need to be > 0')
            self.__exit

        for k,v in __netsim2_device_mapper_temp.items():
            __temp = dict(filter(lambda d: int(d[1]['netconf_ssh_port']) < int(v['netconf_ssh_port']), self.__netsim_device_mapper.items()))
            self.__netsim._dump_netsim_mapper(path, __temp)
            cmd_lst[-2] = '1'
            self.__netsim.run_ncs_netsim__command(cmd_lst)
            del self.__netsim2_device_mapper[k]
            __total_devices -= 1
            if __total_devices == 0:
                break

        self.__netsim._dump_netsim_mapper(path, self.__netsim_device_mapper)
        if __total_devices > 0:
            cmd_lst[-2] = str(__total_devices)
            self.__netsim.run_ncs_netsim__command(cmd_lst)

        # removing the unwanted data
        self.__refactor_netsiminfo(path)
        json.dump(self.__netsim2_device_mapper, open(self.__netsim_path, 'w'))

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
            netsim_dir = self.__netsim.netsim_dir
        
        if cmd_lst[0] in self._ncs_netsim2_commands:
            self.__run_ncs_netsim2__command(['--dir', netsim_dir] + cmd_lst)
        else:
            self.__netsim.run_ncs_netsim__command(['--dir', netsim_dir] + cmd_lst)
            self.__exit

    def read_netsim2(self, path):
        if os.path.exists(path):
            with open(path, 'r') as fp:
                data = json.load(fp)
            return data
        return {}


def run():
    obj = Netsim2()
    if len(sys.argv) >= 2:
        if sys.argv[1] not in obj.options:
            obj.help
        obj.run_command(sys.argv[1:])
    else:
        obj.help


if __name__ == "__main__":
    run()

