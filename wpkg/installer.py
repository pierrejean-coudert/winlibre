import os
import sys
import installerlog
#import fileDownloader
from smart.fetcher import Fetcher
from subprocess import Popen, PIPE
import urlparse
from wpkg.package import Package
import imp

#for scripts in %temp% to work with wpkg.* modules
sys.path.append('..')

class installer ():
    #Workpath -
    #1) Download using SMART.fetcher
    #2) call enumerator to check for previous versions.
    #3) call SMART to resolve/handle dependencies
    #4) install dependencies
    #5) call the respective functions handling the .msi or .nsis installs.
    
    
    def __init__(self,path,package_details):
        self._path = path
        #self._arguments = arguments
        self._package_details = package_details

    def logger(self,package_details):
        installerlog.writeLog(package_details)

    def downloader(self, URL):
    #using smart.fetcher() to download the package
        try:
            fetcher = Fetcher()
            fetcher.reset()
            info = {}#{'uncomp': True}
            #URL = 'http://winlibrepacman.brinkster.net/tas2.msi'
            item = fetcher.enqueue(URL, **info)
            if (fetcher.run(what=False) is False):
                print 'Using cached download'
            
        except:
            print 'Download error occoured'

    def binInstall(self, install_arg):
    #Downloaded binary installer
        print '\n***Installing binary...***'
        try:
            p = Popen(install_arg, stdout=PIPE)
            res = p.communicate()[0]
            print 'Package details :', self._package_details
            return True
        except Exception, e:
            print 'Errors occoured during install', e
            res = -1 #Error code
            return False
    


class MSIInstaller(installer):
    def install(self):
        install_arg = 'msiexec /i '+self._path+' /quiet'
        if(self.binInstall(install_arg)):
            return 'Installed'
    


'''
#placeholder, implementing msi for now
class NSIInstaller():
    def nsis_installer(self,installer_path,package_details):
        print 'Downloading package...'
        try:
            fileDownloader.fileDownloader('http://127.0.0.1/winlibrepacman/tas.msi','b')
        except:
            print 'An error occoured', #name of error
        print 'Download Finished...'
        print 'Now installing...'
        #install_arg = 'msiexec /i '+installer_path+' /quiet'
        try:
            os.system(install_arg)
            print 'Installed the package. ;)'
        except:
            print 'Errors occoured during install'
        print 'Now logging to the installerLog.xml'
        installerlog.writeLog(package_details)
       
'''
def pkg_name(download_url):
    #get the name of the package from the URL
    #considering download URL to look like - http://www.blah.com/downloads/.../example.wlp
    parsed_url = urlparse.urlsplit(download_url)
    print parsed_url[2].split('/')
    bin_name = parsed_url[2].split('/')[-1]
    return bin_name
    

def install(package_type,download_url,package_details):
    if(package_type == 'msi'):
        path = os.getenv('temp') + '\\' + pkg_name(download_url)
        print 'Path : ', path
        installObj = MSIInstaller(path,package_details)
        print '\n***Downloading binaries/installables...***'
        installObj.downloader(download_url)
        if (installObj.install() == 'Installed'):
            #installObj.logger(package_details)
            print '***Logged***'
        else:
            print 'Error occoured during install'
    ## add the if entry for nsis package and inno setup package
    

# pre install - another module
def pre_install(package_name, download_url):
    #pre install - using smart.fetcher module to download package
    #then extracting the package to temp
    #then execute the install scripts
    print '\n***Downloding WinLibre package...***'
    try:
        fetcher = Fetcher()
        fetcher.reset()
        info = {}#{'uncomp': True}
        item = fetcher.enqueue(download_url, **info)
        if (fetcher.run(what=False) is False):
            print 'Using cached download'
    except:
        print 'Download error occoured'
    
    print '\n***Now extracting the package contents...***'
    #print 'Package name: ', pkg_name(download_url)
    #using 7z cli here
    temp_dir = os.getenv('temp')
    download_name = temp_dir + '\\' + pkg_name(download_url)
    #extract arg is temprorary and system dependent
    #appending $PATH to have 7za.exe will remove absolute path neccessity
    extract_arg = 'C:\wpc\wpc2\winlibre1.0\wpkg\\7za.exe'+' e ' + '-o'+temp_dir+' -y '+ download_name 
    try:
        p = Popen([extract_arg], stdout=PIPE, shell = True)
        op = p.communicate()[0]
        print 'Output : ' , op
    except Exception, e:
        print 'Errors occoured during extract', e
        op = -3 #Error code

    #execute the install scripts
    print '\n***Now executing install scripts...***'
    f, file_name, desc = imp.find_module('install', [temp_dir])
    install_script = imp.load_module('install', f, file_name, desc)
    
    #Just another workpath below, not in use now
    '''
    #(1)get the <filename> from info.xml of package,download using 
    fetcher module. But filename of info.xml doesnt have binary info, 
    it has package info but package info was retrieved from packages.xml,
    which is the local database of packages. Shouldnt <filename> of info.xml
    should point to the binary?
    #(2)then execute install script giving location of the binary (%temp%)?
    #**(1)**
    package_info = Package()
    package_info.from_file(temp_dir+'\\info.xml')
    package_loc = package_info.filename
    print package_loc
    '''
    
