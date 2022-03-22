import matplotlib.pyplot as plt

def create_images(model, module, list_var=None,PATH=None):
    SHOW = False
    if PATH == None: SHOW = True
    if list_var == None: list_var = list(model.Vars.keys())
    for name in list_var:
        if model.Vars[name].typ == 'State':
            try:
                x = model.OutVar(name)
                t = range(len(x))
                print('Graficando',name)
                title = model.Vars[name].prn
                units = model.Vars[name].units
                plt.plot(t, x, ms='4',markevery=60, marker='.')
                plt.ylabel(units)
                plt.xlabel('Time')
                plt.title(title)
                if SHOW:
                    plt.show()
                    plt.close()
                else:
                    plt.savefig(PATH + '/images/'+name+'.png')
                    plt.close()
            except:
                print('La variable ', name,'tiene algo raro')
