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

beta_list = [0.99, 0.95] # Only 2 plants are simulated, assuming this is approximately one m**2
theta_c = np.array([3000, 20, 2.3e5]) # theta nominal clima
theta_p = np.array([0.7, 3.3, 0.25]) # theta nominal pdn


SHOW = True


""" Climate director"""

dir_climate = Climate_model()

""" Climate module"""
C1_rhs_ins = C1_rhs(constant_climate)
V1_rhs_ins = V1_rhs(constant_climate)
T1_rhs_ins = T1_rhs(constant_climate)
T2_rhs_ins = T2_rhs(constant_climate)
RHS_list = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
dir_climate.AddModule('ModuleClimate', Module1(Dt=1, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins))
dir_climate.sch += ['ModuleClimate']

""" Meteo module"""

""" 3.1 """
dir_climate.AddModule('RandomControl', Random(constant_control, Dt = minute2seconds(5)))
dir_climate.sch += ['RandomControl']


loader = Loader("Creating weather module").start()
meteo = ReadModule('weather_data/pandas_to_excel.xlsx', t_conv_shift=0.0, t_conv=1, shift_time=30)  # t_conv=1/(60*24) es para pasar el tiempo de minutos (como queda después de la lectura de la base) a días 
loader.stop()
dir_climate.AddModule('ModuleMeteo', meteo)
dir_climate.sch += ['ModuleMeteo']



""" Costs module"""
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

""""""

def PlantDirector( beta, return_Q_rhs_ins=False):
    """Build a Director to hold a Plant, with beta PAR parameter."""
    ### Start model with empty variables
    Dir = Director( t0=0.0, time_unit="", Vars={}, Modules={} )
    ## Create instances of RHS
    Ci_rhs_ins = Ci_rhs(constant_crop)
    Q_rhs_ins = Q_rhs(constant_crop)
    ## Add time information to the Director
    Dir.AddTimeUnit( Ci_rhs_ins.GetTimeUnits())
    Dir.AddTimeUnit( Q_rhs_ins.GetTimeUnits())
    ## Merger the variables of the modules in the Director
    Dir.MergeVarsFromRHSs( [Ci_rhs_ins, Q_rhs_ins], call=__name__)
    ### Add Modules to the Director:
    Dir.AddModule( "Plant", Plant(Q_rhs_ins, Dt_f=minute2seconds(1), Dt_g=day2seconds(1)))
    Dir.AddModule( "Photosynt", PhotoModule(Ci_rhs_ins), Dt=1)
    ## Scheduler for the modules
    Dir.sch = [ "Plant", "Photosynt" ] 

    if return_Q_rhs_ins:
        return Dir, Q_rhs_ins
    else:
        return Dir


"""Greenhouse director"""
director = Director(t0=0.0, time_unit="", Vars={}, Modules={})
#director.MergeVarsFromRHSs(RHS_list, call=__name__)
#director.AddModule('ModuleClimate', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, 
#                        T2=T2_rhs_ins))
director.MergeVars(dir_climate, all_vars=True)
director.AddDirectorAsModule('Climate', dir_climate)

director.PlantList = []
for p, beta in enumerate(beta_list):
    ### Make and instance of a Plant
    Dir = PlantDirector(beta=beta)
    
    ### Merge all ***global*** vars from plant
    director.MergeVars( [ Dir ], call=__name__)

    ### Add the corresponding time unit, most be the same in both
    director.AddTimeUnit(Dir.symb_time_unit)
    #Model.CheckSymbTimeUnits, all repeated instances of the Plant Director-Module 

    ### Add Plant directly, Dir.sch has been already defined
    director.AddDirectorAsModule( "Plant%d" % p, Dir)

    director.PlantList +=["Plant%d" % p]

director.sch += director.PlantList.copy()

#loader = Loader(mensaje).start()
breakpoint()
director.Run(Dt=hour2seconds(1),n=day2hour(7), sch=['Climate'],active=True)
#director.Run(Dt = 1,n=10, sch=['Climate'],active=True)
#loader.stop()

STATE_VARS = ['T1','T2','C1','V1']
CONTROLS  = ['U'+str(i) for i in range(1,12)] 
VARS = STATE_VARS + CONTROLS
PATH = create_path('simulation_results')
create_images(director,PATH = PATH)
create_pdf_images(PATH)