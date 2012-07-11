
from datetime import datetime
from ilg.apwf.gmtTzinfo import ZuluTzinfo

class TrackPoint(object):

    def __init__(self, latitude, longitude, elevation = None, timestamp = None):

        self.latitude = float(latitude)
        self.longitude = float(longitude)
        
        if elevation == None:
            self.elevation = elevation
        else:
            self.elevation = float(elevation)
        
        self.tzUtc = ZuluTzinfo()

        if timestamp == None:
            self.timestamp = None
        else:
            self.timestamp = self._convertStringToDate(timestamp)
        
        
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
        else:
            self.timestamp = self._convertStringToDate(timestampString)   
                
        return
    
    
    def _convertStringToDate(self, timestampString):
    
        try:
            timestamp = datetime.strptime(timestampString, '%Y-%m-%dT%H:%M:%SZ')        
            timestampWithTz = self.tzUtc.localize(timestamp)
        except ValueError as err:
            print err
            timestampWithTz = None
        
        return timestampWithTz
    

    