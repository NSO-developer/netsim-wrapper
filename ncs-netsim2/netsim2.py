import sys
import re
import subprocess
import logging

from operator import methodcaller


class Netsim2:
    name = 'ncs-netsim2'
    command = ['ncs-netsim']
    options = []

    _instance = None
    _ncs_netsim_help = None
    _ncs_netsim_commands = []
    _ncs_netsim2_help = None
    _ncs_netsim2_commands = []
    __stdout = subprocess.PIPE
    __stderr = subprocess.PIPE
    __netsiminfo = '.netsiminfo'
    __netsimdelete = '.netsimdelete'

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
        self.__options
        pass

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

    def __run_ncs_netsim(self, command):
        self.logger.debug(f'command {command} running on ncs-netsim')
        p = subprocess.Popen(command, stdout=self.__stdout,
                             stderr=self.__stderr)
        out, err = p.communicate()
        out, err = out.decode('utf-8'), err.decode('utf-8')
        if err == '':
            self.logger.debug(f'no error detected on command {command} result')
            return out
        self.logger.error(
            f'an error occured while running command {command} in ncs-netsim')
        self.logger.error(f'message: {err}')
        if 'command not found' in err or 'Unknown command' in err:
            raise ValueError("ncs-netsim: command not found.")
        raise ValueError(
            "*** Unknown arg\n Try ncs-netsim2 --help to get usage text")

    @property
    def __get_ncs_netsim__help(self):
        if self._ncs_netsim_help:
            return
        try:
            output = self.__run_ncs_netsim(self.command + ['--help'])
        except ValueError as e:
            self.logger.error(f'{e.args}')
            self.__exit
        self._ncs_netsim_help = output

    def __get_ncs_netsim__commands(self, cmd_lst):
        try:
            output = self.__run_ncs_netsim(self.command + cmd_lst)
        except ValueError as e:
            self.logger.error(f'{e.args}')
            self.__exit
        print(output)
        self.__exit

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
        _commands += ['cli', 'cli-c', 'cli-i']
        return _commands

    def __get_ncs_netsim2__commands(self, cmd_lst):
        index = 0
        if cmd_lst[0] == '--dir':
            index = 2
        f = methodcaller(f"{cmd_lst[index].replace('-','_')}", cmd_lst)
        f(Netsim2)
        self.__exit

    @staticmethod
    def create_network(cmd_lst):
        print('I am in create network..!')
        pass

    @staticmethod
    def create_device(cmd_lst):
        print("I am in create device..!")
        pass

    @staticmethod
    def add_to_network(cmd_lst):
        print("I am in add to network..!")
        pass

    @staticmethod
    def delete_from_network(cmd_lst):
        print("I am in delete from network")
        pass

    @staticmethod
    def add_device(cmd_lst):
        print("I am in add device")

    @staticmethod
    def delete_device(cmd_lst):
        print("I am in delete device")

    @staticmethod
    def delete_network(cmd_lst):
        print("I am in delete network")

    def get_version(self):
        print("TODO: need to add code..")
        self.__exit

    def run_command(self, cmd_lst, netsim_dir=None):
        if cmd_lst[0] == '--dir':
            self.run_command(cmd_lst[2:], netsim_dir=cmd_lst[1])
        if cmd_lst[0] in self._version:
            self.get_version
        if cmd_lst[0] in self._help:
            self.help
        if cmd_lst[0] in self._ncs_netsim2_commands:
            if not netsim_dir:
                self.__get_ncs_netsim2__commands(cmd_lst)
            self.__get_ncs_netsim2__commands(['--dir', netsim_dir] + cmd_lst)
        else:
            if not netsim_dir:
                self.__get_ncs_netsim__commands(cmd_lst)
            self.__get_ncs_netsim__commands(['--dir', netsim_dir] + cmd_lst)

    @property
    def __options(self):
        if len(self.options):
            return
        self._help = ['-h', '--help']
        self._version = ['-v', '--version']
        self._ncs_netsim2_commands = ['create-network', 'create-device', 'add-to-network', 'add-device',
                                      'delete-from-network', 'delete-device', 'delete-network']
        self._ncs_netsim_commands = self.__fetch_ncs_netsim__commands
        self.options = self._help + self._version + \
            self._ncs_netsim2_commands + self._ncs_netsim_commands

    @property
    def help(self):
        if self._ncs_netsim2_help is not None:
            print(self._ncs_netsim2_help)
            self.__exit

        __match_replace = [['add-device <NcsPackage> <DeviceName> |', '''delete-from-network <DeviceNames>          |
                  add-device <NcsPackage> <DeviceName> |
                  delete-device <DeviceNames>      |'''],
                           ['get-port devname [ipc | netconf | cli | snmp]', '''get-port devname [ipc | netconf | cli | snmp] |
                  -v | --version            |
                  -h | --help'''],
                           ['ncs-netsim ', 'ncs-netsim2 ']]
        self._ncs_netsim2_help = self._ncs_netsim_help
        for each in __match_replace:
            self._ncs_netsim2_help = self._ncs_netsim2_help.replace(
                each[0], each[1])
        self.help


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
