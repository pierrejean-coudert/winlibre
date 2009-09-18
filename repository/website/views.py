from repository.winrepo.models import *
from urllib import unquote
from django.shortcuts import *

def packages_list(request, section_title):
    sections = Section.objects.all()
    chosensection = get_object_or_404(Section, title=unquote(section_title))
    packages = Package.objects.filter(section = chosensection.id)
    return render_to_response('packages_list.html',{"sections" : sections,"section" : chosensection, "packages" : packages, },)

def package_details(request, package_name, package_version):
    sections = Section.objects.all()
    package = get_object_or_404(Package, name=unquote(package_name), version=unquote(package_version))
    return render_to_response('package_details.html',{"sections" : sections,"package" : package,}, )
      
