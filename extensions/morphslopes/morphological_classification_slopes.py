from copy import deepcopy
from PyQt5 import QtWidgets
from gpxworker.gpx import Track

class TableSteepnessSlopes(object):
    def __init__(self, angle_from, angle_to, name):
        self.angle_from = angle_from
        self.angle_to = angle_to
        self.name = name
    def belong(self, angle):
        if self.angle_from <= abs(angle) < self.angle_to:
            return True, self.name
        else:
            return False, None

class TableLengthSlopes(object):
    def __init__(self, len_from, len_to, name):
        self.len_from = len_from
        self.len_to = len_to
        self.name = name

    def belong(self, length):
        if self.len_from <= length < self.len_to:
            return True, self.name
        else:
            return False, None

class CounterLengthSlopes(TableLengthSlopes):
    def __init__(self, angle_from, angle_to, name):
        super().__init__(angle_from, angle_to, name)
        self.count = 0
    def add_one(self):
        self.count += 1


class CounterSteepnessSlopes(TableSteepnessSlopes):
    def __init__(self, angle_from, angle_to, name):
        super().__init__(angle_from, angle_to, name)
        self.count = 0
        self.length_slopes_list = None

    def set_slopes_list(self, slopes_list):
        self.length_slopes_list = deepcopy(slopes_list)

    def add_length_one(self, name):
        N = len(self.length_slopes_list)
        for i in range(N):
            if name == self.length_slopes_list[i].name:
                self.length_slopes_list[i].add_one()
                break

    def add_one(self, name):
        self.add_length_one(name)
        self.count += 1

class MorphologicalClassificationSlopes():
    def __init__(self, **kwargs):
        self.init()
        self.module_name = "morphological_classification_slopes"
        self.txtwidget = None
    def init(self):
        self.table_steepness_slopes = [CounterSteepnessSlopes(2,4,"очень пологие"),
                                       CounterSteepnessSlopes(4,8,"пологие"),
                                       CounterSteepnessSlopes(8,15,"склоны средней крутизные"),
                                       CounterSteepnessSlopes(15,35,"крутые"),
                                       CounterSteepnessSlopes(35,90,"очень крутые"),
                                       ]

        self.table_length_slopes = [CounterLengthSlopes(0,50,"короткие склоны"),
                                       CounterLengthSlopes(50,500,"склоны средней длины"),
                                       CounterLengthSlopes(500,4294967295,"длинные"),
                                       ]

        for i in range(len(self.table_steepness_slopes)):
            self.table_steepness_slopes[i].set_slopes_list(self.table_length_slopes)


    def check_steepness_slopes(self, angle):
        N = len(self.table_steepness_slopes)
        name = None
        for i in range(N):
            result, name = self.table_steepness_slopes[i].belong(angle)
            if result:
                break
        return name

    def get_length_name(self, length):
        N = len(self.table_length_slopes)
        for i in range(N):
            result, name = self.table_length_slopes[i].belong(length)
            if result:
                return name

    def add_steepness_one(self, name_steepness, name_length):
        N = len(self.table_steepness_slopes)
        for i in range(N):
            if name_steepness == self.table_steepness_slopes[i].name:
                self.table_steepness_slopes[i].add_one(name_length)
                break

    def classify(self, track_segment):   
        past_name = None
        N = len(track_segment)
        length = 0
        for i in range(N-1):
            start = track_segment[i]
            stop = track_segment[i+1]
            if start.ele == None or stop.ele == None:
                return False
            angle = Track.angle_from_points(None, start, stop)
            name_steepness = self.check_steepness_slopes(angle)
            if name_steepness != past_name:
                if past_name is None:
                    past_name = name_steepness
                    continue
                name_length = self.get_length_name(length)
                self.add_steepness_one(name_steepness, name_length)
                length = 0
                past_name = name_steepness
            else:
                length += Track.distance_from_points(None, start, stop) * 1000
        return True
    
    def ui_init(self, main_window, butt_handler):
        main_window.button_start2 = QtWidgets.QPushButton("Уклоны по категориям",main_window)
        main_window.button_start2.setGeometry(1080,290,140,30)
        main_window.text_edit2 = QtWidgets.QTextEdit(main_window)
        self.txtwidget = main_window.text_edit2 
        main_window.text_edit2.setGeometry(850,260,200,100)
        main_window.text_edit2.setReadOnly(True)
        main_window.button_start2.clicked.connect(lambda: butt_handler(self.module_name))

    def update_mess(self):
        mess = "Типы спусков/подъемов: \n"
        for x in self.table_steepness_slopes:
            mess += " %s: %d \n" % (x.name,x.count)
            for y in x.length_slopes_list:
                mess += "      %s : %d\n" % (y.name, y.count)
            mess += "\n\n"
        return mess
    def run(self, track_segment):
        self.init()
        mess = ""
        result = self.classify(track_segment)
        if result:
            mess = self.update_mess()
        else:
            mess = "Отсутствуют данные о высоте!"
        self.txtwidget.setText(mess)

    def accept(self, visitor):
        visitor.visit(self)


class EModule(MorphologicalClassificationSlopes):
    def __init__(self):
        super().__init__()



