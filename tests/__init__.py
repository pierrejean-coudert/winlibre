#!/usr/bin/env python

import sys
import os
import unittest


def search_files_recursively(search_path, search_filter, found_items):
    files = os.listdir(search_path)
    for found_file in filter(search_filter, files):
        found_items.append(os.path.join(search_path, found_file))
    for aFile in files:
        if os.path.isdir(os.path.join(search_path, aFile)) :
            search_files_recursively(join(search_path,aFile), search_filter, found_items)

def search_test_files(path):
    import re
    rule = re.compile(".*\_test.py$", re.IGNORECASE)
    test_files = []
    search_files_recursively(path, rule.search, test_files)
    return test_files

def suite(paths):
    import unittest    
    def my_import(name):
        # See http://docs.python.org/lib/built-in-funcs.html#l2h-6
        components = name.split('.')
        try:
            # python setup.py test
            mod = __import__(name)
            for comp in components[1:]:
                mod = getattr(mod, comp)
        except ImportError, e:
            print 'Error', e
            # python tests/alltests.py
            mod = __import__(components[1])
        return mod
        
    def convert_filename_to_modulname(filename):
        modulname = filename.replace(os.sep, '.').replace('.py', '')
        return modulname
    local_path = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(local_path)
    alltests = unittest.TestSuite()
    if not (len(paths) > 0):
        paths = ['package_manager', 'package_creator', 'repository']
    for path in paths:
        sys.path.append(os.path.join(local_path, path))
        test_files = search_test_files(os.path.join(path, 'tests'))
        modules_to_test = map(convert_filename_to_modulname, test_files)
        for module in map(my_import, modules_to_test):
            alltests.addTest(module.suite())
    return alltests

if __name__ == '__main__':
    def run_all():
        try:
            unittest.TextTestRunner().run(suite(sys.argv[1:]))
        finally:
            pass
    run_all()
