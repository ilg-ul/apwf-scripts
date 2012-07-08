
from datetime import datetime
import pytz

from ilg.apwf.aperture import Aperture


class CommonApplication(object):

    def __init__(self, *argv):
        
        self.argv = argv
        
        self.aperture = Aperture()
        
        self.isVerbose = False

        return

    
    # return string
    def addCameraImageDateIfNotPresent(self, photo, cameraDate):
    
        try:
            cameraImageDate = self.aperture.getCameraImageDate(photo)
            cameraImageDateString = self.aperture.convertDateToString(cameraImageDate)
            return cameraImageDateString
        
        except:
            pass

        photoName = photo.name.get()
                
        newCameraDateString = self.aperture.addCameraImageDate(photo, cameraDate)
        print ("Added CameraImageDate='{0}' to '{1}'".format(newCameraDateString, photoName))

        return newCameraDateString


    # return string
    def updateGpsInterpolatedReferenceDateOrAddIfNotPresent(self, photo, cameraDate):
    
        try:
            self.aperture.getGpsInterpolatedReferenceDate(photo)
            cameraDateString = self.aperture.setGpsInterpolatedReferenceDate(photo, cameraDate)
            return cameraDateString
        
        except:
            pass

        photoName = photo.name.get()
                
        newCameraDateString = self.aperture.addGpsInterpolatedReferenceDate(photo, cameraDate)
        print ("Added GpsInterpolatedReferenceDate='{0}' to '{1}'".
               format(newCameraDateString, photoName))
    
        return newCameraDateString


    # return string
    def addGpsInterpolatedReferenceDateIfNotPresent(self, photo, cameraDate):
    
        try:
            cameraImageDate = self.aperture.getGpsInterpolatedReferenceDate(photo)
            cameraImageDateString = self.aperture.convertDateToString(cameraImageDate)
            return cameraImageDateString
        
        except:
            pass

        photoName = photo.name.get()
                
        newCameraDateString = self.aperture.addGpsInterpolatedReferenceDate(photo, cameraDate)
        print ("Added GpsInterpolatedReferenceDate='{0}' to '{1}'".
               format(newCameraDateString, photoName))
    
        return newCameraDateString


    def parseInputDate(self, inDateString):
        
        # may raise ValueError
        binDate = datetime.strptime(inDateString, '%d-%m-%Y %H:%M:%S')
        return binDate


    def parseInputUtcDate(self, inDateString):
        
        dt = self.parseInputDate(inDateString)
        
        tz = pytz.utc
        
        binDate = tz.localize(dt)
        return binDate
