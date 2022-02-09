import numpy as np
import pandas as pd
import numpy as np
from time import time
import matplotlib.pyplot as plt
from director_climate.dir_climate import Climate_model
#from director_production import I_2, Production_model
from ModMod import Director


class Greenhouse(Director):
    def __init__(self, controls_dir):
        super().__init__(t0=0.0, time_unit="", Vars={}, Modules={})
        climate_dir = Climate_model()
        production_dir = Production_model()
        self.AddDirectorAsModule("Controls_Dir", controls_dir)
        self.AddDirectorAsModule("Climate_Dir", climate_dir)
        self.AddDirectorAsModule("Production_Dir", production_dir)


        self.sch = ["Controls_Dir", "Climate_Dir", "Production_Dir"] , # Photosintesis_Dir]
        #self.MergeVarsFromRHSs
        #self.AddTimeUnit(Dir.symb_time_unit)

    def Scheduler(self, t1, sch):
        #return super().Scheduler(t1, sch)
        pass


    def Run(self, Dt, n, sch, save=None):
        #return super().Run(Dt, n, sch, save)
        pass


    def reset(self):
        self.V_Set('<nombre>', valor) # -> cualquier variable que no sea constante

    def step(self, action):
        pass

    def reward(self, state, action):
        pass

