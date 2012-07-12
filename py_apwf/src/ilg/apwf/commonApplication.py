
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
        print ("    Added CameraImageDate='{0}' to '{1}'".format(newCameraDateString, photoName))

        return newCameraDateString


    # return string
    def updateGpsInterpolatedReferenceDateOrAddIfNotPresent(self, photo, cameraDate):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getGpsInterpolatedReferenceDate(photo)
            cameraDateString = self.aperture.setGpsInterpolatedReferenceDate(photo, cameraDate)
            print ("    Updated GpsInterpolatedReferenceDate='{0}' to '{1}'".
                   format(cameraDateString, photoName))
            
            return cameraDateString
        
        except:
            pass

        newCameraDateString = self.aperture.addGpsInterpolatedReferenceDate(photo, cameraDate)
        print ("    Added GpsInterpolatedReferenceDate='{0}' to '{1}'".
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
        print ("    Added GpsInterpolatedReferenceDate='{0}' to '{1}'".
               format(newCameraDateString, photoName))
    
        return newCameraDateString


    # return string
    def updateCustomAltitudeOrAddIfNotPresent(self, photo, altitudeFloat):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getCustomAltitude(photo)
            altitudeString = self.aperture.setCustomAltitude(photo, altitudeFloat)
            print ("    Updated custom Altitude='{0}' to '{1}'".
                   format(altitudeString, photoName))
            
            return altitudeString
        
        except:
            pass

        altitudeString = self.aperture.addCustomAltitude(photo, altitudeFloat)
        print ("    Added custom Altitude='{0}' to '{1}'".
               format(altitudeString, photoName))
    
        return altitudeString


    # return string
    def updateGeotagInterpolateIntervalSecondsOrAddIfNotPresent(self, photo, intervalFloat):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getGeotagInterpolateIntervalSeconds(photo)
            intervalString = self.aperture.setGeotagInterpolateIntervalSeconds(photo, intervalFloat)
            print ("    Updated GeotagInterpolateIntervalSeconds='{0}' to '{1}'".
                   format(intervalString, photoName))
            
            return intervalString
        
        except:
            pass

        intervalString = self.aperture.addGeotagInterpolateIntervalSeconds(photo, intervalFloat)
        print ("    Added GeotagInterpolateIntervalSeconds='{0}' to '{1}'".
               format(intervalString, photoName))
    
        return intervalString


    # return string
    def updateGeotagInterpolateRatioOrAddIfNotPresent(self, photo, ratioFloat):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getGeotagInterpolateRatio(photo)
            ratioString = self.aperture.setGeotagInterpolateRatio(photo, ratioFloat)
            print ("    Updated GeotagInterpolateRatio='{0}' to '{1}'".
                   format(ratioString, photoName))
            
            return ratioString
        
        except:
            pass

        ratioString = self.aperture.addGeotagInterpolateRatio(photo, ratioFloat)
        print ("    Added GeotagInterpolateRatio='{0}' to '{1}'".
               format(ratioString, photoName))
    
        return ratioString


    def updateGpsLatitudeLongitude(self, photo, latitudeFloat, longitudeFloat):
        
        photoName = photo.name.get()
        
        self.aperture.setLatitude(photo, latitudeFloat)
        self.aperture.setLongitude(photo, longitudeFloat)
    
        print ("    Updated Latitude={0}, Longitude={1} to '{2}'".
               format(latitudeFloat, longitudeFloat, photoName))
        
        return
    

    def parseInputDate(self, inDateString):
        
        # may raise ValueError
        binDate = datetime.strptime(inDateString, '%d-%m-%Y %H:%M:%S')
        return binDate


    def parseInputUtcDate(self, inDateString):
        
        dt = self.parseInputDate(inDateString)
        
        tz = pytz.utc
        
        binDate = tz.localize(dt)
        return binDate
