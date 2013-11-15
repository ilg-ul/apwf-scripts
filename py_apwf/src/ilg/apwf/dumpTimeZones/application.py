"""
Usage:
    python ilg.apwf.updateTimeZones [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Dump the custom time zones of the selected images.
    
"""


import getopt

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.aperture import Aperture


class Application():
    
    def __init__(self, *argv):
        
        self.argv = argv
                
        self.aperture = Aperture()
        
        self.isVerbose = False
        
        self.photos = None
        
        # clear all intermediate results
        

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
        print "Dump the custom time zones of the selected images."
        print

        self.getMultipleSelection()        
        
        self.updateTimeZones()

        return
    

    def getMultipleSelection(self):
        
        self.photos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.photos))

        return
    

    def updateTimeZones(self):
        
        count = 0
        print 'Pictures with existing time zone settings... '
        for photo in self.photos:
            
            photoName = photo.name.get()
            locationName = self.aperture.getMasterLocation(photo)
                     
            try:
                pictureTimeZoneName = self.aperture.getPictureTimeZoneName(photo)
            except:
                pictureTimeZoneName = None
        
            try:
                cameraTimeZoneName = self.aperture.getCameraTimeZoneName(photo)
            except:
                cameraTimeZoneName = None

            if pictureTimeZoneName != None or cameraTimeZoneName != None:
                
                print "  '{0} / {1}' camera='{2}' picture='{3}'".format(locationName, 
                    photoName, cameraTimeZoneName, pictureTimeZoneName)
                count += 1

        if count == 0:
            print '  none found in selection'

        if (len(self.photos) - count) > 0:
            print ('  photos without time zones: {0}'.
                   format(len(self.photos) - count))
               
        return
        