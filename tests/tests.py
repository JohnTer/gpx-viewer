import unittest
import time
import string
import pickle
from copy import deepcopy
from random import randint, choice, uniform
from commands.base_command import RmCommand
from commands.command import AddCommandGPX, CngCommandGPX, CngCommandPoints, AddCommandPoint
from gpxworker.points import TrackPoint
from gpxworker.gpx import GPX, Track
from gpxworker.parser_gpx import Parser
from plotter.plotter import Plotter

class AddPointsTestCase(unittest.TestCase):
    def setup(self, N):
        self.N = N
        self.track_segment = []
        for _ in range(N):
            tp = TrackPoint(randint(-180,180),randint(-180,180),randint(-10000,10000))
            self.track_segment.append(tp)

    def test_add_single_point(self, start_val = 5):
        self.setup(start_val)
        benchmark_data = deepcopy(self.track_segment)

        tp = TrackPoint(123,456,789)
        comm = AddCommandPoint(tp, self.track_segment, self.N)
        comm.execute()   
        benchmark_data.append(deepcopy(tp))       
        

        self.assertTrue(len(self.track_segment) == len(benchmark_data))
        for i in range(len(benchmark_data)):
            self.assertEqual(self.track_segment[i] , benchmark_data[i] )

    def test_add_multi_point(self, start_val = 5, count_value = 2):
        self.setup(start_val)
        benchmark_data = deepcopy(self.track_segment)

        for i in range(count_value):
            self.N = len(self.track_segment)
            tp = TrackPoint(randint(-180,180),randint(-180,180),randint(-10000,10000))
            comm = AddCommandPoint(tp, self.track_segment, self.N)
            comm.execute() 
            benchmark_data.append(deepcopy(tp))       

        self.assertTrue(len(self.track_segment) == len(benchmark_data))
        for i in range(len(benchmark_data)):
            self.assertEqual(self.track_segment[i] , benchmark_data[i] )

class AddGPXTestCase(unittest.TestCase):

    def __get_random_string(self,min_char = 8, max_char = 12):
        allchar = string.ascii_letters + string.punctuation + string.digits
        st = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        return st

    def __gen_gpx(self, data = None):
        if data is None:
            data = [self.__get_random_string(),randint(1, 1000),"%d.%d.%d" % (randint(1, 30),randint(1, 12),randint(1970, 2018)) ]
        gp = GPX()
        gp.track = Track()
        gp.set_describe(data[0])
        gp.set_name(data[1])
        gp.set_time(data[2])
        return gp

    def __setup(self, N):
        self.N = N
        self.gpxs = []
        for _ in range(N):
            tp = self.__gen_gpx()
            self.gpxs.append(tp)

    def test_add_single_gpx(self, start_val = 5):
        self.__setup(start_val)
        benchmark_data = deepcopy(self.gpxs)

        gp = GPX()
        gp.track = Track()
        gp.set_describe("Test1")
        gp.set_name("123")
        gp.set_time("1.01.1970")
        comm = AddCommandGPX(gp, self.gpxs, self.N)
        comm.execute()   
        benchmark_data.append(deepcopy(gp)) 

        self.assertTrue(len(self.gpxs) == len(benchmark_data))
        for i in range(len(benchmark_data)):
            self.assertEqual(self.gpxs[i] , benchmark_data[i] )
            
    def test_add_multiple_gpx(self, start_val = 5, count_value = 2):
        self.__setup(start_val)
        benchmark_data = deepcopy(self.gpxs)

        for i in range(count_value):
            self.N = len(self.gpxs)
            gp = self.__gen_gpx()
            comm = AddCommandGPX(gp, self.gpxs, self.N)
            comm.execute()   
            benchmark_data.append(deepcopy(gp)) 

        self.assertTrue(len(self.gpxs) == len(benchmark_data))
        for i in range(len(benchmark_data)):
            self.assertEqual(self.gpxs[i] , benchmark_data[i] )

