class Struct_weather():
    def __init__(self,orig_name,units = 1,new_name=None,sheet=None,obs = 'ok'):
        self.orig_name = orig_name
        self.units     = units
        self.new_name  = orig_name if new_name == None else new_name
        self.sheet     = sheet
        self.obs       = obs

    def verbose(self):
        print(self.__dict__)


