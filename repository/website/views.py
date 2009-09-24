from repository.winrepo.models import *
from repository.website.forms import *
from urllib import unquote
from django.shortcuts import *
from django.contrib.auth import authenticate, login
from django.template import Context, Template, RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import re
from django.db.models import Q
from repository.settings import MEDIA_ROOT, MEDIA_URL

def getsections(request):
    ''' Returns a dictionary that fills the RequestContext object with other parameter to fill
    the templates. Here we take the available sections, etc.
    '''
    sections = Section.objects.all()
    path = request.path
    loginform = LoginForm()
    return {'sections': sections, 'path' : path, 'loginform' : loginform, "requesturl" : path}

def packages_list(request, section_title):
    ''' Returns a rendered html tha displays the list of packages available
    in the repository for certain section
    '''
    requesturl = request.path
    user = request.user
    login = LoginForm()
    chosensection = get_object_or_404(Section, title=unquote(section_title))
    packages_found = Package.objects.filter(section = chosensection.id)
    return render_to_response('packages_list.html',{"section" : chosensection, "packages" : packages_found, "loginform" : login, "requesturl" : requesturl, }, context_instance=RequestContext(request))

def package_details(request, package_name, package_version):
    ''' Returns a rendered html that displays the details of package selected
    from the repository
    '''
    requesturl = request.path
    user = request.user
    login = LoginForm()
    package_received = get_object_or_404(Package, name=unquote(package_name), version=unquote(package_version))
    already_voted = False
    if package_received.rating.get_rating_for_user(user, request.META['REMOTE_ADDR']) > 0:
        already_voted = True
    return render_to_response('package_details.html',{"package" : package_received, "loginform" : login, "requesturl" : requesturl, "already_voted" : already_voted, }, context_instance=RequestContext(request) )

def news_list(request):
    ''' Returns a rendered html that displays the list of news in the website
    '''
    requesturl = request.path
    user = request.user
    login = LoginForm()
    news = NewsItem.objects.all()
    return render_to_response('news_list.html',{"news" : news, "loginform" : login, "requesturl" : requesturl, }, context_instance=RequestContext(request))

def news_details(request, news_id):
    ''' Returns a rendered html that displays the details of a selected news item
    '''
    requesturl = request.path
    login = LoginForm()
    newsfound = get_object_or_404(NewsItem, id=unquote(news_id))
    return render_to_response('news_details.html',{"newsitem" : newsfound, "loginform" : login, "requesturl" : requesturl,  }, context_instance=RequestContext(request) )

def vote(request):
    ''' Registers a vote of the logged in user for certain 
    package  and redirects the user to the same page he was at '''
    package = get_object_or_404(Package, id=request.POST['package_id'])
    package.rating.add(score=request.POST['vote'], user=request.user, ip_address=request.META['REMOTE_ADDR'])
    return HttpResponseRedirect(request.path)

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
    ''' Retunrs a render html that contains the matched packages for the given string in the query.
    the query istring is in request.POST['q']
    '''
    sections = Section.objects.all()
    login = LoginForm()
    query_string = ''
    found_entries = None
    if ('q' in request.POST) and request.POST['q'].strip():
        query_string = request.POST['q']
        print "Hola: "
        print query_string
        
        entry_query = get_query(query_string, ['name', 'version', 'creator', 'short_description', 'long_description', ])
        
        found_entries = Package.objects.filter(entry_query).order_by('release_date')

    return render_to_response('search_results.html',
                          { 'query_string': query_string, 'found_packages': found_entries,  'sections' : sections, },
                          context_instance=RequestContext(request))

## Upload handling

def upload_file(request):
    ''' Returns a rendered html displaying a UploadFileForm or a confirmation that the package was uploaded
    It saves the package in the specified directory
    '''
    sections = Section.objects.all()
    login = LoginForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        package = get_object_or_404(Package, id=request.POST['package'])
        dir = package.section.title
        filename = package.name+'_'+package.version+'_'+package.architecture+'.wlp'
        if form.is_valid():
            destination = open('%s/%s/%s' % (MEDIA_ROOT, dir, filename), 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
                destination.close()
            file_url = MEDIA_URL+dir+'/'+filename
            uf = UploadedFiles(package=package,owner=request.user,url=file_url)
            uf.save()
            return render_to_response('upload_complete.html', {'file_url' : file_url, 'sections' : sections, }, context_instance=RequestContext(request) )
    else:
        form = UploadFileForm()
    return render_to_response('upload_file.html', {'form': form, 'sections' : sections, }, context_instance=RequestContext(request))


def uploaded_files (request):
    ''' Returns a rendered html that displays the uploaded files by the logged in user
    '''
    sections = Section.objects.all()
    uploaded_files = UploadedFiles.objects.filter(owner=request.user)
#    uploaded_files = UploadedFiles.objects.all()
    return render_to_response('uploaded_files.html', {'sections' : sections, 'uploaded_files' : uploaded_files,}, context_instance=RequestContext(request))
