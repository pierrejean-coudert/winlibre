import pyRegistry
from wpkg import repoList
from wpkg import package


def client_list():
    '''
    The clientList function gets the list of all the 
    installed software on the users computer. 
    '''
    
    basereg = pyRegistry.open ('HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall')
    total_keys = basereg.getKeyNames()

    for i in total_keys:
        key_name = 'HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\\' + i

        key = pyRegistry.open(key_name)
    
        for i in key.getValueNames():
            if (i == 'DisplayName'):
                print 'Name : ', key.getValue('DisplayName'),'\n'
            if (i == 'DisplayVersion'):
                print 'Version : ', key.getValue('DisplayVersion'), '\n'
            
        key.close()
        basereg.close()
    #write to xml ? or just plain text file with suitable delimeters?
    #end clientList

def repo_list(name='all',version='multiple',format='xml',listing='all'):
    #by default, all packages are listed
    #if name, version,format is passed and listing=single, specific package info fetched.
    #name,version,format -> for repository
    #listing -> single package(info,latest info) or all packages
    '''
    The repoList function gets the list of the software available on the
    repository. The minimum overhead data is to be exchanged and 
    timestamps will be sent to the repository and the parsed list 
    (timestamps as key) will be appended to the local listing
    '''
    #To-Do -
    #get timestamp info from file
    #pass that to repo
    # send timestamp->[server parses the listing (?), sends the new data]->append to existing list.
    #right now, just getting the lists acoording to the present options available for repo
    if(listing = 'all'):
        repoList.all_package_details('all','multiple','xml')
        repo_list_info = Package()
        repo_list_info.from_file('packages.xml')
        print repo_list_info.to_string()
    
    version = version.lower()
    
    elif(listing == 'single' && version != 'latest'):
        repoList.package_details(name,version,'xml')
        repo_list_info = Package()
        repo_list_info.from_file('packages.xml')
        print repo_list_info.to_string()
    
    else:
        repolist.package_details(name,'latest','xml')
        repo_list_info = Package()
        repo_list_info.from_file('packages.xml')
        print repo_list_info.to_string()



def winpacman_list():
    '''
    winpacmanList will give the list of programs 
    installed by using package manager.
    '''
    pass
