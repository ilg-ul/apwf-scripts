"""
Usage:
    python ilg.apwf.backupCreationDate [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Copy the EXIT ImageDate into a custom attribute.
    
"""


import getopt
import math

from datetime import timedelta

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication


class Application(CommonApplication):
    
    def __init__(self, *argv):
        
        super(Application,self).__init__(*argv)
        
        self.selectedPhotos = None
        
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
        return


    def run(self):
        
        try:
            (opts, args) = getopt.getopt(self.argv[1:], 'hv', 
                                         ['help', 'verbose'])
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
        print "Copy the EXIT ImageDate into a custom attribute."
        print
        
        self.getMultipleSelection()        
        
        self.backupCreationDate()
                
        return
        

    def getMultipleSelection(self):
        
        self.selectedPhotos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.selectedPhotos)),
        if self.isVerbose:
            print 'Verbose.',
            
        print
        print
        
        return

    def backupCreationDate(self):
        
        print 'Backing up the creation date of photos in collection... '
        for photo in self.selectedPhotos:
            
            cameraDate = self.aperture.getExifImageDate(photo)
            self.addCameraImageDateIfNotPresent(photo, cameraDate)
         
        print "  done."
        
        return
        
        