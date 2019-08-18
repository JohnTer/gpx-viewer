from PyQt5 import QtWidgets
from length_slopes import CounterSteepnessLengthSlopes
from gpxworker.gpx import Track


class SignClassificationSlopes(object):
    def __init__(self, **kwargs):
        self.init()
        self.module_name = "sign_classification_slopes"
        self.txtwidget = None
    def init(self):
        self.table_steepness_length_slopes = [CounterSteepnessLengthSlopes(40,50,600,0),
                                        CounterSteepnessLengthSlopes(50,60,450,1),
                                        CounterSteepnessLengthSlopes(60,70,350,2),
                                        CounterSteepnessLengthSlopes(70,80,300,3),
                                        CounterSteepnessLengthSlopes(80,4294967295,270,4),
                                       ]


    def add_steepness_one(self, name):
        N = len(self.table_steepness_length_slopes)
        for i in range(N):
            if name == self.table_steepness_length_slopes[i].name:
                self.table_steepness_length_slopes[i].add_one()
                break
                    
    def check_steepness_slopes(self, tangens):
        N = len(self.table_steepness_length_slopes)
        name = None
        for i in range(N):
            result, name = self.table_steepness_length_slopes[i].belong_tangens(tangens)
            if result:
                break
        return name

    def check_length_slopes(self, name, length):
        N = len(self.table_steepness_length_slopes)
        result = False
        for i in range(N):
            if name == self.table_steepness_length_slopes[i].name:
                if self.table_steepness_length_slopes[i].belong_length(length):
                    result = True
                else:
                    result = False
                break
        return result

    def classify(self, track_segment):
        past_name = None
        N = len(track_segment)
        length = 0
        for i in range(N-1):
            start = track_segment[i]
            stop = track_segment[i+1]
            if start.ele == None or stop.ele == None:
                return False
            tangens = Track.angle_from_points(None, start, stop, True) * 100 #проценты
            name_steepness = self.check_steepness_slopes(tangens)


            if name_steepness != past_name:
                if past_name is None:
                    past_name = name_steepness
                    continue

                if self.check_length_slopes(name_steepness,length):
                    self.add_steepness_one(name_steepness)

                length = 0
                past_name = name_steepness
            else:
                length += Track.distance_from_points(None, start, stop) * 1000
        return True


    def accept(self, visitor):
        visitor.visit(self)

    def ui_init(self, main_window, butt_handler):
        main_window.button_start1 = QtWidgets.QPushButton("Количество знаков",main_window)
        main_window.button_start1.setGeometry(1020,180,140,30)
        main_window.text_edit1 = QtWidgets.QTextEdit(main_window)
        self.txtwidget = main_window.text_edit1
        main_window.text_edit1.setGeometry(850,150,150,100)
        main_window.text_edit1.setReadOnly(True)
        main_window.button_start1.clicked.connect(lambda: butt_handler(self.module_name))

    def update_mess(self):
        mess = "Типы знаков: \n"
        for x in self.table_steepness_length_slopes:
            mess += "Уклон %d: %d \n" % (x.tangens_from, x.count)
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



class EModule(SignClassificationSlopes):
    def __init__(self):
        super().__init__()