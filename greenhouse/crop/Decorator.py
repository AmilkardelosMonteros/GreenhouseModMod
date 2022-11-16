import numpy as np

def check(funtion):
    def check_nan(**kwargs):
        result = funtion(*list(kwargs.values()))
        if np.isnan(result):
            print('La funcion {} tiene algo mal'.format(funtion))
            print('Parametros:')
            print(print(kwargs))
            return result
        else:
            return result
    return check_nan

def main():
    @check
    def suma(x,y):
        return x+y
    suma(x=np.nan,y = 1)

if __name__ == '__main__':
    main()
