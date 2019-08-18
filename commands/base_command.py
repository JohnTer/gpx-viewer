class Command(object):
	def execute(self):
		raise NotImplementedError()
	def cancel(self):
		raise NotImplementedError()		


class RmCommand(Command):
    def __init__(self,index,datalist,type):
        self.datalist = datalist
        self.index = index
        self.rows = [] 
        self.type = type

    def execute(self):
        self.working_data()
    def cancel(self):
        self.restore_data()

    def working_data(self):
        self.object = self.datalist[self.index]
        del self.datalist[self.index]

    def restore_data(self):
        self.datalist.insert(self.index,self.object)

class AddCommand(Command):
    def __init__(self,row, datalist, row_index,type):
        self.datalist = datalist
        self.index = row_index
        self.type = type

    def cancel(self):
        self.__restore_data()

    def __restore_data(self):
        del self.datalist[self.index]



class CngCommand(Command):
    def __init__(self,i,j,type):
        self.i_index = i
        self.j_index = j
        self.type = type