# -*- coding: utf-8 -*-

"""
Usage:
    python ilg.apwf.fillLocationNames [options]

Options:
    -n, --dry
        dry run, do not add/update tags
        
    -o, --overwrite
        Process all photos, even if the location names were already filled in.
        
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Fill the IPTC image geocoding fields for the selected photos. By default, if the
    values are set, avoid the expensive Google access.
    
"""


import getopt

from appscript import k

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.commonApplication import CommonApplication
from ilg.apwf.google import GoogleApi


class Application(CommonApplication):
    
    def __init__(self, *argv):
                
        super(Application,self).__init__(*argv)

        # application specific members
        
        self.doOverwrite = False
        
        return
    

    def usage(self):
        
        print __doc__
        return


    def run(self):
        
        try:
            (opts, args) = getopt.getopt(self.argv[1:], 'nohv', 
                                         ['dry', 'overwrite', 'help', 'verbose'])
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
        print "Fill the IPTC image geocoding fields for the selected photos."
        print

        self.getMultipleSelection()        
        
        self.processReverseGeocodding()
        
        return
            

    def getMultipleSelection(self):
        
        self.selectedPhotos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.selectedPhotos)),
        if self.isDryRun:
            print 'Dry run.',
        if self.isVerbose:
            print 'Verbose.',
        if self.doOverwrite:
            print 'Overwrite.',
            
        print
        print

    
    def processReverseGeocodding(self):
        
        self.google = GoogleApi(self.isVerbose)
        
        count = 0
        
        print 'Checking photos... '
        for photo in self.selectedPhotos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
                        
            latitude = photo.latitude.get()
            longitude = photo.longitude.get()
            
            if latitude == k.missing_value or longitude == k.missing_value:
                
                print ("  '{0}' from '{1}' not geotagged".
                       format(photoName, photoExifDate))
                continue
            
            doUpdate = self.doOverwrite
            
            crtDict = self.getGeocodingFields(photo)

            if not self.doOverwrite:                
                # check if any empty field
                for val in crtDict.values():
                    if val == None:
                        doUpdate = True
                        break
            
            if not doUpdate:
                print "  '{0}' from '{1}' needs no changes ".format(photoName, photoExifDate)
                continue
                            
            # fetch geocoding data from Google
            newDict = self.google.getReverseGeocoding(latitude, longitude)
            
            # update all fields that changed
            changedDict = self.updateGeocodingFieldsOrAddIfNotPresent(photo, crtDict, newDict, 
                                                        self.doOverwrite)
            
            print "  '{0}' from '{1}' update".format(photoName, photoExifDate),
            for key in ['CountryCode', 'CountryName', 'Province', 'City', 'Location']:
                val = changedDict[key]
                if val != None:
                    print "{0}='{1}'".format(key, val),
            print
            
            count += 1

        
        if count == 0:
            print '... nothing to do.'
        elif count == 1:
            print '... 1 photo updated.'
        else:
            print '... {0} photos updated.'.format(count)
             
        return


        