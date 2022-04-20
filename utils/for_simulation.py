def set_train(dir):
    dir.Modules['Climate'].Modules['ModuleClimate'].train    = True
    dir.Modules['Climate'].Modules['ModuleClimate'].noise.on = True

def set_simulation(dir):
    dir.Modules['Climate'].Modules['ModuleClimate'].train    = False
    dir.Modules['Climate'].Modules['ModuleClimate'].noise.on = False
