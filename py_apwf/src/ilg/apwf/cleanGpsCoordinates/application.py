# -*- coding: utf-8 -*-

"""
Usage:
    python ilg.apwf.cleanGpsCoordinates [options]

Options:
    -n, --dry
        dry run, do not add/update tags
        
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Remove the GPS latitude/longitude tags from the selected photos.
    Also remove the associated custom tags.
    
"""


import getopt

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.aperture import Aperture
from ilg.apwf.commonApplication import CommonApplication


class Application(CommonApplication):
    
    def __init__(self, *argv):
        
        super(Application,self).__init__(*argv)
        
        # application specific members
                
        self.selectedPhotos = None
        

    def usage(self):
        
        print __doc__


    def run(self):
        
        try:
            (opts, args) = getopt.getopt(self.argv[1:], 'nhv', ['dry', 'help', 'verbose'])
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
                if o in ('-n', '--dry'):
                    self.isDryRun = True
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
        print "Remove the GPS latitude/longitude tags from the selected photos."
        print

        self.getMultipleSelection()        
        
        self.cleanGpsCoordinates()
        
        return
        

    def cleanGpsCoordinates(self):
        
        print 'Removing GPS coordinates... '
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
            
            if not self.isDryRun:
                
                # unfortunately this is not effective               
                self.removeGpsLocation(photo)
                
                self.removeCustomAltitude(photo)
                self.removeGpsAltitude(photo)
                self.removeGoogleAltitude(photo)
                
                self.removeGeotagInterpolateIntervalSeconds(photo)
                self.removeGeotagInterpolateRatio(photo)

            print ("  '{0}' from '{1}' cleaned".
                       format(photoName, photoExifDate))
            
        return

        