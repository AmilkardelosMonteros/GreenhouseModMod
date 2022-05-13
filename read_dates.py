import pandas as pd
import datetime
data            = pd.read_csv('weather_data/dataset.csv',usecols=[1,2,3,4], header=0)
data.columns    = ['Year','Month','Day','Hour']


def get_indexes():
    limit = data.shape[0] - 91*24 ## Vamos a quitar 91 dias

    #Primera semana de enero a primera de abril
    SEASON1         = data.copy()
    SEASON1_1       = SEASON1[SEASON1.Month.isin([1,2,3])]
    SEASON1_2       = SEASON1[(SEASON1.Month == 4) & (SEASON1.Day.isin([1,2,3,4,5,6,7]))]
    SEASON1_indexes = list(SEASON1_1.index) + list(SEASON1_2.index)
    SEASON1_indexes = list(filter(lambda x: x < limit, SEASON1_indexes))

    #De abril a mediados de agosto
    SEASON2 = data.copy() 
    SEASON2_1       = SEASON2[SEASON2.Month.isin([4,5,6,7])]
    SEASON2_2       = SEASON2[(SEASON2.Month == 8) & (SEASON2.Day.isin(range(15)))]
    SEASON2_indexes = list(SEASON2_1.index) + list(SEASON2_2.index)
    SEASON2_indexes = list(filter(lambda x: x < limit, SEASON2_indexes))

    return {'1':SEASON1_indexes,'2':SEASON2_indexes, 'limit':limit}

def get_index(year,month,day,hour = 12):
    data_copy = data.copy()
    new_data = data_copy[ (data_copy.Year == year) & (data_copy.Month == month) & (data_copy.Day == day) & (data_copy.Hour == hour)]
    if new_data.shape[0] == 0: ##No existe esa fecha
        print('Esa fecha no existe')
        return 0
    else:
        return new_data.index[0]

def create_date(index_):
    info = data.iloc[index_]
    info = info.astype('int')
    date = datetime.datetime(info.Year,info.Month,info.Day,info.Hour)
    return date


def compute_indexes(inicio,n,frec):
    '''Indexes for a dataframe'''
    freq = str(frec)+'min'
    indexes = pd.date_range(inicio, periods=n, freq=freq)
    return indexes

