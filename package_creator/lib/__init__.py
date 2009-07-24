import os
import os.path
import shutil

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import wpkg.package
from wpkg.package import Package

def init(overwrite):
    """ Initializes a package """
    if os.path.exists(wpkg.package.INFO_FILENAME) and not overwrite:
        raise IOError, 'Package already initialized.'
        return False
    else:
        e = Package()
        e.write() # uses default filename of wpkg.package.INFO_FILENAME without specifying
        return True

def set_script(type, filename, overwrite=False):
    """ Sets an install/remove script """
    scripts = ['preinstall', 'install', 'postinstall', 'preremove', 'remove',
               'postremove']
    type = type.lower()
    for script in scripts:
        if type == script:
            f = script + '.py'
            if filename == 'remove': # Remove the script
                try:
                    os.remove(f)
                    return True
                except:
                    raise IOError, 'Unable to remove %s from package' % f
            else:
                # copy filename to script+'.py'
                if not os.path.exists(f) or overwrite:
                    shutil.copyfile(filename, f)
                    return True
                else:
                    raise IOError, '%s already exists. Use --overwrite if you ' \
                                   'wish to replace the existing file.' % f
    raise AttributeError, '%s is not a valid script' % type
    return False