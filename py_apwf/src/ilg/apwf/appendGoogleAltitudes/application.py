# -*- coding: utf-8 -*-

"""
Usage:
    python ilg.apwf.appendGoogleAltitudes [options]

Options:
    -n, --dry
        dry run, do not add/update tags
        
    -a, --all
        Process all photos, even if the GPS altitude is present
        
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Append the Google altitude to the selected photos. By default, if the
    GPS altitude is set, avoid the expensive Google access.
    
"""


import getopt
import urllib
import simplejson


from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication

from appscript import k


class Application(CommonApplication):
    
    def __init__(self, *argv):
                
        super(Application,self).__init__(*argv)

        # application specific members
        
        self.isComplete = False
        
        return
    

    def usage(self):
        
        print __doc__
        return


    def run(self):
        
        try:
            (opts, args) = getopt.getopt(self.argv[1:], 'nahv', ['dry', 'all', 'help', 'verbose'])
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
                elif o in ('-a', '--all'):
                    self.isComplete = True
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
        print "Append the Google altitude to the selected photos."
        print

        self.getMultipleSelection()        
        
        self.processAltitudes()
        
        return
            

    def getMultipleSelection(self):
        
        self.selectedPhotos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.selectedPhotos)),
        if self.isDryRun:
            print 'Dry run.',
        if self.isVerbose:
            print 'Verbose.',
        if self.isComplete:
            print 'Complete.',
            
        print
        print
    
    def processAltitudes(self):
        
        count = 0
        
        print 'Checking photos... '
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
                        
            latitude = photo.latitude.get()
            longitude = photo.longitude.get()
            
            if latitude == k.missing_value or longitude == k.missing_value:
                
                print ("  '{0}' from '{1}' not geotagged".
                       format(photoName, photoExifDate))
                continue
            
            try:
                altitude = self.aperture.getExifAltitude(photo)
                if altitude != k.missing_value:
                    continue    # if EXIF altitude is present, we're done
            except:
                pass    # not existing
            
            if not self.isComplete:          
                try:
                    self.aperture.getGpsAltitude(photo)
                    continue
                except:
                    pass    # not existing or empty
            
            try:
                self.aperture.getGoogleAltitude(photo)
                continue
            except:
                pass    # not existing or empty
            
            # all attempts failed, fetch value from Google
            
            count += 1
            
            altitudeFloat = self.getGoogleElevation(latitude, longitude)
            altitudeString = self.updateGoogleAltitudeOrAddIfNotPresent(photo, altitudeFloat)
            print ("  '{0}' from '{1}' Google alt={2}".
                       format(photoName, photoExifDate, altitudeString))
        
        if count == 0:
            print '... nothing to do.'
        elif count == 1:
            print '... 1 photo updated.'
        else:
            print '... {0} photos updated.'.format(count)
             
        return


    def getGoogleElevation(self, latitude, longitude):
        
        requestUrl = ('http://maps.googleapis.com/maps/api/elevation/json?'
                      'locations={0},{1}&sensor=false'.format(latitude, longitude))

        f = urllib.urlopen(requestUrl)
        parsedJsonResponse = simplejson.load(f)
        f.close()
        
        if self.isVerbose:
            print parsedJsonResponse
        
        results = parsedJsonResponse['results']
        result = results[0]
        elevationString =  result['elevation']
        
        return float(elevationString)
    
        
    
        
        