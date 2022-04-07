def minute2seconds(x):
    return 60*x

def hour2seconds(x):
    return 60*minute2seconds(x)

def day2seconds(x):
    return 24*hour2seconds(x)

def week2seconds(x):
    return 7*day2seconds()

def hour2minutes(x):
    return x*60

def day2minutes(x):
    return x*24*60

def day2hours(x):
    return x*24

def get_dt_and_n(minute, days):
    Dt = minute2seconds(minute)
    m = hour2minutes(1) // minute
    n = m * day2hours(days)
    return Dt, n 
