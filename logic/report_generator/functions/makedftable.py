import numpy as np
import pandas as pd

def selectvariables(namelist,keylist,it, active_components):
    names = list()
    keys = list()
    for n in np.arange(len(namelist)):
        if active_components[it[n]]:
            names = names.append(namelist[n])
            keys = keys.append(keylist[n])
    return names,keys

def selectunits(unitlist,it, active_components):
    for n in np.arange(len(namelist)):
        if active_components[it[n]]:
            units = units.append(unitlist[n])
    return units
    
def maketable(names, keys, titles, settings):
    vals = list()
    for key in keys:
        vals = vals.append(settings[key])
    t = pd.DataFrame({'1':names, '2':vals})
    t.columns = titles
    
    return t