class DeleteGPXTestCase(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        self.default_data = None

    def setUp(self):
        with open("three_test.pickle", 'rb') as f:
                self.default_data = pickle.load(f)


    def test_single_gpx_delete(self):
        self.setUp()
        index = 1
        benchmark_list = deepcopy(self.default_data)
        cmnd = RmCommand(index, self.default_data, "gpx")
        cmnd.execute()
        del benchmark_list[index]

        self.assertCountEqual(benchmark_list, self.default_data)
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == self.default_data[i]
            self.assertTrue(cond)
        
    def test_multiple_gpx_delete(self):
        self.setUp()
        index1 = 2
        index2 = 0
        benchmark_list = deepcopy(self.default_data)
        cmnd = RmCommand(index1, self.default_data, "gpx")
        cmnd.execute()
        cmnd = RmCommand(index2, self.default_data, "gpx")
        cmnd.execute()

        del benchmark_list[index1]
        del benchmark_list[index2]

        self.assertCountEqual(benchmark_list, self.default_data)
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == self.default_data[i]
            self.assertTrue(cond)      
            
             
    def test_delete_from_empty(self):
        index = 1
        cmnd = RmCommand(index, self.default_data, "gpx")
        flag = True
        try:
            cmnd.execute()
            flag = False
        except: 
            flag = True
        if not flag:
            self.assertEqual(1, 0)
        
class DeletePointsTestCase(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        self.default_data = None

    def setUp(self):
        with open("three_test.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.default_data = gpxs[2].track.track_segment


    def test_single_point_delete(self):
        self.setUp()
        index = 1
        benchmark_list = deepcopy(self.default_data)
        cmnd = RmCommand(index, self.default_data, "points")
        cmnd.execute()
        del benchmark_list[index]

        

        self.assertTrue(len(benchmark_list) == len(self.default_data))
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == self.default_data[i]
            self.assertTrue(cond)
        
    def test_multiple_point_delete(self):
        self.setUp()
        index1 = 2
        index2 = 0
        benchmark_list = deepcopy(self.default_data)
        cmnd = RmCommand(index1, self.default_data, "points")
        cmnd.execute()
        cmnd = RmCommand(index2, self.default_data, "points")
        cmnd.execute()

        del benchmark_list[index1]
        del benchmark_list[index2]

        self.assertTrue(len(benchmark_list) == len(self.default_data))
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == self.default_data[i]
            self.assertTrue(cond)      
            
             
    def test_delete_from_empty(self):
        index = 1
        cmnd = RmCommand(index, self.default_data, "points")
        flag = True
        try:
            cmnd.execute()
            flag = False
        except: 
            flag = True
        if not flag:
            self.assertEqual(1, 0)
     
class ChangePointsTestCase(unittest.TestCase):
    def __init__(self, columnname = 'lat',methodName = 'runTest'):
        self.default_data = None
        self.column_index = 0
        self.colname = columnname
        if columnname == 'lat':
            self.column_index = 0
        elif columnname == 'lon':
            self.column_index = 1
        elif columnname == 'ele':
            self.column_index = 2
        else:
            raise ValueError("This type of column not found")

    def setUp(self):
        with open("three_test.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.default_data = gpxs[2]



    def __manual_change(self,index,value, benchmark_list):
        columnname = self.colname
        if columnname == 'lat':
            benchmark_list[index].lat = float(value)
        elif columnname == 'lon':
            benchmark_list[index].lon = float(value)
        elif columnname == 'ele':
            benchmark_list[index].ele = float(value)


    def test_point_change(self):
        self.setUp()
        index = 1
        value = "12345"
        benchmark_list = deepcopy(self.default_data)
        cmnd = CngCommandPoints(index,self.column_index, value,self.default_data)
        cmnd.execute()
        
        

        benchmark_list = benchmark_list.track.track_segment
        self.__manual_change(index, value, benchmark_list)

        working_list = self.default_data.track.track_segment

        self.assertTrue(len(working_list) == len(benchmark_list))
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == working_list[i]
            self.assertTrue(cond)
        
        
    def test_multiple_point_change(self):
        self.setUp()
        index1 = 1
        index2 = 10
        value1 = "12345"
        value2 = "321"
        benchmark_list = deepcopy(self.default_data)
        cmnd = CngCommandPoints(index1,self.column_index, value1, self.default_data)
        cmnd.execute()
        cmnd = CngCommandPoints(index2,self.column_index, value2, self.default_data)
        cmnd.execute()

        
        

        benchmark_list = benchmark_list.track.track_segment
        self.__manual_change(index1, value1, benchmark_list)
        self.__manual_change(index2, value2, benchmark_list)

        working_list = self.default_data.track.track_segment

        self.assertTrue(len(working_list) == len(benchmark_list))
        for i in range(len(benchmark_list)):
            cond = benchmark_list[i] == working_list[i]
            self.assertTrue(cond)  
            
             

    def test_change_notexisting(self):
        self.setUp()
        index = 100000
        value = "12345"
        cmnd = CngCommandPoints(index,self.column_index, value,self.default_data)
        flag = True
        try:
            cmnd.execute()
            flag = False
        except: 
            flag = True
        if not flag:
            self.assertEqual(1, 0)

class PlotterTestCase(unittest.TestCase):
    def setUp(self, index):
        with open("three_test.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        return gpxs[index]

    def test_plot_exist_data(self):
        gpx = self.setUp(2)
        points = gpx.track.track_segment

        plot = Plotter(points)
        result = plot.setup()
        self.assertTrue(result)

    def test_plot_not_exist_data(self):
        gpx = self.setUp(1)
        points = gpx.track.track_segment

        plot = Plotter(points)
        result = plot.setup()
        self.assertFalse(result)

class RestoreConditionTestCase(unittest.TestCase):

    def test_empty_list(self):
        gpxs = None
        with open("restoretest0.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.assertTrue(len(gpxs) == 0)

    def test_single_list(self):
        benchmark_gpx = GPX()
        benchmark_gpx.track = Track()
        benchmark_gpx.set_describe("111")
        benchmark_gpx.set_name("test1")
        benchmark_gpx.set_time("1.01.2000")
        gpxs = None
        benchmark_gpxs = [benchmark_gpx]

        with open("restoretest1.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.assertTrue(len(gpxs) == len(benchmark_gpxs))
        self.assertTrue(gpxs[0] == benchmark_gpxs[0])

    def test_multi_list(self):
        benchmark_gpx = GPX()
        benchmark_gpx.track = Track()
        benchmark_gpx.set_describe("111")
        benchmark_gpx.set_name("test1")
        benchmark_gpx.set_time("1.01.2000")
        benchmark_gpxs = [benchmark_gpx]

        benchmark_gpx = GPX()
        benchmark_gpx.track = Track()
        benchmark_gpx.set_describe("222")
        benchmark_gpx.set_name("test2")
        benchmark_gpx.set_time("2.02.2000")

        benchmark_gpxs.append(benchmark_gpx)
        gpxs = None
        with open("restoretest2.pickle", 'rb') as f:
            gpxs = pickle.load(f)
        self.assertTrue(len(gpxs) == len(benchmark_gpxs))
        for i in range(len(gpxs)):
            self.assertTrue(gpxs[i] == benchmark_gpxs[i])
        
