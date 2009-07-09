from django.utils.encoding import smart_unicode
from django.utils.xmlutils import SimplerXMLGenerator
from django.db.models.query import QuerySet
from piston.emitters import Emitter

import datetime
import os
import os.path
import sys

sys.path.append('..')
from wpkg.package import Package

from piston.utils import HttpStatusCode, Mimer

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class WLPXMLEmitter(Emitter):
    def _to_xml(self, data, e, answer):
        """ Turns each element on the self.construct() list into a complete Package object with its complete information """
        if isinstance(data, (list, tuple)):
            for item in data:
                self._to_xml(item, e, answer)
        elif isinstance(data, dict):
            for key, value in data.iteritems():
                if isinstance(value, datetime.date):
                    setattr(e, key, value.strftime("%d/%m/%y"))
                elif key.endswith("email"):
                    # Here we append the email to the name.
                    # If the email come first,we add it
                    # and then we add the name
                    key = key.rstrip("_email")
                    oldvalue = getattr(e, key)
                    if not (oldvalue):
                        setattr(e, key, '<'+value+'>')
                    else:
                        setattr(e, key, oldvalue+'<'+value+'>')
                elif isinstance(value, list):
                    # Here comes the properties for
                    # each M2M relation: Replaces, Suggests, 
                    # Provides, Conflicts, etc...
                    for element in value:
                        if 'name' in element.keys():
                            e.append_property(key, element['name']+" "+element['version'])
                        elif 'os_version' in element.keys():
                            e.append_property(key, element['os_version'])
                        elif 'language' in element.keys():
                            e.append_property(key, element['language'])
                elif isinstance(value, dict):
                    # Here section property gets its value
                    setattr(e, key, value['title'])
                else:
                    # Here each property gets its value.
                    # oldvalue just works when email for someone
                    # was setted before his/her name
                    oldvalue = getattr(e, key)
                    if oldvalue:                    
                        setattr(e, key, value+" "+oldvalue)
                    else:
                        setattr(e, key, value)
            answer.append(e.to_string())   

         
    def render(self, request):
        """ Render/Serializer Function to create XML information files for each Package or list of packages """
        answer = ["<packages>"]
        # self.construct() is a method defined in Piston to get the data from a Model
        data = self.construct()
        if isinstance(self.construct(), list):
            for element in self.construct():
                e = Package()
                self._to_xml(element, e, answer)
        else:
            e = Package()
            self._to_xml(self.construct(), e, answer)
        answer.append("</packages>")
        return ''.join(answer) #Turn the list into a string and return it

Emitter.unregister('xml')
Emitter.register('xml', WLPXMLEmitter, 'text/xml; charset=utf-8')
#Mimer.register(lambda *a: None, ('text/xml',))
