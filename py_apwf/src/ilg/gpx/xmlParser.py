
from xml.sax.handler import ContentHandler

class TrackHandler(ContentHandler):

    def __init__(self):
        self.inGpx = False
        self.innerHandler = _Ignore()
        return
        
    def startElement(self, name, attributes):
        if self.inGpx:
            self.innerHandler.startElement(name, attributes)
        else:
            if name == "gpx":
                self.inGpx = True
                self.innerHandler = _Gpx()
                
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

    def __init__(self):
        self.inTrk = False
        self.innerHandler = _Ignore()
        return
        
    def startElement(self, name, attributes):
        if self.inTrk:
            self.innerHandler.startElement(name, attributes)
        else:
            if name == "trk":
                self.inTrk = True
                self.innerHandler = _Trk()
                
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

    def __init__(self):
        self.inName = False
        self.inTrkseg = False
        self.innerHandler = _Ignore()
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
            elif name == "trkseg":
                self.inTrkseg = True
                self.innerHandler = _Trkseg()
                
        return
    
 
    def characters(self, data):
        if self.inName:
            print "Track name '{0}'".format(data)
        else:
            self.innerHandler.characters(data)
        return
 
    def endElement(self, name):
        if self.inName:
            if name == "name":
                self.inName = False
                self.innerHandler = _Ignore()
            else:
                self.innerHandler.endElement(name)

        elif self.inTrkseg:
            if name == "trkseg":
                self.inTrkseg = False
                self.innerHandler = _Ignore()                
            else:
                self.innerHandler.endElement(name)
        else:
            pass
            
        return

            
class _Trkseg():

    def __init__(self):
        self.inTrkpt = False
        self.innerHandler = _Ignore()
        return

        
    def startElement(self, name, attributes):
        if self.inTrkpt:
            self.innerHandler.startElement(name, attributes)
        else:
            if name == "trkpt":
                self.inTrkpt = True
                #print "Latitude={0}, Longitude={1}".format(attributes['lat'], attributes['lon'])
                self.innerHandler = _Trkpt()
                
        return
    
 
    def characters(self, data):
        self.innerHandler.characters(data)
        return
 
    def endElement(self, name):
        if self.inTrkpt:
            if name == "trkpt":
                self.inTrkpt = False
                self.innerHandler = _Ignore()
            else:
                self.innerHandler.endElement(name)
        else:
            pass
           
        return

  
class _Trkpt():

    def __init__(self):
        self.inEle = False
        self.inTime = False
        self.innerHandler = _Ignore()
        return

        
    def startElement(self, name, attributes):
        if self.inEle:
            pass    # ignore elements in <ele>
        elif self.inTime:
            pass    # ignore elements in <time>
        else:
            if name == "ele":
                self.inEle = True
            elif name == "time":
                self.inTime = True
            else:
                pass
            
        return
    
 
    def characters(self, data):
        if self.inEle:
            pass #print "Elevation '{0}'".format(data)
        elif self.inTime:
            pass #print "Time '{0}'".format(data)
        else:
            pass # ignore other characters
        
        return

 
    def endElement(self, name):
        if self.inEle:
            if name == "ele":
                self.inEle = False
            else:
                pass # ignore other closing elements
                
        elif self.inTime:
            if name == "time":
                self.inTime = False
            else:
                pass # ignore other closing elements
        
        else:
            pass # ignore other closing elements
          
        return
          
    