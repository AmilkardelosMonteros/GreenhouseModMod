import matplotlib.pyplot as plt

def create_images(model, module, list_var=None,PATH=None):
    SHOW = False
    if PATH == None: SHOW = True
    if list_var == None: list_var = list(model.Vars.keys())
    for j,name in enumerate(list_var):
        if model.Vars[name].typ == 'State':
            try:
                fig = plt.figure()
                x = model.OutVar(name)
                t = range(len(x))
                print('Graficando',name)
                title = model.Vars[name].prn
                subtitle = model.Vars[name].desc
                units = model.Vars[name].units
                plt.plot(t, x, ms='4',alpha = 0.7)
                plt.ylabel(units)
                plt.xlabel('Time')
                plt.title(title)
                plt.suptitle(subtitle)
                fig.tight_layout(rect = [0,0.03,1,0.95])
                if SHOW:
                    plt.show()
                    plt.close()
                else:
                    plt.savefig(PATH + '/images/'+name+'_'+str(j)+'_.png')
                    plt.close()
            except:
                print('La variable ', name,'tiene algo raro')