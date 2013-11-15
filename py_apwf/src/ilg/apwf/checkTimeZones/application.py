"""
Usage:
    python ilg.apwf.checkTimeZones [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Check if the time zones of the selected photos are properly set,
    to allow further processing.
    
"""


import getopt

#from datetime import timedelta

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication


class Application(CommonApplication):
    
    def __init__(self, *argv):
        
        super(Application,self).__init__(*argv)
        
        self.photos = None
        
        # clear all intermediate results
        
        self.collectionMake = None
        self.collectionModel = None

        self.firstPhotoInCollection = None
        self.lastPhotoInCollection = None

        self.gpsPhotoInCollection = None

        self.gpsBeforePhoto = None
        self.gpsAfterPhoto = None

        self.timedeltaToCamera = None
        
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
        print "Check if the time zones of the selected photos are properly set,"
        print "to allow further processing."
        print
        
        self.getMultipleSelection()        
        
        self.checkTimeZones()
                
        return
        

    def getMultipleSelection(self):
        
        self.photos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.photos))
        print
        
        return


    def checkTimeZones(self):
        
        hasBothTimeZones = False
        hasSomeTimeZones = False

        cameraTimeZoneName = None
        pictureTimeZoneName = None
        
        for photo in self.photos:
            
            photoName = photo.name.get()

            if cameraTimeZoneName == None:
                try:
                    cameraTimeZoneName = self.aperture.getCameraTimeZoneName(photo)
                except:
                    pass

            if pictureTimeZoneName == None:
                try:
                    pictureTimeZoneName = self.aperture.getPictureTimeZoneName(photo)
                except:
                    pass
        
            if pictureTimeZoneName != None and cameraTimeZoneName != None:
                
                if self.isVerbose:
                    print "'{0}' camera='{1}' picture='{2}'".format(photoName, 
                        cameraTimeZoneName, pictureTimeZoneName)
                    
                hasBothTimeZones = True
                break

            if pictureTimeZoneName != None or cameraTimeZoneName != None:
                hasSomeTimeZones = True
                
        if not hasSomeTimeZones and not hasBothTimeZones:
            
            print 'There are no time zone tags at all, use Batch Change to update'
            return
        
        count = 0
        for photo in self.photos:
            
            photoName = photo.name.get()

            try:
                crtCameraTimeZoneName = self.aperture.getCameraTimeZoneName(photo)
            except:
                crtCameraTimeZoneName = None

            try:
                crtPictureTimeZoneName = self.aperture.getPictureTimeZoneName(photo)
            except:
                crtPictureTimeZoneName = None
               
            if ((crtCameraTimeZoneName == cameraTimeZoneName) and 
                (crtPictureTimeZoneName == pictureTimeZoneName)):
                count += 1
            
        if count == len(self.photos):
            
            print "All photos have the same time zone settings:"
            print "  camera='{0}'".format(cameraTimeZoneName)
            print "  picture='{0}'".format(pictureTimeZoneName)
            return

        
        # If not all photos have the same settings, group them
        summary = dict()
        
        for photo in self.photos:
            
            photoName = photo.name.get()
            locationName = self.aperture.getMasterLocation(photo)

            try:
                crtCameraTimeZoneName = self.aperture.getCameraTimeZoneName(photo)
            except:
                crtCameraTimeZoneName = ""

            try:
                crtPictureTimeZoneName = self.aperture.getPictureTimeZoneName(photo)
            except:
                crtPictureTimeZoneName = ""

            tzKey = (crtCameraTimeZoneName, crtPictureTimeZoneName)
            
            locationTuple = (locationName,photoName)
            if tzKey in summary:
                summary[tzKey].append(locationTuple)
            else:
                summary[tzKey] = [locationTuple]

        print 'Multiple sets with different settings:'        
        for tzKey in summary.keys():
            
            (crtCameraTimeZoneName, crtPictureTimeZoneName) = tzKey
            print "- camera='{0}', picture='{1}'".format(crtCameraTimeZoneName, 
                                                      crtPictureTimeZoneName)
            
            locations = summary[tzKey]

            for locatioTuple in locations:
                
                (locationName,photoName) = locatioTuple
                print "    '{0} / {1}'".format(locationName,photoName)
        
