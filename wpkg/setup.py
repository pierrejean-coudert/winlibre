import installer

#tas.msi is adummy .mis package made by me and hosted on url below.
#it has one pic of the robot i made and a small story about it ;)

def install_wrapper():
    package_details = 'The Agrobot story2','v1.02','stable','a','temp',\
                        'temp','temp'
    package_type = 'msi'
    download_url = 'http://winlibrepacman.brinkster.net/tas.msi'
    installer.declare_installer(package_type,download_url,package_details)
    

#Entry point

#install_wrapper()
