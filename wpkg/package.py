# Setup the logger for elements lib
import logging
logging.basicConfig()

# Normal imports
from elements import Element
from UserList import UserList

"""
 WinLibre xml metadata parser/writer 

Usage:
e = Packages()
e.from_file('info.xml')
print e.to_string()
"""

INFO_FILENAME = 'info.xml'
PACKAGES_FILENAME = 'packages.xml'
NAMESPACE='' #Empty NameSpace just to trick python-elements and avoid warning because NameSpace is None

#########################
# Lists/Helper classes
class Writeable(Element):
    def write(self, filename=INFO_FILENAME):
        """ Write an XML selfance to file """
        f = open(filename, 'wb')
        f.write(self.to_string())
        f.close()

class List(UserList, Writeable):
    _tag = ''
    _namespace = NAMESPACE
    def __init__(self, datas=None):
        super(List, self).__init__()
        UserList.__init__(self)
        Element.__init__(self)
        self.data = isinstance(datas, list) and data or []
        self._text = None
        
    def __str__(self):
        return self.data
        

class Supported(List):
    _tag = 'supported'
    _children = Element.copy_children()
    _children['version'] = ('data', [unicode])
    def __init__(self, versions=None):
        super(Supported, self).__init__(versions)
        
class Languages(List):
    _tag = 'languages'
    _children = Element.copy_children()
    _children['language'] = ('data', [unicode])
    def __init__(self, languages=None):
        super(Languages, self).__init__(languages)
        
class Replaces(List):
    _tag = 'replaces'
    _children = Element.copy_children()
    _children['replace'] = ('data', [unicode])
    def __init__(self, replaces=None):
        super(Replaces, self).__init__(replaces)
        
class Provides(List):
    _tag = 'provides'
    _children = Element.copy_children()
    _children['provide'] = ('data', [unicode])
    def __init__(self, provides=None):
        super(Provides, self).__init__(provides)
        
class PreDepends(List):
    _tag = 'pre-depends'
    _children = Element.copy_children()
    _children['pre-depend'] = ('data', [unicode])
    def __init__(self, pre_depends=None):
        super(PreDepends, self).__init__(pre_depends)
        
class Depends(List):
    _tag = 'depends'
    _children = Element.copy_children()
    _children['depend'] = ('data', [unicode])
    def __init__(self, depends=None):
        super(Depends, self).__init__(depends)
        
class Recommends(List):
    _tag = 'recommends'
    _children = Element.copy_children()
    _children['recommend'] = ('data', [unicode])
    def __init__(self, recommends=None):
        super(Recommends, self).__init__(recommends)
        
class Suggests(List):
    _tag = 'suggests'
    _children = Element.copy_children()
    _children['suggest'] = ('data', [unicode])
    def __init__(self, suggests=None):
        super(Suggests, self).__init__(suggests)
        
class Conflicts(List):
    _tag = 'conflicts'
    _children = Element.copy_children()
    _children['conflict'] = ('data', [unicode])
    def __init__(self, conflicts=None):
        super(Conflicts, self).__init__(conflicts)
        
class URLs(List):
    _tag = 'urls'
    _children = Element.copy_children()
    _children['url'] = ('data', [unicode])
    
    def __init__(self, urls=None):
        super(URLs, self).__init__(urls)

