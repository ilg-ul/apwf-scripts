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

from datetime import datetime

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
        
        self.inputTimes()
        
        self.selectReference()
        self.restoreTags()
        
        return
    

    def getMultipleSelection(self):
        
        self.selectedPhotos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.selectedPhotos))


    def inputTimes(self):
        
        line = raw_input("Enter original and adjusted times as "
                         "'dd-mm-yyyy HH:MM:SS HH:MM:SS': ")
        line = line.strip()
        if len(line) == 0:
            raise ErrorWithDescription('No date')
        
        ts = line.split()
        
        dateOrigString = ts[0] + ' ' + ts[1]
        timeActualString = ts[2]
        
        dateOrig = datetime.strptime(dateOrigString, '%d-%m-%Y %H:%M:%S')
        timeActual = datetime.strptime(timeActualString, '%H:%M:%S').time()
        dateActual = datetime.combine(dateOrig.date(), timeActual)
        
        timeDelta = dateOrig - dateActual
        
        print ("Original date='{0}', adjusted date='{1}', delta={2} sec".
               format(dateOrig, dateActual, timeDelta.total_seconds()))
           
        self.dateActual = dateActual
        self.timeDelta = timeDelta
        
        return
    

    def selectReference(self):
               
        print 'Selecting the reference photo... '
        for photo in self.selectedPhotos:

            photoExifDateTz = self.aperture.getExifImageDate(photo)            
            photoExifDateNoTz = photoExifDateTz.replace(tzinfo = None)

            if photoExifDateNoTz == self.dateActual:
                self.referencePhoto = photo

        if self.referencePhoto == None:
            raise ErrorWithDescription('No reference found in the collection')
        
        print '  {0} found.'.format(self.referencePhoto.name.get())
        
        return
    

    def restoreTags(self):
        
        print 'Restoring tags... '
        for photo in self.selectedPhotos:
            
            #photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)            

            cameraDate = photoExifDate + self.timeDelta
            self.addCameraImageDateIfNotPresent(photo, cameraDate)
            
            if photo == self.referencePhoto:
                self.addGpsInterpolatedReferenceDateIfNotPresent(photo, 
                                                                 photoExifDate)

        print '  done'
                    
        return


        