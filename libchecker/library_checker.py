import sys

class LibraryChecker(object):
    def __init__(self, modules_list, egg_path = None):
        self.modules_list = modules_list
        self.loaded_modules = []
        self.name_loaded_modules = []     
        if egg_path is None:
            self.base_path = 'C:\\Python36\\eggs\\'
        else:
            self.base_path = egg_path
             
    def load_modues(self):
        for modules in self.modules_list:
            try:
                egg_path = self.base_path + '%s.egg\\' % modules
                sys.path.append(egg_path)
                mod = __import__(modules)
                self.name_loaded_modules.append(modules)
                self.loaded_modules.append(mod)
            except ImportError:
                print("Нет модуля (.egg) %s" % modules)
        return self.loaded_modules, self.name_loaded_modules



