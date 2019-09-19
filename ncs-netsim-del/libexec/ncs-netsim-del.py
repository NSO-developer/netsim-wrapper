import sys

def main(*argv):
    print(argv)

main(sys.argv[1:])

# TODO: need to check the flags like -v, --version, -h, --help as a first arg 
# TODO: if the arg list contains --dir need to read the "NetsimDir" path
# TODO: need to store the devices names need to be deleted. 


# TODO: need to deleting the device folders
# TODO: need to update the .netsiminfo file

# TODO: need to add logging messages