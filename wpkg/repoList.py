from urllib2 import Request, urlopen, URLError, HTTPError
import sys



#package_info gets the data from the repository
def package_info(name='',version='',format=''):
    
    global repo_url

    repo_url = "http://ks201796.kimsufi.com:8004/"
    #package details filename = pkg_det_filename
    pkg_det_filename = None
    
    #this function gets the data from the repository
    #request_URL = repo.address/api/package/name/version/format/ 
    if(format is ''):
        format = 'xml'
        
    if(name is ''):
        print 'Specify a package name to download its details'
        sys.exit('No package name specified')
        
    
    if(version is ''):
        print 'Specify a version for the package'
        sys.exit('No version specified')
    
    if(repo_url[-1] is not '/'):
        print 'repo url added with /'
        repo_url = repo_url + '/'
    
    #standard request_URL is for single package info
    request_URL = repo_url + 'api/'+'package/' + name + \
                '/'+str(version) +'/'+ format
    
    if(name is 'all' and version is 'multiple'):
    #fetching multiple package info(all package list)
        request_URL = repo_url+ 'api/'+'packages/'+name+'/'+format
        pkg_det_filename = 'packages.xml'
        
    
    #actual fetching from the server begins
    try:
        #request URL to end with /
        if(request_URL[-1] is not '/'):
            request_URL = request_URL + '/'
        print request_URL
        data = urlopen(request_URL)
        if(pkg_det_filename is None):
            pkg_det_filename = name +'-'+ str(version) + '.' + format
        print pkg_det_filename
        pkg_det_file = open(pkg_det_filename,'w')
        pkg_det_file.write(data.read())
        pkg_det_file.close()
    
    except HTTPError,e:
        print 'The server could\'nt fulfill the request'
        print 'Error code:', e.code
    
    except URLError, e:
        print "Can\'t reach server/bad repository address %s" % request_URL
        print "Reason : ", e.reason
    
    except IOError:
        print "Error writing to filename : %s" % filename
    
    except:
        print 'Unexpected error occoured'




#getting single package details
#name,version,format required
def package_details(name='',version='',format=''):
    
    #request_URL = repo.address/api/package/name/version/format/ 
    package_info(name,version,format)
    

#getting single package details
#name,format required.version set to latest
def latest_package_details(name='',version='latest',format=''):
    
    #request_URL = repo.address/api/package/name/latest/format
    package_details(name,version,'xml')
    

#getting the list of all packages
#name set to all, version='', format xml
def all_package_details(name='',version='',format=''):
    #request_URL = repo.address/api/packages/all/format
    name = 'all'
    version = 'multiple'
    package_details(name,version,'xml')

#entry point 
package_details('Firefox','latest','xml')
    
