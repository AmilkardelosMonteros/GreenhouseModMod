import matplotlib.pyplot as plt

def create_images(model, module, list_var=None,PATH=None):
    SHOW = False
    if PATH == None: SHOW = True
    if list_var == None: list_var = list(model.Modules[module].Vars.keys())
    for j,name in enumerate(list_var):
        if model.Vars[name].typ == 'State':
            try:
                x = model.Modules[module].Vars[name].GetRecord()
                t = range(len(x))
                print('Graficando',name)
                title = model.Modules[module].Vars[name].prn
                subtitle = model.Modules[module].Vars[name].desc
                units = model.Modules[module].Vars[name].units
                plt.plot(t, x, ms='4',alpha = 0.7)
                plt.ylabel(units)
                plt.xlabel('Time')
                plt.title(title)
                plt.suptitle(subtitle)
                if SHOW:
                    plt.show()
                    plt.close()
                else:
                    plt.savefig(PATH + '/images/'+name+'_'+str(j)+'_.png')
                    plt.close()
            except:
                print('La variable ', name,'tiene algo raro')
