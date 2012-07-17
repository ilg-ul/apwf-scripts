
from datetime import datetime
import pytz

from appscript import k

from ilg.apwf.aperture import Aperture


CUSTOM_TAG_EMPTY_VALUE = ''


class CommonApplication(object):

    def __init__(self, *argv):
        
        self.argv = argv
        
        self.aperture = Aperture()
        
        self.isVerbose = False
        self.isDryRun = False

        self.selectedPhotos = None

        return


    def getMultipleSelection(self):
        
        self.selectedPhotos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.selectedPhotos)),
        if self.isDryRun:
            print 'Dry run.',
        if self.isVerbose:
            print 'Verbose.',
            
        print
        print
        
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
        if self.isVerbose:
            print ("    Added CameraImageDate='{0}' to '{1}'".format(newCameraDateString, photoName))

        return newCameraDateString


    # return string
    def updateGpsInterpolatedReferenceDateOrAddIfNotPresent(self, photo, cameraDate):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getGpsInterpolatedReferenceDate(photo)
            cameraDateString = self.aperture.setGpsInterpolatedReferenceDate(photo, cameraDate)
            if self.isVerbose:
                print ("    Updated GpsInterpolatedReferenceDate='{0}' for '{1}'".
                       format(cameraDateString, photoName))
            
            return cameraDateString
        
        except:
            pass

        newCameraDateString = self.aperture.addGpsInterpolatedReferenceDate(photo, cameraDate)
        if self.isVerbose:
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
        if self.isVerbose:
            print ("    Added GpsInterpolatedReferenceDate='{0}' to '{1}'".
                   format(newCameraDateString, photoName))
    
        return newCameraDateString


    # return string
    def updateCustomAltitudeOrAddIfNotPresent(self, photo, altitudeFloat):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getCustomAltitude(photo)
            altitudeString = self.aperture.setCustomAltitude(photo, altitudeFloat)
            if self.isVerbose:
                print ("    Updated custom Altitude='{0}' for '{1}'".
                       format(altitudeString, photoName))
            
        except:
 
            altitudeString = self.aperture.addCustomAltitude(photo, altitudeFloat)
            if self.isVerbose:
                print ("    Added custom Altitude='{0}' to '{1}'".
                       format(altitudeString, photoName))
    
        return altitudeString


    # return string
    def updateGpsAltitudeOrAddIfNotPresent(self, photo, altitudeFloat):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getGpsAltitude(photo)
            altitudeString = self.aperture.setGpsAltitude(photo, altitudeFloat)
            if self.isVerbose:
                print ("    Updated GpsAltitude='{0}' for '{1}'".
                       format(altitudeString, photoName))
            
            return altitudeString
        
        except:
            pass

        altitudeString = self.aperture.addGpsAltitude(photo, altitudeFloat)
        if self.isVerbose:
            print ("    Added GpsAltitude='{0}' to '{1}'".
                   format(altitudeString, photoName))
    
        return altitudeString


    # return string
    def updateGoogleAltitudeOrAddIfNotPresent(self, photo, altitudeFloat):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getGoogleAltitude(photo)
            altitudeString = self.aperture.setGoogleAltitude(photo, altitudeFloat)
            if self.isVerbose:
                print ("    Updated GoogleAltitude='{0}' for '{1}'".
                       format(altitudeString, photoName))
        
        except:
            altitudeString = self.aperture.addGoogleAltitude(photo, altitudeFloat)
            if self.isVerbose:
                print ("    Added GoogleAltitude='{0}' to '{1}'".
                       format(altitudeString, photoName))
    
        return altitudeString


    # return string
    def updateGeotagInterpolateIntervalSecondsOrAddIfNotPresent(self, photo, intervalFloat):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getGeotagInterpolateIntervalSeconds(photo)
            intervalString = self.aperture.setGeotagInterpolateIntervalSeconds(photo, intervalFloat)
            if self.isVerbose:
                print ("    Updated GeotagInterpolateIntervalSeconds='{0}' for '{1}'".
                       format(intervalString, photoName))
            
        except:
            intervalString = self.aperture.addGeotagInterpolateIntervalSeconds(photo, intervalFloat)
            if self.isVerbose:
                print ("    Added GeotagInterpolateIntervalSeconds='{0}' to '{1}'".
                       format(intervalString, photoName))
    
        return intervalString


    def removeGeotagInterpolateIntervalSeconds(self, photo):

        photoName = photo.name.get()
                
        try:
            self.aperture.getGeotagInterpolateIntervalSeconds(photo)
            # set it to empty only if it exists
            self.aperture.setGeotagInterpolateIntervalSeconds(photo, 
                CUSTOM_TAG_EMPTY_VALUE)
            if self.isVerbose:
                print ("    Removing GeotagInterpolateIntervalSeconds from '{0}'".
                       format(photoName))
        except:
            pass
        
        return
        

    def removeGeotagInterpolateRatio(self, photo):

        photoName = photo.name.get()
                
        try:
            self.aperture.getGeotagInterpolateRatio(photo)
            # set it to empty only if it exists
            self.aperture.setGeotagInterpolateRatio(photo, 
                CUSTOM_TAG_EMPTY_VALUE)
            if self.isVerbose:
                print ("    Removing GeotagInterpolateRatio from '{0}'".
                       format(photoName))
        except:
            pass
        
        return
        

    def removeCustomAltitude(self, photo):

        photoName = photo.name.get()
                
        try:
            self.aperture.getCustomAltitude(photo)
            # set it to empty only if it exists
            self.aperture.setCustomAltitude(photo, CUSTOM_TAG_EMPTY_VALUE)
            if self.isVerbose:
                print ("    Removing custom Altitude from '{0}'".
                       format(photoName))
        except:
            pass
        
        return
        

    def removeGpsAltitude(self, photo):

        photoName = photo.name.get()
                
        try:
            self.aperture.getGpsAltitude(photo)
            # set it to empty only if it exists
            self.aperture.setGpsAltitude(photo, CUSTOM_TAG_EMPTY_VALUE)
            if self.isVerbose:
                print ("    Removing GpsAltitude from '{0}'".
                       format(photoName))
        except:
            pass
        
        return


    def removeGoogleAltitude(self, photo):

        photoName = photo.name.get()
                
        try:
            self.aperture.getGoogleAltitude(photo)
            # set it to empty only if it exists
            self.aperture.setGoogleAltitude(photo, CUSTOM_TAG_EMPTY_VALUE)
            if self.isVerbose:
                print ("    Removing GoogleAltitude from '{0}'".
                       format(photoName))
        except:
            pass
        
        return



    # return string
    def updateGeotagInterpolateRatioOrAddIfNotPresent(self, photo, ratioFloat):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getGeotagInterpolateRatio(photo)
            ratioString = self.aperture.setGeotagInterpolateRatio(photo, ratioFloat)
            if self.isVerbose:
                print ("    Updated GeotagInterpolateRatio='{0}' for '{1}'".
                       format(ratioString, photoName))
            
        except:
            ratioString = self.aperture.addGeotagInterpolateRatio(photo, ratioFloat)
            if self.isVerbose:
                print ("    Added GeotagInterpolateRatio='{0}' to '{1}'".
                       format(ratioString, photoName))
    
        return ratioString


    def updateGpsLatitudeLongitude(self, photo, latitudeFloat, longitudeFloat):
        
        photoName = photo.name.get()
        
        self.aperture.setLatitude(photo, latitudeFloat)
        self.aperture.setLongitude(photo, longitudeFloat)
    
        print ("    Updated Latitude={0}, Longitude={1} for '{2}'".
               format(latitudeFloat, longitudeFloat, photoName))
        
        return
    

    def removeGpsLocation(self, photo):
        
        photoName = photo.name.get()

        if False:
            # unfortunately it is not possible (or I don't know how)
            # to remove a tag value                
            self.aperture.setLatitude(photo, k.missing_value)
            self.aperture.setLongitude(photo, k.missing_value)
        
            if self.isVerbose:
                print ("    Removing Latitude/Longitude from '{0}'".
                       format(photoName))

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


    def getGeocodingFields(self, photo):
        
        crtDict = {}
                    
        try:
            crtDict['CountryCode'] = self.aperture.getImageCountryCode(photo)
        except:
            crtDict['CountryCode'] = None
                    
        try:
            crtDict['CountryName'] = self.aperture.getImageCountryName(photo)
        except:
            crtDict['CountryName'] = None
                
        try:
            crtDict['Province'] = self.aperture.getImageStateProvince(photo)
        except:
            crtDict['Province'] = None

        try:
            crtDict['City'] = self.aperture.getImageCity(photo)
        except:
            crtDict['City'] = None

        try:
            crtDict['Location'] = self.aperture.getImageSubLocation(photo)
        except:
            crtDict['Location'] = None
            
        return crtDict
    
    
    def updateGeocodingFieldsOrAddIfNotPresent(self, photo, crtDict, newDict, 
                                               doOverwrite):
        
        retDict = {}
        
        if doOverwrite or crtDict['CountryCode'] == None:
            val = newDict['CountryCode']
            retDict['CountryCode'] = val
            if val == None:
                val =''
            self.updateImageCountryCodeOrAddIfMissing(photo, val)
        else:
            retDict['CountryCode'] = None
            
        if doOverwrite or crtDict['CountryName'] == None:
            val = newDict['CountryName']
            retDict['CountryName'] = val
            if val == None:
                val =''
            self.updateImageCountryNameOrAddIfMissing(photo, val)
        else:
            retDict['CountryName'] = None

        if doOverwrite or crtDict['Province'] == None:
            val = newDict['Province']
            retDict['Province'] = val
            if val == None:
                val =''
            self.updateImageStateProvinceOrAddIfMissing(photo, val)
        else:
            retDict['Province'] = None

        if doOverwrite or crtDict['City'] == None:
            val = newDict['City']
            retDict['City'] = val
            if val == None:
                val =''
            self.updateImageCityOrAddIfMissing(photo, val)
        else:
            retDict['City'] = None

        if doOverwrite or crtDict['Location'] == None:
            val = newDict['Location']
            retDict['Location'] = val
            if val == None:
                val =''
            self.updateImageSubLocationOrAddIfMissing(photo, val)
        else:
            retDict['Location'] = None
            
        return retDict
    

    def updateImageCountryCodeOrAddIfMissing(self, photo, countryCodeString):
        
        photoName = photo.name.get()
                
        try:
            self.aperture.getImageCountryCode(photo)
            self.aperture.setImageCountryCode(photo, countryCodeString)
            if self.isVerbose:
                print ("    Updated IPTC Country/PrimaryLocationCode='{0}' for '{1}'".
                       format(countryCodeString, photoName))
        
        except:
            self.aperture.addImageCountryCode(photo, countryCodeString)
            if self.isVerbose:
                print ("    Added IPTC Country/PrimaryLocationCode='{0}' to '{1}'".
                       format(countryCodeString, photoName))
    
        return


    def updateImageCountryNameOrAddIfMissing(self, photo, countryNameString):
        
        photoName = photo.name.get()
                
        try:
            self.aperture.getImageCountryName(photo)
            self.aperture.setImageCountryName(photo, countryNameString)
            if self.isVerbose:
                print ("    Updated IPTC Country/PrimaryLocationName='{0}' for '{1}'".
                       format(countryNameString, photoName))
        
        except:
            self.aperture.addImageCountryName(photo, countryNameString)
            if self.isVerbose:
                print ("    Added IPTC Country/PrimaryLocationName='{0}' to '{1}'".
                       format(countryNameString, photoName))
    
        return


    def updateImageStateProvinceOrAddIfMissing(self, photo, stateProvinceString):
        
        photoName = photo.name.get()
                
        try:
            self.aperture.getImageStateProvince(photo)
            self.aperture.setImageStateProvince(photo, stateProvinceString)
            if self.isVerbose:
                print ("    Updated IPTC Province/State='{0}' for '{1}'".
                       format(stateProvinceString, photoName))
        
        except:
            self.aperture.addImageStateProvince(photo, stateProvinceString)
            if self.isVerbose:
                print ("    Added IPTC Province/State='{0}' to '{1}'".
                       format(stateProvinceString, photoName))
    
        return


    def updateImageCityOrAddIfMissing(self, photo, cityString):
        
        photoName = photo.name.get()
                
        try:
            self.aperture.getImageCity(photo)
            self.aperture.setImageCity(photo, cityString)
            if self.isVerbose:
                print ("    Updated IPTC Image City='{0}' for '{1}'".
                       format(cityString, photoName))
        
        except:
            self.aperture.addImageCity(photo, cityString)
            if self.isVerbose:
                print ("    Added IPTC Image City='{0}' to '{1}'".
                       format(cityString, photoName))
    
        return

        
    def updateImageSubLocationOrAddIfMissing(self, photo, subLocationString):
        
        photoName = photo.name.get()
                
        try:
            self.aperture.getImageSubLocation(photo)
            self.aperture.setImageSubLocation(photo, subLocationString)
            if self.isVerbose:
                print ("    Updated IPTC SubLocation='{0}' for '{1}'".
                       format(subLocationString, photoName))
        
        except:
            self.aperture.addImageSubLocation(photo, subLocationString)
            if self.isVerbose:
                print ("    Added IPTC SubLocation='{0}' to '{1}'".
                       format(subLocationString, photoName))
    
        return

  
        
