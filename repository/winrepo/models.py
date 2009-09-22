from django.db import models
from django.forms import ModelForm
from djangoratings.fields import RatingField
from django.contrib.auth.models import User

class Section(models.Model):
    title = models.CharField(max_length=200)
    def get_absolute_url(self):
        return "/website/section/%s/" % self.title

    def __unicode__(self):
        return self.title

class Supported(models.Model):
    os_version = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.os_version

class Languages(models.Model):
    language = models.CharField(max_length=200)

    def __unicode__(self):
        return self.language

class Urls(models.Model):
    url = models.CharField(max_length=300)
    
    def __unicode__(self):
        return self.url

class Package(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    architecture = models.CharField(max_length=5)
    installed_size = models.CharField(max_length=20)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    creator = models.CharField(max_length=200, blank=True)
    creator_email = models.EmailField(blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    publisher_email = models.EmailField(blank=True)
    maintainer = models.CharField(max_length=200, blank=True)
    maintainer_email = models.EmailField(blank=True)
    rights_holder = models.CharField(max_length=200, blank=True)
    rights_holder_email = models.EmailField(blank=True)
    release_date = models.DateField()
    changes = models.TextField(blank=True)
    size = models.DecimalField(max_digits=20, decimal_places=0, blank=True)
    license = models.CharField(max_length=200, blank=True)
    sha256 = models.CharField(max_length=200)
    homepage = models.URLField(blank=True)
    replaces = models.ManyToManyField('self', symmetrical=False, related_name='replaces_set', blank=True)
    pre_depends = models.ManyToManyField('self', symmetrical=False, related_name='pre_depends_set', blank=True)
    depends = models.ManyToManyField('self', symmetrical=False, related_name='depends_set', blank=True)
    provides = models.ManyToManyField('self', symmetrical=False, related_name='provides_set', blank=True)
    recommends = models.ManyToManyField('self', symmetrical=False, related_name='recommends_set', blank=True)
    suggests = models.ManyToManyField('self', symmetrical=False, related_name='suggests_set', blank=True)
    section = models.ForeignKey(Section, blank=True)
    supported = models.ManyToManyField(Supported, blank=True) 
    languages = models.ManyToManyField(Languages, blank=True)    
    urls = models.ManyToManyField(Urls, blank=True)
    rating = RatingField(range=5)
    user = models.ForeignKey(User)

    def get_absolute_url(self):
        return "/website/package/%s/%s/" % (self.name, self.version)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.version)

# Site related models

class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateField()
    author = models.ForeignKey(User)

    def __unicode__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        return "/website/news/%i/" % self.id
    
