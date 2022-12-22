import numpy as np

def check(funtion):
    def check_nan(**kwargs):
        result = funtion(*list(kwargs.values()))
        flag = False
        if isinstance(result, list) | isinstance(result, np.ndarray):
            flag = np.isnan(result).any() or np.isinf(result).any()
        else:
            flag = np.isnan(result) or np.isinf(result)
        
        if flag:
            print('La funcion {} tiene algo mal'.format(funtion))
            print('Parametros:')
            print(print(kwargs))
            exit()
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
