
from xml.sax.handler import ContentHandler

from ilg.gpx.track import Tracks
from ilg.gpx.track import TrackByTimestamp
from ilg.gpx.trackPoint import TrackPoint

class TrackHandler(ContentHandler):

    def __init__(self):
        
        self.inGpx = False
        self.innerHandler = _Ignore()
        
        # empty list of tracks
        self.tracks = Tracks()
        
        return

      
    def getResult(self):
        
        return self.tracks;
    
      
    def startElement(self, name, attributes):
        
        if self.inGpx:
            self.innerHandler.startElement(name, attributes)
        else:
            if name == "gpx":
                self.inGpx = True
                self.innerHandler = _Gpx(self.tracks)
                
        return
    
 
    def characters(self, data):
        self.innerHandler.characters(data)
        return

 
    def endElement(self, name):
        
        if self.inGpx:
            if name == "gpx":
                self.inGpx = False
                self.innerHandler = _Ignore()
            else:
                self.innerHandler.endElement(name)
                
        else:
            pass
            
        return
            

# ----- Internal classes ------------------------------------------------------

class _Ignore():

    def startElement(self, name, attributes):
        pass
 
    def characters(self, data):
        pass
 
    def endElement(self, name):
        pass

    
class _Gpx():

    def __init__(self, tracks):
        
        self.inTrk = False
        self.innerHandler = _Ignore()
        
        self.tracks = tracks
        
        return

        
    def startElement(self, name, attributes):
        
        if self.inTrk:
            self.innerHandler.startElement(name, attributes)
        else:
            if name == "trk":
                self.inTrk = True
                self.innerHandler = _Trk(self.tracks)
                
        return
    
 
    def characters(self, data):
        self.innerHandler.characters(data)
        return

 
    def endElement(self, name):
        
        if self.inTrk:
            if name == "trk":
                self.inTrk = False
                self.innerHandler = _Ignore()
            else:
                self.innerHandler.endElement(name)
        else:
            pass
            
        return
            

class _Trk():

    def __init__(self, tracks):
        
        self.inName = False
        self.inTrkseg = False
        self.innerHandler = _Ignore()
        
        self.tracks = tracks
                
        # create new track
        self.track = TrackByTimestamp()

        return

        
    def startElement(self, name, attributes):
        
        if self.inName:
            self.innerHandler.startElement(name, attributes)
        elif self.inTrkseg:
            self.innerHandler.startElement(name, attributes)
        else:
            if name == "name":
                self.inName = True
                self.innerHandler = _Ignore()                
                self.name = "" # will be used to collect characters
            elif name == "trkseg":
                self.inTrkseg = True
                
                self.innerHandler = _Trkseg(self.track)
                
        return
    
 
    def characters(self, data):
        
        if self.inName:
            self.name += data
        else:
            self.innerHandler.characters(data)
            
        return

 
    def endElement(self, name):
        
        if self.inName:
            
            if name == "name":
                self.inName = False
                self.innerHandler = _Ignore()
                
                #print "Track name '{0}'".format(self.name)
                self.track.setName(self.name)

            else:
                self.innerHandler.endElement(name)

        elif self.inTrkseg:
            
            if name == "trkseg":
                self.inTrkseg = False
                self.innerHandler = _Ignore()
                
                # append to parent
                self.tracks.append(self.track)
                
            else:
                self.innerHandler.endElement(name)
        else:
            pass
            
        return

            
class _Trkseg():

    def __init__(self, track):
        
        self.inTrkpt = False
        self.innerHandler = _Ignore()
        
        self.track = track
        
        return

        
    def startElement(self, name, attributes):
        
        if self.inTrkpt:
            self.innerHandler.startElement(name, attributes)
        else:
            if name == "trkpt":
                self.inTrkpt = True
                
                latitude = attributes['lat']
                longitude = attributes['lon']
                
                self.trackpoint = TrackPoint(latitude, longitude)
                #print "Latitude={0}, Longitude={1}".format(latitude, longitude)
                self.innerHandler = _Trkpt(self.trackpoint)
                
        return
    
 
    def characters(self, data):
        self.innerHandler.characters(data)
        return

 
    def endElement(self, name):
        
        if self.inTrkpt:
            if name == "trkpt":
                self.inTrkpt = False
                self.innerHandler = _Ignore()
                
                # now the track point is complete, add it to track
                self.track.add(self.trackpoint)
            else:
                self.innerHandler.endElement(name)
        else:
            pass
           
        return

  
class _Trkpt():

    def __init__(self, trackpoint):
        
        self.inEle = False
        self.inTime = False
        self.innerHandler = _Ignore()
        
        self.trackpoint = trackpoint
          
        return

        
    def startElement(self, name, attributes):
        
        if self.inEle:
            pass    # ignore elements in <ele>
        elif self.inTime:
            pass    # ignore elements in <time>
        else:
            if name == "ele":
                self.inEle = True                
                self.elevation = "" # will be used to collect characters
            elif name == "time":
                self.inTime = True                
                self.timestamp = "" # will be used to collect characters
            else:
                pass
            
        return
    
 
    def characters(self, data):
        
        if self.inEle:
            self.elevation += data
        elif self.inTime:
            self.timestamp += data
        else:
            pass # ignore other characters
        
        return

 
    def endElement(self, name):
        
        if self.inEle:
            
            if name == "ele":
                self.inEle = False
                
                self.trackpoint.setElevation(self.elevation)
                #print "Elevation '{0}'".format(self.elevation)
            else:
                pass # ignore other closing elements
                
        elif self.inTime:
            
            if name == "time":
                self.inTime = False
                
                self.trackpoint.setTimestamp(self.timestamp)
                #print "Time '{0}'".format(data)

            else:
                pass # ignore other closing elements
        
        else:
            pass # ignore other closing elements
          
        return
          
    