from pickle import TRUE
from re import S
from greenhouse.climate.module_climate import Module1
#from greenhouse.climate.qelec_rhs import Qelec_rhs
from parameters.climate_constants import CONSTANTS as constant_climate
from parameters.climate_constants import CONTROLS as constant_control
from parameters.crop_contants import CONSTANTS as constant_crop
from greenhouse.climate.director import Climate_model
from greenhouse.climate.module_costs import ModuleCosts
from greenhouse.control.random_module import Random
from greenhouse.crop.ci_rhs import Ci_rhs
from greenhouse.crop.q_rhs import Q_rhs
from greenhouse.crop.module_photo import PhotoModule
from greenhouse.crop.module_plant import Plant
from greenhouse.director import Greenhouse
from factory_of_rhs import*
from auxModMod.Dir import Director
from auxModMod.new_read_module import ReadModule
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from util import Loader
from utils.convert import day2seconds, hour2seconds, minute2seconds, day2minute,day2hour,hour2minute
from utils.graphics import create_images
from utils.create_folders import create_path
from utils.images_to_pdf import create_pdf_images
from reports.report_constants import Constants
from parameters.climate_constants import INPUTS, CONTROLS, OTHER_CONSTANTS, STATE_VARS

beta_list = [0.99, 0.95] # Only 2 plants are simulated, assuming this is approximately one m**2
theta_c = np.array([3000, 20, 2.3e5]) # theta nominal clima
theta_p = np.array([0.7, 3.3, 0.25]) # theta nominal pdn


""" Climate director"""

dir_climate = Climate_model()
#dir_climate.Dt = minute2seconds(5) # minutos

""" Climate module"""
C1_rhs_ins = C1_rhs(constant_climate)
V1_rhs_ins = V1_rhs(constant_climate)
T1_rhs_ins = T1_rhs(constant_climate)
T2_rhs_ins = T2_rhs(constant_climate)
RHS_list = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
dir_climate.AddModule('ModuleClimate', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins))

meteo = ReadModule('weather_data/pandas_to_excel.xlsx', t_conv_shift=0.0, t_conv=1, shift_time=0) 
dir_climate.AddModule('ModuleMeteo', meteo)
dir_climate.AddModule('Control', Random(constant_control))

Qh2o_rhs_ins = Qh2o_rhs(constant_climate)
Qco2_rhs_ins = Qco2_rhs(constant_climate)
Qgas_rhs_ins = Qgas_rhs(constant_climate)
#Qelec_rhs_ins = Qelec_rhs(constanst_climate)
cost_list = [Qgas_rhs_ins, Qh2o_rhs_ins, Qco2_rhs_ins]#, Qelec_rhs_ins]
dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
dir_climate.AddModule('ModuleCosts', ModuleCosts(Dt=60, Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins))
dir_climate.sch = list(dir_climate.Modules.keys()) 
director = Greenhouse()
director.MergeVarsFromRHSs(RHS_list, call=__name__)
director.MergeVars(dir_climate, all_vars=True)
director.AddDirectorAsModule('Climate', dir_climate)

director.sch = ['Climate']

director.Run(60*60,24*4,director.sch)
#Dt de Director = 1440 (numero de minutos en un dia)
#Dt de Director clima = 60, 1440/60 = 24 numero de registros de clima * n
variables = list(director.Vars.keys())
Data = pd.DataFrame(columns=variables)
for v in variables:
    try:
        Data[v] = director.OutVar(v)
    except:
        pass

variables = list(director.Vars.keys())
Data1 = pd.DataFrame(columns=variables)
for v in variables:
    try:
        Data1[v] = director.OutVar(v)
    except:
        pass

PATH = create_path('simulation_results')
Data.to_csv(PATH+'/output/' + 'VariablesClimate.csv',index=0)
Data1.to_csv(PATH+'/output/' + 'VariablesDir.csv',index=0)
create_images(director, 'Climate' ,PATH = PATH)
print(PATH)

