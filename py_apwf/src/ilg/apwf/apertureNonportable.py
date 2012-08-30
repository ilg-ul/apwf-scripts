
import subprocess
import sqlite3

class ApertureNonportable():
    
    def __init__(self):
        
        shellCommand = 'defaults read com.apple.aperture LibraryPath'
        shellCommandList = shellCommand.split()
        self.apertureLibraryPath = subprocess.check_output(shellCommandList)
        
        self.apertureLibraryPath = self.apertureLibraryPath.strip()
        
        if self.apertureLibraryPath[-1] != '/':
            self.apertureLibraryPath = self.apertureLibraryPath + '/'
            
        libraryDbPath = self.apertureLibraryPath + 'Database/apdb/Library.apdb'
        facesDbPath = self.apertureLibraryPath + 'Database/apdb/Faces.db'
        
        self.libraryConnection = sqlite3.connect(libraryDbPath)
        self.libraryConnection.row_factory = sqlite3.Row
        
        self.facesConnection = sqlite3.connect(facesDbPath)
        self.facesConnection.row_factory = sqlite3.Row
        

    def getMasterUuid(self, uuid):
        
        command = 'select masterUuid from RKVersion where uuid=:uuidParam;'
        
        cursor = self.libraryConnection.cursor()
        cursor.execute(command, {"uuidParam":uuid})
        
        raw = cursor.fetchone()
        masterUuid = raw['masterUuid']
        
        return masterUuid
    

    def getFaceKeys(self, masterUuid):
        
        command = 'select faceKey from RKDetectedFace where masterUuid=:masterUuidParam;'
        
        cursor = self.facesConnection.cursor()
        cursor.execute(command, {"masterUuidParam":masterUuid})
        
        faceKeys = []
        
        raws = cursor.fetchall()
        for raw in raws:
            faceKey = raw['faceKey']
            faceKeys.append(faceKey)
            
        return faceKeys

    
    def getFaceNames(self, faceKey):

        command = 'select name,fullName from rkFaceName where faceKey=:faceKeyParam;'
        
        cursor = self.facesConnection.cursor()
        cursor.execute(command, {"faceKeyParam":faceKey})
        
        raw = cursor.fetchone()
        if raw == None:
            return None
        
        name = raw['name']
        fullName = raw['fullName']
        
        return (name, fullName)

    
    def getAlbumVersionIdsBlob(self, albumId):
        
        command = 'select selectedVersionIds from RKAlbum where uuid=:uuid;'
        
        cursor = self.libraryConnection.cursor()
        cursor.execute(command, {"uuid":albumId})
        
        raw = cursor.fetchone()
        if raw == None:
            return None
        
        blob = raw['selectedVersionIds']
        
        return blob
        