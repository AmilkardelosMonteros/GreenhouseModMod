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
    for j,name in enumerate(list_var):
        if model.Modules[module].Vars[name].typ == 'State':
            try:
                fig = plt.figure()
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
                fig.tight_layout(rect = [0,0.03,1,0.95])
                if SHOW:
                    plt.show()
                    plt.close()
                else:
                    plt.savefig(PATH + '/images/'+module+'/'+name+'_'+str(j)+'_.png')
                    plt.close()
                    plt.cla()
                    plt.clf()
            except:
                print('La variable ', name,'tiene algo raro')


def create_images(model, module, indexes,list_var=None,PATH=None,train =True):
    SHOW = False
    if PATH == None: SHOW = True
    if list_var == None: list_var = list(model.Vars.keys())
    fig = plt.figure()
    fig.tight_layout(rect = [0,0.03,1,0.95])
    for j,name in enumerate(list_var):
        if model.Vars[name].typ == 'State':
            try:
                x = model.OutVar(name)
                data_x = pd.DataFrame(x,columns=[name])
                data_x.index = indexes 
                title = model.Vars[name].prn
                ax = data_x.plot(figsize=(10, 7),title = title)
                print('Graficando',name)
                subtitle = model.Vars[name].desc
                units = model.Vars[name].units
                plt.ylabel(units)
                plt.xlabel('Time')
                plt.title(title)
                plt.suptitle(subtitle)
                plt.gcf().autofmt_xdate()
                if SHOW:
                    plt.show()
                    plt.cla()
                    plt.clf()
                    plt.close(fig)
                else:
                    if train:
                        complete_path = PATH + '/images/train/'+name+'_'+str(j)+'.png'
                    else:
                        complete_path = PATH + '/images/test/'+name+'_'+str(j)+'.png'
                    plt.savefig(complete_path)
                    #plt.savefig(PATH + '/output/'+name+'_'+str(j)+'_.png')
                    plt.cla()
                    plt.clf()
                    plt.close(fig)
            except:
                print('La variable ', name,'tiene algo raro')
