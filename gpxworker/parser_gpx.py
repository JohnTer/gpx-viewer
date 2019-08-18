import dateutil.parser
from lxml import etree
from .gpx import Track, GPX
from .points import TrackPoint, WayPoint

class Parser(object):
    def __init__(self):
        self.gpx = GPX()

        self.__WAYPOINT = "wpt"
        self.__TRACK = "trk"
        self.__NAME = "name"
        self.__DESCRIBE = "desc"
        self.__TRACKSEGMENTS = "trkseg"
        self.__TIME = "time"
        self.__ELEVATION = "ele"
        self.__METADATA = "metadata"
        

    def __get_tag(self,node):
        return node.tag[node.tag.find("}") + 1 :]

    def __get_xml(self,xmlFile):
        with open(xmlFile) as fobj:
            self.xml = fobj.read()

    def __get_waypoint(self,node):
        trackpoint = node.attrib
        waypoint = WayPoint(TrackPoint(float(trackpoint['lat']),float(trackpoint['lon'])))
        for extended in node:
            tag = self.__get_tag(extended)
            if (tag == self.__NAME):
                waypoint.name = extended.text
            elif (tag == self.__DESCRIBE):
                waypoint.desc = extended.text
        return waypoint

    def __get_dotinf(self,nodes,dot):
        for node in nodes:
            tag = self.__get_tag(node)
            if  tag == self.__TIME:
                texttime = node.text
                dtime = texttime[:texttime.index('T')]
                dtime = dtime.split('-')
                dtime[0], dtime[2] = dtime[2], dtime[0]
                dot.time = '.'.join(dtime)
            elif tag == self.__ELEVATION:
                dot.ele = float(node.text)
                


    def __get_track(self,node):
        track = Track()
        for extended in node:
            tag = self.__get_tag(extended)
            if (tag == self.__NAME):
                track.name = extended.text
            elif (tag == self.__DESCRIBE):
                track.desc = extended.text
            elif (tag == self.__TRACKSEGMENTS):
                for trackpoint in extended:
                    tp = trackpoint.attrib
                    dot = TrackPoint(float(tp['lat']),float(tp['lon']))
                    self.__get_dotinf(trackpoint,dot)
                    track.add_track(dot)
        return track 
    
    def setup(self,filename):
        self.Filename = filename
        try:
            f = open(self.Filename)
            f.close()
        except FileNotFoundError:
            self.Filename = None

      
    def GetData(self):
        try:
            tree = etree.parse(self.Filename)
        except:
            return None


        nodes = tree.getroot()

        gpx = GPX()
        for node in nodes:
            tag = self.__get_tag(node) 
            if (tag == self.__WAYPOINT):
                wp = self.__get_waypoint(node)
                gpx.add_waypoint(wp)
            elif (tag == self.__TRACK):
                gpx.track = self.__get_track(node)
        gpx.set_time()
        gpx.set_distance()
        gpx.check_name_existing(self.Filename)
        return gpx



