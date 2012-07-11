
#from ilg.gpx.trackPoint import TrackPoint

from ilg.gpx.exceptions import NotFoundEmptyTrack
from ilg.gpx.exceptions import NotFoundBeforeFirst
from ilg.gpx.exceptions import NotFoundAfterLast
from ilg.gpx.exceptions import NotFoundBetween

class TrackByTimestamp(object):

    def __init__(self):

        self.points = []
        self.name = None
        
        return
    
    
    def setName(self, name):
        self.name = name
        return
    
    
    def add(self, trackpoint):
        
        crtLen = len(self.points)
        
        if crtLen == 0:
            self.points.append(trackpoint)
            return
        
        lastPoint = self.points[crtLen-1]
        if trackpoint.timestamp > lastPoint.timestamp:
            self.points.append(trackpoint)
            return
        
        print 'insert not implemented'
        return


    # return the index of the trackpoint.
    # if not found, raise error
    def locateByTimestamp(self, timestamp):
        
        if len(self.points) == 0:
            raise NotFoundEmptyTrack()
              
        if timestamp < self.points[0].timestamp:            
            raise NotFoundBeforeFirst()
            
        indexLast = len(self.points)-1
        if timestamp > self.points[indexLast].timestamp:
            raise NotFoundAfterLast()
        
        return self._recurseLocateByTimestamp(0, indexLast, timestamp)
    
    
    def _recurseLocateByTimestamp(self, indexFirst, indexLast, timestamp):
        
        if ((indexFirst + 1) == indexLast) or (indexFirst == indexLast):
            
            timestampFirst = self.points[indexFirst].timestamp
            if timestamp == timestampFirst:
                return indexFirst
            
            timestampLast = self.points[indexLast].timestamp
            if timestamp == timestampLast:
                return indexLast
            
            if (timestampFirst < timestamp) and (timestamp < timestampLast):
                raise NotFoundBetween(indexFirst)
            
            if timestamp < timestampFirst:
                
                if indexFirst == 0:
                    raise NotFoundBeforeFirst()
                else:
                    raise NotFoundBetween(indexFirst-1)
                
            elif timestamp > timestampLast:
            
                if indexLast == (len(self.points)-1):
                    raise NotFoundAfterLast()
                else:
                    raise NotFoundBetween(indexLast)
            
        indexMiddle = int((indexFirst + indexLast) / 2)
        
        timestampMiddle = self.points[indexMiddle].timestamp
        if timestamp == timestampMiddle:
            return indexMiddle
        
        if timestamp < timestampMiddle:
            return self._recurseLocateByTimestamp(indexMiddle, indexLast, timestamp)            
        else:
            return self._recurseLocateByTimestamp(indexFirst, indexMiddle, timestamp)
                
           
            