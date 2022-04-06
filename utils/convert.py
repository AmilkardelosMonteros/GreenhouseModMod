def minute2seconds(x):
    return 60*x

def hour2seconds(x):
    return 60*minute2seconds(x)

def day2seconds(x):
    return 24*hour2seconds(x)

def week2seconds(x):
    return 7*day2seconds()

def hour2minute(x):
    return x*60

def day2minute(x):
    return x*24*60

def day2hour(x):
    return x*24

