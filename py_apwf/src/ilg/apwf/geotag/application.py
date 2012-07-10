"""
Usage:
    python ilg.apwf.geotag [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Geotag the selected photos, using a GPS track file in gpx format.
    
"""


import getopt

import pytz

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.aperture import Aperture

from appscript import k


class Application():
    
    def __init__(self, *argv):
        
        self.argv = argv
                
        self.aperture = Aperture()
        
        self.isVerbose = False
        
        # application specific members
        self.photos = None
        

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
        print "Geotag the selected photos, using a GPS track file in gpx format."
        print

        self.getMultipleSelection()        
        
        self.geotag()
        
        return
        

    def getMultipleSelection(self):
        
        self.photos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.photos))
        print
        
        return
    

    def geotag(self):
        
        print 'Geotagging photos... '
        for photo in self.photos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
            
            tzUtc = pytz.utc
            photoExifDateUtc = photoExifDate.astimezone(tzUtc)
            
            latitude = photo.latitude.get()
            longitude = photo.longitude.get()
            
            if latitude != k.missing_value and longitude != k.missing_value:
                
                print ("  '{0}' from '{1}' already geotagged, lat={2}, lon={3}".
                       format(photoName, photoExifDate, latitude, latitude))
                continue
            
            print ("  '{0}' from '{1}' not geotagged".
                       format(photoName, photoExifDate))
            
                
                
            
        return



        