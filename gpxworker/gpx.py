from lxml import etree
from math import sin, cos, radians, atan2, atan, sqrt, degrees, pi, acos

class Track(object):
    def __init__(self):
        self.track_segment = []
        self.name = None
        self.ele = None
        self.desc = None 
        self.time = None
    def add_track(self,trackpoint):
        self.track_segment.append(trackpoint)
    def get_trackpoint(self,index):
        return self.track_segment[index]

    @staticmethod
    def distance_from_points(self,A,B):
        delta_lat = radians(A.lat - B.lat)
        delta_lon = radians(A.lon - B.lon)
        a = sin(delta_lat/2)**2 + cos(radians(A.lat)) * cos(radians(B.lat)) * (sin(delta_lon/2)**2)
        distance = 2 * atan2(sqrt(a), sqrt(1-a)) * 6371 #R = 6371 is radius of the Earth
        return distance


    @staticmethod
    def angle_from_points(self, A, B, tangens_mode = False):
        delta_h = B.ele - A.ele
        delta_l = Track.distance_from_points(None, A, B) * 1000 # k = 1000, to meters
        if delta_l == 0:
            return 0
        tangens = delta_h / delta_l
        if tangens_mode:
            return tangens
        result = atan(tangens)
        return degrees(result)

    @staticmethod
    def turn_angle(self, A, B, C):
        ab = Track.distance_from_points(None, A, B)
        bc = Track.distance_from_points(None, B, C)
        ac = Track.distance_from_points(None, A, C)

        if ab == 0 or bc == 0 or ac == 0:
            return 180
        cos_gamma = (ab*ab + bc*bc - ac*ac)/(2*ab*bc)
        if abs(cos_gamma) > 1:
            return 180
        gamma = acos(cos_gamma)
        return degrees(gamma)

    def set_distance(self):
        N = len(self.track_segment)
        dist = 0
        for i in range(N - 1):
            A = self.track_segment[i]
            B = self.track_segment[i + 1]
            dist += self.distance_from_points(self, A,B)
        self.desc = dist
    def set_time(self):
        pnt = self.track_segment[0]
        self.time = pnt.time




class GPX(object):
    def __init__(self):
        self.waypoints = []
        self.track = None
    def add_waypoint(self,wp):
        self.waypoints.append(wp)
    def get_time(self):
        return self.track.time
    def get_describe(self):
        return self.track.desc
    def get_name(self):
        return self.track.name
    def set_name(self,value):
        self.track.name = value
    def set_describe(self,value):
        self.track.desc = value
    def set_time(self,value = None):
        if value is not None:
            self.track.time = value
        else:
            self.track.set_time()
    def get_trackpoint(self,index):
        return self.track.get_trackpoint(index)
    def insert_trackpoint(self,index,data):
        self.track.track_segment.insert(index,data)
    def set_distance(self):
        self.track.set_distance()
    def check_name_existing(self, value):
        if self.track.name is None:
            self.track.name = value.split('/')[-1]


    def __eq__(self, other):
        result = True
        result &= (self.track.time == other.track.time)
        result &= (self.track.name == other.track.name)
        result &= (self.track.desc == other.track.desc)
        return result
        
