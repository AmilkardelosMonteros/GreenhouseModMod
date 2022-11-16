import numpy as np

def check(funtion):
    def check_nan(*args):
        if np.nan in args:
            print('Error en los parametros')
            print(args)  
            return np.nan
        else:
            result = funtion(*args)
            if np.isnan(result):
                print('La funcion {} tiene algo mal'.format(function))
            else:
                return result
    return check_nan

def main():
    @check
    def suma(x,y):
        return x+y
    print(suma(np.nan,1))

if __name__ == '__main__':
    main()
