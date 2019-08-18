import sys
from gpxworker.gpx import Track
import matplotlib.pyplot as plt




class Plotter(object):
    def __init__(self, points):
        self.points = points

    def setup(self):
        N = len(self.points)
        dist = 0
        self.distance = [dist]
        self.elevation = [self.points[0].ele]
        for i in range(1,N):
            ele = self.points[i].ele
            if ele is None:
                return False
            self.elevation.append(ele)
            A = self.points[i-1]
            B = self.points[i]
            dist += Track.distance_from_points(None, A ,B)
            self.distance.append(dist)
        return True
        
    def plot(self):
        plt.plot(self.distance, self.elevation)
        plt.xlabel('Расстояние (км)')
        plt.ylabel('Высота (м)')
        plt.title('Карта высот')
        plt.grid(True)
        plt.show()



