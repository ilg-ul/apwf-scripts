# -*- coding: utf-8 -*-

"""
Usage:
    python ilg.apwf.resyncFlickrSet [options]

Options:
    -n, --dry
        dry run, do not add/update tags

    -o, --overwrite
        process all photos, even if the coordinates were already filled in.

    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    For the parent album of the selected photos, resynchronise the content 
    of the Flickr set.
    
"""


import getopt

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication
from ilg.apwf.apertureNonportable import ApertureNonportable
from ilg.apwf.flickr import Flickr
from ilg.apwf.flickr import FlickrException


class Application(CommonApplication):
    
    def __init__(self, *argv):
                
        super(Application,self).__init__(*argv)

        # application specific members
        
        #self.apertureNonportable = ApertureNonportable()
        self.flickr = Flickr()
        
        self.doOverwrite = False
        
        return
    

    def usage(self):
        
        print __doc__
        return


    def run(self):
        
        try:
            (opts, args) = getopt.getopt(self.argv[1:], 'nohv', ['dry', 'overwrite', 'help', 'verbose'])
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
                elif o in ('-o', '--overwrite'):
                    self.doOverwrite = True
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
        print "Resynchronise the content of the Flickr set."
        print

        self.getMultipleSelection()        
        
        self.computeParentAlbum()
        self.computeAlbumPhotosOrdered()
        
        self.checkPhotosPublished()
        
        self.selectFlickrSet()
        
        #self.removePhotosFromFlickerSet()
        #self.addPhotosToFlickrSet()
        
        return
            

    def z_computeAlbumPhotos(self):
        
        blob = self.apertureNonportable.getAlbumVersionIdsBlob(self.albumId)
        print len(blob)
        for i in range(len(blob)):
            print repr(blob[i]),
            
        print
        
        return
    

    def selectFlickrSet(self):
        
        photoFlickrId = self.aperture.getFlickrID(self.selectedPhoto)
        
        try:
            flickrSets = self.flickr.getPhotoSets(photoFlickrId)
        except FlickrException:
            flickrSets = None
        
        if flickrSets == None or len(flickrSets) == 0:
            print 'None'
            return
        
        count = len(self.albumPhotosOrdered)
        
        for flickrSet in flickrSets:
            flickrSet['delta'] = abs(int(flickrSet['count_photo']) - count)
        
        # compute delta with the current number of photos
        # and sort result    
        flickrSetsOrdered = sorted(flickrSets, 
                                   key=lambda flickrSet: flickrSet['delta'])
        
        if len(flickrSetsOrdered) == 1:
            
            flickrSet = flickrSetsOrdered[0]
            
            message = ("Synchronise Flickr set '{0}', {1} photos: (y) ".
                       format(flickrSet['title'], flickrSet['count_photo']))
            
            inString = raw_input(message)
            inString = inString.strip()

            if inString != 'y':
                raise ErrorWithDescription('Quitting.')
                            
        else:
                
            print 'Flickr sets associated with the selected photo:'
            
            for i in range(len(flickrSetsOrdered)):
                flickrSet = flickrSetsOrdered[i]
                print "{0}) '{1}' ({2} photos)".format(i+1, flickrSet['title'], 
                                                       flickrSet['count_photo'])
                
            inString = raw_input('Enter selection: (1-{0}) '.
                                 format(len(flickrSetsOrdered)))
            inString = inString.strip()
            
            try:
                inNumber = int(inString)
            except:
                raise ErrorWithDescription('Selection not a number, quitting.')
            
            inNumber -= 1
            if inNumber < 0 or inNumber >= len(flickrSetsOrdered):
                raise ErrorWithDescription('Selection not in range, quitting.')            
            
            flickrSet = flickrSetsOrdered[inNumber]
            
        
        self.flickrSetId = flickrSet['id']
        self.flickrSetName = flickrSet['title']
        
        return
    
   
    def removePhotosFromFlickerSet(self):
        
        print   
        print "Removing photos from Flickr set '{0}'... ".format(self.flickrSetName)
        
        while True:
            pass
            
        return
    
     
    