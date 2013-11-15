"""
Usage:
    python ilg.apwf.recreateCameraDate [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Recreate the original camera image date.
    
"""


import getopt

#from datetime import datetime

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication


class Application(CommonApplication):
    
    def __init__(self, *argv):
        
        super(Application,self).__init__(*argv)
                
        # clear all intermediate results
        
        self.dateOrig = None
        self.timeDelta = None
        
        self.referencePhoto = None
        
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
        print "Recreate the original camera image date."
        print

        self.getMultipleSelection()        
        
        self.restoreTags()
        
        return
    

    def getMultipleSelection(self):
        
        self.selectedPhotos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.selectedPhotos))


    def restoreTags(self):
        
        print 'Restoring dates... '
        for photo in self.selectedPhotos:
            
            cameraImageDate = self.aperture.getCameraImageDate(photo)
            self.aperture.adjustImageDate(photo, cameraImageDate)
            
        print '  done'
                    
        return


        