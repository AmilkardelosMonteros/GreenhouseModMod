import matplotlib.pyplot as plt
import pathlib
import pandas as pd
import numpy as np


def create_images_per_module(model, module, list_var=None,PATH=None):
    SHOW = False
    if PATH == None: SHOW = True
    if list_var == None: list_var = list(model.Modules[module].Vars.keys())
    if isinstance(PATH, str):
        pathlib.Path(PATH + '/images/'+module).mkdir(parents=True, exist_ok=True)
    # fig = plt.figure()
    for j,name in enumerate(list_var):
        if model.Modules[module].Vars[name].typ == 'State':
            try:
                x = model.Modules[module].Vars[name].GetRecord()
                t = range(len(x))
                print('Graficando',name)
                title = model.Modules[module].Vars[name].prn
                subtitle = model.Modules[module].Vars[name].desc
                units = model.Modules[module].Vars[name].units
                fig, ax = plt.subplots(dpi=150)
                ax.plot(t, x, ms='4',alpha = 0.7)
                ax.set_ylabel(units)
                ax.set_xlabel('Time')
                ax.set_title(title + '\n' + subtitle)
                # ax.set_suptitle(subtitle)
                fig.tight_layout(rect = [0,0.03,1,0.95])
                show = True if name == 'T1' else SHOW
                if show:
                    plt.show()
                    plt.close(fig)
                else:
                    plt.savefig(PATH + '/images/'+module+'/'+name+'_'+str(j)+'_.png')
                    plt.close(fig)
            except:
                print('La variable ', name,'tiene algo raro')
