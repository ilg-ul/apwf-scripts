
from datetime import datetime

from appscript import app, k
import pytz

from errorWithDescription import ErrorWithDescription
from gmtTzinfo import GmtTzinfo

# ISO 8601 date format, with explicit field separators, 
# and without the 'T' separator. The time zone is parsed separately.
# An example is '2011-12-01 21:32:27+02:00'

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class Aperture():
    
    def __init__(self):
        
        self.aperture = app('Aperture')

    
    def getSingleSelection(self):
        
        sels = self.aperture.selection.get()
        cnt = len(sels)
        if cnt == 0:
            raise ErrorWithDescription('Please select an image.')
        elif cnt > 1:
            raise ErrorWithDescription('Please select a single image.')
    
        sel = sels[0]
        return sel
    
    
    def getMultipleSelection(self):
        
        sels = self.aperture.selection.get()
        cnt = len(sels)
        if cnt == 0:
            raise ErrorWithDescription('Please select at least one image.')
    
        return sels
    
    
    def getItemByName(self, coll, name):
    
        if coll == None:
            raise ErrorWithDescription('No collection')
        
        if len(coll) == 0:
            raise ErrorWithDescription('Zero length collection')
        
        for item in coll:
            
            itemName = item.name.get()
            if itemName == name:
                
                itemValue = item.value.get()
                return itemValue
            
        raise ErrorWithDescription("Item '{0}' not found". format(name))
    
    
    # return old value
    def setItemByName(self, coll, name, value):
    
        if coll == None:
            return None
        
        if len(coll) == 0:
            return None
        
        for item in coll:
            
            itemName = item.name.get()
            if itemName == name:
                
                itemValue = item.value.get()
                
                item.value.set(value)
                return itemValue
            
        return None
    
    
    def convertDateToString(self, binDate):
        
        strTz = self.convertTimeZoneOffsetToString(binDate)
        if strTz == None:
            strDate = binDate.strftime(DATE_FORMAT)
        else:
            strDate = binDate.strftime((DATE_FORMAT + "{0}").format(strTz))
    
        return strDate
    
    
    def convertTimeZoneOffsetToString(self, binDate):
        
        tzOff = binDate.utcoffset()
        if tzOff == None:
            return None
        
        tzOffMinutes = tzOff.total_seconds()/60
    
        if tzOffMinutes < 0:
            sign = '-'
            tzOffMinutes = -tzOffMinutes
        else:
            sign = '+'
    
        stz = "{0}{1:02d}:{2:02d}".format(sign,int(tzOffMinutes/60), 
                                          int(tzOffMinutes%60))
        return stz

    
    # Return a date with time zone or raise exception
    def getExifImageDate(self, photo):
        
        exif_tags = photo.EXIF_tags.get()
        custom_tags = photo.custom_tags.get()
    
        try:
            exifImageDate = self.getItemByName(exif_tags, 'ImageDate')
            #print exifImageDate
        except ErrorWithDescription as err:
            print err
            raise ErrorWithDescription('No EXIF ImageDate attribute')
        
        #localTimeZoneName = tzlocal().tzname(exifImageDate)
        # Unfortunately this returns EEST, which is not recognised by pytz
        # WARNING: static value!
        localTimeZoneName = "Europe/Bucharest"
        #print localTimeZoneName
        
        try:
            tzl = pytz.timezone(localTimeZoneName)
        except pytz.UnknownTimeZoneError:
            raise ErrorWithDescription("Unknown local time zone '{0}'".
                                       format(localTimeZoneName))
        
        exifImageDateWithLocalTimeZone = tzl.localize(exifImageDate)
        #print exifImageDateWithLocalTimeZone
            
        try:
            pictureTimeZoneName = self.getItemByName(custom_tags, 
                                                     'pictureTimeZoneName')
        except ErrorWithDescription as err:
            print err
            raise ErrorWithDescription("Missing 'pictureTimeZoneName',"
                " Metadata -> Batch Change -> Adjust Time Zone -> Actual Time Zone")
        
        pictureTimeZoneName = pictureTimeZoneName.strip()
        try:
            tz = pytz.timezone(pictureTimeZoneName)
        except pytz.UnknownTimeZoneError:
            raise ErrorWithDescription("Unknown custom time zone '{0}'".
                                       format(pictureTimeZoneName))
    
        exifImageDateTz = exifImageDateWithLocalTimeZone.astimezone(tz)
        #print exifImageDateTz
    
        return exifImageDateTz
 
 
    def getPictureTimeZoneName(self, photo):
        
        custom_tags = photo.custom_tags.get()

        pictureTimeZoneName = self.getItemByName(custom_tags,
                                                 'pictureTimeZoneName')
        
        return pictureTimeZoneName


    def setPictureTimeZoneName(self, photo, pictureTimeZoneName):
        
        custom_tags = photo.custom_tags.get()

        self.setItemByName(custom_tags, 'pictureTimeZoneName', 
                           pictureTimeZoneName)
        
        return
               

    def getCameraTimeZoneName(self, photo):
        
        custom_tags = photo.custom_tags.get()

        cameraTimeZoneName = self.getItemByName(custom_tags, 
                                                'cameraTimeZoneName')
        
        return cameraTimeZoneName


    def setCameraTimeZoneName(self, photo, cameraTimeZoneName):
        
        custom_tags = photo.custom_tags.get()

        self.setItemByName(custom_tags, 'cameraTimeZoneName', 
                           cameraTimeZoneName)
        
        return

        
    # Return a date with time zone or raise exception
    def getGpsReferenceDate(self, photo):
        
        custom_tags = photo.custom_tags.get()
    
        gpsReferenceDateString = self.getItemByName(custom_tags, 
                                                    'GpsReferenceDate')
        
        gpsReferenceDate = self.parseStringDate(gpsReferenceDateString)
        return gpsReferenceDate
    
        
    # Return a date with time zone or raise exception
    def getCameraImageDate(self, photo):
        
        custom_tags = photo.custom_tags.get()
    
        cameraImageDateString = self.getItemByName(custom_tags, 
                                                   'CameraImageDate')
        
        cameraImageDate = self.parseStringDate(cameraImageDateString)
        return cameraImageDate


    def addCameraImageDate(self, photo, cameraDate):
                
        cameraDateString = self.convertDateToString(cameraDate)    
        self.makeTag(photo, k.custom_tag, 'CameraImageDate', cameraDateString)

        return cameraDateString


    # Return a date with time zone or raise exception
    def getGpsInterpolatedReferenceDate(self, photo):
        
        custom_tags = photo.custom_tags.get()
    
        gpsInterpolatedReferenceDateString = self.getItemByName(custom_tags, 
            'GpsInterpolatedReferenceDate')
        
        gpsInterpolatedReferenceDate = self.parseStringDate(
            gpsInterpolatedReferenceDateString)
        
        return gpsInterpolatedReferenceDate


    def setGpsInterpolatedReferenceDate(self, photo, newDate):
        
        custom_tags = photo.custom_tags.get()
    
        newDateString = self.convertDateToString(newDate)
        self.setItemByName(custom_tags, 'GpsInterpolatedReferenceDate', 
                           newDateString)

        return newDateString
    

    def addGpsInterpolatedReferenceDate(self, photo, newDate):
                
        newGpsInterpolatedReferenceDateString = self.convertDateToString(
            newDate)
    
        self.makeTag(photo, k.custom_tag, 'GpsInterpolatedReferenceDate', 
                     newGpsInterpolatedReferenceDateString)

        return newGpsInterpolatedReferenceDateString


    def makeTag(self, photo, tagType, tagName, tagValue):

        photo.make(new=tagType, with_properties={k.name: tagName, 
                                                 k.value: tagValue})
        return
    

    # parse YYYY-MM-DD HH:MM:SS+HH:MM and return a time zone aware date
    def parseStringDate(self, inStringDate):
        
        inStringDate = inStringDate.strip()
        
        ix = inStringDate.index('+')
        if ix < 0:
            ix = inStringDate.index('-')
            
        if ix >= 0:
            timeZoneName = inStringDate[ix:]
            
            try:
                tz = GmtTzinfo(timeZoneName)
            except ValueError as err:
                print err
                raise ErrorWithDescription("Unknown  time zone '{0}'".
                                           format(timeZoneName))
    
            stringDate = inStringDate[0:ix].strip()
        else:
            tz = GmtTzinfo('+00:00')
            stringDate = inStringDate.strip()
        
        parsedDate = datetime.strptime(stringDate, DATE_FORMAT)
    
        # make the naive date a TZ aware one
        parsedDateWithTimeZone = tz.localize(parsedDate)        
        return parsedDateWithTimeZone

    
    def getGpsReferenceAlbum(self):
        
        photos = self.aperture.albums['GPS Reference Photos'].image_versions.get()
        return photos


    def adjustImageDate(self, photo, newDate):
        
        #photo.adjust_image_date(newDate)
        
        newDateNoTimezone = newDate.replace(tzinfo=None)
        photos =[photo]
        self.aperture.adjust_image_date(newDateNoTimezone, of_images=photos)
        return
    

    def getMasterLocation(self, photo):
        
        other_tags = photo.other_tags.get()

        masterLocation = self.getItemByName(other_tags, 'MasterLocation')        
        return masterLocation


