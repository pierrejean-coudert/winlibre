from django.conf.urls.defaults import *
from repository.settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^website/', include('repository.website.urls')),
    (r'^api/', include('repository.api.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),

    # Examples:
    #(r'^repository/', include('repository.foo.urls')),
                      
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/(.*)', admin.site.root),
)
