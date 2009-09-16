from django.contrib import admin
from repository.winrepo.models import *

admin.site.register(Package)
admin.site.register(Section)
admin.site.register(Supported)
admin.site.register(Languages)
admin.site.register(Urls)
