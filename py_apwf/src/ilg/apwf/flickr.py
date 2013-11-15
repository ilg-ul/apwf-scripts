
import flickrapi
import json

api_key = '42e492688f5779a16741aa1e3d73a9c9'
api_secret = '83f293d3f7f79917'

class FlickrException(Exception):

    def __init__(self, codeString, descriptionString):
        
        self.codeString = codeString
        self.descriptionString = descriptionString
        
        return
    
    
    def getCode(self):
        
        return self.codeString
    
    
    def getDescription(self):
        
        return self.descriptionString
    
        
    def __str__(self):
        return '{0} (code={1})'.format(self.descriptionString, self.codeString)


class Flickr():
    
    def __init__(self):
        
        self.flickrapi = flickrapi.FlickrAPI(api_key, api_secret, format='json')
        
        return


    def parseJsonResponse(self, response):
        
        prefix = 'jsonFlickrApi('
        sufix = ')'
        if not response.startswith(prefix) or not response.endswith(sufix):
            return None
        
        response = response[len(prefix):-len(sufix)]
        parsedJson = json.loads(response)

        if parsedJson['stat'] == 'fail':
            raise FlickrException(parsedJson['code'], parsedJson['message'])
        
        return parsedJson
    
        
    def setPhotoMetadata(self, photoIdString, titleString, descriptionString):
        
        response = self.flickrapi.photos_setMeta(photo_id=photoIdString, 
                    title=titleString, description=descriptionString)
        
        if response == 'jsonFlickrApi({"stat":"ok"})':        
            return True
        else:
            return False
       
        
    def setPhotoTags(self, photoIdString, tagsList):
        
        tagsString = ','.join(tagsList)    
        response = self.flickrapi.photos_setTags(photo_id=photoIdString, 
                                                 tags=tagsString)

        if response == 'jsonFlickrApi({"stat":"ok"})':        
            return True
        else:
            return False


    def getPhotoSets(self, photoIdString):
        
        response = self.flickrapi.photos_getAllContexts(photo_id=photoIdString)
        
        parsedJson = self.parseJsonResponse(response)
        
        return parsedJson['set']
    
    
    def getSetPhotos(self, setIdString):
        
        photoIds = []
        
        page = 1
        while True:
            
            response = self.flickrapi.photosets_getPhotos(photoset_id=setIdString, page=page)
        
            try:
                parsedJson = self.parseJsonResponse(response)
            except FlickrException as ex:
                if page == 1:
                    raise ex
                
                if ex.getCode() == 1:
                    break
                
                raise ex
            
            if len(parsedJson['photoset']['photo']) == 0:
                break
            
            for setPhoto in parsedJson['photoset']['photo']:
                photoIds.append(setPhoto['id'])
                
            page += 1

        return photoIds

        
    def createSet(self, title, photoIdString):
        
        response = self.flickrapi.photosets_create(title=title, 
                                            primary_photo_id=photoIdString)
        
        parsedJson = self.parseJsonResponse(response)

        return parsedJson['photoset']['id']
   
   
    def addPhotoToSet(self, setIdString, photoIdString):

        response = self.flickrapi.photosets_addPhoto(photoset_id=setIdString,
                                            photo_id=photoIdString)
        
        self.parseJsonResponse(response)

        return


    def removePhotoFromSet(self, setIdString, photoIdString):
        
        response = self.flickrapi.photosets_removePhoto(photoset_id=setIdString,
                                            photo_id=photoIdString)
        
        self.parseJsonResponse(response)

        return
    