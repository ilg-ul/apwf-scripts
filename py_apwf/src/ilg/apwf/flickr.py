
import flickrapi

api_key = '42e492688f5779a16741aa1e3d73a9c9'
api_secret = '83f293d3f7f79917'

class Flickr():
    
    def __init__(self):
        
        self.flickrapi = flickrapi.FlickrAPI(api_key, api_secret, format='json')
        
        return


    def setPhotoMetadata(self, photoIdString, titleString, descriptionString):
        
        response = self.flickrapi.photos_setMeta(photo_id=photoIdString, 
                    title=titleString, description=descriptionString)
        
        if response == 'jsonFlickrApi({"stat":"ok"})':        
            return True
        else:
            return False
       
        
    def setPhotoTags(self, photoIdString, tagsList):
        
        tagsString = ''
        for tag in tagsList:
            if tagsString != '':
                tagsString += ','
            tagsString += tag
            
        response = self.flickrapi.photos_setTags(photo_id=photoIdString, 
                                                 tags=tagsString)

        if response == 'jsonFlickrApi({"stat":"ok"})':        
            return True
        else:
            return False
