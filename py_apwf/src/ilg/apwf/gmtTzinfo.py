
from datetime import timedelta, tzinfo

class GmtTzinfo(tzinfo):
    
    def __init__(self, stringTimeZone):
        
        # initialise parent tzinfo
        super(GmtTzinfo,self).__init__()
        
        stringTimeZone = stringTimeZone.strip()
        
        if stringTimeZone != 'Z':
            
            ix = 0
            signCh = stringTimeZone[ix:ix+1]
            splits = stringTimeZone[ix+1:].split(':')
            minutes = int(splits[0])*60 + int(splits[1])
            if signCh == '-':
                minutes = -minutes
                
        else:
           
            minutes = 0 
            
        
        self.offsetMinutes = minutes
        self.stringTimeZone = stringTimeZone

        return
    
        
    def utcoffset(self, dt):
        
        # fixed-offset class
        return timedelta(minutes=self.offsetMinutes)
    
    
    def localize(self, dt):
        
        if dt.tzinfo is not None:
            raise ValueError('Not naive datetime (tzinfo is already set)')

        localizedDatetime = dt.replace(tzinfo=self)
        return localizedDatetime
    
    
    def dst(self, dt):
        
        # a fixed-offset class:  doesn't account for DST
        return timedelta(0)
    
        
    def tzname(self, dt):
        
        return self.stringTimeZone
    
    
    def __repr__(self):
        
        return repr(self.stringTimeZone)
    

# A simple Zulu time zone

class ZuluTzinfo(GmtTzinfo):

    def __init__(self):
            
        super(ZuluTzinfo,self).__init__('Z')

        return
    
    # All other methods inherited from parent
    

