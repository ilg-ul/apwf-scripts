
#from ilg.gpx.trackPoint import TrackPoint
from ilg.gpx.trackPoint import InterpolatedTrackPoint

from ilg.gpx.exceptions import NotFound
from ilg.gpx.exceptions import NotFoundEmptyTrack
from ilg.gpx.exceptions import NotFoundBeforeFirst
from ilg.gpx.exceptions import NotFoundAfterLast
from ilg.gpx.exceptions import NotFoundBetween


class Tracks(object):
    
    def __init__(self):
        
        self.tracks = []
        return
    
    
    def getTracks(self):
        
        return self.tracks
    
    
    def append(self, track):
        
        self.tracks.append(track)
        return
    
        
    def locateByTimestamp(self, timestamp):
        
        for track in self.tracks:
            
            points = track.getPoints()
            
            try:
                
                index = track.locateByTimestamp(timestamp)
                trackPoint = points[index]
                return trackPoint
            
            except NotFoundBetween as err:
                
                indexBefore = err.getIndexBefore()
                trackPointBefore = points[indexBefore]
                trackPointAfter = points[indexBefore+1]
                return InterpolatedTrackPoint(timestamp, trackPointBefore, 
                                              trackPointAfter)                
                
            except NotFound as err:
                print err, repr(err)

        return None


class TrackByTimestamp(object):

    def __init__(self):

        self._points = []
        self._name = None
        
        return
    
    
    def setName(self, name):
        self._name = name
        return
    
    
    def getName(self):
        return self._name
    

    def getPoints(self):
        return self._points
    
    
    def add(self, trackpoint):
        
        crtLen = len(self._points)
        
        if crtLen == 0:
            self._points.append(trackpoint)
            return
        
        lastPoint = self._points[crtLen-1]
        if trackpoint.timestamp > lastPoint.timestamp:
            self._points.append(trackpoint)
            return
        
        print 'insert not implemented'
        return


    # return the index of the trackpoint.
    # if not found, raise error
    def locateByTimestamp(self, timestamp):
        
        if len(self._points) == 0:
            raise NotFoundEmptyTrack()
              
        if timestamp < self._points[0].timestamp:            
            raise NotFoundBeforeFirst()
            
        indexLast = len(self._points)-1
        if timestamp > self._points[indexLast].timestamp:
            raise NotFoundAfterLast()
        
        return self._recurseLocateByTimestamp(0, indexLast, timestamp)
    
    
    def _recurseLocateByTimestamp(self, indexFirst, indexLast, timestamp):
        
        if ((indexFirst + 1) == indexLast) or (indexFirst == indexLast):
            
            timestampFirst = self._points[indexFirst].timestamp
            if timestamp == timestampFirst:
                return indexFirst
            
            timestampLast = self._points[indexLast].timestamp
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
            
                if indexLast == (len(self._points)-1):
                    raise NotFoundAfterLast()
                else:
                    raise NotFoundBetween(indexLast)
            
        indexMiddle = int((indexFirst + indexLast) / 2)
        
        timestampMiddle = self._points[indexMiddle].timestamp
        if timestamp == timestampMiddle:
            return indexMiddle
        
        if timestamp < timestampMiddle:
            return self._recurseLocateByTimestamp(indexFirst, indexMiddle, timestamp)
        else:
            return self._recurseLocateByTimestamp(indexMiddle, indexLast, timestamp)            
                
           
            