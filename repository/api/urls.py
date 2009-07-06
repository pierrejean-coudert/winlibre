from django.conf.urls.defaults import *
from handlers import *
from piston.resource import Resource


package = Resource(handler=PackageHandler)
packages = Resource(handler=PackagesHandler)

urlpatterns = patterns('',
url(r'package/(?P<name>[^/]*)/(?P<version>[^/]*)/(?P<emitter_format>[^/]*)/$', package),
url(r'package/id/(?P<id>\d{1,10})/(?P<emitter_format>[^/]*)/$', package),
url(r'package/(?P<name>[^/]*)/(?P<generalquery>latest)/(?P<emitter_format>[^/]*)/$', package),
url(r'package/(?P<name>[^/]*)/(?P<generalquery>all)/(?P<emitter_format>[^/]*)/$', package),
url(r'package/(?P<name>[^/]*)/(?P<emitter_format>[^/]*)/$', package),
#Pattern for packages list
url(r'packages/all/(?P<emitter_format>[^/]*)/$', packages),
url(r'packages/(?P<date>\d{2}-\d{2}-\d{4})/(?P<emitter_format>[^/]*)/$', packages),
)

#(?P<emitter_format>.+)
