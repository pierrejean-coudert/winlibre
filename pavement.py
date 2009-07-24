from paver.easy import *
from paver.setuputils import setup

import paver.doctools

paver.setuputils.install_distutils_tasks()

options(
    setup=dict(
    name='winlibre',
    version="0.0.1",
    description='Windows Package Manager',
    author='Bertrand Cachet',
    author_email='bertrand.cachet@gmail.com',
    url='http://code.google.com/p/winlibre',
    packages=['package_manager', 'package_creator', 'repository', ],
#    package_data = paver.setuputils.find_package_data("smart", package="smart",
#                                             only_in_packages=False),
    install_requires=[],
    test_suite='tests.suite',
    zip_safe=False,
    entry_points="""
    [console_scripts]
    paver = paver.command:main
    """,
    ),

    sphinx=Bunch(
        builddir="build",
        sourcedir="source"
    ),

    virtualenv=Bunch(
    	packages_to_install=['virtualenv', 'elementtree', 'elements', 
    	                     'sphinx', 'nose', 'pylint', 'django', 
    	                     'pywin32'],
    	script_name='bootstrap.py',
    	paver_command_line=None
    )
)

@task
@consume_args
def test():
    import unittest
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    import tests
    suite = tests.suite(options.args)
    unittest.TextTestRunner(verbosity=2).run(suite)

def get_paths(args):
    if len(args) > 0:
        paths = args
    else:
        _paths = os.listdir('.')
        paths = []
        for _path in _paths:
            if ((os.path.isdir(_path)) and (_path not in ['.svn', 'docs', 'lib', 'bin', 'include'])):
                paths.append(_path)
    return paths

@task
@consume_args
def clean():
    path("build").rmtree()
    try:
        paths = get_paths(options.args)
    except AttributeError:
        paths = []
    for _path in paths:
        cleaner = Cleaner(_path, ['pyc', '~'])
        if cleaner.is_permitted('delete'):
            cleaner.execute('file/folder removal')

@task
@needs(["clean", "doc_clean"])
def dist_clean():
    """Cleans up this paver directory. Removes the virtualenv traces, build directory and generated docs"""
    path(".Python").remove()
    path(".coverage").remove()
    path("%s.egg-info" % options.setup['name']).rmtree()
    import os
    if os.name == 'nt':
        path('Scripts').rmtree()
    elif os.name == 'posix':
        path("bin").rmtree()
    path("lib").rmtree()
    path("include").rmtree()

@task
@consume_args
def endings():    
    paths = get_paths(options.args)
    for _path in paths:
        cleaner = Cleaner(_path, ['.py'])
        if cleaner.is_permitted('change windows line-endings to unix line-endings'):
            cleaner.execute('convert endings')

from os.path import join, isdir, isfile
import sys, os, shutil
class Cleaner(object):
    """recursively cleans patterns of files/directories
    """
    def __init__(self, path, patterns):
        self.path = path
        self.patterns = patterns
        self.condition = lambda o: any(o.endswith(x) for x in self.patterns)
        self.path_funcs = {
            'show': lambda p: self.show(p) if self.condition(p) else None,
            'file/folder removal': self.delete,
            'convert endings': self.clean_endings,
        }
        self.targets = []

    def __repr__(self):
        return "<<Cleaner: path:%s , patterns:%s>>" % (
            self.path, self.patterns)

    def show(self, path):
        '''displays the path
        '''
        return path

    def clean_endings(self, path):
        ''' convert windows endings to unix endings
        '''
        old = file(path)
        lines = old.readlines()
        old.close()
        string = "".join([l.rstrip()+'\n' for l in lines])
        new = file(path, 'w')
        new.write(string)
        new.close()

    def delete(self, path):
        ''' delete path recursively
        '''
        if isfile(path):
            os.remove(path)
        if isdir(path):
            shutil.rmtree(path)

    def is_permitted(self, question):
        '''finds pattern and approves action on results
        '''
        results = self.walk(self.path, func=self.path_funcs['show'])
        if results:
            q = '%s items found. %s (y/n)? ' % (len(results), question)
            if raw_input(q) in ['y','Y']:
                self.targets = results
                return True
            else:
                print 'action aborted.'
        else:
            #print "No results."
            pass

    def execute(self, visitor):
        '''finds a pattern and applies a visitor function to path
        '''
        func = self.path_funcs[visitor]
        for target in self.targets:
            func(target)
        print 'completed %s of %s item(s).' % (visitor, len(self.targets))

    def walk(self, path, func, log=True):
        ''' walk path recursively
        '''
        results = []
        def visit(root, target, prefix):
            for i in target:
                item = join(root, i)
                obj = func(item)
                if obj:
                    results.append(obj)
                    if log: print prefix, obj
        for root, dirs, files in os.walk(path):
            visit(root, dirs, ' +-->')
            visit(root, files,' |-->')
        return results

@task
@needs('paver.virtual.bootstrap')
def bootstrap():
    """Build a virtualenv bootstrap for developing paver."""
    paver.virtual.bootstrap(options.script_name,
							options.packages_to_install,
							options.paver_command_line,
							)
									
