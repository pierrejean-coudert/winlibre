from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
url(r'package/(?P<package_name>[^/]*)/(?P<package_version>[^/]*)/$', package_details),
url(r'section/(?P<section_title>[^/]*)/$', packages_list),
)
