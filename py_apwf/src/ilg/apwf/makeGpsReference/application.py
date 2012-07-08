"""
Usage:
    python ilg.apwf.makeGpsReference [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Mark the selected photo as a GPS reference.
    
"""


import getopt
#from datetime import datetime

#import pytz

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication

from appscript import k


class Application(CommonApplication):
    
    def __init__(self, *argv):
        
        super(self.__class__,self).__init__()

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
        print "Mark the selected photo as a GPS reference."
        print

        self.getSingleSelection()
        self.makeGpsReference()

        
    def getSingleSelection(self):
        
        self.photo = self.aperture.getSingleSelection()
        
        return


    def makeGpsReference(self):
           
        photo = self.photo
        custom_tags = photo.custom_tags.get()
    
        try:
            gpsReferenceDate = self.aperture.getGpsReferenceDate(photo)
        except:
            gpsReferenceDate = None
            
        #print 'GpsReferenceDate="{0}"'.format(gpsReferenceDate)  
        
        mustUpdate = False
        mustAdd = False
        if gpsReferenceDate == None:
            mustAdd = True
        else:
            print ('This photo is already marked as reference ({0}).'.
                format(gpsReferenceDate))
            line = raw_input('Do you want to update it? (Yes): ')
            if line != 'Yes':
                raise ErrorWithDescription('No changes.')
            
            mustUpdate = True
                
        if mustUpdate or mustAdd:
            
            line = raw_input('Enter the UTC GPS reference date & time '
                             '(DD-MM-YYYY hh:mm:ss): ')
            
            if line == None:
                raise ErrorWithDescription('No date.')
            
            line = line.strip()
            
            if line == '':
                raise ErrorWithDescription('No date entered, ignored.') 

            try:
                newDateUtc = self.parseInputUtcDate(line)
            except ValueError:
                raise ErrorWithDescription("The date is not formatted as "
                       "'DD-MM-YYYY hh:mm:ss', ignored.")
                
            photoExifDate = self.aperture.getExifImageDate(self.photo)
            self.addCameraImageDateIfNotPresent(self.photo, photoExifDate)

            self.adjustImageDate(self.photo, newDateUtc)

            newGpsDateString = self.aperture.convertDateToString(newDateUtc)
            if mustAdd:
                
                self.aperture.makeTag(photo, k.custom_tag, 
                    'GpsReferenceDate', newGpsDateString)
                print ("Added GpsReferenceDate='{}'".
                       format(newGpsDateString))
                
            elif mustUpdate:
                
                self.aperture.setItemByName(custom_tags, 
                    'GpsReferenceDate', newGpsDateString)       
                print ("Updated GpsReferenceDate='{}'".
                       format(newGpsDateString))
                
        return
    
    
    def adjustImageDate(self, photo, newDate):
        
        # get the current date, to obtain the time zone
        exifImageDateTz = self.aperture.getExifImageDate(photo)

        # adjust the new date to the current image time zone
        newDateTz = newDate.astimezone(exifImageDateTz.tzinfo)
        self.aperture.adjustImageDate(photo, newDateTz)
        
        return
    
        
    
