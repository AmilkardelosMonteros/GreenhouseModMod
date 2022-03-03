def minute2seconds(s):
    return 60*s

def hour2seconds(s):
    return 60*minute2seconds(s)

def day2seconds(s):
    return 24*hour2seconds(s)

def week2seconds(s):
    return 7*day2seconds(s)