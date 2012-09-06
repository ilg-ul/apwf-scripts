# -*- coding: utf-8 -*-

"""
Usage:
    python ilg.apwf.createFlickrSet [options]

Options:
    -n, --dry
        dry run, do not add/update tags

    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Create a new Flickr set and populate it with already published photos,
    grouped in the parent album of the selected photos.
    
"""


import getopt

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication
from ilg.apwf.flickr import Flickr

MONTHS_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                'August', 'September', 'October', 'November', 'December']


class Application(CommonApplication):
    
    def __init__(self, *argv):
                
        super(Application,self).__init__(*argv)

        # application specific members
        
        self.flickr = Flickr()
        
        self.doOverwrite = False
        
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
        print "Create a new Flickr set."
        print

        self.getMultipleSelection()        
        
        self.computeParentAlbum()
        self.computeAlbumPhotosOrdered()
        
        self.checkPhotosPublished()
        
        self.createFlickrSet()
        
        self.addPhotosToFlickrSet()
        
        return
            
            
    def createFlickrSet(self):
        
        defaultName = self.suggestFlickrSetName()
        
        prompt = 'Enter the new set name: '
        if defaultName != None:
            prompt += '[{0}] '.format(defaultName)
        
        try:    
            setName = raw_input(prompt)
        except KeyboardInterrupt:
            print
            raise ErrorWithDescription('KeyboardInterrupt')
        
        setName = setName.strip()
        if len(setName) == 0:
            if defaultName != None:
                setName = defaultName
            else:
                raise ErrorWithDescription('Empty name')
        
        print   
        print "Creating Flickr set '{0}'...".format(setName),

        photo = self.albumPhotosOrdered[0]
        
        photoFlickrId = self.aperture.getFlickrID(photo)
        
        flickrSetId = self.flickr.createSet(setName, photoFlickrId)   
           
        self.flickrSetId = flickrSetId
        self.flickrSetName = setName
        
        print "done."
        
        photoName = self.aperture.getName(photo)
        photoExifDate = self.aperture.getExifImageDate(photo)
        
        print ("Key photo '{0}' from '{1}'".
                       format(photoName, photoExifDate))

        self.countAddedPhotos = 1
        
        return
    
   
    def suggestFlickrSetName(self):
        
        # suggest a default set name (based on my project/album naming convention)
        try:
            photo = self.selectedPhoto
            parent = photo.parent.get()
            
            albumName = parent.name.get()
            project = self.aperture.getMasterProject(photo)
            projectName = project.name.get()
            defaultName = '{0} ({1})'.format(projectName.split(' - ')[1].encode('utf-8'), 
                                             albumName.split(' - ')[1].encode('utf-8'))
            
            # TODO: add first-last dates
            
            parent = self.selectedPhoto.parent.get()
            albumPhotos = parent.image_versions.get()
        
            # currently sort photos by EXIF date and name     
            albumPhotosOrderedByDate = sorted(albumPhotos, key=lambda photo: 
            (self.aperture.getExifImageDate(photo),self.aperture.getName(photo)))

            firstDate = self.aperture.getExifImageDate(albumPhotosOrderedByDate[0]).date()
            lastDate = self.aperture.getExifImageDate(albumPhotosOrderedByDate[-1]).date()
            
            datesRange = None
            if firstDate == lastDate:
                # same year, month, day
                datesRange = ', {0} {1}, {2}'.format(
                        MONTHS_NAMES[firstDate.month-1], firstDate.day, 
                        firstDate.year)
            elif firstDate.year == lastDate.year:
                if firstDate.month == lastDate.month:
                    # same year and month, different days
                    datesRange = ', {0} {1} - {2}, {3}'.format(
                        MONTHS_NAMES[firstDate.month-1], firstDate.day, 
                        lastDate.day, firstDate.year)
                else:
                    # same year, different months and days
                    datesRange = ', {0} {1} - {2} {3}, {4}'.format(
                        MONTHS_NAMES[firstDate.month-1], firstDate.day, 
                        MONTHS_NAMES[firstDate.month-1], lastDate.day, firstDate.year)
            else:
                # different years
                datesRange = ', {0} {1}, {2} - {3} {4}, {5}'.format(
                        MONTHS_NAMES[firstDate.month-1], firstDate.day, firstDate.year, 
                        MONTHS_NAMES[firstDate.month-1], lastDate.day, lastDate.year)
            
            defaultName += datesRange
            
        except:
            defaultName = None

        return defaultName