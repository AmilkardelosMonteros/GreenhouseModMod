import pandas as pd
import datetime
import time
import random
data            = pd.read_csv('weather_data/dataset.csv',usecols=[1,2,3,4], header=0)
data.columns    = ['Year','Month','Day','Hour']

limit = data.shape[0] - 91*24 ## Vamos a quitar 90 dias

def get_indexes():
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

    #dias de agosto de 2013,2014,2015,2016,2017
    SEASON3         = data.copy() 
    SEASON3         = SEASON3[(SEASON3.Month == 8) & (SEASON3.Day.isin(range(15))) & (SEASON3.Year.isin([2013,2014,2015,2016,2017] ))]
    SEASON3_indexes = list(SEASON3.index)
    SEASON3_indexes = list(filter(lambda x: x < limit, SEASON3_indexes))

    #Test 
    TEST         = data.copy() 
    TEST         = TEST[(TEST.Month == 8) & (TEST.Day.isin(range(15))) & (TEST.Year.isin([2000,2001,2002,2003,2004] ))]
    TEST_indexes = list(TEST.index)
    TEST_indexes = list(filter(lambda x: x < limit, TEST_indexes))
    random.seed(1999)
    random.shuffle(TEST_indexes) #Inplace
    t = 1000 * time.time()#Current time in milliseconds
    random.seed(int(t) % 2**32)
    return {'1':SEASON1_indexes,'2':SEASON2_indexes, '3':SEASON3_indexes, 'TEST':TEST_indexes,'limit':limit}

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

