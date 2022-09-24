import pandas as pd
import datetime
data            = pd.read_csv('weather_data/dataset.csv',usecols=[1,2,3,4], header=0)
data.columns    = ['Year','Month','Day','Hour']

limit = data.shape[0] - 91*24 ## Vamos a quitar 90 dias


TEST = [108627, 126263, 126377, 100065, 100019,  91252, 126280, 126241,
       117664,  99847,  99864, 126456,  99868, 100165,  99867, 126381,
       100146, 126423, 108814,  91381, 100151,  99934, 108810,  91253,
       117418, 117591, 100124,  91323, 126362, 108817, 126325, 117520,
       108754,  91154,  91414, 117578,  99955, 126156, 126208, 117700,
       108871,  91337, 117561,  91255,  91195, 117413,  91309, 100057,
        99920,  91211,  91253,  99968, 100159, 108924, 117614,  99884,
        91352,  91334, 126248, 126150, 108638, 100096, 117699, 108921,
       108919,  91226,  99965, 117696, 108939, 117706,  91394, 108659,
       117672, 117412,  91348, 108852, 126232, 117711, 126346, 108671,
       100143, 117558, 117534,  99846, 108676, 100165, 117604,  99860,
       126364, 100172,  99899,  91405,  91094, 126334, 108930, 100009,
        91189, 126226, 100021, 126213] #This indexes was generated randomly with dates of the first 15 days on august 1998,1999,2000,2001,2002

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

    #Solo 15 dias de agosto de 2017
    SEASON3         = data.copy() 
    SEASON3         = SEASON3[(SEASON3.Month == 12) & (SEASON2.Day.isin(range(15))) & (SEASON3.Year.isin([2013,2014,2015,2016,2017] ))]
    SEASON3_indexes = list(SEASON3.index)
    SEASON3_indexes = list(filter(lambda x: x < limit, SEASON3_indexes))

    return {'1':SEASON1_indexes,'2':SEASON2_indexes, '3':SEASON3_indexes, 'TEST':TEST,'limit':limit}

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

