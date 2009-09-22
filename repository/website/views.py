from repository.winrepo.models import *
from repository.website.forms import *
from urllib import unquote
from django.shortcuts import *
from django.contrib.auth import authenticate, login
from django.template import Context, Template, RequestContext
import re
from django.db.models import Q

# def get_sections():
#     return Section.objects.all()

# def login_form():
#     return LoginForm
    
def packages_list(request, section_title):
    requesturl = request.path
    user = request.user
    login = LoginForm()
    sections = Section.objects.all()
    chosensection = get_object_or_404(Section, title=unquote(section_title))
    packages_found = Package.objects.filter(section = chosensection.id)
    return render_to_response('packages_list.html',{"sections" : sections,"section" : chosensection, "packages" : packages_found, "loginform" : login, "requesturl" : requesturl, }, context_instance=RequestContext(request))

def package_details(request, package_name, package_version):
    requesturl = request.path
    user = request.user
    login = LoginForm()
    sections = Section.objects.all()
    package_received = get_object_or_404(Package, name=unquote(package_name), version=unquote(package_version))
    return render_to_response('package_details.html',{"sections" : sections,"package" : package_received, "loginform" : login, "requesturl" : requesturl, }, context_instance=RequestContext(request) )

def news_list(request):
    requesturl = request.path
    user = request.user
    login = LoginForm()
    sections = Section.objects.all()
    news = NewsItem.objects.all()
    return render_to_response('news_list.html',{"sections" : sections,"news" : news, "loginform" : login, "requesturl" : requesturl, }, context_instance=RequestContext(request))

def news_details(request, news_id):
    requesturl = request.path
    login = LoginForm()
    sections = Section.objects.all()
    newsfound = get_object_or_404(NewsItem, id=unquote(news_id))
    return render_to_response('news_details.html',{"sections" : sections, "newsitem" : newsfound, "loginform" : login, "requesturl" : requesturl,  }, context_instance=RequestContext(request) )

## Search methods. Taken from http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.POST) and request.POST['q'].strip():
        query_string = request.POST['q']
        print "Hola: "
        print query_string
        
        entry_query = get_query(query_string, ['name', 'version', 'creator', 'short_description', 'long_description', ])
        
        found_entries = Package.objects.filter(entry_query).order_by('release_date')

    return render_to_response('search_results.html',
                          { 'query_string': query_string, 'found_packages': found_entries },
                          context_instance=RequestContext(request))
