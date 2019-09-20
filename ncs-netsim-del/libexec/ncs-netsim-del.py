import sys, logging, subprocess
from collections import OrderedDict

class NcsNetsimDel:
    def __init__(self, path):
        self.path = path
        self.netsim_path = './netsim'
        self.bash = '/bin/bash'
        self.libexec = '../libexec'

    def help(self):
        subprocess.run([self.bash, '{}/{}/ncs-netsim-del-help'.format(self.path, self.libexec)])

    def version(self, arg=None):
        if arg is None:
            subprocess.run([self.bash, '{}/{}/ncs-netsim-del---version'.format(self.path, self.libexec)])
        else:
            subprocess.run([self.bash, '{}/{}/ncs-netsim-del---version'.format(self.path, self.libexec),
             '--help'])

    def dir_path(self, path):
        self.netsim_path = path

    def del_devices(self, argv):
        netsim_config = self._read_netsiminfo()
        netsim_config = self._to_dict(netsim_config)
        self._update_netsiminfo(netsim_config, argv)
        self._del_devices(argv)

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
                self.success(device)
            except Exception:
                self.error_device(device)
        logging.info('Done..!')

    def _read_netsiminfo(self):
        try:
            data = open('{}/.netsiminfo'.format(self.netsim_path)).read()
            data = data.split('#######')
            return data
        except IOError:
            self.file_not_found()
            exit(-1)

    def _update_netsiminfo(self, config, device_lst):
        for each_device in device_lst:
            if each_device in config:
                del config[each_device]
            else:
                self.error_device(each_device)
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
        return logging.error("netsim configuration file not found at {}".format(self.netsim_path))

    def success(self, device):
        return logging.info("Device {} deleted successfully".format(device))

    def error(self):
        return logging.error("Arguments mismatch, please check ncs-netsim-del --help")
    
    def error_device(self, device):
        return logging.error("Device {} details not found..!".format(device))

def main(*argv):
    obj = NcsNetsimDel(argv[0])
    try:
        # ncs-netsim-del help
        if len(argv) == 1:
            obj.help()
        elif argv[1] == '-h' or argv[1] == '--help':
            obj.help()

        # ncs-netsim-del version
        elif argv[1] == '-v' or argv[1] == '--version':
            if len(argv) >= 3 and ( argv[2] == '-h' or argv[2] == '--help' ):
                obj.version(arg='--help')
            else:
                obj.version()
        
        # ncs-netsim-del dir
        elif argv[1] == '--dir':
            obj.dir_path(argv[2])
            if len(argv) > 4 and argv[3] == 'device':
                obj.del_devices(argv[4:])
            else:
                obj.error()
        
        # ncs-netsim-del device
        elif argv[1] == 'device':
            obj.del_devices(argv[2:])
        
        # error
        else:
            obj.error()
    except Exception:
        obj.error()


if __name__ == "__main__":
    main(*sys.argv[1:])


# TODO: need to deleting the device folders
# TODO: need to update the .netsiminfo file

# TODO: need to add logging messages