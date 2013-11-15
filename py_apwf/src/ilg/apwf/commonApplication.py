# -*- coding: utf-8 -*-

from datetime import datetime
import pytz

from appscript import k

from ilg.apwf.aperture import Aperture
from ilg.apwf.errorWithDescription import ErrorWithDescription

from ilg.apwf.flickr import FlickrException


CUSTOM_TAG_EMPTY_VALUE = ''


class CommonApplication(object):

    def __init__(self, *argv):
        
        self.argv = argv
        
        self.aperture = Aperture()
        
        self.isVerbose = False
        self.isDryRun = False

        self.selectedPhotos = None

        self.locationKeyNames = ['CountryCode', 'CountryName', 
                                 'Province', 'City', 'Location']

        return


    def getMultipleSelection(self):
        
        self.selectedPhotos = self.aperture.getMultipleSelection()
        count = len(self.selectedPhotos)
        
        if count == 1:
            print 'Processing 1 photo.',
        else:
            print 'Processing {0} photos.'.format(count),
            
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

        newCameraDateString = self.aperture.addGpsInterpolatedReferenceDate(
                                                photo, cameraDate)
        if self.isVerbose:
            print ("    Added GpsInterpolatedReferenceDate='{0}' to '{1}'".
                   format(newCameraDateString, photoName))
    
        return newCameraDateString


    # return string
    def updateFlickrMetadataDateOrAddIfNotPresent(self, photo, metadataDate):
    
        photoName = photo.name.get()
                
        try:
            self.aperture.getFlickrMetadataDate(photo)
            metadataDateString = self.aperture.setFlickrMetadataDate(photo, 
                        metadataDate)
            if self.isVerbose:
                print ("    Updated FlickrMetadataDate='{0}' for '{1}'".
                       format(metadataDateString, photoName))
            
            return metadataDateString
        
        except:
            pass

        newMetadataDateString = self.aperture.addFlickrMetadataDate(photo, 
                        metadataDate)
        if self.isVerbose:
            print ("    Added FlickrMetadataDate='{0}' to '{1}'".
                   format(newMetadataDateString, photoName))
    
        return newMetadataDateString


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
    
        if self.isVerbose:
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
        crtDict['hasNone'] = False
                    
        try:
            crtDict['CountryCode'] = self.aperture.getImageCountryCode(photo)
        except:
            crtDict['CountryCode'] = None
            crtDict['hasNone'] = True
                    
        try:
            crtDict['CountryName'] = self.aperture.getImageCountryName(photo)
        except:
            crtDict['CountryName'] = None
            crtDict['hasNone'] = True
                
        try:
            crtDict['Province'] = self.aperture.getImageStateProvince(photo)
        except:
            crtDict['Province'] = None
            crtDict['hasNone'] = True

        try:
            crtDict['City'] = self.aperture.getImageCity(photo)
        except:
            crtDict['City'] = None
            crtDict['hasNone'] = True

        try:
            crtDict['Location'] = self.aperture.getImageSubLocation(photo)
        except:
            crtDict['Location'] = None
            crtDict['hasNone'] = True
                        
        return crtDict

    
    def checkFieldsToUpdate(self, photo, crtDict, newDict, doOverwrite):
        
        retDict = {}
        retDict['changed'] = False
       
        for key in ['CountryCode', 'CountryName', 'Province', 'City', 'Location']:
            if doOverwrite or crtDict[key] == None:
                val = newDict[key]
                if val == None:
                    val ='-'
                
                retDict[key] = val
                
                retDict['changed'] = True
            else:
                retDict[key] = None
            
        return retDict
    
     
    def updateGeocodingFieldsOrAddIfNotPresent(self, photo, newDict):
        
        if newDict['CountryCode'] != None:
            self.updateImageCountryCodeOrAddIfMissing(photo, newDict['CountryCode'])
            
        if newDict['CountryName'] != None:
            self.updateImageCountryNameOrAddIfMissing(photo, newDict['CountryName'])

        if newDict['Province'] != None:
            self.updateImageStateProvinceOrAddIfMissing(photo, newDict['Province'])

        if newDict['City'] != None:
            self.updateImageCityOrAddIfMissing(photo, newDict['City'])

        if newDict['Location'] != None:
            self.updateImageSubLocationOrAddIfMissing(photo, newDict['Location'])
            
        return
    

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

  
    def fixSedilaDiacritics(self, strName):
        
        if strName == None:
            return None
        
        strName = strName.replace(u'ş',u'ș')
        strName = strName.replace(u'Ş',u'Ș')
        strName = strName.replace(u'ţ',u'ț')
        strName = strName.replace(u'Ţ',u'Ț')
        
        return strName
    

    def computeParentAlbum(self):
        
        # consider only the first selected photo 
        photo = self.selectedPhotos[0]
        parent = photo.parent.get()
        
        albumName = parent.name.get()
        count = parent.image_versions.count()
                
        print "Parent album '{0}' has {1} photos.".format(albumName.encode('utf-8'), count)
        print
        
        self.selectedPhoto = photo
            
        return
    

    def computeAlbumPhotosOrdered(self):
        
        # normally, the order should be obtained from Aperture, but, for unknown
        # reasons, in Python the order does not come properly (either 
        # py-appscript messes it or even Aperture itself). 

        parent = self.selectedPhoto.parent.get()
        albumPhotos = parent.image_versions.get()
        
        # currently sort photos by EXIF date and name     
        self.albumPhotosOrdered = sorted(albumPhotos, key=lambda photo: 
            (self.aperture.getExifImageDate(photo),self.aperture.getName(photo)))
        
        return

    
    def checkPhotosPublished(self):
        
        count = 0
        print 'Checking parent album photos... '
        for photo in self.albumPhotosOrdered:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
            
            try:
                self.aperture.getFlickrID(photo)
            except ErrorWithDescription:
                count += 1
                print ("  '{0}' from '{1}' not published on Flickr".
                       format(photoName, photoExifDate))
                
        if count > 0:
            if count == 1:
                retMsg = '... 1 photo'
            else:
                retMsg = '... {0} photos'.format(count)
                    
            retMsg += ' not published on Flickr, quitting.'
            
            raise ErrorWithDescription(retMsg)         
        
        print '... all photos are published on Flickr, continue.'
        print

        return
    
    
    def addPhotosToFlickrSet(self):
         
        print   
        print "Adding photos to Flickr set '{0}'... ".format(self.flickrSetName)
                                                        
        for photo in self.albumPhotosOrdered:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)

            flickrPhotoId = self.aperture.getFlickrID(photo)

            print("  '{0}' from '{1}'".
                       format(photoName, photoExifDate)),
            try:
                self.flickr.addPhotoToSet(self.flickrSetId, flickrPhotoId)
                print('succeeded')
                
                self.countAddedPhotos += 1

            except FlickrException as ex:
                print('failed [{0}]'.format(ex))
                continue
            
        
        print '{0} photos added.'.format(self.countAddedPhotos)
            
        return


