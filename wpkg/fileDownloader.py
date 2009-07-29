from urllib2 import Request, urlopen, URLError, HTTPError
import urlparse

#TO-DO : to show the progress, learn to read and parse the HTTP_RESPONSE
def fileDownloader (url,file_mode,local_file_name = ''):
    '''This function takes three args (URL,file_mode,local_file_name)and
    downloads the installer file 
    from the url specified. local_file_name is the file name which is used
    to write on the disk. If its empty, then the file_name from the URL is used.
    '''
    print 'url:',url,'\n','filemode :',file_mode,'\n','file_name:',local_file_name,'\n'
    parsed_url = urlparse.urlsplit(url)
    
    #based on parsed_url(0) we can decide whether to go for package:// or html://
    baseurl = parsed_url[0]+'://'+parsed_url[1]+'/'
    file_name = (parsed_url[2][1:])
    if (local_file_name == ''):
    #if no arg is passed as filename, then the filename is decided by the URL
        local_file_name = (parsed_url[2][1:])

    #create the url and the request
    url = baseurl + file_name
    req = Request (url)
    

    try:
        downloading_file = urlopen (req)
        print 'Downloading ', url
        
        #opening file for writing 
        local_file = open(local_file_name, "w" + file_mode)
        #writing to the local file
        print 'Now writing to ', local_file_name
        local_file.write(downloading_file.read())
        local_file.close()

    except HTTPError, e:
        print 'The server could\'nt fulfill the request'
        print 'Error code:', e.code
    except URLError, e:
        print "Can\'t reach server, check internet connection! "
        print "Reason : ", e.reason
    
    return local_file_name
    
