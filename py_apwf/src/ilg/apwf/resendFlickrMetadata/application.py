# -*- coding: utf-8 -*-

"""
Usage:
    python ilg.apwf.resendFlickrMetadata [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    For the selected photos, resend the metadata to Flickr.
    
"""


import getopt

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication
from ilg.apwf.apertureNonportable import ApertureNonportable

class Application(CommonApplication):
    
    def __init__(self, *argv):
                
        super(Application,self).__init__(*argv)

        # application specific members
        
        self.apertureNonportable = ApertureNonportable()
        
        return
    

    def usage(self):
        
        print __doc__
        return


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
        print "Resend the metadata to Flickr."
        print

        self.getMultipleSelection()        
        
        self.resendFlickrMetadata()
        
        return
            
    
    def resendFlickrMetadata(self):
        
        count = 0
        print 'Check photos... '
        for photo in self.selectedPhotos:
            
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
                print '... 1 photo',
            else:
                print '... {0} photos'.format(count),
                    
            print 'not published on Flickr, quitting.'
            return         
        
        print '... all photos published on Flickr.'
        print
        
        print 'Resending metadata... '
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)

            print ("  '{0}' from '{1}'".
                       format(photoName, photoExifDate))
            
            flickrIdString = self.aperture.getFlickrID(photo)

            # ${Title|Headline|Filename}
            
            flickrTitle = self.computeFlickrTitle(photo)   
            print "    Title='{0}'".format(flickrTitle)
            
            
            # prepare values, check None or '-'
            crtDict = self.getGeocodingFields(photo)
            for key in self.locationKeyNames:
                val = crtDict[key]
                if val != None:
                    val = val.strip()
                    if val == '-':
                        val = ''
                else:
                    val = ''
                crtDict[key] = val
            
            flickrDescription = self.computeFlickrDescription(photo, flickrTitle, crtDict)
            print "    Description='{0}'".format(flickrDescription)
               
            flickrTags = self.computeFlickrTags(photo, crtDict)
            print "    Tags=[",
            for tag in flickrTags:
                flickrTagUtf = tag.encode('utf-8')
                print "'{0}'".format(flickrTagUtf),
            print "]"
                                                        
        return


    # favour headline for title, default to version name
    def computeFlickrTitle(self, photo):
            
        flickrTitle = ""
        
        # first try the headline field
        try:
            headlineString = self.aperture.getHeadline(photo)
        except ErrorWithDescription:
            headlineString = ""
        headlineString = headlineString.strip()
        if len(headlineString) > 0:
            flickrTitle = headlineString
            
        if len(flickrTitle) == 0:
        
            # than try the title, which is more technical (like file name)
            try:
                objectNameString = self.aperture.getObjectName(photo)
            except ErrorWithDescription:
                objectNameString = ""
            
            objectNameString = objectNameString.strip()
            if len(objectNameString) > 0:
                flickrTitle = objectNameString
                    
        if len(flickrTitle) == 0:
            # default to version name
            photoName = photo.name.get()
            flickrTitle = photoName

        return flickrTitle

        
    def computeFlickrDescription(self, photo, flickrTitle, crtDict):
        
        flickrDescription = ""

        mustAddComma = False
        for key in ['CountryName', 'Province', 'City', 'Location']:
               
            val = crtDict[key]
            if len(val) > 0:
                if mustAddComma:
                    flickrDescription += ', '
                else:
                    # on first value do not add comma
                    mustAddComma = True
                flickrDescription += val

        flickerAltitudeInt = None
        try:
            flickerAltitudeInt = int(self.aperture.getExifAltitude(photo))
        except:
            pass
        
        if flickerAltitudeInt == None:
            try:
                flickerAltitudeInt = int(self.aperture.getGpsAltitude(photo))
            except:
                pass
        
        if flickerAltitudeInt == None:
            try:
                flickerAltitudeInt = int(self.aperture.getGoogleAltitude(photo))
            except:
                pass
        
        if flickerAltitudeInt == None:
            if mustAddComma:
                flickrDescription += ', '
            else:
                # on first value do not add comma
                mustAddComma = True
            flickrDescription += '{0} m'
        
        # TODO: add 'Airborne' if needed
        
        flickrDescription += '<br>'

        photoExifDate = self.aperture.getExifImageDate(photo)
        monShortString = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 
                          'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][photoExifDate.month-1]
        
        flickrDescription += photoExifDate.strftime('%d-{0}-%Y %H:%M:%S %Z'.
                                                    format(monShortString))
        photoName = photo.name.get()

        if flickrTitle != photoName:
            flickrDescription += ', {0}'.format(photoName)
        
        flickrDescription += '<br>'
        
        try:
            captionString = self.aperture.getCaption(photo)
            captionString = captionString.strip()
            if len(captionString) > 0:
                flickrDescription += captionString
        except Exception:
            pass

        return flickrDescription

        
    def computeFlickrTags(self, photo, crtDict):
        
        tags = {}
        
        # first add current tags, with their parents, up to the first
        # tag not containing lower case letters
        keywords = self.aperture.getKeywords(photo)
        for keywordName in keywords.keys():
            
            tags[keywordName] = None
            
            keywordParents = keywords[keywordName]
            if len(keywordParents) != 0:
                for parentKeywordName in keywordParents:                    
                    if not self.isTagExportable(parentKeywordName):
                        break
                    
                    tags[parentKeywordName] = 'p'

        # create tags from location names
        for key in ['CountryName', 'Province', 'City', 'Location']:
               
            val = crtDict[key]
            if len(val) > 0:
                vals = val.split(',')
                for subval in vals:
                    if len(subval) > 0:
                        tags[subval] = 'l'
        
        # create tags from names
        fullNames = self.getFacesFullNames(photo)
        
        for fullName in fullNames:
            
            # one tag for each full name
            tags[fullName] = 'f'
              
            for name in fullName.split():
                
                # another tag for each first/last name
                tags[name] = 'f'
                
                if False:
                    faceNameWithoutDiacritics = self.removeDiacritics(name)
                    
                    # another fag for each name without diacritics
                    tags[faceNameWithoutDiacritics] = 'f'

        return tags.keys()

    
    def isTagExportable(self, tag):
        
        tag = tag.strip()
        
        if tag[0] == '[':
                return False
            
        return True


    def removeDiacritics(self, name):
        
        # TODO: remove diacritics
        return name
    
    
    def getFacesFullNames(self, photo):
        
        facesNames = []
        photoId = self.aperture.getId(photo)
        
        masterUuid = self.apertureNonportable.getMasterUuid(photoId)
        
        faceKeys = self.apertureNonportable.getFaceKeys(masterUuid)
        
        for faceKey in faceKeys:
            
            namesTuple = self.apertureNonportable.getFaceNames(faceKey)
            if namesTuple != None:
                (name, fullName) = namesTuple
                if fullName != None:
                    facesNames.append(fullName)
                else:
                    facesNames.append(name)
        
        return facesNames
    
    