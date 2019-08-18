
class TableSteepnessLengthSlopes(object):
    def __init__(self, tangens_from, tangens_to, length, name):
        self.tangens_from = tangens_from
        self.tangens_to = tangens_to
        self.name = name
        self.minlength = length
    def belong_tangens(self, angle):
        if (self.tangens_from <= abs(angle) < self.tangens_to):
            return True, self.name
        else:
            return False, None

    def belong_length(self, length):
        if (length > self.minlength):
            return True
        else:
            return False

class CounterSteepnessLengthSlopes(TableSteepnessLengthSlopes):
    def __init__(self, angle_from, angle_to, minlength,name):
        super().__init__(angle_from, angle_to,minlength, name)
        self.count = 0
    def add_one(self):
        self.count += 1



