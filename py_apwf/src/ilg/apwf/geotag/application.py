"""
Usage:
    python ilg.apwf.geotag [options]

Options:
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Geotag the selected photos, using a GPS track file in gpx format.
    
"""


import getopt

import pytz

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.aperture import Aperture

from ilg.gpx.trackPoint import InterpolatedTrackPoint

from appscript import k

from xml.sax import make_parser
from ilg.gpx.xmlParser import TrackHandler


class Application():
    
    def __init__(self, *argv):
        
        self.argv = argv
                
        self.aperture = Aperture()
        
        self.isVerbose = False
        
        # application specific members
        self.photos = None
        
        self.tracks = None
        

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
        print "Geotag the selected photos, using a GPS track file in gpx format."
        print

        self.getMultipleSelection()        
        
        self.parseGpx()
        
        self.geotag()
        
        return
        

    def getMultipleSelection(self):
        
        self.photos = self.aperture.getMultipleSelection()
        print 'Processing {0} photos.'.format(len(self.photos))
        print
        
        return
    

    def parseGpx(self):

        file_name = '/Users/ilg/Desktop/g.gpx'

        print "Parsing track file '{0}'... ".format(file_name)
        
        th = TrackHandler()
        parser = make_parser()
        parser.setContentHandler(th)
        parser.parse(file_name)

        # get the list of tracks
        self.gpxTracks = th.getResult()
        tracks = self.gpxTracks.getTracks()
        for track in tracks:
            name = track.getName()
            points = track.getPoints()
            count = len(points)
            firstPointTimestamp = points[0].timestamp
            lastPointTimestamp = points[count-1].timestamp
            print ("  Track '{0}', {1} points, from '{2}' to '{3}'".format(
                name, count, firstPointTimestamp, lastPointTimestamp))
            
        return
    
    
    def geotag(self):
        
        print 'Geotagging photos... '
        for photo in self.photos:
            
            photoName = photo.name.get()
            photoExifDate = self.aperture.getExifImageDate(photo)
            
            tzUtc = pytz.utc
            photoExifDateUtc = photoExifDate.astimezone(tzUtc)
            
            latitude = photo.latitude.get()
            longitude = photo.longitude.get()
            
            if latitude != k.missing_value and longitude != k.missing_value:
                
                print ("  '{0}' from '{1}' already geotagged, lat={2}, lon={3}".
                       format(photoName, photoExifDate, latitude, latitude))
                continue
            
            trackPoint = self.gpxTracks.locateByTimestamp(photoExifDateUtc)
            if trackPoint != None:
                
                latitude = trackPoint.latitude
                longitude = trackPoint.longitude
                elevation = trackPoint.elevation
    
                if isinstance(trackPoint, InterpolatedTrackPoint):
                    kind = 'interpolated'
                else:
                    kind = ''
                    
                print ("  '{0}' from '{1}' geotagged, lat={2}, lon={3}, alt={4} {5}".
                           format(photoName, photoExifDate, latitude, longitude, 
                                  elevation, kind))
            else:
                print ("  '{0}' from '{1}' not geotagged".
                       format(photoName, photoExifDate))
            
                
                
            
        return



        