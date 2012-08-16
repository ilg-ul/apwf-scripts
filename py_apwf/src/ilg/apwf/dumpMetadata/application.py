# -*- coding: utf-8 -*-

"""
Usage:
    python -m ilg.apwf.dumpMetadata [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Dump all metadata for the selected photo.
    
"""

import getopt

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.aperture import Aperture

import appscript

class Application():
    
    def __init__(self, *argv):
        
        self.argv = argv
                
        self.aperture = Aperture()
        
        self.isVerbose = False

        return


    def usage(self):
        
        print __doc__


    def run(self):
        
        try:
            (opts, args) = getopt.getopt(self.argv[1:], 'hv', ['help', 'verbose'])
        except getopt.GetoptError as err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognised"
            self.usage()
            return 2
        
        try:
            if len(args) > 0:
                print 'unused arguments: ', args
                self.usage()
                return 2
                    
            for (o, a) in opts:
                a = a
                if o in ('-v', '--verbose'):
                    self.isVerbose = True
                elif o in ('-h', '--help'):
                    self.usage()
                    return 0
                else:
                    assert False, 'option not handled'
    
            self.process()
            
        except ErrorWithDescription as err:
            print err
    
        finally: 
            print   
            print '[done]'
            
        return 0        


    def process(self):
        
        print
        print "Dump all metadata for the selected photo."
        print
        
        self.getSingleSelection()
        self.dumpMetadata()


    def getSingleSelection(self):
        
        self.photo = self.aperture.getSingleSelection()
        return


    def dumpMetadata(self):
        
        photo = self.photo
        
        try:
            value = photo.color_label.get()
            print "color label: {0} {1}".format(value, type(value))
        except:
            print "!color label: missing" 
        
        value = photo.flagged.get()
        print "flagged: {0} {1}".format(value, type(value)) 
        
        value = photo.height.get()
        print "height: {0} {1}".format(value, type(value)) 
        
        value = photo.id.get()
        print "id: {0} {1}".format(value, type(value)) 
        
        value = photo.latitude.get()
        print "latitude: {0} {1}".format(value, type(value)) 
        
        value = photo.longitude.get()
        print "longitude: {0} {1}".format(value, type(value)) 
        
        value = photo.main_rating.get()
        print "main rating: {0} {1}".format(value, type(value)) 
        
        value = photo.name.get()
        print "name: {0} {1}".format(value, type(value)) 
        
        value = photo.online.get()
        print "online: {0} {1}".format(value, type(value)) 
        
        try:
            parentName = photo.parent.name.get()
            print "parent: {0} name:'{1}'".format(photo.parent.get(), parentName)
        except:
            print "!parent: missing"
                    
        value = photo.picked.get()
        print "picked: {0} {1}".format(value, type(value)) 
        
        value = photo.referenced.get()
        print "referenced: {0} {1}".format(value, type(value)) 
        
        value = photo.selected.get()
        print "selected: {0} {1}".format(value, type(value)) 
        
        value = photo.width.get()
        print "width: {0} {1}".format(value, type(value))    
            
        self.dumpCollection("EXIF", photo.EXIF_tags.get())
        
        self.dumpCollection("IPTC", photo.IPTC_tags.get())
        
        self.dumpCollection("custom", photo.custom_tags.get())
        
        self.dumpCollection("other", photo.other_tags.get())
        
        self.dumpKeywords(photo.keywords.get())
                  
        return

 
    def dumpCollection(self, name, coll):
        
        print
        
        if coll == None:
            return
        
        if len(coll) == 0:
            return
        
        for item in coll:
            
            itemName = item.name.get()
            
            try:
                itemValue = item.value.get().decode('utf-8')
            except:
                itemValue = None
                
            #if itemName == 'ImageDate':
            #    pass    # to allow a breakpoint
            
            if isinstance(itemValue, appscript.reference.Reference):
                print "{0} {1}: {2} name: '{3}'".format(name, itemName, itemValue, itemValue.name.get())
            else:
                itemValueOut = str(itemValue)
                try:
                    print "{0} {1}: {2} {3}".format(name, itemName, itemValueOut, str(itemValue.__class__))
                except:
                    print "!{0} {1}:".format(name, itemName)
                        
        return

    def dumpKeywords(self, coll):
        
        print
        
        if coll == None:
            return
        
        if len(coll) == 0:
            return
        
        for item in coll:
            
            keywordName = item.name.get()
            keywordNameUtf = keywordName.encode('utf-8')
            
            try:
                keywordParent = item.parent.get()
                keywordParentOut = str(keywordParent)
                print "keyword '{0}' of '{1}'".format(keywordNameUtf, 
                                                      keywordParentOut)
                
            except:
                print "keyword '{0}'".format(keywordNameUtf)
                                                
        return

