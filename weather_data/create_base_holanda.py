import pandas as pd
from numpy import exp
import numpy as np

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


def create_dataset():
    data         = pd.read_csv('meteoHolanda.csv')
    data         = data[['time','Iglob (W/m2)','Windsp(m/s)','Tout(C)','Rhout(%)']]
    #chunks       = range(0,len(data),12)
    #new_data     = dict() 
    #for name in ['Iglob (W/m2)','Windsp(m/s)','Tout(C)','Rhout(%)']:
    #    new_data[name] = list()
    #    for i in range(len(chunks)-1):
    #        inicio, fin = chunks[i],chunks[i+1]
    #        data_aux = data[name].iloc[inicio:fin]
    #        value = data_aux.mean()
    #        new_data[name].append(value)

    #Data = pd.DataFrame.from_dict(new_data)
    Data = data.fillna(0)
    Data = add_colums(Data,presion_de_vapor_exterior,'Tout(C)','Rhout(%)','Outside_Vapor_Pressure')
    Data = Data.rename(columns={'Iglob (W/m2)':'I2','Windsp(m/s)':'I8',"Tout(C)": "I5", "Rhout(%)": "Rhout(%)",'Outside_Vapor_Pressure':'I11'})
    Data = Data[['I5','I2','I8','I11']]
    t1 = data['time'][0]
    t2 = data['time'][len(data)-1]
    dates = range(300,(len(Data)+1)*300,300) #300 = 5minutos x 60 (segundos en un minuto)
    Data['Time_Stamp'] = dates
    return Data


def create_inputs_table():
    f0 = ['I5', 'I52mabove gnd','C','Meteo','I5','C',0,1,'Time_Stamp',None ,300,1]
    f1 = ['I2', 'I2sfc','Wm2','Meteo','I2','Wm2',0,1,'Time_Stamp',None ,300,1]
    f2 = ['I8', 'I8 10mabove gnd','C','Meteo','I8','KmH',0,1,'Time_Stamp',None ,300,1]
    f3 = ['I11', 'I11','Pa','Meteo','I11','Pa',0,1,'Time_Stamp',None ,300,1]
    columas = ['Var','Description','Units'	,'Sheet'	,'Column',	'Column_units',	'Column_conv_shift',	'Column_conv',	'Time_column',	'Time_column_units',	'Time_conv_shift',	'Time_conv']
    df = pd.DataFrame(columns=columas)
    df.loc[0] = f0
    df.loc[1] = f1
    df.loc[2] = f2
    df.loc[3] = f3
    return df 

def create_xls():
    with pd.ExcelWriter('excel_holanda.xlsx') as writer:
        create_dataset().to_excel(writer, sheet_name='Meteo')
        create_inputs_table().to_excel(writer, sheet_name='InputVars')
    print('Done')

if __name__ == '__main__':
    create_xls()