class Package(Writeable):
    _tag = 'package'
    _namespace = NAMESPACE
    _children = Element.copy_children()
    _children['name'] = ('name', unicode)
    _children['version'] = ('version', unicode)
    _children['architecture'] = ('architecture', unicode)
    _children['short-description'] = ('short_description', unicode)
    _children['long-description'] = ('long_description', unicode)
    _children['section'] = ('section', unicode)
    _children['selfalled-size'] = ('selfalled_size',int)
    _children['maintainer'] = ('maintainer', unicode)
    _children['creator'] = ('creator', unicode)
    _children['publisher'] = ('publisher', unicode)
    _children['rights-holder'] = ('rights_holder', unicode)
    _children['filename'] = ('filename', unicode)
    _children['release-date'] = ('release_date', unicode)
    _children['supported'] = ('supported', Supported)
    _children['changes'] = ('changes', unicode)
    _children['size'] = ('size', int)
    _children['languages'] = ('languages', Languages)
    _children['license'] = ('license', unicode)
    _children['md5sum'] = ('md5sum', unicode)
    _children['sha1'] = ('sha1', unicode)
    _children['sha256'] = ('sha256', unicode)
    _children['homepage'] = ('homepage', unicode)
    _children['replaces'] = ('replaces', Replaces)
    _children['provides'] = ('provides', Provides)
    _children['pre-depends'] = ('pre_depends', PreDepends)
    _children['depends'] = ('depends', Depends)
    _children['recommends'] = ('recommends', Recommends)
    _children['suggests'] = ('suggests', Suggests)
    _children['conflicts'] = ('conflicts', Conflicts)
    _children['urls'] = ('urls', URLs)
    
    def __init__(self, name=None, version=None, architecture=None,
            short_description=None, long_description=None, section=None,
            selfalled_size=None, maintainer=None, creator=None, publisher=None,
            rights_holder=None, filename=None, release_date=None, 
            supported=None, changes=None, size=None, languages=None,
            license=None, md5sum=None, sha1=None, sha256=None, homepage=None,
            replaces=None, provides=None, pre_depends=None, depends=None,
            recommends=None, suggests=None, conflicts=None, urls=None):
        self.name = name
        self.version = version
        self.architecture = architecture
        self.short_description = short_description
        self.long_description = long_description
        self.section = section
        self.selfalled_size = selfalled_size
        self.maintainer = maintainer
        self.creator = creator
        self.publisher = publisher
        self.rights_holder = rights_holder
        self.filename = filename
        self.release_date = release_date
        self.supported = isinstance(supported, Supported) and supported or Supported()
        self.changes = changes
        self.size = size
        self.languages = isinstance(languages, Languages) and languages or Languages()
        self.license = license
        self.md5sum = md5sum
        self.sha1 = sha1
        self.sha256 = sha256
        self.homepage = homepage
        self.replaces = isinstance(replaces, Replaces) and replaces or Replaces()
        self.provides = isinstance(provides, Provides) and provides or Provides()
        self.pre_depends = isinstance(pre_depends, PreDepends) and pre_depends or PreDepends()
        self.depends = isinstance(depends, Depends) and depends or Depends()
        self.recommends = isinstance(recommends, Recommends) and recommends or Recommends()
        self.suggests = isinstance(suggests, Suggests) and suggests or Suggests()
        self.conflicts = isinstance(conflicts, Conflicts) and conflicts or Conflicts()
        self.urls = isinstance(urls, URLs) and urls or URLs()
        self.installed = False

    def get_property(self, prop):
        """ Get the value of a property """
        prop = prop.lower()
        if prop in dir(self):
            return getattr(self, prop)
        else:
            raise AttributeError, '%s property does not exist' % prop

    def set_property(self, prop, value):
        """ Set the value of a property """
        prop = prop.lower()
        if prop in dir(self):
            if isinstance(getattr(self, prop), List):
                if not isinstance(value, list):
                    raise Exception, 'Invalid value type'
                getattr(self, prop).data = value
            else:
                setattr(self, prop, value)
        else:
            raise AttributeError, '%s property does not exist' % prop
    
    def append_property(self, prop, value):
        """ Append item(s) to a property that is a List """
        prop = prop.lower()
        if prop in dir(self):
            if isinstance(getattr(self, prop), List):
                if isinstance(value, list):
                    getattr(self, prop).data += value
                else:
                    getattr(self, prop).data.append(value)
            else:
                raise Exception, 'Only setting of %s is allowed' % prop
        else:
            raise AttributeError, '%s property does not exist' % prop
    
    def install(self, path):
        self.installed = True
        print 'Package path is %s' % path
        return 0, 'installed'
    
class Packages(List):
    _tag = 'packages'
    _children = Element.copy_children()
    _children['package'] = ('data', [Package])
    def __init__(self, packages=None):
        super(Packages, self).__init__(packages)
        

##########################################
# RFC822 Conversion Functions
def to_RFC_string_format(string, part="all"):  
    """  
    Returns a standard formatted name/email string  
    to_RFC_string_format(string, part="all")  

    string MUST be in the following format: First Last "email@address.com"  

    The second paramter has 3 options: "all", "name", and "email"  
    "all" returns the string in standard format "First Last <email@address.com>"  
       and is the default option  
    "name" returns only the name portion of the string  
    "email" returns only the email address portion of the string  

    Raises TypeError if the string is improperly formatted  
    """
    if string.count('"') > 1 and string.endswith('"'):  
     proper = string[:-1] + '>'  
     index = proper.rfind('"')  
     proper = proper[:index] + '<' + proper[index + 1:]  
     if part == 'all':  
         return proper  
     elif part == 'name':  
         return proper.split('<')[0].strip()  
     elif part == 'email':  
         return proper.split('<')[1][:-1]  
     else:  
         return ""
    else:  
     raise TypeError, '%s is not in standard First Last format' % string  

def to_XML_string_format(string):
    """
    Converts a string in RFC format to be XML compatible  
    """  
    return string.replace('<', '"').replace('>', '"') 

