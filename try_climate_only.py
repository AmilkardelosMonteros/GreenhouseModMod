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
from parameters.modelo_fotosintesis import MODELO_FOTOSINTESIS
from parameters.parameters_env import PARAMS_ENV, PARAMS_TRAIN
#Para el entrenamiento
from try_ddpg import agent
from try_noise import noise
from utils.for_simulation import set_simulation,save_nets,set_index
from read_dates import  create_date,compute_indexes,get_indexes

from sympy import symbols
from ModMod import StateRHS
from parameters.parameters_dir import PARAMS_DIR

from keeper import keeper
from parameters.parameters_ddpg import CONTROLS
from save_parameters import save
ACTIVE_CONTROLS = [k for k,v in CONTROLS.items() if v]

beta_list = [0.99, 0.95] # Only 2 plants are simulated, assuming this is approximately one m**2
theta_c = np.array([3000, 20, 2.3e5]) # theta nominal clima
theta_p = np.array([0.7, 3.3, 0.25]) # theta nominal pdn
dicc_all = {'CONSTANTS':constant_climate, 'INPUTS':INPUTS, 'OTHER_CONSTANTS':OTHER_CONSTANTS, 'STATE_VARS':STATE_VARS}
PATH = create_path('simulation_results')
from reports.report_constants import Constants
Constants(dicc_all,PATH)


""" Climate director"""

dir_climate = Climate_model()
#dir_climate.Dt = minute2seconds(5) # minutos

""" Climate module"""
C1_rhs_ins = C1_rhs(MODELO_FOTOSINTESIS,constant_climate)
V1_rhs_ins = V1_rhs(constant_climate)
T1_rhs_ins = T1_rhs(constant_climate)
T2_rhs_ins = T2_rhs(constant_climate)
T3_rhs_ins = T3_rhs(constant_climate)

#Cost
Qh2o_rhs_ins  = Qh2o_rhs(constant_climate)
Qco2_rhs_ins  = Qco2_rhs(constant_climate)
Qgas_rhs_ins  = Qgas_rhs(constant_climate)
Qelec_rhs_ins = Qelec_rhs(constant_climate)

#Control
U7_rhs_ins = U7_rhs(constant_climate)
U6_rhs_ins = U6_rhs(constant_climate)

RHS_list  = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins,T3_rhs_ins]
RHS_list += [Qgas_rhs_ins, Qh2o_rhs_ins, Qco2_rhs_ins, Qelec_rhs_ins]

if CONTROLS['U6_c'] and not CONTROLS['U7_c']:
    print('primer condicion')
    RHS_list += [U6_rhs_ins]
    dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
    dir_climate.AddModule('ModuleClimate', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins, T3=T3_rhs_ins, Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins,Qelec = Qelec_rhs_ins,U6 = U6_rhs_ins))
    #El key de arriba tiene que coincidir con el nombre de la variable

if not CONTROLS['U6_c'] and CONTROLS['U7_c']:
    print('segundo condicion')
    RHS_list += [U7_rhs_ins]
    dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
    dir_climate.AddModule('ModuleClimate', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins, T3=T3_rhs_ins, Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins,Qelec = Qelec_rhs_ins, U7 = U7_rhs_ins))
    #El key de arriba tiene que coincidir con el nombre de la variable

if CONTROLS['U6_c'] and CONTROLS['U7_c']:
    print('tercer condicion')
    RHS_list += [U7_rhs_ins,U6_rhs_ins]
    dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
    dir_climate.AddModule('ModuleClimate', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins,T3=T3_rhs_ins,Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins,Qelec = Qelec_rhs_ins, U7 = U7_rhs_ins,U6 = U6_rhs_ins))
    #El key de arriba tiene que coincidir con el nombre de la variable

if not CONTROLS['U6_c'] and not CONTROLS['U7_c']:
    print('Ultimo condicional')
    dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
    dir_climate.AddModule('ModuleClimate', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins,T3=T3_rhs_ins,Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins,Qelec = Qelec_rhs_ins))
    #el key de arriba tiene que coincidir con el nombre de la variable

mensaje = "Leyendo datos"
loader = Loader(mensaje).start()
meteo = ReadModule('weather_data/pandas_to_excel.xlsx', t_conv_shift=0.0, t_conv=1)#, shift_time=0) #Este es el codigo correcto!!!
#meteo = ReadModule('weather_data/excel_holanda.xlsx', t_conv_shift=0.0, t_conv=1)#, shift_time=0) 
dir_climate.AddModule('ModuleMeteo', meteo)
loader.stop()
#dir_climate.AddModule('Control', Random(constant_control))


#Qelec_rhs_ins = Qelec_rhs(constanst_climate)

#dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
#dir_climate.AddModule('ModuleCosts', ModuleCosts(Dt=3600, Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins))
dir_climate.sch = list(dir_climate.Modules.keys())
director = Greenhouse(agent, noise)
director.MergeVarsFromRHSs(RHS_list, call=__name__)
director.MergeVars(dir_climate, all_vars=True)
director.AddDirectorAsModule('Climate', dir_climate)
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
Bmt, mg, m, C, s, W, mg_CO2, Joule, Pa, kg_water, kg, K, ppm = symbols('mt mg m C s W mg_CO2 Joule Pa kg_water kg K ppm')
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
    Dir.AddModule( "Photosynt", PhotoModule(Ci_rhs_ins, modelo = MODELO_FOTOSINTESIS, Dt=60))
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


Dt, n = get_dt_and_n(minute=PARAMS_DIR['minutes'], days=PARAMS_DIR['days'])


