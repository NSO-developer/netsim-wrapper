import os
import sys
import logging
import subprocess
import random
import pathlib
from collections import OrderedDict


class NcsNetsim2:
    netsiminfo = '.netsiminfo'
    netsimdelete = '.netsimdelete'
    split = '#######'
    name = 'ncs-netsim'

    def __init__(self, path, log_level=logging.INFO, log_format=None):
        self.path = path
        self.netsim_path = './netsim'
        self.bash = '/bin/bash'
        self.libexec = '../libexec'
        self.format = log_format
        self.logger = self.set_logger_level(log_level)

    def set_logger_level(self, log_level):
        if self.format is None:
            self.format = '[ %(levelname)s ] :: [ %(name)s ] :: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level,
                            format=self.format, datefmt=None)
        logger = logging.getLogger(self.name)
        logger.setLevel(log_level)
        return logger

    def help(self):
        subprocess.run(
            [self.bash, '{}/{}/ncs-netsim2-help'.format(self.path, self.libexec)])

    def version(self, arg=None):
        if arg is None:
            subprocess.run(
                [self.bash, '{}/{}/ncs-netsim2---version'.format(self.path, self.libexec)])
        else:
            subprocess.run([self.bash, '{}/{}/ncs-netsim2---version'.format(self.path, self.libexec),
                            '--help'])

    def dir_path(self, path):
        self.netsim_path = path

    def del_devices(self, argv):
        netsim_config = self._read_netsiminfo()
        netsim_config_mapper = self._to_device_map(netsim_config)
        self._update_netsiminfo(netsim_config_mapper, argv, netsimdelete=True)
        self._del_devices(argv)

    def _to_device_map(self, config):
        _netsim_config = OrderedDict()
        for each_device in config:
            device = each_device.split('=')
            if len(device) > 1:
                device = device[1].split('\n')[0]
                _netsim_config[device] = each_device
        return _netsim_config

    def _to_keypair(self, device_config):
        device = {}
        for each_line in device_config.split('\n'):
            if len(each_line.split('[')) > 1:
                key = each_line.split('[')[0]
                value = each_line.split('=')[1]
                device[key] = value
        return device

    def _del_devices(self, devices, ignore=False):
        for device in devices:
            try:
                subprocess.Popen(
                    'rm -rf {}/*/{}'.format(self.netsim_path, device), shell=True)
                self.success(device)
            except Exception:
                if not ignore:
                    self.error_device(device)
                    exit(-1)
        self.logger.info('Done..!')

    def _read_netsiminfo(self, file=None):
        if file is None:
            file = self.netsiminfo
        try:
            data = open('{}/{}'.format(self.netsim_path, file)).read()
            data = data.split(self.split)
            return data
        except IOError:
            self.file_not_found()
            exit(-1)

    def _update_netsiminfo(self, config_mapper, device_lst=[], netsimdelete=False):
        exit_flag = 0
        fp = open('{}/{}'.format(self.netsim_path, self.netsimdelete), 'a+')
        for each_device in device_lst:
            if each_device in config_mapper:
                if netsimdelete:
                    fp.write(config_mapper[each_device].replace(
                        '\n\n\n', '\n'))
                    fp.write(self.split)
                    fp.write('\n')
                del config_mapper[each_device]
            else:
                exit_flag = 1
                self.error_device(each_device)
        fp.close()

        if exit_flag:
            exit(-1)

        for device, data in config_mapper.items():
            config_mapper[device] = self._to_keypair(data)

        self._write_netsiminfo(config_mapper)

    def _write_netsiminfo(self, config):
        fp = open('{}/{}'.format(self.netsim_path, self.netsiminfo), 'w')
        fp.write('\n')
        index = 0
        for device_name, device_dict in config.items():
            fp.write('## device {}\n'.format(device_name))
            for key, value in device_dict.items():
                fp.write('{}[{}]={}\n'.format(key, index, value))
            fp.write('#######\n\n')
            index += 1
        fp.close()

    def file_not_found(self):
        return self.logger.error("netsim configuration file not found at {}".format(self.netsim_path))

    def success(self, device, operation='deleted'):
        return self.logger.info("Device {} {} successfully".format(device, operation))

    def error(self, msg=None):
        if msg:
            return self.logger.error("Arguments mismatch, please check ncs-netsim2 --help")
        return self.logger.error(msg)

    def error_device(self, device):
        return self.error("Device {} details not found..!".format(device))

    def _is_network_empty(self):
        data = self._read_netsiminfo()
        if len(data) >= 1:
            if '##' not in data[0]:
                return True
        return False

    def _is_cmd_in_args(self, cmd, args):
        for each in args:
            if cmd in each:
                return True
        return False

    def _is_add_to_network_in_args(self, args):
        return self._is_cmd_in_args('add-to-network', args)

    def _is_delete_network_in_args(self, args):
        return self._is_cmd_in_args('delete-device', args)

    def _add_devices_to_empty_network(self, args):
        tmp = '_tmp{}'.format(random.randrange(12022, 13022))
        subprocess.run(['mv', self.netsim_path, self.netsim_path + tmp])
        subprocess.run(['ncs-netsim', 'create-network'] +
                       [each for each in args])
        subprocess.run(['cp', '-Rn', self.netsim_path + tmp, self.netsim_path])
        subprocess.run(['rm', '-rf', self.netsim_path + tmp])
        subprocess.run(
            ['rm', '-rf', '{}/{}'.format(self.netsim_path, self.netsimdelete)])

    def _fetch_device_ports(self, data):
        _device_ports = {}
        for key, device in data.items():
            try:
                _device_ports[key] = device.split('netconf_ssh_port')[
                    1].split('=')[1].split('\n')[0]
            except IndexError:
                self.error(
                    "Couldn't able to find the ssh port of netsim devices")
        _device_ports_sorted = OrderedDict(
            sorted(_device_ports.items(), key=lambda kv: kv[1]))
        return _device_ports_sorted

    def _add_devices_to_network(self, args):
        file_path = pathlib.Path(
            '{}/{}'.format(self.netsim_path, self.netsimdelete))
        if file_path.exists():
            # Reading Netsiminfo
            netsiminfo_data = self._read_netsiminfo()
            netsiminfo_mapper = self._to_device_map(netsiminfo_data)
            # Reading Netsimdelete
            netsimdelete_data = self._read_netsiminfo(self.netsimdelete)
            netsimdelete_mapper = self._to_device_map(netsimdelete_data)
            netsimdelete_keys = list(netsimdelete_mapper.keys())

            # Devices created and deleted so far
            netsim_mapper = OrderedDict()
            netsim_mapper.update(netsiminfo_mapper)
            netsim_mapper.update(netsimdelete_mapper)
            netsim_keys = self._fetch_device_ports(netsim_mapper)
            netsim_mapper_sorted = OrderedDict(
                (key, netsim_mapper[key]) for key in netsim_keys)

            # NOTE: changed the list from netsim_keys to netsimdelete_keys
            if any(args[3] in key for key in netsimdelete_keys) is False:
                self.logger.debug(
                    "Patter {} not found in Deleted Devices".format(args[3]))
                self._update_netsiminfo(netsim_mapper_sorted)
                self._add_netsim_devices(args)
                netsiminfo_data = self._read_netsiminfo()
                netsiminfo_mapper = self._to_device_map(netsiminfo_data)
                self._update_netsiminfo(netsiminfo_mapper, netsimdelete_keys)
            else:
                self.logger.debug(
                    "Patter {} found in Deleted Devices".format(args[3]))
                for each in range(int(args[2])):
                    del_index = -1
                    # NOTE: don't replace for loop "list(netsimdelete_mapper.keys())" to netsimdelete_keys
                    for i, each_del in enumerate(list(netsimdelete_mapper.keys())):
                        if args[3] in each_del:
                            del_index = i
                            break
                    if del_index == -1:
                        self.logger.info(
                            "Restored all deleted adding at the end.")
                        result = subprocess.run(
                            ['ncs-netsim2', 'list'], capture_output=True)
                        result = str(result.stdout.decode("utf-8"))
                        self._update_netsiminfo(netsim_mapper_sorted)

                        self._add_netsim_device(args, count=int(args[2])-each)
                        netsiminfo_data = self._read_netsiminfo()
                        netsiminfo_mapper = self._to_device_map(
                            netsiminfo_data)
                        self._update_netsiminfo(
                            netsiminfo_mapper, netsimdelete_keys)
                        self._override_netsimdel(netsimdelete_mapper)
                        exit(-1)
                    else:
                        netsim_sub_key = netsimdelete_keys[del_index]
                        netsim_sub_index = list(
                            netsim_keys).index(netsim_sub_key)

                        def subset(d, keys): return [
                            (key, d[key]) for key in keys]
                        self._update_netsiminfo(OrderedDict(
                            subset(netsim_mapper_sorted, list(netsim_keys)[:netsim_sub_index])))

                        # Adding new device..
                        self._add_netsim_device(args)
                        # Updating the delete list..
                        del netsimdelete_mapper[netsim_sub_key]
                        del netsimdelete_keys[del_index]
                self._override_netsimdel(netsimdelete_mapper)
                # Added Need to check:
                self._update_netsiminfo(netsim_mapper_sorted)
                netsiminfo_data = self._read_netsiminfo()
                netsiminfo_mapper = self._to_device_map(netsiminfo_data)
                self._update_netsiminfo(netsiminfo_mapper, netsimdelete_keys)
        else:
            self._add_netsim_devices(args)

    def _override_netsimdel(self, netsimdelete_mapper):
        subprocess.run(
            ['rm', '-rf', '{}/{}'.format(self.netsim_path, self.netsimdelete)])
        fp = open('{}/{}'.format(self.netsim_path, self.netsimdelete), 'w')
        for each_device in netsimdelete_mapper:
            fp.write(netsimdelete_mapper[each_device].replace('\n\n\n', '\n'))
            fp.write(self.split)
        fp.close()

    def _add_netsim_device(self, args, count=1):
        result = subprocess.run(
            ['ncs-netsim', 'add-to-network', args[1], str(count), args[3]], capture_output=True)
        error = str(result.stderr.decode("utf-8"))
        result = str(result.stdout.decode("utf-8"))

        if error:
            self.error(error)
            exit(-1)
        print(result)

    def _add_netsim_devices(self, args):
        result = subprocess.run(
            ['ncs-netsim'] + [each for each in args], capture_output=True)
        error = str(result.stderr.decode("utf-8"))
        result = str(result.stdout.decode("utf-8"))

        if error:
            self.error(error)
            exit(-1)
        print(result)

    def ncs_netsim(self, args):
        if self._is_add_to_network_in_args(args) and self._is_network_empty():
            self._add_devices_to_empty_network(args[1:])
            exit(-1)

        if self._is_add_to_network_in_args(args):
            self._add_devices_to_network(args)
            exit(-1)

        if self._is_delete_network_in_args(args):
            self.del_devices(args[1:])
            exit(-1)

        result = subprocess.run(
            ['ncs-netsim'] + [each for each in args], capture_output=True)
        error = str(result.stderr.decode("utf-8"))
        result = str(result.stdout.decode("utf-8"))

        if '*** Unknown arg' in error:
            self.error()
            exit(-1)

        elif '*** Need to either specify a netsim directory with --dir' in error:
            self.logger.warning("Couldn't able to find netsim dir.")
            print(error)
            exit(-1)

        elif error:
            self.logger.error('')
            print(error)
            exit(-1)

        print(result)


def main(*argv):
    obj = NcsNetsim2(argv[0])
    try:
        # ncs-netsim2 help
        if len(argv) == 1:
            obj.help()
        elif argv[1] == '-h' or argv[1] == '--help':
            obj.help()

        # ncs-netsim2 version
        elif argv[1] == '-v' or argv[1] == '--version':
            if len(argv) >= 3 and (argv[2] == '-h' or argv[2] == '--help'):
                obj.version(arg='--help')
            else:
                obj.version()

        # ncs-netsim2 dir
        elif argv[1] == '--dir':
            obj.dir_path(argv[2])
            obj.ncs_netsim(argv[3:])

        # ncs-netsim
        else:
            obj.ncs_netsim(argv[1:])
    except Exception:
        obj.error()


if __name__ == "__main__":
    main(*sys.argv[1:])
