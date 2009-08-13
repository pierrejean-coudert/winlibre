import installerXMLLog

def writeLog(package_details):
    '''
    This module appends the data of recent installs (in tempholder.xml) 
    to installedLog.xml
    '''
    #installerXMLLog creates 'tempholder.xml' which contains data
    #to be appended to the file 'installedLog.xml'
    installerXMLLog.installerLog(package_details)

    #opening the tempholder.xml and stripping off its <xml> and </xml> tags
    tempholder = open('tempholder.xml','rb')
    new_temp_data = tempholder.read()
    new_temp_data = new_temp_data[5:-6] 
    tempholder.close()

    #creating installedLog.xml if its not there
    open('installedLog.xml', 'a').close()
    

    #if installedLog.xml contains data, written=1
    #if written ==1, strip the </xml> from installedLog.xml to write new entries
    try:
        logFileInfo = open('installedLog.xml','r+b')
        if (logFileInfo.read()):
            written = 1 #flagging its written
            #print 'cursor pos when opend written file :',logFileInfo.tell()
            logFileInfo.seek(0)
            orig_log_data = logFileInfo.read()
            orig_log_data = orig_log_data[:-6] #removing </xml> installedLog.xml
            #print 'orig_log_Data : ',orig_log_data
            logFileInfo.seek(0)
            logFileInfo.write(orig_log_data)
        else:
            written = 0
    except IOError:
        print 'Error to write to the log file', IOError
        return -2, 'not logged'

    finally:
        logFileInfo.close()

    
    #now appending the install data to installedLog.xml
    #new_temp_data has list of newly added packages (no <xml> & </xml> tags)
    logFile = open('installedLog.xml', "wb")
    if(written == 1):
        final_write_data = orig_log_data + new_temp_data + '\n' + '</xml>'
        logFile.write(final_write_data)
    else:
        final_write_data = '<xml>\n' + new_temp_data + '\n</xml>'
        logFile.write(final_write_data)

    logFile.close()
