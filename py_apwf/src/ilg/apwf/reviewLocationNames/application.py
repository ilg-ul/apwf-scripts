# -*- coding: utf-8 -*-

"""
Usage:
    python ilg.apwf.reviewLocationNames [options]

Options:
    -a, --all
        display all details
        
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    For the selected photos, list the location names, for visual review.
    
"""


import getopt

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication


class Application(CommonApplication):
    
    def __init__(self, *argv):
                
        super(Application,self).__init__(*argv)

        # application specific members
        
        self.isAll = False
        
        return
    

    def usage(self):
        
        print __doc__
        return


    def run(self):
        
        try:
            (opts, args) = getopt.getopt(self.argv[1:], 'ahv', ['all', 'help', 'verbose'])
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
                if o in ('-a', '--all'):
                    self.isAll = True
                elif o in ('-v', '--verbose'):
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
        print "List the location names of the selected photos."
        print

        self.getMultipleSelection()        
        
        self.reviewLocationNames()
        
        return
            
    
    def reviewLocationNames(self):
        
        print 'Reviewing location names for photos... '
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
                  
            crtDict = self.getGeocodingFields(photo) 
            
            if self.isAll:                 
                print ("  '{0}' from '{1}' in".
                       format(photoName, photoExifDate)),
                       
                for key in self.locationKeyNames:
                    val = crtDict[key]
                    if val != None:
                        val = val.encode('utf-8')
                    print "'{0}'".format(val),
            else:
                print ("  '{0}' in".format(photoName)),
                       
                for key in ['Province', 'City', 'Location']:
                    val = crtDict[key]
                    if val != None:
                        val = val.encode('utf-8')
                    print "'{0}'".format(val),
                    
                        
            print
                         
        return


    
    
        
        