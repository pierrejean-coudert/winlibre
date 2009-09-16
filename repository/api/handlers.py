from piston.handler import AnonymousBaseHandler
from piston.handler import BaseHandler
from emitters import *
from django.http import Http404, HttpResponse
from piston.utils import rc, require_extended, require_mime, Mimer
from django.db import transaction

import re
import datetime
import os
import os.path
import sys
sys.path.append('..')
from repository.winrepo.models import *
from wpkg.package import Package as PackageParser

### Default fields list to be used in every class definition below.
defaultfields =  ('name', 'version', 'architecture',
                  'filename', 'short_description',
                  'long_description', 'creator', 'creator_email',
                  'publisher', 'publisher_email', 'maintainer',
                  'maintainer_email', 'rights_holder', 'rights_holder_email',
                  'release_date', 'changes', 'size', 'license',
                  'sha256', 'homepage', 'installed_size',
                  ('languages', ('language', ), ),
                  ('section', ('title', ), ),
                  ('supported', ('os_version', ), ),
                  ('depends', ('name', 'version', ), ),
                  ('provides', ('name', 'version', ), ),
                  ('suggests', ('name', 'version', ), ),
                  ('replaces', ('name', 'version', ), ),
                  ('pre_depends', ('name', 'version', ), ),
                  ('recommends', ('name', 'version', ), ),
                  ('conflicts', ('name', 'version', ), ),
                  ('urls', ('url', ), ),
                  )


class AnonymousPackageHandler(AnonymousBaseHandler):
    ''' Manages the anonymous petitions to the PackageHandler.

    model: Defines the model from winrepo.models which is use to server or create resources.
    fields: Defines the used fields for the GET methods provided by the class.
    '''
    model = Package
    fields = defaultfields

