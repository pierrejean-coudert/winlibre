from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
(r'^profiles/', include('profiles.urls')),
url(r'^uploaded_files/$', uploaded_files),
url(r'^upload/$', upload_file),
url(r'^vote/$', vote),                      
url(r'^search/$', search),
url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/website/'}),
url(r'^accounts/', include('registration.urls')),
url(r'^$', news_list),
url(r'news/(?P<news_id>\d+)/$', news_details),
url(r'package/(?P<package_name>[^/]*)/(?P<package_version>[^/]*)/$', package_details),
url(r'section/(?P<section_title>[^/]*)/$', packages_list),
)
