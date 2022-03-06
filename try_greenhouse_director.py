from pickle import TRUE
from re import S
from greenhouse.climate.module_climate import Module1
#from greenhouse.climate.qelec_rhs import Qelec_rhs
from parameters.climate_constants import CONSTANTS as constant_climate
from parameters.climate_constants import CONTROLS as constant_control
from greenhouse.climate.director import Climate_model
from greenhouse.climate.module_costs import ModuleCosts
from greenhouse.control.random_module import Random
from greenhouse.director import Greenhouse
from factory_of_rhs import*
from auxModMod.Dir import Director
from auxModMod.new_read_module import ReadModule
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from util import Loader
from utils.convert import day2seconds, hour2seconds, minute2seconds, day2minute,day2hour
from utils.graphics import create_images
from utils.create_folders import create_path
from utils.images_to_pdf import create_pdf_images
SHOW = True


""" 3. Climate director"""

dir_climate = Climate_model()

""" 3.1 Climate module"""
C1_rhs_ins = C1_rhs(constant_climate)
V1_rhs_ins = V1_rhs(constant_climate)
T1_rhs_ins = T1_rhs(constant_climate)
T2_rhs_ins = T2_rhs(constant_climate)
RHS_list = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
dir_climate.AddModule('ModuleClimate', Module1(Dt=1, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins))
dir_climate.sch += ['ModuleClimate']

""" 3.0 Meteo module"""

""" 3.1 """
dir_climate.AddModule('RandomControl', Random(constant_control, Dt = minute2seconds(5)))
dir_climate.sch += ['RandomControl']


loader = Loader("Creating weather module").start()
meteo = ReadModule('weather_data/pandas_to_excel.xlsx', t_conv_shift=0.0, t_conv=1, shift_time=30)  # t_conv=1/(60*24) es para pasar el tiempo de minutos (como queda después de la lectura de la base) a días 
loader.stop()
dir_climate.AddModule('ModuleMeteo', meteo)
dir_climate.sch += ['ModuleMeteo']



""" 3.2 Costs module"""
Qh2o_rhs_ins = Qh2o_rhs(constant_climate)
Qco2_rhs_ins = Qco2_rhs(constant_climate)
Qgas_rhs_ins = Qgas_rhs(constant_climate)
#Qelec_rhs_ins = Qelec_rhs(constanst_climate)
cost_list = [Qgas_rhs_ins, Qh2o_rhs_ins, Qco2_rhs_ins]#, Qelec_rhs_ins]
#dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
#dir_climate.AddModule('ModuleCosts', ModuleCosts(Dt=1, Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins))

#dir_climate.sch += ['ModuleCosts']

#dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
symb_time_units = C1_rhs_ins.CheckSymbTimeUnits(C1_rhs_ins)
# Genetare the director


"""Greenhouse director"""
director = Director(t0=0.0, time_unit="", Vars={}, Modules={})
#director.MergeVarsFromRHSs(RHS_list, call=__name__)
#director.AddModule('ModuleClimate', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, 
#                        T2=T2_rhs_ins))
director.MergeVars(dir_climate, all_vars=True)
director.AddDirectorAsModule('Climate', dir_climate)


#loader = Loader(mensaje).start()

director.Run(Dt=hour2seconds(1),n=day2hour(7), sch=['Climate'],active=True)
#director.Run(Dt = 1,n=10, sch=['Climate'],active=True)
#loader.stop()

STATE_VARS = ['T1','T2','C1','V1']
CONTROLS  = ['U'+str(i) for i in range(1,12)] 
VARS = STATE_VARS + CONTROLS
PATH = create_path('simulation_results')
create_images(director,PATH = PATH)
create_pdf_images(PATH)