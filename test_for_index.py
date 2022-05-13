import pandas as pd 
from parameters.parameters_dir import PARAMS_DIR
from parameters.parameters_env import day2hours
from read_dates import limit


def main():
    print('Leyendo datos ...')
    data            = pd.read_excel('weather_data/pandas_to_excel.xlsx')
    indices         = list(data.index)
    dias            = PARAMS_DIR['days']
    minutos         = day2hours(dias)
    indices_filtred = [i for i in indices if i < limit]
    flag = True
    for i in indices_filtred:
        new_i = i + minutos
        try:
            indices[new_i]
        except:
            print('El indice i no debe estar en la base')
            flag = False
    if flag:
        print('Todo esta bien')


if __name__ == '__main__':
    main()