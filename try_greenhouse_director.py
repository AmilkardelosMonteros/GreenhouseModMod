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
from utils.convert import day2seconds, hour2seconds, minute2seconds, day2minute,day2hour
from utils.graphics import create_images
from utils.create_folders import create_path
from utils.images_to_pdf import create_pdf_images

beta_list = [0.99, 0.95] # Only 2 plants are simulated, assuming this is approximately one m**2
theta_c = np.array([3000, 20, 2.3e5]) # theta nominal clima
theta_p = np.array([0.7, 3.3, 0.25]) # theta nominal pdn


""" Climate director"""

dir_climate = Climate_model()

""" Climate module"""
C1_rhs_ins = C1_rhs(constant_climate)
V1_rhs_ins = V1_rhs(constant_climate)
T1_rhs_ins = T1_rhs(constant_climate)
T2_rhs_ins = T2_rhs(constant_climate)
RHS_list = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
dir_climate.AddModule('ModuleClimate', Module1(Dt=minute2seconds(1), C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins))
dir_climate.sch = ['ModuleClimate']

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
dir_climate.MergeVarsFromRHSs(cost_list, call=__name__)
dir_climate.AddModule('ModuleCosts', ModuleCosts(Dt=minute2seconds(1), Qgas=Qgas_rhs_ins, Qh2o=Qh2o_rhs_ins, Qco2=Qco2_rhs_ins))

dir_climate.sch += ['ModuleCosts']

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



#################################################################
############ RHS modelo de crecimiento ##########################
#################################################################    
class Q_rhs(StateRHS):
    """
    Q is the weight of all fruits for plant
    """
    def __init__( self, theta_p):
        """Define a RHS, ***this an assigment RHS***, V1 = h2(...), NO ODE."""
        ### uses the super class __init__
        super().__init__()
        
        ### Define variables here.  Each fruit will have repeated variables.
        ### Later some will be shared and the Local variable swill be exclusive
        ### of each fruit.
        
        self.SetSymbTimeUnits(d) # days

        ### State variables coming from the climate model
        self.AddVar( typ='State', varid='T2', prn=r'$T_2$',\
                    desc="Greenhouse air temperature", units= C , val=20) 
        
        #self.AddVar( typ='State', varid='PAR', prn=r'$PAR$',\
         #   desc="PAR radiation", units=mu_mol_phot * (m**-2) * d**-1 , val=300.00)
        self.AddVar( typ='State', varid='I2', prn=r'$I_2$',\
                    desc="External global radiation", units= W * m**-2 , val=100) # It's takes as the PAR 
        
        
        ### Local variables, separate for each plant
        self.AddVarLocal( typ='State', varid='A', prn=r'$A$',\
           desc="Assimilation rate", units= g * (m**-2), val=0)
        
        self.AddVarLocal( typ='StatePartial', varid='Q', prn=r'$Q$',\
           desc="Weight of all fruits for plant", units= g, val=0.0)
        
        self.AddVarLocal( typ='StatePartial', varid='m_k', prn=r'$m_k$',\
           desc="Simulation number of fruits harvested for plant", units= n_f, val=0.0)
        
        self.AddVarLocal( typ='StatePartial', varid='n_k', prn=r'$n_k$',\
           desc="Number of fruits harvested for plant", units= n_f, val=0)

        self.AddVarLocal( typ='StatePartial', varid='h_k', prn=r'$h_k$',\
           desc="Weight of all harvested fruits for plant", units= g, val=0.0)

        self.AddVarLocal( typ='StatePartial', varid='Q_h', prn=r'$H$',\
           desc="Accumulated weight of all harvested fruits for plant", units= g, val=0.0)

        self.AddVarLocal( typ='StatePartial', varid='Y_sum', prn=r'$Y_{sum}$',\
           desc="Sum of all potentail growths", units= g/d**2, val=0.0)


        ### Canstants, shared by all plants.  Shared Cnts cannot be local
        self.AddVar( typ='Cnts', varid='k1_TF', prn=r'$k1_TF$',\
           desc="Aux in function TF", units= MJ * m**-2 * d**-1, val=300.0)

        self.AddVar( typ='Cnts', varid='k2_TF', prn=r'$k2_TF$',\
           desc="Aux in function TF", units= C * d**-1, val=1.0)

        self.AddVarLocal( typ='Cnts', varid='k3_TF', prn=r'$k3_TF$',\
           desc="Aux in function TF", units= n_f * C**-1, val=1.0)

        self.AddVarLocal( typ='Cnts', varid='dw_ef', prn=r'$dw_{efficacy}$',\
           desc="Constant in t_wg for fruits", units= 1, val=1.3)
        
        self.AddVarLocal( typ='Cnts', varid='dw_ef_veg', prn=r'$dw_{efficacy}$',\
           desc="Constant in t_wg for vegetative part", units= 1, val=1.15)

        self.AddVarLocal( typ='Cnts', varid='a_ef', prn=r'$a_{efficacy}$',\
           desc="Matching constant in remaining assimilates", units= 1/m**2, val=1.0)

        self.AddVarLocal( typ='Cnts', varid='C_t', prn=r'$C_t$',\
           desc="Constant in Y_pot", units= C * d, val=131.0)

        self.AddVarLocal( typ='Cnts', varid='B', prn=r'$B$',\
           desc="Constant in Y_pot", units= (C * d)**-1, val=0.017)

        self.AddVarLocal( typ='Cnts', varid='D', prn=r'$D$',\
           desc="Constant in Y_pot", units= 1, val=0.011)

        self.AddVarLocal( typ='Cnts', varid='M', prn=r'$M$',\
           desc="Constant in Y_pot", units= g, val=60.7)
        
        self.AddVarLocal( typ='Cnts', varid='a', prn=r'$a$',\
           desc="Constant in Y_pot_veg", units= 1, val=theta_p[1])
        
        self.AddVarLocal( typ='Cnts', varid='b', prn=r'$b$',\
           desc="Constant in Y_pot_veg", units= 1, val=theta_p[2])


    def RHS( self, Dt):
        """RHS( Dt ) = 
           
           ************* IN ASSIGMENT RHSs WE DON'T NEED TO CALL STATE VARS WITH self.Vk ******************
        """
        ### The assigment is the total weight of the fuits
        return self.V('Q')

def PlantDirector( beta, return_Q_rhs_ins=False):
    """Build a Director to hold a Plant, with beta PAR parameter."""
    ### Start model with empty variables
    Dir = Director( t0=0.0, time_unit="", Vars={}, Modules={} )
    ## Create instances of RHS
<<<<<<< HEAD
    Ci_rhs_ins = Ci_rhs(constant_crop)
    #Q_rhs_ins = Q_rhs(constant_crop)
    Q_rhs_ins = Q_rhs(theta_p)
=======
    Ci_rhs_ins = Ci_rhs()#constant_crop)
    Q_rhs_ins = Q_rhs()#constant_crop)
>>>>>>> ed88cf7445121c886e83556dba3b33d3c3a06587
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
    breakpoint()
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
director.Run(Dt=day2seconds(1),n=90, sch=director.sch) #,active=True)
#director.Run(Dt = 1,n=10, sch=['Climate'],active=True)
#loader.stop()

STATE_VARS = ['T1','T2','C1','V1']
CONTROLS  = ['U'+str(i) for i in range(1,12)] 
VARS = STATE_VARS + CONTROLS
PATH = create_path('simulation_results')
create_images(director, PATH = PATH)
create_pdf_images(PATH)