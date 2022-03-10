from auxModMod.new_read_module import  ReadModule
from util import Loader
from greenhouse.climate.director import Climate_model
from utils.graphics import create_images
from factory_of_rhs import*
from greenhouse.climate.module_climate import Module1
from parameters.climate_constants import CONSTANTS as constant_climate

loader = Loader("Creating weather module").start()
MeteoModule = ReadModule('weather_data/pandas_to_excel.xlsx', t_conv_shift=0.0, t_conv=1, shift_time=30)  # t_conv=1/(60*24) es para pasar el tiempo de minutos (como queda después de la lectura de la base) a días 
loader.stop()
dir_climate = Climate_model()

""" Climate module"""
C1_rhs_ins = C1_rhs(constant_climate)
V1_rhs_ins = V1_rhs(constant_climate)
T1_rhs_ins = T1_rhs(constant_climate)
T2_rhs_ins = T2_rhs(constant_climate)
RHS_list = [C1_rhs_ins, V1_rhs_ins, T1_rhs_ins, T2_rhs_ins]
dir_climate.MergeVarsFromRHSs(RHS_list, call=__name__)
dir_climate.AddModule('ModuleClimate', Module1(Dt=60, C1=C1_rhs_ins, V1=V1_rhs_ins, T1=T1_rhs_ins, T2=T2_rhs_ins))
dir_climate.AddModule('ModuleMeteo', MeteoModule)
dir_climate.sch = ['ModuleClimate','ModuleMeteo']



dir_climate.Run(Dt=60 * 60 * 24, n=7, sch=dir_climate.sch)
breakpoint()
create_images(dir_climate, list_var=None, PATH='borrame')


'''
vid = 'I2'
s = 0
traw = MeteoModule.data[MeteoModule.input_vars.loc[vid,'Sheet']].loc[MeteoModule.input_vars.loc[vid,'time_index']+s,MeteoModule.input_vars.loc[vid,'Time_column']]
output = MeteoModule.tconv*(MeteoModule.input_vars.loc[vid,'Time_conv']*(traw - MeteoModule.input_vars.loc[vid,'Time_conv_shift']) - MeteoModule.tconv_a)
'''
