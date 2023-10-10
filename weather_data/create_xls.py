from vars import Vars,New_vars
import pandas as pd
import numpy as np
from numpy import exp
import Struct_weather
HEADER = False

active_vars = ['Temperature','Shortwave_Radiation','Wind_Speed10m']
time_var = ['Time_Stamp']


def presion_de_vapor_exterior(i5,rh):
    def q2(T1):
        if (T1 > 0):
            return 611.21*exp((18.678 - (T1/234.5)) * (T1/(257.14+T1)))
        else:
            return 611.21*exp((23.036 - (T1/333.7)) * (T1/(279.82+T1)))

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
    data         = add_colums(data,presion_de_vapor_exterior,'Temperature','Relative_Humidity',list(New_vars.keys())[0])
    data         = data[active_vars + time_var + [list(New_vars.keys())[0]]]
    #check        = data.isnull().values.any()
    if limit != None:
        data = data.iloc[0:limit]
    return data

def create_inputs_table():
    columns = ['Var', 'Description','Units','Sheet'	,'Column','Column_units','Column_conv_shift','Column_conv',	'Time_column',	'Time_column_units','Time_conv_shift','Time_conv']
    data    = pd.DataFrame(columns = columns)
    for i,var in enumerate(active_vars):
        list_tem    = [Vars[var].new_name,Vars[var].new_name + Vars[var].obs,Vars[var].units,'Meteo',var,Vars[var].units,0,Vars[var].column_conv,'Time_Stamp',pd.NA,2667452400,1]
        data.loc[i] = list_tem
    for j,var in enumerate(New_vars.keys()):
         list_tem    = [New_vars[var].new_name,New_vars[var].new_name + New_vars[var].obs,New_vars[var].units,'Meteo',var,New_vars[var].units,0,1,'Time_Stamp',pd.NA,2667452400,1]
         data.loc[i+1] = list_tem
    return data


def create_xls():
    with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
        create_dataset().to_excel(writer, sheet_name='Meteo')
        create_inputs_table().to_excel(writer, sheet_name='InputVars')

if __name__ == '__main__':
    create_xls()
