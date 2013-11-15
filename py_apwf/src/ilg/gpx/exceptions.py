
class NotFound(Exception):
    
    pass
 

class NotFoundEmptyTrack(NotFound):

    pass

    
class NotFoundBeforeFirst(NotFound):

    pass


class NotFoundAfterLast(NotFound):
    
    pass


class NotFoundBetween(NotFound):
    
    def __init__(self, index):
        
        self.indexBefore = index
        
        return

    
    def __str__(self):
        
        return str(self.indexBefore)
    

    def getIndexBefore(self):
        
        return self.indexBefore
    
    