class PackageHandler(BaseHandler):
    ''' Manages the anonymous petitions to the PackageHandler.

    This class manages the petitions for individual packages descriptor.
    model: Defines the model from winrepo.models which is use to server or create resources.
    fields: Defines the used fields for the GET methods provided by the class.
    anonymous: Defines the class that handles the anonymous petitions for this resource.
    '''

    model = Package
    fields = defaultfields
    anonymous = AnonymousPackageHandler

    def read(self, request, name=None, version=None, id=None, generalquery=None):
        ''' GET method for Package resource. Return the package data depending on the URL '''
        base = Package.objects

        if name and version:
            try:
                return base.get(name=name, version=version)
            except:
                return None #This should be modified by a default error message
        elif name:
            try:
                return base.filter(name=name)
            except:
                return None

    @require_extended
    def create(self, request, name=None, version=None):
        ''' POST method for the Package resource.
        Takes data from a POST petition, deserializes it and
        saves it into the database model. '''
        base = Package.objects
        sectionbase = Section.objects
        languagesbase = Languages.objects
        supportedbase = Supported.objects
        # In this properties list, every m2m relationship is not yet developed.
        propertieslist = ['name', 'version', 'architecture',
                          'short_description', 'long_description',
                          'installed_size', 'maintainer', 'creator',
                          'publisher', 'rights_holder', 'filename',
                          'release_date', 'changes',
                          'size', 'license', 'sha256',
                          'homepage',  'languages', 'supported', 'section',
                          'replaces', 'pre_depends', 'depends',
                          'provides', 'recommends', 'suggests']

        # Using wpkg parser
        pkg = PackageParser()
        pkg.from_string(request.raw_post_data)
        packagemodel = Package()
        if pkg:
            #Here I match each property from Package to the model properties.
            # Important note: After every mandatory field is set, the package is saved into
            # the database in order to create the m2m relations
            for prop in propertieslist:
                if prop == 'section':
                    try:
                        sectionexist = sectionbase.get(title=pkg.get_property(prop))
                    except:
                        sectionexist = None
                        packagemodel.delete()
                        return HttpResponse("Section doesnt exist "+pkg.get_property(prop))
                        #RISE ERROR
                    if sectionexist:
                        # Here there is a nasty solution. Section is the last added element
                        # and the package should be saved before adding it to the set.
                        # Pending for a better solution.
                        packagemodel.save()
                        sectionexist.package_set.add(packagemodel)
                elif prop == 'maintainer' or prop == 'creator'or prop == 'publisher' or prop == 'rights_holder':
                    # Here we split name and email.
                    rex = re.compile('(?P<name>[^"]*) "(?P<email>[^"]*)')
                    exrex = rex.match(pkg.get_property(prop))
                    if exrex:
                        setattr(packagemodel, prop+"_email", exrex.group('email'))
                        setattr(packagemodel, prop, exrex.group('name'))
                    else:
                        packagemodel.delete()
                        return HttpResponse("Invalid name and email format in: "+prop)
                elif prop == 'release_date':
                    ds = pkg.get_property(prop).split('/')
                    dateobject = datetime.date(year=int(ds[2]), month=int(ds[1]), day=int(ds[0]))
                    setattr(packagemodel, prop, dateobject)
                elif prop == 'languages':
                    for language in pkg.get_property(prop):
                        try:
                            languageexist = languagesbase.get(language=language)
                        except:
                            packagemodel.delete()
                            return HttpResponse("Language doesn't exist")
                        packagemodel.save()
                        packagemodel.languages.add(languageexist)
                elif prop == 'supported':
                    for supported in pkg.get_property(prop):
                        try:
                            supportedexist = supportedbase.get(os_version=supported)
                        except:
                            packagemodel.delete()
                            return HttpResponse("Windows version doesn't exist:"+supported)
                        packagemodel.save()
                        packagemodel.supported.add(supportedexist)
                elif  prop == 'replaces' or prop == 'pre_depends' or prop == 'depends' or prop == 'provides' or prop == 'recommends' or prop == 'suggests':
                    for item in pkg.get_property(prop):
                        if item:
                            rex = re.compile('(?P<name>[^"]*) \((?P<version>[^\)]*)')
                            exrex = rex.match(item)
                            try:
                                packageexist = base.get(name=exrex.group('name'), version=exrex.group('version'))
                            except:
                                packagemodel.delete()
                                return HttpResponse("Package not found: "+exrex.group('name')+" in "+prop)
                        else:
                            break
                        tmpprop = getattr(packagemodel, prop)
                        tmpprop.add(packageexist)
                else:
                    setattr(packagemodel, prop, pkg.get_property(prop))
            packagemodel.save()
            return rc.CREATED
        else:
            #RISE ERROR
            return HttpResponse("There is nothing")


class AnonymousPackagesHandler(AnonymousBaseHandler):
    ''' Manages the anonymous petitions to the PackageHandler.

    model: Defines the model from winrepo.models which is use to server or create resources.
    fields: Defines the used fields for the GET methods provided by the class.
    '''
    model = Package
    fields = defaultfields

class PackagesHandler(BaseHandler):
    ''' Manages the anonymous petitions to the PackageHandler.

    This class manage petitions for a set of packages descriptors.
    model: Defines the model from winrepo.models which is use to server or create resources.
    fields: Defines the used fields for the GET methods provided by the class.
    anonymous: Defines the class that handles the anonymous petitions for this resource.
    '''

    model = Package
    fields = defaultfields
    anonymous = AnonymousPackagesHandler

    def read(self, request, date=None):
        ''' GET method for Packages resource.
        Return the packages data depending on the query defined in URL '''
        base = Package.objects

        if date:
            list_date = date.split('-')
            try:
                date = {'day':int(list_date[0]),
                        'month': int(list_date[1]),
                        'year': int(list_date[2])}
                return base.filter(release_date__gte=(datetime.date(date['year'],
                                                                    date['month'],
                                                                    date['day'])))
            except:
                return None
        else:
            try:
                return base.all()
            except:
                return None
