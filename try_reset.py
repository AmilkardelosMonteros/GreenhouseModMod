from ast import Name
from pickle import TRUE
from re import S
from greenhouse.climate.module_climate import Module1
#from greenhouse.climate.qelec_rhs import Qelec_rhs
from parameters.climate_constants import CONSTANTS as constant_climate
from parameters.climate_constants import CONTROLS as constant_control
from parameters.crop_contants import CONSTANTS as constant_crop
from greenhouse.climate.director import Climate_model
from greenhouse.crop.ci_rhs import Ci_rhs
from greenhouse.crop.q_rhs import Q_rhs
from greenhouse.crop.module_photo import PhotoModule
from greenhouse.crop.module_plant import Plant
from greenhouse.director import Greenhouse
from factory_of_rhs import*
from ModMod import Director
from ModMod import ReadModule
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from util import Loader
from utils.convert import get_dt_and_n
from utils.convert import day2seconds, hour2seconds, minute2seconds, day2minutes,day2hours,hour2minutes
from utils.graphics import create_images, create_images_per_module
from utils.create_folders import create_path
from utils.images_to_pdf import create_pdf_images
from reports.report_constants import Constants
from parameters.climate_constants import INPUTS, CONTROLS, OTHER_CONSTANTS, STATE_VARS
#Para el entrenamiento
from try_ddpg import agent
from try_noise import noise
from utils.for_simulation import set_simulation
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

#Cost
Qh2o_rhs_ins  = Qh2o_rhs(constant_climate)
Qco2_rhs_ins  = Qco2_rhs(constant_climate)
Qgas_rhs_ins  = Qgas_rhs(constant_climate)
Qelec_rhs_ins = Qelec_rhs(constant_climate)

RHS_list  = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
RHS_list += [Qgas_rhs_ins, Qh2o_rhs_ins, Qco2_rhs_ins, Qelec_rhs_ins]
dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
dir_climate.AddModule('ModuleClimate', Module1(agent,noise,Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins,Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins,Qelec = Qelec_rhs_ins))

meteo = ReadModule('weather_data/pandas_to_excel.xlsx', t_conv_shift=0.0, t_conv=1)#, shift_time=0) 
dir_climate.AddModule('ModuleMeteo', meteo)
#dir_climate.AddModule('Control', Random(constant_control))


#Qelec_rhs_ins = Qelec_rhs(constanst_climate)

#dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
#dir_climate.AddModule('ModuleCosts', ModuleCosts(Dt=3600, Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins))
dir_climate.sch = list(dir_climate.Modules.keys()) 
director = Greenhouse()
director.MergeVarsFromRHSs(RHS_list, call=__name__)
director.MergeVars(dir_climate, all_vars=True)
director.AddDirectorAsModule('Climate', dir_climate)
from sympy import symbols
from ModMod import StateRHS
s, mol_CO2, mol_air, mol_phot, m, d, C, g, mol_O2, pa, ppm = symbols('s mol_CO2 mol_air mol_phot m d C g mol_O2 pa ppm')
mu_mol_CO2 = 1e-6 * mol_CO2
mu_mol_phot = 1e-6 * mol_phot
mu_mol_O2 = 1e-6 * mol_O2
mg = 1e-3*g
n_f, n_p, MJ = symbols('n_f n_p MJ') # number of fruits, number of plants
## Climate model
# C1
mt, mg, m, C, s, W, mg_CO2, Joule, g, mol_CH2O = symbols('mt mg m C s W mg_CO2 Joule g mol_CH2O')
# V1
mt, mg, m, C, s, W, mg_CO2, Joule, Pa, kg_water, kg, K, ppm, kmol, kg_air, kg_vapour = symbols('mt mg m C s W mg_CO2 Joule Pa kg_water kg K ppm kmol kg_air kg_vapour')
# T1
mt, mg, m, C, s, W, mg_CO2, Joule, Pa, kg_water, kg, K, ppm = symbols('mt mg m C s W mg_CO2 Joule Pa kg_water kg K ppm')
# T2
mt, mg, m, C, s, W, mg_CO2, Joule, Pa, kg_water, kg, K, ppm, m_cover, kg_air = symbols('mt mg m C s W mg_CO2 Joule Pa kg_water kg K ppm m_cover kg_air')


def PlantDirector( beta, return_Q_rhs_ins=False):
    """Build a Director to hold a Plant, with beta PAR parameter."""
    ### Start model with empty variables
    Dir = Director( t0=0.0, time_unit="", Vars={}, Modules={} )
    ## Create instances of RHS
    Ci_rhs_ins = Ci_rhs()#constant_crop)
    Q_rhs_ins = Q_rhs()#constant_crop)
    ## Add time information to the Director
    Dir.AddTimeUnit( Ci_rhs_ins.GetTimeUnits())
    Dir.AddTimeUnit( Q_rhs_ins.GetTimeUnits())
    ## Merger the variables of the modules in the Director
    Dir.MergeVarsFromRHSs( [Ci_rhs_ins, Q_rhs_ins], call=__name__)
    ### Add Modules to the Director:
    Dir.AddModule( "Plant", Plant(beta, Q_rhs_ins, Dt_f=minute2seconds(30), Dt_g=minute2seconds(30)))
    Dir.AddModule( "Photosynt", PhotoModule(Ci_rhs_ins, Dt=60))
    ## Scheduler for the modules
    Dir.sch = ["Photosynt","Plant"] # 

    if return_Q_rhs_ins:
        return Dir, Q_rhs_ins
    else:
        return Dir


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

director.sch = ['Climate']
director.sch += director.PlantList.copy()
from parameters.parameters_dir import PARAMS_DIR

Dt, n = get_dt_and_n(minute=PARAMS_DIR['minutes'], days=PARAMS_DIR['days'])
director.Dt = Dt
director.n = n 



from keeper import keeper
from parameters.parameters_ddpg import CONTROLS
ACTIVE_CONTROLS = list()
for k,v in CONTROLS.items(): 
    if v:
        ACTIVE_CONTROLS.append(k)


#set_simulation(director)
Keeper = keeper()

episodes = 3
y = np.array([])
for i in range(episodes):
    director.Run(director.Dt, director.n, director.sch,active=True)
    x = director.OutVar('Qco2')
    y = np.concatenate([y, x])
    director.Reset()

plt.plot(y)
plt.show()