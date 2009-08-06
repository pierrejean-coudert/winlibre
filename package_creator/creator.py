########################################
# Imports
import logging
import os
import os.path
import shutil
import sys

from optparse import OptionParser

# WinLibre imports
import lib
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # For importing wpkg
import wpkg.package
from wpkg.package import Package, List, PackageList, PackageShort

""" WinLibre Package Creator"""

########################################
# Meta variables
__appname__ = 'WinLibre Package Creator'
__version__ = '0.0.1'
LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
DATE = '%a, %d %b %Y %H:%M:%S'
VERSION = '%s %s' % (__name__, __version__)
USAGE = """%prog [options] command

Commands:
  init - Creates the files required for a package
  set PROPERTY VALUE - Sets a property with a value
  clear PROPERTY - Clears a property
  show PROPERTY - Shows a property
  
Properties:
  name, version, architecture, short-description, long-description,
  section, installed-size, maintainer, creator, publisher, rights-holder,
  filename, release-date, supported, changes, size, languages, license,
  md5sum, sha1, sha256, homepage, replaces, provides, pre-depends, depends,
  recommends, suggests, conflicts
  
Examples:
  %prog init
  %prog set name Example
  %prog show name"""

########################################
# Helper functions
def parse(args=None):
    """ Parses options and arguments passed """
    parser = OptionParser(usage=USAGE, version=VERSION,)
    parser.add_option('-f', '--folder', dest='folder', 
                        help='use FOLDER as the working directory.', 
                        metavar='FOLDER')
    parser.add_option('-q', '--quiet', action='store_const', const=0, 
                        dest='verbose', default=logging.WARNING, 
                        help='display only errors or warnings, ' \
                        'enabled by default')
    parser.add_option('-v', '--verbose',
                      action='store_const', const=logging.INFO, dest='verbose',
                      help='display more information')
    parser.add_option('-d', '--debug',
                      action='store_const', const=logging.DEBUG, dest='verbose',
                      help='display debugging information')
    parser.add_option('-o', '--overwrite', action='store_true',
            default=False, dest='overwrite', help='overwrite existing files')
    if args:
        return parser.parse_args(args)
    else:
        return parser.parse_args()

########################################
def main(argv):
    """ Main function of execution """
    opts, args = parse(argv)

    # Setup logging
    logging.basicConfig(level=opts.verbose, format=LOG_FORMAT, datefmt=DATE)

    # Change dir if necessary
    if opts.folder:
        if not os.path.exists(opts.folder):
            logging.info('Creating non-existant directory: %s' 
                         % opts.folder)
            os.mkdir(opts.folder)
        os.chdir(opts.folder)

    # Start parsing arguments
    if len(args) == 0:
#        try:
        if 1:
            import frontend
            app = frontend.CreatorApp(0)
            app.MainLoop()
        return

    elif args[0].lower() == 'init':
        lib.init(opts.overwrite)
        sys.exit()

    elif len(args) < 2 or (args[0] == 'set' and len(args) < 3):
        parse(['--help'])

    # Parse
    e = Package()
    if os.path.exists(wpkg.package.INFO_FILENAME):
        try:
            e.from_file(wpkg.package.INFO_FILENAME)
        except:
            pass
    else:
        print os.getcwd()
        raise IOError, 'info.xml does not exist'
    
    # Convert parameters to variable names
    args[1] = args[1].replace('-','_') 
    args[0] = args[0].lower()
    
    for i in range(0,len(args)):
        args[i] = args[i].replace('\\n','\n')
    
    # Set the values
    if args[0] == 'show':
        x = e.get_property(args[1])#.to_string()
        if isinstance(x, List): # Received a list
            if x == []:
                print None
            else:
                print x
        else: # Just a string
            print x
    elif args[0] == 'clear':
        if isinstance(e.get_property(args[1]), List):
            e.set_property(args[1], [])
        else:
            e.set_property(args[1], '')
        e.write()
    elif args[0] == 'set':
        x = e.get_property(args[1])#.to_string()
        if isinstance(x, PackageList):
            x.clear()
            for package in ''.join(args[2:]).split(';'):
                name, version = package.split(',')
                pkg = PackageShort(name, version)
                x.append(pkg)
        elif isinstance(e.get_property(args[1]), List):
            e.set_property(args[1], args[2:])
        else:
            e.set_property(args[1], ' '.join(args[2:]))
        e.write() # Write the package info.xml file
    elif args[0] == 'append':    
        e.append_property(args[1], args[2:])
        e.write()
    elif args[0] == 'script':
        lib.set_script(args[1], args[2], opts.overwrite)

if __name__ == "__main__":
    main(sys.argv[1:])
