import numpy as np
import pandas as pd

def selectvariables(namelist,keylist,it, active_components):
    names = list()
    keys = list()
    for n in np.arange(len(namelist)):
        if active_components[it[n]]:
            names.append(namelist[n])
            keys.append(keylist[n])
    return names,keys

def selectunits(unitlist,it, active_components):
    units = list()
    for n in np.arange(len(unitlist)):
        if active_components[it[n]]:
            units.append(unitlist[n])
    return units

def maketable(names, keys, titles, settings,investtable = False):
    vals = list()
    for key in keys:
        vals.append(settings[key])
    if investtable:
        vals.append(sum(vals))
        names.append('Total')
    t = pd.DataFrame({'1':names, '2':vals})
    t.columns = titles

    return t
