from ModMod import  ReadModule
from util import Loader
loader = Loader("Creating weather module").start()
MeteoModule = ReadModule('Weather_Data/pandas_to_excel.xlsx', t_conv_shift=0.0, t_conv=1)  # t_conv=1/(60*24) es para pasar el tiempo de minutos (como queda después de la lectura de la base) a días 
loader.stop()

'''
vid = 'I2'
s = 0
traw = MeteoModule.data[MeteoModule.input_vars.loc[vid,'Sheet']].loc[MeteoModule.input_vars.loc[vid,'time_index']+s,MeteoModule.input_vars.loc[vid,'Time_column']]
output = MeteoModule.tconv*(MeteoModule.input_vars.loc[vid,'Time_conv']*(traw - MeteoModule.input_vars.loc[vid,'Time_conv_shift']) - MeteoModule.tconv_a)
'''
