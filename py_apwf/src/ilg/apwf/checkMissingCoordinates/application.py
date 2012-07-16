# -*- coding: utf-8 -*-

"""
Usage:
    python ilg.apwf.checkMissingCoordinates [options]

Options:
    -n, --dry
        dry run, do not add/update tags
        
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Check the selected photos, and list those without latitude/longitude.
    
"""


import getopt

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication

from appscript import k


class Application(CommonApplication):
    
    def __init__(self, *argv):
                
        super(Application,self).__init__(*argv)

        # application specific members
        
        return
    

    def usage(self):
        
        print __doc__
        return


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
        print "Check the selected photos, and list those without latitude/longitude."
        print

        self.getMultipleSelection()        
        
        self.checkMissingCoordinates()
        
        return
            
    
    def checkMissingCoordinates(self):
        
        count = 0
        
        print 'Checking photos... '
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
                        
            latitude = photo.latitude.get()
            longitude = photo.longitude.get()
            
            if latitude == k.missing_value or longitude == k.missing_value:
                
                count += 1

                print ("  '{0}' from '{1}' not geotagged".
                       format(photoName, photoExifDate))
                continue
            
        
        if count == 0:
            print '... all photos have lat/lon.'
        elif count == 1:
            print '... 1 not geotagged photo found.'
        else:
            print '... {0} not geotagged photos found.'.format(count)
             
        return


    
    
        
        