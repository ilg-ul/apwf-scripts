"""
Usage:
    python ilg.apwf.rename [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Rename the selected photos, using the current date template.
    
"""


import getopt

import pytz

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.aperture import Aperture

from appscript import k


class Application():
    
    def __init__(self, *argv):
        
        self.argv = argv
                
        self.aperture = Aperture()
        
        self.isVerbose = False
        
        # application specific members
        self.photos = None
        

    def usage(self):
        
        print __doc__


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
        print "Rename the selected photos, using the UTC capture date template."
        print

        self.getMultipleSelection()        
        
        self.rename()
        
        return
        

    def getMultipleSelection(self):
        
        self.photos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.photos))
        print
        
        return
    

    def rename(self):
        
        defaultPrefix = 'ILG'
        prefix = raw_input("Enter name prefix (default '{0}'): ".
                           format(defaultPrefix))
        if prefix == '':
            prefix = defaultPrefix
            
        prefix = prefix.strip()
        prefix = prefix.upper()

        print 'Renaming photos... '
        for photo in self.photos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
            
            tzUtc = pytz.utc
            photoExifDateUtc = photoExifDate.astimezone(tzUtc)
            
            year = photoExifDateUtc.year
            month = photoExifDateUtc.month
            day = photoExifDateUtc.day
            
            nameDigits = self.getLastDigits(photoName)
            
            newName = ("{0}_{1:04d}{2:02d}{3:02d}_{4}".
                       format(prefix, year, month, day, nameDigits))

            custom_tags = photo.custom_tags.get()
            other_tags = photo.other_tags.get()

            fileName = self.aperture.getItemByName(other_tags, 'FileName')
            
            try:
                self.aperture.getItemByName(custom_tags, 'CameraFileName')
                # if it exists, leave it as is
            except:
                # otherwise add it, with the original file name
                self.aperture.makeTag(photo, k.custom_tag, 'CameraFileName', 
                                      fileName)
            
            if photoName != newName:
                
                photo.name.set(newName)
                
                if False:
                    # disabled, since FileName is not writable
                    # use Batch to rename the originals
                    extension = fileName.split('.')[1]
                    newFileName = '{0}.{1}'.format(newName, extension)
                
                    self.aperture.setItemByName(other_tags, 'FileName', newFileName)
                    
                print ("  '{0}' to '{1}'".format(photoName, newName))
                
            else:
                # if the name is already changed, just report  
                print ("  '{0}' is fine".format(photoName))
                     
        return


    def getLastDigits(self, name):
        
        for i in range(len(name)):
            subString = name[i:]
            if subString.isdigit():
                return subString
            
        raise ErrorWithDescription("Name '{0}' not ending with digits".format(name))

        