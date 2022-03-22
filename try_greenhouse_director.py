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
from ModMod import ReadModule # auxModMod.new_read_module
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from util import Loader
from utils.convert import day2seconds, hour2seconds, minute2seconds, day2minute,day2hour
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
dir_climate.Dt = minute2seconds(5)

""" Climate module"""
C1_rhs_ins = C1_rhs(constant_climate)
V1_rhs_ins = V1_rhs(constant_climate)
T1_rhs_ins = T1_rhs(constant_climate)
T2_rhs_ins = T2_rhs(constant_climate)
RHS_list = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
dir_climate.AddModule('ModuleClimate', Module1(Dt=minute2seconds(1), C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins))


""" Meteo module"""

""" 3.1 """
dir_climate.AddModule('Control', Random(constant_control, Dt = minute2seconds(5)))



loader = Loader("Creating weather module").start()
#'weather_data/pandas_to_excel.xlsx'
meteo = ReadModule('Módulos_Juntos/Read_Inputs_inf.xls', t_conv_shift=0.0, t_conv=1)#, shift_time=30)  # t_conv=1/(60*24) es para pasar el tiempo de minutos (como queda después de la lectura de la base) a días 
loader.stop()
dir_climate.AddModule('ModuleMeteo', meteo)




""" Costs module"""
Qh2o_rhs_ins = Qh2o_rhs(constant_climate)
Qco2_rhs_ins = Qco2_rhs(constant_climate)
Qgas_rhs_ins = Qgas_rhs(constant_climate)
#Qelec_rhs_ins = Qelec_rhs(constanst_climate)
cost_list = [Qgas_rhs_ins, Qh2o_rhs_ins, Qco2_rhs_ins]#, Qelec_rhs_ins]
dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
dir_climate.AddModule('ModuleCosts', ModuleCosts(Dt=minute2seconds(1), Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins))


dir_climate.sch = ['ModuleMeteo','ModuleClimate','Control','ModuleCosts']
#dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
symb_time_units = C1_rhs_ins.CheckSymbTimeUnits(C1_rhs_ins)
# Genetare the director
from sympy import symbols
from ModMod import StateRHS
s, mol_CO2, mol_air, mol_phot, m, d, C, g, mol_O2, pa, ppm = symbols('s mol_CO2 mol_air mol_phot m d C g mol_O2 pa ppm')
mu_mol_CO2 = 1e-6 * mol_CO2
mu_mol_phot = 1e-6 * mol_phot
mu_mol_O2 = 1e-6 * mol_O2
mg = 1e-3*g
## Growth model

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
    Dir.AddModule( "Plant", Plant(beta, Q_rhs_ins, Dt_f=minute2seconds(1), Dt_g=day2seconds(1)))
    Dir.AddModule( "Photosynt", PhotoModule(Ci_rhs_ins, Dt=minute2seconds(1)))
    ## Scheduler for the modules
    Dir.sch = ["Photosynt", "Plant"] 

    if return_Q_rhs_ins:
        return Dir, Q_rhs_ins
    else:
        return Dir


"""Greenhouse director"""
director = Greenhouse()
director.MergeVarsFromRHSs(RHS_list, call=__name__)
#director.AddModule('ModuleClimate', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, 
#                        T2=T2_rhs_ins))
director.MergeVars(dir_climate, all_vars=True)
director.AddDirectorAsModule('Climate', dir_climate)

director.sch = ['Climate']

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
director.Run(Dt=day2seconds(1),n=1, sch=director.sch) #,active=True)
#director.Run(Dt = 1,n=10, sch=['Climate'],active=True)
#loader.stop()
PATH = create_path('simulation_results')
create_images(director, 'Climate', PATH = PATH)
create_pdf_images(PATH)
print(PATH)
''' Amilkar's version
dicc_all = {'CONSTANTS':constant_climate, 'INPUTS':INPUTS, 'CONTROLS':CONTROLS, 'OTHER_CONSTANTS':OTHER_CONSTANTS, 'STATE_VARS':STATE_VARS}
Constants(dic_constants=dicc_all,PATH = PATH)
create_images(director, PATH = PATH)
create_pdf_images(PATH)
'''
