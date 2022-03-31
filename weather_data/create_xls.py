from vars import Vars
import pandas as pd
HEADER = False

active_vars = ['Temperature','Shortwave_Radiation',
       'Wind_Speed10m']
time_var = ['Time_Stamp']
def create_dataset():
    data         = pd.read_csv('dataset.csv')
    data.columns = list(Vars.keys()) if HEADER == False else data.columns
    data         = data[active_vars + time_var]
    return data

def create_inputs_table():
    columns = ['Var', 'Description','Units','Sheet'	,'Column','Column_units','Column_conv_shift','Column_conv',	'Time_column',	'Time_column_units','Time_conv_shift','Time_conv']
    data    = pd.DataFrame(columns = columns)
    for i,var in enumerate(active_vars):
        list_tem    = [Vars[var].new_name,Vars[var].new_name + Vars[var].obs,Vars[var].units,'Meteo',var,Vars[var].units,0,1,'Time_Stamp',pd.NA,2667452400,60*(1/3600)]
        data.loc[i] = list_tem
    return data


def create_xls():
    with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
        create_dataset().to_excel(writer, sheet_name='Meteo')
        create_inputs_table().to_excel(writer, sheet_name='InputVars')

if __name__ == '__main__':
    create_xls()