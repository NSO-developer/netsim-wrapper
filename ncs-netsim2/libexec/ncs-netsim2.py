import sys, logging, subprocess, random
from collections import OrderedDict

class NcsNetsimDel:
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
        logging.basicConfig(stream=sys.stdout, level=log_level, format=self.format, datefmt=None)
        logger = logging.getLogger('ncs-netsim2')
        logger.setLevel(log_level)
        return logger

    def help(self):
        subprocess.run([self.bash, '{}/{}/ncs-netsim2-help'.format(self.path, self.libexec)])

    def version(self, arg=None):
        if arg is None:
            subprocess.run([self.bash, '{}/{}/ncs-netsim2---version'.format(self.path, self.libexec)])
        else:
            subprocess.run([self.bash, '{}/{}/ncs-netsim2---version'.format(self.path, self.libexec),
             '--help'])

    def dir_path(self, path):
        self.netsim_path = path

    def del_devices(self, argv):
        netsim_config = self._read_netsiminfo()
        devicesxml = self._read_devicesxml()
        netsim_config = self._to_dict(netsim_config)
        self._update_netsiminfo(netsim_config, argv)
        self._update_devicesxml(devicesxml, argv)
        self._del_devices(argv)

    def _read_devicesxml(self):
        # TODO: Need to read the device xml file
        return ''

    def _update_devicesxml(self, devicexml, argv):
        # TODO: Need to update the device xml file
        pass

    def _to_dict(self, config):
        _netsim_config = OrderedDict()
        for each_device in config:
            device = {}
            for each_line in each_device.split('\n'):
                if len(each_line.split('[')) > 1:
                    key = each_line.split('[')[0]
                    value = each_line.split('=')[1]
                    device[key] = value
            if len(device):
                _netsim_config[device['devices']] = device
        return _netsim_config

    def _del_devices(self, devices):
        for device in devices:
            try:
                subprocess.Popen('rm -rf {}/*/{}'.format(self.netsim_path, device), shell=True)
                # TODO: if the directory is empty then delete the directory
                self.success(device)
            except Exception:
                self.error_device(device)
                exit(-1)
        self.logger.info('Done..!')

    def _read_netsiminfo(self):
        try:
            data = open('{}/.netsiminfo'.format(self.netsim_path)).read()
            data = data.split('#######')
            return data
        except IOError:
            self.file_not_found()
            exit(-1)

    def _update_netsiminfo(self, config, device_lst):
        exit_flag = 0
        for each_device in device_lst:
            if each_device in config:
                del config[each_device]
            else:
                exit_flag = 1
                self.error_device(each_device)
        if exit_flag:
            exit(-1)
        self._write_netsiminfo(config)

    def _write_netsiminfo(self, config):
        fp = open('{}/.netsiminfo'.format(self.netsim_path), 'w')
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

    def error(self):
        return self.logger.error("Arguments mismatch, please check ncs-netsim2 --help")
    
    def error_device(self, device):
        return self.logger.error("Device {} details not found..!".format(device))
    
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
        subprocess.run(['ncs-netsim', 'create-network'] + [each for each in args])
        subprocess.run(['cp', '-Rn', self.netsim_path + tmp, self.netsim_path])
        subprocess.run(['rm', '-rf', self.netsim_path + tmp])

    def _add_devices_to_network(self, args):
        # TODO: need to manipulate the netsiminfo on adding each config...
        print('TDA: adding devices to the network..')
        pass

    def ncs_netsim(self, args):
        # TODO: Check on adding new devices to the existing network
        # TODO: On deletion keep a track of them
        # TODO: Delete and add
        # TODO: Need to move delete device call from here

        
        if self._is_add_to_network_in_args(args) and self._is_network_empty():
            self._add_devices_to_empty_network(args[1:])
            exit(-1)

        if self._is_add_to_network_in_args(args):
            self._add_devices_to_network(args)
            exit(-1)
        
        if self._is_delete_network_in_args(args):
            self.del_devices(args[1:])
            exit(-1)
        
        result = subprocess.run(['ncs-netsim'] + [each for each in args], capture_output=True)
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
    obj = NcsNetsimDel(argv[0])
    try:
        # ncs-netsim2 help
        if len(argv) == 1:
            obj.help()
        elif argv[1] == '-h' or argv[1] == '--help':
            obj.help()

        # ncs-netsim2 version
        elif argv[1] == '-v' or argv[1] == '--version':
            if len(argv) >= 3 and ( argv[2] == '-h' or argv[2] == '--help' ):
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
