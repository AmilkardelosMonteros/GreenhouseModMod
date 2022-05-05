from importlib.resources import path


def set_train(dir):
    #dir.Modules['Climate'].Modules['ModuleClimate'].train    = True
    #dir.Modules['Climate'].Modules['ModuleClimate'].noise.on = True
    dir.train    = True
    dir.noise.on = True

def set_simulation(dir):
    #dir.Modules['Climate'].Modules['ModuleClimate'].train    = False
    #dir.Modules['Climate'].Modules['ModuleClimate'].noise.on = False
    dir.true     = False
    dir.noise.on = False

def save_nets(dir,PATH,i):
    print('Guardando red' + str(i))
    #dir.Modules['Climate'].Modules['ModuleClimate'].agent.save(path = PATH, name = str(i))
    dir.agent.save(path = PATH, name = str(i))

def set_index(dir,index_):
    dir.Modules['Climate'].Modules['ModuleMeteo'].shift_time = index_
