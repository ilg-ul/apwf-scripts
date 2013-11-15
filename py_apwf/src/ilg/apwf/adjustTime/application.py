"""
Usage:
    python ilg.apwf.adjustTime [options]

Options:
    -n, --dry
        dry run, do not add/update tags

    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Adjust EXIT ImageDate for the selected photos, using the nearest 
    GPS references.
    
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
            (opts, args) = getopt.getopt(self.argv[1:], 'nhv', 
                                         ['dry', 'help', 'verbose'])
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
                if o in ('-n', '--dry'):
                    self.isDryRun = True
                elif o in ('-v', '--verbose'):
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
        print "Adjust EXIT ImageDate for the selected photos, using the nearest"
        print "GPS references."
        print
        
        self.getMultipleSelection()        
        
        self.checkSameMakeAndModel()
        
        self.backupCreationDate()
        
        self.selectLimits()
        
        self.selectInnerGpsReference()
        self.selectOuterGpsReferences()
        
        self.computeTimeOffsetSeconds()
         
        self.validateImageDateAdjustment()
        
        if not self.isDryRun:
            self.performImageDateAdjustment()
        
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


    def checkSameMakeAndModel(self):
        
        collectionMake = None
        collectionModel = None
        
        print 'Checking same camera make and model... '
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            if self.isVerbose:
                print photoName
    
            exif_tags = photo.EXIF_tags.get()
    
            try:
                photoMake = self.aperture.getItemByName(exif_tags, 'Make')
            except ErrorWithDescription as err:
                print err
                raise ErrorWithDescription('No EXIF Make attribute')
        
            if collectionMake == None:
                collectionMake = photoMake
            elif collectionMake != photoMake:
                raise ErrorWithDescription("Make '{0}' different from '{1}',"
                    " please split collection".format(collectionMake, photoMake))
                
            try:
                photoModel = self.aperture.getItemByName(exif_tags, 'Model')
            except ErrorWithDescription as err:
                print err
                raise ErrorWithDescription('No EXIF Model attribute')
        
            if collectionModel == None:
                collectionModel = photoModel
            elif collectionModel != photoModel:
                raise ErrorWithDescription("Model '{0}' different from '{1}',"
                    " please split collection".format(collectionModel, photoModel))
    
        print "  all identical, make='{0}', model='{1}'.".format(collectionMake, 
                                                               collectionModel)
        
        # store results in class members
        self.collectionMake = collectionMake
        self.collectionModel = collectionModel
        
        return


    def backupCreationDate(self):
        
        print 'Backing up the creation date of photos in collection... '
        for photo in self.selectedPhotos:
            
            cameraDate = self.aperture.getExifImageDate(photo)
            self.addCameraImageDateIfNotPresent(photo, cameraDate)
         
        print "  done."
        
        return
        
        
    # Since the collections are not ordered, do a pass and select the 
    # first and last photos. 
    # The selection is based on the original camera date, not the possibly
    # erroneously adjusted EXIF date. (it assumes the camera time setting
    # is not touched during a collection)
    
    def selectLimits(self):
        
        firstPhoto = None
        firstPhotoDate = None
        lastPhoto = None
        lastPhotoDate = None
    
        print 'Identifying first/last photos in collection... '
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            if self.isVerbose:
                print photoName

            # raise an exception if something goes wrong
            photoDate = self.aperture.getCameraImageDate(photo)
            
            if firstPhotoDate == None or photoDate < firstPhotoDate:
                # if photos with identical date, get the first one encountered
                firstPhotoDate = photoDate
                firstPhoto = photo
    
            if lastPhotoDate == None or photoDate >= lastPhotoDate:
                # if photos with identical date, get the last one encountered
                lastPhotoDate = photoDate
                lastPhoto = photo
           
        print "  first photo: '{0}'".format(firstPhoto.name.get())
        print "  last photo: '{0}'".format(lastPhoto.name.get())
        
        # store results in class members
        self.firstPhotoInCollection = firstPhoto
        self.lastPhotoInCollection = lastPhoto
        
        return    
    
    
    # If there is any GPS reference photo inside the collection,
    # it'll be later used as collection reference, instead of the 
    # first photo in collection. (multiple references are triggered as
    # errors)
    
    def selectInnerGpsReference(self):
        
        gpsPhoto = None
    
        print 'Checking for any GPS reference in collection... '
    
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            if self.isVerbose:
                print photoName
            
            try:
                # Only the photos having the custom tag will end
                # properly, regular photos will raise an exception
                self.aperture.getGpsReferenceDate(photo)
                print "  '{0}' is a GPS reference".format(photoName)
                
            except Exception:
                # ignore photos without a GPS reference date
                continue
            
            if gpsPhoto == None:
                gpsPhoto = photo
            else:
                raise ErrorWithDescription('Multiple GPS references,'
                    ' please split the collection')
    
        if gpsPhoto == None:
            print '  none found.'
            
        # store results in class members
        self.gpsPhotoInCollection = gpsPhoto
        
        if gpsPhoto == None:
            return False
        else:
            return True


    # If the collection does not include a GPS reference, we need to
    # interpolate the GPS time. for this to be possible, we need a
    # reference point before the first photo of the collection and
    # another one after the last photo of the collection.
    # As before, comparisons are made on original camera image date.
    
    # Only photos with the required camera Make/Model are used in the
    # comparison.
     
    def selectOuterGpsReferences(self):

        gpsBeforePhoto = None
        gpsBeforePhotoDate = None
        gpsAfterPhoto = None
        gpsAfterPhotoDate = None
    
        print 'Identifying before/after GPS references in library... '
        
        photos = self.aperture.getGpsReferenceAlbum()

        print ("  found {0} photos, selecting those with '{1}' '{2}'... ".format(
            len(photos), self.collectionMake, self.collectionModel))
        
        dateFirstPhoto = self.aperture.getCameraImageDate(self.firstPhotoInCollection)
        dateLastPhoto = self.aperture.getCameraImageDate(self.lastPhotoInCollection)
                        
        for photo in photos:
            
            if self.isVerbose:
                photoName = photo.name.get()
                print photoName

            exif_tags = photo.EXIF_tags.get()
    
            try:
                photoMake = self.aperture.getItemByName(exif_tags, 'Make')
            except ErrorWithDescription as err:
                print err
                raise ErrorWithDescription('No EXIF Make attribute')
        
            if self.collectionMake != photoMake:
                continue
                            
            try:
                photoModel = self.aperture.getItemByName(exif_tags, 'Model')
            except ErrorWithDescription as err:
                print err
                raise ErrorWithDescription('No EXIF Model attribute')

            if self.collectionModel != photoModel:
                continue
        
            if self.isVerbose:
                print 'make & model ok'
            
            photoDate = self.aperture.getCameraImageDate(photo)
            
            # select the latest reference before or identical to the first photo
            if photoDate <= dateFirstPhoto:
                if gpsBeforePhoto == None or photoDate > gpsBeforePhotoDate:
                    gpsBeforePhoto = photo
                    gpsBeforePhotoDate = photoDate
                
            # select the earliest reference after or identical to the last photo
            if photoDate >= dateLastPhoto:
                if gpsAfterPhoto == None or photoDate < gpsAfterPhotoDate:
                    gpsAfterPhoto = photo
                    gpsAfterPhotoDate = photoDate
           
        if gpsBeforePhoto == None:
            raise ErrorWithDescription('No reference before, cancelling.')
        else:
            print "  reference before: '{0}'".format(gpsBeforePhoto.name.get())
            
        if gpsAfterPhoto != None:
            print "  reference after: '{0}'".format(gpsAfterPhoto.name.get())
        else:
            print "  reference after: None"
            
        self.gpsBeforePhoto = gpsBeforePhoto
        
        # may be None, if the GPS reference is in the set
        self.gpsAfterPhoto = gpsAfterPhoto
        
        return

    
    # Adjusting time requires an offset, in seconds. If possible, use the
    # collection GPS reference point. If this does not exist, interpolate 
    # for the first photo in the collection.
    
    def computeTimeOffsetSeconds(self):
        
        if self.gpsPhotoInCollection != None:
            
            # There is a GPS reference in the collection, use it.
            
            photo = self.gpsPhotoInCollection
            photoNewDate = self.aperture.getGpsReferenceDate(photo)
            
        else:
            
            # Without a GPS reference, we need the before/after references
            # to interpolate.
            
            if self.gpsBeforePhoto == None:
                raise ErrorWithDescription('No GPS reference photo before')
            
            if self.gpsAfterPhoto == None:
                raise ErrorWithDescription('No GPS reference photo after')

            # Use the first photo in the collection as interpolated reference
            
            photo = self.firstPhotoInCollection            
            photoNewDate = self.interpolate(photo, self.gpsBeforePhoto, 
                                            self.gpsAfterPhoto)
            
        # Adjust the time zone of the newly computed date
        # to match the actual one. (in case the photo time zone was
        # later updated)
              
        photoExifDate = self.aperture.getExifImageDate(photo)
        photoCameraDate = self.aperture.getCameraImageDate(photo)
        
        photoNewDate = photoNewDate.astimezone(photoExifDate.tzinfo)
        
        if self.gpsPhotoInCollection != None:

            self.updateGpsInterpolatedReferenceDateOrAddIfNotPresent(
                photo, photoNewDate)
        
        # Remember the reference photo
        self.referencePhoto = photo
        
        # ... the new adjusted date
        self.photoNewDate = photoNewDate
        
        # ... the time offset to the original camera date
        self.timedeltaToCamera = photoNewDate - photoCameraDate
                        
        return


    def validateImageDateAdjustment(self):
                      
        # initialise the interpolate mean square error 
        interpolateMse = 0
        # initialise the interpolate mean value
        interpolateMean = 0

        # initialise the shift mean square error 
        shiftMse = 0
        # initialise the shift mean value
        shiftMean = 0
        
        mustAdjustDate = False
        
        if self.gpsAfterPhoto != None:
            gpsLastAvailable = self.gpsAfterPhoto
        else:
            gpsLastAvailable = self.gpsPhotoInCollection
            
        gpsLastAvailableCameraDate = self.aperture.getCameraImageDate(gpsLastAvailable)
        
        countShift = 0
        countInterpolate = 0
        
        timedeltaToCameraSeconds = self.timedeltaToCamera.total_seconds()
        
        if self.gpsPhotoInCollection != None:
            reason = "exactly"
        else:
            reason = "interpolated"
        
        print ("Preparing to 'adjust time' with {0} {1} seconds for the following photos:".
               format(reason, timedeltaToCameraSeconds))
        
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
            photoCameraDate = self.aperture.getCameraImageDate(photo)
            adjustedDate = photoCameraDate + self.timedeltaToCamera

            if photoCameraDate > gpsLastAvailableCameraDate:
                print ("  '{0}' from '{1}' to '{2}' after GPS reference".
                        format(photoName, photoExifDate, adjustedDate))
                continue

            shiftTimedelta = adjustedDate - photoExifDate
            shiftTimedeltaSeconds = shiftTimedelta.total_seconds()
            
            if shiftTimedeltaSeconds != 0:
                shiftDelta = shiftTimedeltaSeconds

                shiftMean += shiftDelta
                shiftMse += (shiftDelta*shiftDelta)

                countShift += 1
                                              
            interpolatedDate = self.interpolate(photo, self.gpsBeforePhoto, 
                                                   gpsLastAvailable)
            
            errorTimedelta = adjustedDate - interpolatedDate
            errorTimedeltaSeconds = errorTimedelta.total_seconds()
            if errorTimedeltaSeconds != 0:
                            
                interpolateMean += errorTimedeltaSeconds
                interpolateMse += (errorTimedeltaSeconds*errorTimedeltaSeconds)
            
                countInterpolate += 1

            if shiftTimedeltaSeconds != 0:
                
                mustAdjustDate = True

                if errorTimedeltaSeconds == 0:
                    print ("  '{0}' from '{1}' to '{2}'".
                           format(photoName, photoExifDate, adjustedDate))
                else:  
                    print ("  '{0}' from '{1}' to '{2}' interpolation delta {3} sec".
                           format(photoName, photoExifDate, adjustedDate, 
                                  errorTimedeltaSeconds))
                    
            else:
                
                # The EXIT date already set
                if errorTimedeltaSeconds == 0:
                    print ("  '{0}' time '{1}' properly set".
                           format(photoName, photoExifDate))
                else:  
                    print ("  '{0}' time '{1}' properly set, interpolation delta {2} seconds".
                           format(photoName, photoExifDate, errorTimedeltaSeconds))
        
        if countInterpolate > 0:        
            interpolateMean /= countInterpolate
            interpolateMse /= countInterpolate
            interpolateMse = math.sqrt(interpolateMse)
            
        if countShift > 0:
            shiftMean /= countShift
            shiftMse /= countShift
            shiftMse = math.sqrt(shiftMse)
            
        if not mustAdjustDate: 
            raise ErrorWithDescription('All photos in this collection '
                'have the time properly set, nothing to do.')
           
        if interpolateMean != 0 or interpolateMse != 0:
            print ('Interpolation error mean value={0}, mean square error={1}'.
                   format(interpolateMean, interpolateMse))

        if shiftMean != 0 or shiftMse != 0:            
            print ('Shift offset mean value={0}, mean square error={1}'.
                   format(shiftMean, shiftMse))
                
        return
    
    
    # Finally perform the action.
    # Add the offset to the original camera date
    
    def performImageDateAdjustment(self):

        timedeltaToCameraSeconds = self.timedeltaToCamera.total_seconds()
        
        msg = ('Do you want to apply an offset of {0} seconds? (Yes): '.
                   format(timedeltaToCameraSeconds))
        line = raw_input(msg)

        if line != 'Yes':
            raise ErrorWithDescription('No changes.')

        print 'Adjusting time... '
        
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            
            photoExifDate = self.aperture.getExifImageDate(photo)
            photoCameraDate = self.aperture.getCameraImageDate(photo)
            adjustedDate = photoCameraDate + self.timedeltaToCamera
            
            # Adjust the time zone of the newly computed date
            # to match the actual one. (in case the photo time zone was
            # later updated)
            adjustedDate = adjustedDate.astimezone(photoExifDate.tzinfo)

            print "  '{0}' to '{1}'... ".format(photoName, adjustedDate),
            
            self.aperture.adjustImageDate(photo, adjustedDate)
            
            print "done"
                    
        return


    # Linear interpolation, based on original camera date and manually
    # added GPS date.
    # Return the estimated GPS time for the given reference photo.
    # Computations are performed in double, so precision should be fine.
    
    def interpolate(self, photo, beforeGpsPhoto, afterGpsPhoto):
        
        photoCameraDate = self.aperture.getCameraImageDate(photo)

        beforeGpsReferenceDate = self.aperture.getGpsReferenceDate(beforeGpsPhoto)
        beforeCameraDate = self.aperture.getCameraImageDate(beforeGpsPhoto)
                
        afterGpsReferenceDate = self.aperture.getGpsReferenceDate(afterGpsPhoto)
        afterCameraDate = self.aperture.getCameraImageDate(afterGpsPhoto)

        if beforeGpsPhoto.id.get() == afterGpsPhoto.id.get():
            
            if beforeGpsPhoto.id.get() == photo.id.get():
                return beforeGpsReferenceDate
            
            raise ErrorWithDescription('Before == After GPS references')
            
             
        timedeltaReferenceTotal = afterGpsReferenceDate - beforeGpsReferenceDate
        timedeltaCameraTotal = afterCameraDate - beforeCameraDate
            
        timedeltaCameraPhoto = photoCameraDate - beforeCameraDate
            
        offsetFactor = (timedeltaReferenceTotal.total_seconds() / 
            timedeltaCameraTotal.total_seconds())
        offsetSeconds = int(timedeltaCameraPhoto.total_seconds() * offsetFactor)

        newGpsDate = beforeGpsReferenceDate + timedelta(seconds=offsetSeconds)
        return newGpsDate
    
        