from vars import Vars
import pandas as pd
from math import exp
import numpy as np
from Struct_weather import Struct_weather
HEADER = False
####################Dt de Meteo####################
#    t0      = 2667452400
#    t1      = 2667456000             
#    t1 - t0 = 3600 
#    3600  is equivalent to 60 minutes -> 1 = second
#

active_vars = ['Temperature','Shortwave_Radiation','Wind_Speed10m']
new_vars = ['Outside_Vapor_Pressure']
time_var = ['Time_Stamp']

def presion_de_vapor_exterior(i5,rh):
    def q2(T1):
        if (T1 > 0):
            return 611.21*exp((18.678 - (T1/234.5)) * (T1/(257.14+T1)))
        else:
            return 611.15*exp((23.036 - (T1/333.7)) * (T1/(279.82+T1)))

    return q2(i5)*(rh/100.0) 

def add_colums(data,f,x,y,name):
    """
    z = f(x,y)
    x is a name of one column of data, also y
    """
    data_copy = data.copy()
    vf = np.vectorize(f)
    data_copy[name] = vf(data[x],data[y])
    return data_copy



def create_dataset(limit = None):
    data         = pd.read_csv('dataset.csv')
    data.columns = list(Vars.keys()) if HEADER == False else data.columns
    data         = add_colums(data,presion_de_vapor_exterior,'Temperature','Relative_Humidity','Outside_Vapor_Pressure')
    data         = data[active_vars + new_vars + time_var]
    #check        = data.isnull().values.any()
    if limit != None:
        data = data.iloc[0:limit]
    return data

def create_inputs_table():
    columns = ['Var', 'Description','Units','Sheet'	,'Column','Column_units','Column_conv_shift','Column_conv',	'Time_column',	'Time_column_units','Time_conv_shift','Time_conv']
    data    = pd.DataFrame(columns = columns)
    New_vars = {'Outside_Vapor_Pressure': Struct_weather(orig_name='Outside_Vapor_Pressure',units='Pa',new_name = 'I11',obs = 'q2(i5)*(rh/100.0)')} 
    for i,var in enumerate(active_vars):
        list_tem    = [Vars[var].new_name,Vars[var].new_name + Vars[var].obs,Vars[var].units,'Meteo',var,Vars[var].units,Vars[var].conv_shift,Vars[var].conv,'Time_Stamp',pd.NA,2667452400,1]
        data.loc[i] = list_tem
    for j,var in enumerate(new_vars):
        list_tem    = [New_vars[var].new_name,New_vars[var].new_name + New_vars[var].obs,New_vars[var].units,'Meteo',var,New_vars[var].units,New_vars[var].conv_shift,New_vars[var].conv,'Time_Stamp',pd.NA,2667452400,1]
        data.loc[i+j+1] = list_tem
    return data


def create_xls():
    with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
        create_dataset(3000).to_excel(writer, sheet_name='Meteo')
        create_inputs_table().to_excel(writer, sheet_name='InputVars')

if __name__ == '__main__':
    create_xls()