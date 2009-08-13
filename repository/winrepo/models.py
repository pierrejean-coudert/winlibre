from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    architecture = models.CharField(max_length=5)
    filename = models.CharField(max_length=250, blank=True)
    installed_size = models.CharField(max_length=20, blank=True)
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
    replaces = models.ManyToManyField('ReplacesList', symmetrical=False, related_name='replaces_set', blank=True)
    pre_depends = models.ManyToManyField('Pre_dependsList', symmetrical=False, related_name='pre_depends_set', blank=True)
    depends = models.ManyToManyField('DependsList', symmetrical=False, related_name='depends_set', blank=True)
    provides = models.ManyToManyField('ProvidesList', symmetrical=False, related_name='provides_set', blank=True)
    recommends = models.ManyToManyField('RecommendsList', symmetrical=False, related_name='recommends_set', blank=True)
    suggests = models.ManyToManyField('SuggestsList', symmetrical=False, related_name='suggests_set', blank=True)
    section = models.ForeignKey('Section', blank=True)
    supported = models.ManyToManyField('Supported', blank=True) 
    languages = models.ManyToManyField('Language', blank=True)    
    urls = models.ManyToManyField('Url', blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.version)

class ReplacesList(models.Model):
    packages = models.ManyToManyField(Package, related_name='replaces_set', blank=True, through='ReplacesOperator')

class Pre_dependsList(models.Model):
    packages = models.ManyToManyField(Package, symmetrical=False, related_name='pre_depends_set', blank=True, through='Pre_dependsOperator')

class DependsList(models.Model):
    packages = models.ManyToManyField(Package, symmetrical=False, related_name='depends_set', blank=True, through='DependsOperator')

class ProvidesList(models.Model):
    packages = models.ManyToManyField(Package, symmetrical=False, related_name='provides_set', blank=True, through='ProvidesOperator')

class RecommendsList(models.Model):
    packages = models.ManyToManyField(Package, symmetrical=False, related_name='recommends_set', blank=True, through='RecommendsOperator')

class SuggestsList(models.Model):
    packages = models.ManyToManyField(Package, symmetrical=False, related_name='suggests_set', blank=True, through='SuggestsOperator')

class ReplacesOperator(models.Model):
    OPERATOR = (
        (u'LT', u'less than'),
        (u'LTE', u'less than or equal to'),
        (u'EQ', u'equal to'),
        (u'GTE', u'greater than or equal to'),
        (u'GT', u'greater than'),
        )
    replacesList = models.ForeignKey(ReplacesList)
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=200)
    op = models.CharField(max_length=4, choices=OPERATOR)
    
class Pre_dependsOperator(models.Model):
    OPERATOR = (
        (u'LT', u'less than'),
        (u'LTE', u'less than or equal to'),
        (u'EQ', u'equal to'),
        (u'GTE', u'greater than or equal to'),
        (u'GT', u'greater than'),
        )
    pre_dependsList = models.ForeignKey(Pre_dependsList)
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=200)
    op = models.CharField(max_length=4, choices=OPERATOR)

class DependsOperator(models.Model):
    OPERATOR = (
        (u'LT', u'less than'),
        (u'LTE', u'less than or equal to'),
        (u'EQ', u'equal to'),
        (u'GTE', u'greater than or equal to'),
        (u'GT', u'greater than'),
        )
    dependsList = models.ForeignKey(DependsList)
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=200)
    op = models.CharField(max_length=4, choices=OPERATOR)

class ProvidesOperator(models.Model):
    OPERATOR = (
        (u'LT', u'less than'),
        (u'LTE', u'less than or equal to'),
        (u'EQ', u'equal to'),
        (u'GTE', u'greater than or equal to'),
        (u'GT', u'greater than'),
        )
    providesList = models.ForeignKey(ProvidesList)
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=200)
    op = models.CharField(max_length=4, choices=OPERATOR)

class RecommendsOperator(models.Model):
    OPERATOR = (
        (u'LT', u'less than'),
        (u'LTE', u'less than or equal to'),
        (u'EQ', u'equal to'),
        (u'GTE', u'greater than or equal to'),
        (u'GT', u'greater than'),
        )
    recommendsList = models.ForeignKey(RecommendsList)
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=200)
    op = models.CharField(max_length=4, choices=OPERATOR)

class SuggestsOperator(models.Model):
    OPERATOR = (
        (u'LT', u'less than'),
        (u'LTE', u'less than or equal to'),
        (u'EQ', u'equal to'),
        (u'GTE', u'greater than or equal to'),
        (u'GT', u'greater than'),
        )
    suggestsList = models.ForeignKey(SuggestsList)
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=200)
    op = models.CharField(max_length=4, choices=OPERATOR)


class Section(models.Model):
    title = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.title

class Supported(models.Model):
    os_version = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.os_version

class Language(models.Model):
    language = models.CharField(max_length=200)

    def __unicode__(self):
        return self.language

class Url(models.Model):
    url = models.CharField(max_length=500, blank=True)
    
    def __unicode__(self):
        return self.url
