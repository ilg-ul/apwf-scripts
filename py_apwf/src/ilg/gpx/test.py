
from xml.sax import make_parser
from ilg.gpx.xmlParser import TrackHandler

if __name__ == '__main__':
    file_name = '/Users/ilg/Desktop/g.gpx'
    
    if False:
        f = open( file_name, 'r' )
        gpx_xml = f.read()
        f.close()
    else:
        th = TrackHandler()
        parser = make_parser()
        parser.setContentHandler(th)
        parser.parse(file_name)
        
    print '[done]'