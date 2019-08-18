

class TrackPoint(object):
    def __init__(self,Latitude,Longitude,time = None,elevation = None):
        self.lat = Latitude
        self.lon = Longitude
        self.time = time
        self.ele = elevation
    def __eq__(self, other):
        result = True
        result &= (self.lat == other.lat)
        result &= (self.lon == other.lon)
        result &= (self.ele == other.ele)
        return result

class WayPoint(object):
    def __init__(self,trackpoint):
        self.trkpt = trackpoint
        self.name = None
        self.ele = None
        self.desc = None 

    def set_extension(self, name = None,description = None,elevation = None):
        self.name = name
        self.ele = elevation
        self.desc = description 