director.Dt      = Dt
director.n       = n
director.type    = PARAMS_TRAIN['TYPE']
SEASON           = PARAMS_DIR['season']
INDEXES          = get_indexes()
limit            = INDEXES['limit']
INDEXES_FOR_TEST = INDEXES['TEST']
INDEXES          = INDEXES[SEASON]
if max(INDEXES) < limit:
    print('Los indices estan bien calculados')

vars_to_plot  = ['T1','T2','V1','C1','I5','H','NF']
vars_to_plot += ['U' + str(i) for i in range(1,13)]


save(PATH) #Save all parameters of the enviroment
###############################################
path_net = PARAMS_TRAIN['PATH_NET']
name_net = PARAMS_TRAIN['NET']
if path_net is not None:
    print('Cargando red '+ name_net + ' del folder '+ path_net)
    director.agent.load('simulation_results/'+path_net, name=name_net)


#TRAIN
Keeper         = keeper()
episodes       = PARAMS_TRAIN['EPISODES']
specialization = PARAMS_TRAIN['SPECIALIZATION_PERIOD']
active         = not(PARAMS_TRAIN['SERVER'])
if episodes + specialization > 0:
    for i in range(episodes + specialization):
        index1 = np.random.choice(INDEXES,size=1)[0] 
        print('Indice = ', index1)
        director.Reset()
        set_index(director,index1)
        print('sigma = ', director.noise.sigma)
        director.Run(director.Dt, director.n, director.sch,active=active)
        if i%PARAMS_TRAIN['SAVE_FREQ'] == 0: save_nets(director,PATH=PATH,i=i)
        Keeper.add(director)
        Keeper.save(PATH)
        director.agent.save_losses(PATH)
        director.agent.save_real_changes(PATH)
        director.noise.reset()
        print('max sigma = ',director.noise.max_sigma)
        print('sigma = ',director.noise.sigma)
    Keeper.plot_cost(PATH=PATH)
    Keeper.plot_rewards(PATH=PATH)
    Keeper.plot_actions(ACTIVE_CONTROLS,PATH=PATH)
    Keeper.plot_rewards(PATH=PATH)

if episodes + specialization > 0:
    date = create_date(index1)
    frec = Dt/director.Modules['Climate'].Modules['ModuleClimate'].Dt ###Si o si debe estar en minutos
    dates = compute_indexes(date,n,frec)
    vars_to_plot  = ['T1','T2','V1','C1','H','NF']
    vars_to_plot += ['U' + str(i) for i in range(1,13)]
    create_images(director,'Climate',dates,vars_to_plot, PATH = PATH,train=True)

###TEST

Keeper_for_test = keeper()
set_simulation(director)
FLAG = 'test'
import random
#random.seed(1999)
random.seed(3000)
for _ in range(PARAMS_TRAIN['N_TEST']):
    index1 = INDEXES_FOR_TEST[_]
    print('Indice = ', index1)
    director.Reset()
    director.t = 0
    RHSs_ids = director.Modules['Climate'].Modules['ModuleMeteo'].Assigm_S_RHS_ids
    director.Modules['Climate'].Modules['ModuleMeteo'].input_vars['time_index'] = [0]*len(RHSs_ids)
    set_index(director,index1)
    director.Run(director.Dt, director.n, director.sch,active=active)
    Keeper_for_test.add(director)
    Keeper_for_test.save(PATH,flag = 'test')
    director.noise.reset()
Keeper_for_test.plot_cost(FLAG,PATH=PATH)
Keeper_for_test.plot_rewards(FLAG,PATH=PATH)
Keeper_for_test.plot_gains(FLAG,PATH=PATH)
Keeper_for_test.plot_actions(ACTIVE_CONTROLS,FLAG,PATH=PATH)

variables = ['T1','T2','V1','C1','VPD','RH','I5','I8','I2','I11','U1','U2','U3','U4','U5','U6_c','U7_c','U8','U9','U10','U11','U12','H','NF','reward']
info = [director.OutVar(var) for var in variables]
date = create_date(index1)

frec = Dt/director.Modules['Climate'].Modules['ModuleClimate'].Dt ###Si o si debe estar en minutos
dates = compute_indexes(date,n,frec)
data = pd.DataFrame(columns = variables)
#data['date'] = dates
#data.to_csv(PATH+'/output/' + 'VariablesProduccion.csv')
data = pd.DataFrame(np.array(info).T,columns = variables)
data.to_csv(PATH+'/output/' + 'VariablesProduccion.csv')
create_images_per_module(director, 'Climate' ,PATH=PATH)
create_pdf_images('final_report', PATH, 'output')

date = create_date(index1)
frec = Dt/director.Modules['Climate'].Modules['ModuleClimate'].Dt ###Si o si debe estar en minutos
dates = compute_indexes(date,n,frec)
vars_to_plot  = ['T1','T2','T3','V1','C1','H','NF']
vars_to_plot += ['U6','U9','U10','U11','U12']
create_images(director,'Climate',dates,vars_to_plot, PATH = PATH,train=False)
#Data.to_csv(PATH+'/output/' + 'VariablesClimate.csv',index=0)
#Data1.to_csv(PATH+'/output/' + 'VariablesDir.csv',index=0)
#create_images_per_module(director, 'Climate' ,PATH=PATH)
#create_images_per_module(director, 'Plant1' ,PATH=PATH)


print(PATH)

try:
    if PARAMS_TRAIN['SEND_MAIL']: from correo import send_correo; send_correo(PATH + '/reports/final_report.pdf')
except:
    print('No tienes credenciales para enviar correos')
