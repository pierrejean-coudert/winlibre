from django.http import *

import os
import os.path
import sys
sys.path.append('..')
from repository.winrepo.models import *
from wpkg.vercmp import vercmp

def redirect(request, name=None, version=None, id=None, generalquery=None, emitter_format=None):
    r''' Defines petition redirection for every kind of query defined in the URL. Redirect the query
    to the standard /api/name/version/format/ petition format.'''
    base = Package.objects
    if id:
        try:
            result = base.get(id=id)
            return HttpResponseRedirect('/api/package/'+result.name+'/'+result.version+'/xml/')
        except:
            return HttpResponseNotFound
    elif name and generalquery:
        versions = []
        if generalquery == "latest":
            #Get all the packages with certain name
            result = base.filter(name=name)
            #Build a list with the different versions of the package
            for row in result:
                versions.append(row.version)
            versions.sort(vercmp)
            #After the versions list is sorted, get information for the last version package
            lastversion = result.get(name=name, version=versions[len(versions)-1])
            return HttpResponseRedirect('/api/package/'+lastversion.name+'/'+lastversion.version+'/xml/')
        elif generalquery == "all":
            return HttpResponseRedirect('/api/package/'+name+'/xml/')
    else:
        HttpResponseNotFound
