
from datetime import datetime
from ilg.apwf.gmtTzinfo import ZuluTzinfo

class TrackPoint(object):

    def __init__(self, latitude, longitude, elevation = None, timestamp = None):

        self.latitude = float(latitude)
        self.longitude = float(longitude)
        
        self.setElevation(elevation)
        
        self.tzUtc = ZuluTzinfo()

        self.setTimestamp(timestamp)
              
        return
    
    
    def setElevation(self, elevation):
        
        if elevation == None:
            self.elevation = None
        else:
            self.elevation = float(elevation)
        
        return
    
    
    def setTimestamp(self, timestampString):
        
        if timestampString == None:
            self.timestamp = None
        elif isinstance(timestampString, unicode):
            self.timestamp = self._convertStringToDate(timestampString)
        else:
            self.timestamp = timestampString
                
        return
    
    
    def _convertStringToDate(self, timestampString):
    
        try:
            timestamp = datetime.strptime(timestampString, '%Y-%m-%dT%H:%M:%SZ')        
            timestampWithTz = self.tzUtc.localize(timestamp)
        except ValueError as err:
            print err
            timestampWithTz = None
        
        return timestampWithTz
    

class InterpolatedTrackPoint(TrackPoint):

    def __init__(self, timestamp, trackPointBefore, trackPointAfter):
        
        timestampBefore = trackPointBefore.timestamp
        timestampAfter = trackPointAfter.timestamp
        ratio = (float((timestamp-timestampBefore).total_seconds())/
                     float((timestampAfter-timestampBefore).total_seconds()))
        
        latitudeBefore = trackPointBefore.latitude
        latitudeAfter = trackPointAfter.latitude
        
        latitude = latitudeBefore + (latitudeAfter - latitudeBefore) * ratio
        
        longitudeBefore = trackPointBefore.longitude
        longitudeAfter = trackPointAfter.longitude
        
        longitude = longitudeBefore + (longitudeAfter - longitudeBefore) * ratio
       
        elevationBefore = trackPointBefore.elevation
        elevationAfter = trackPointAfter.elevation
        
        elevation = elevationBefore + (elevationAfter - elevationBefore) * ratio
        
        super(InterpolatedTrackPoint,self).__init__(latitude, longitude, elevation, timestamp)
        
        self.ratio = ratio
        self.trackPointBefore = trackPointBefore
        self.trackPointAfter = trackPointAfter
        
        return
    

        

