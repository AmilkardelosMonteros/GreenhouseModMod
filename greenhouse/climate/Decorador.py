import numpy as np

def check(funtion):
    def check_nan(**kwargs):
        if np.nan in kwargs.values():
            print('Error en los parametros')
            print(kwargs)  
            return np.nan
        else:
            result = funtion(*list(kwargs.values()))
            if np.isnan(result):
                print('La funcion {} tiene algo mal'.format(function))
            else:
                return result
    return check_nan

def main():
    @check
    def suma(x,y):
        return x+y
    print(suma(x=np.nan,y = 1))

if __name__ == '__main__':
    main()