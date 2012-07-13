# -*- coding: utf-8 -*-

"""
Usage:
    python ilg.apwf.geotag [options]

Options:
    -n, --dry
        dry run, do not add/update tags
        
    -v, --verbose
        print progress output

    -h, --help
        print this message
        
Purpose:
    Geotag the selected photos, using a GPS track file in gpx format.
    
"""


import getopt
import math

import pytz

from ilg.apwf.errorWithDescription import ErrorWithDescription
from ilg.apwf.aperture import Aperture
from ilg.apwf.commonApplication import CommonApplication

from ilg.gpx.trackPoint import InterpolatedTrackPoint

from appscript import k

from xml.sax import make_parser
from ilg.gpx.xmlParser import TrackHandler


class Application(CommonApplication):
    
    def __init__(self, *argv):
                
        # application specific members
        
        self.maxInterpolateCoordinateSeconds = 10*60    # 10 minutes
        self.maxInterpolateTimeSeconds = 5*60   # 5 minutes
        
        self.tracks = None
        

    def usage(self):
        
        print __doc__


    def run(self):
        
        try:
            (opts, args) = getopt.getopt(self.argv[1:], 'nhv', ['dry', 'help', 'verbose'])
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
        print "Geotag the selected photos, using a GPS track file in gpx format."
        print

        self.getMultipleSelection()        
        
        self.parseGpx()
        
        self.geotag()
        
        return
            

    def parseGpx(self):

        #file_name = u'/Users/ilg/Desktop/g.gpx'
        #fileName = u'/Volumes/MacMini\ External/Library/Photos/Aperture\ GPX\ tracks/2012/20120327\ -\ Păulești\ demo.gpx'
        fileName = u'/Volumes/MacMini\ External/Library/Photos/Aperture GPX tracks/2012/20120323 - Păulești test.gpx'
        
        fileName = fileName.replace('\\','')
        
        print "Parsing track file '{0}'... ".format(fileName)
        
        th = TrackHandler()
        parser = make_parser()
        parser.setContentHandler(th)
        parser.parse(fileName)

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
        for photo in self.selectedPhotos:
            
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
            if trackPoint == None:
                print ("  '{0}' from '{1}' NOT geotagged".
                       format(photoName, photoExifDate))
                continue
            
            latitude = trackPoint.latitude
            longitude = trackPoint.longitude
            elevation = trackPoint.elevation

            if isinstance(trackPoint, InterpolatedTrackPoint):
                
                if not self._isInterpolationValid(trackPoint, photoName, 
                                                  photoExifDate):
                    continue
                
                kind = (', interpolate=({0},{1}s)'.format(
                    trackPoint.ratio, trackPoint.deltaTimestampSeconds))
                
                if not self.isDryRun:
                    self.updateGeotagInterpolateIntervalSecondsOrAddIfNotPresent(
                        photo, trackPoint.deltaTimestampSeconds)
                    self.updateGeotagInterpolateRatioOrAddIfNotPresent(
                        photo, trackPoint.ratio)
                
            else:
                kind = ''
                
            if not self.isDryRun:
                self.updateGpsLatitudeLongitude(photo, latitude, longitude)
                self.updateCustomAltitudeOrAddIfNotPresent(photo, elevation)

            print ("  '{0}' from '{1}' geotagged, lat={2}, lon={3}, alt={4}{5}".
                       format(photoName, photoExifDate, latitude, longitude, 
                              elevation, kind))
            
        return


    def _isInterpolationValid(self, trackPoint, photoName, photoExifDate):
        
        trackPointBefore = trackPoint.trackPointBefore
        trackPointAfter = trackPoint.trackPointAfter
                
        latitudeBefore = trackPointBefore.latitude
        latitudeAfter = trackPointAfter.latitude

        deltaLatitudeSeconds = math.fabs(latitudeAfter - latitudeBefore) * 60 * 60
        if (deltaLatitudeSeconds > self.maxInterpolateCoordinateSeconds):
            print ("  '{0}' from '{1}' NOT geotagged, {2} seconds of latitude apart".
                format(photoName, photoExifDate, deltaLatitudeSeconds))
            return False
        
        longitudeBefore = trackPointBefore.longitude
        longitudeAfter = trackPointAfter.longitude

        deltaLongitudeDegrees = math.fabs(longitudeAfter - longitudeBefore)
        if trackPoint.isReciprocated:
            deltaLongitudeDegrees = 360-deltaLongitudeDegrees
        
        deltaLongitudeSeconds = deltaLongitudeDegrees * 60 * 60
        if (deltaLongitudeSeconds > self.maxInterpolateCoordinateSeconds):
            print ("  '{0}' from '{1}' NOT geotagged, {2} seconds of longitude apart".
                format(photoName, photoExifDate, deltaLongitudeSeconds))
            return False

        timestampBefore = trackPointBefore.timestamp
        timestampAfter = trackPointAfter.timestamp

        deltaTimestampSeconds = (timestampAfter-timestampBefore).total_seconds()
        if (deltaTimestampSeconds > self.maxInterpolateTimeSeconds):
            print ("  '{0}' from '{1}' NOT geotagged, {2} seconds apart".
                format(photoName, photoExifDate, deltaTimestampSeconds))
            return False
        
        return True
    
    
    
        
        