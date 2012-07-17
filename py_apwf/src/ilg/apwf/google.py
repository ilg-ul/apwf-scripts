
import urllib
import simplejson
import pycountry

from ilg.apwf.errorWithDescription import ErrorWithDescription


class GoogleApi(object):

    def __init__(self, isVerbose = False):
       
        self.isVerbose = isVerbose
        return
    
   
    # The Google Elevation API
    # https://developers.google.com/maps/documentation/elevation/
    
    def getElevation(self, latitude, longitude):
        
        requestUrl = ('http://maps.googleapis.com/maps/api/elevation/json?'
                      'locations={0},{1}&sensor=false'.format(latitude, longitude))

        f = urllib.urlopen(requestUrl)
        parsedJsonResponse = simplejson.load(f)
        f.close()
        
        if self.isVerbose:
            print parsedJsonResponse
        
        results = parsedJsonResponse['results']
        result = results[0]
        elevationString =  result['elevation']
        
        return float(elevationString)

    
    # The Google Geocoding API
    # https://developers.google.com/maps/documentation/geocoding/
    
    def getReverseGeocoding(self, latitude, longitude):
        
        requestUrl = ('http://maps.googleapis.com/maps/api/geocode/json?'
                      'latlng={0},{1}&sensor=false'.format(latitude, longitude))
    
        f = urllib.urlopen(requestUrl)
        parsedJsonResponse = simplejson.load(f)
        f.close()

        if self.isVerbose:
            print parsedJsonResponse

        status = parsedJsonResponse['status']
        if status == 'ZERO_RESULTS':
            raise ErrorWithDescription('Zero results from Google')
        
        if status != 'OK':
            raise ErrorWithDescription("Reverse Geocodding Error '{0}'".format(status))
        
        results = parsedJsonResponse['results']
        #print results
        
        jsonDict = {}
        
        for result in results:
            address_components = result['address_components']
            for address_component in address_components:
                acType = address_component['types'][0]
                value = unicode(address_component['long_name'])
                if acType in jsonDict:
                    if jsonDict[acType] != value:
                        #print "    {0} initialy '{1}', redefined '{2}'".format(acType, jsonDict[acType], address_component['long_name'])
                        jsonDict[acType] += '/' + value
                else:
                    jsonDict[acType] = value
        
        #print jsonDict

        resultDict = {}
        
        countryName = None
        countryCode = None
                    
        if 'country' in jsonDict:
            
            countryName = jsonDict['country']
            del jsonDict['country']
            
            countryCode = self.convertCountryNameToIso3(countryName)
            

        resultDict['CountryCode'] = countryCode
        resultDict['CountryName'] = countryName
        
        province = None
        
        for keyName in ['administrative_area_level_1']:      
            if keyName in jsonDict:
                province = jsonDict[keyName]
                del jsonDict[keyName]
                break
            
        resultDict['Province'] = province

        city = None
        
        try:
            if 'locality' in jsonDict and 'administrative_area_level_2' in jsonDict:
                if jsonDict['administrative_area_level_2'] == province:
                    del jsonDict['administrative_area_level_2']
        except:
            pass
        
        for keyName in ['locality', 'administrative_area_level_2']:      
            if keyName in jsonDict:
                city = jsonDict[keyName]
                del jsonDict[keyName]
                break

        if 'administrative_area_level_2' in jsonDict:
            city += '/' + jsonDict['administrative_area_level_2']
            del jsonDict['administrative_area_level_2']
            
        resultDict['City'] = city

        
        location = None

        try:
            if jsonDict['route'] == jsonDict['neighborhood']:
                del jsonDict['route']
        except:
            pass
        
        for keyName in ['route', 'establishment', 'sublocality', 'neighborhood', 'postal_code', 'administrative_area_level_3']:      
            if keyName in jsonDict:
                if location == None:
                    location = jsonDict[keyName]
                else:
                    location += ', ' + jsonDict[keyName]
                
                del jsonDict[keyName]
        
        
        resultDict['Location'] = location

        # remove uninteresting data
        for keyName in []:      
            if keyName in jsonDict:
                del jsonDict[keyName]
        
        if len(jsonDict) > 0:
            raise ErrorWithDescription('Unprocessed geocodding data: {0}'.format(jsonDict))
        
        return resultDict
    
    
    def convertCountryNameToIso3(self, countryNameString):
        
        try:
            country = pycountry.countries.get(name=countryNameString)
            countryCode = country.alpha3
        except:
            countryCode = None

        return countryCode
    