'''
This file contains the functions that determine the per unit wind power based on the wind speed profiles

'''
import numpy as np
import pandas as pd
import logic.settings as settings
## Rough estimate; straight power line from 0 to 24 m/s
def rough(wind_speed):
    windgen = wind_speed/24
    return windgen

## WES 100 power curve
def powercurve(windspeed):
    import numpy as np
    import pandas as pd

    #WES 100 power curve
    pcspeed = np.arange(25)
    pcpower = [0,0,0,1,2.9,6,11,17.7,27.3,39.2,53.8,68.4,82.8,89.1,95.9,98.7,99.5,100,100,100,100,100,100,100,100]
    pcpower[:] = [x/100 for x in pcpower]
    windgen = np.interp(windspeed, pcspeed,pcpower)
    windgen = pd.Series(windgen)
    return windgen

def chosen_turbine(wind_speed, demands):
    turbine_type = choose_turbine(wind_speed, demands)
    windgen = speed_to_power(wind_speed, turbine_type)
    return windgen, turbine_type

def speed_to_power(wind_speed, turbine_type):
    power_curve = pd.read_csv(settings.INPUT_DIRECTORY+'/wind_turbines/power_curves/'+turbine_type+'.csv', header = None)
    power_curve.index = ['wind_speed', 'power']
    pc_speed = list(power_curve.loc[['wind_speed']].values)[0]
    power = list(power_curve.loc[['power']].values)[0]
    pu_power = power/max(power)
    windgen = np.interp(wind_speed, pc_speed, pu_power)
    windgen = pd.Series(windgen)
    return windgen

def choose_turbine(wind_speed, demands):
    turbine_matrix = pd.read_csv(settings.INPUT_DIRECTORY+'/wind_turbines/turbine_matrix.csv')
    windbounds = turbine_matrix['0']
    powerbounds = list(turbine_matrix.columns[1:len(turbine_matrix.columns)])
    wind_class = find_wind_class(wind_speed, windbounds)
    power_class_index = find_power_class(demands, powerbounds)
    turbine_type = turbine_matrix[power_class_index][wind_class]
    return turbine_type

def find_power_class(demands,bounds):
    totaldemand = 0
    for key in demands.keys():
        totaldemand = totaldemand+demands[key]
    estimated_wind_energy = totaldemand*0.4 # NOTE: hard coded estimated fraction of wind power
    estimated_load_hours = 2100 # NOTE: hard coded guess relevant for NL    TODO: some smarter estimation
    estimated_wind_power = estimated_wind_energy/estimated_load_hours

    cla = 0
    while float(bounds[cla])<estimated_wind_power:
        cla = cla+1
        if cla == len(bounds)-1:
            break
    power_class_index = bounds[cla]
    return power_class_index

def find_wind_class (wind_speed, bounds):
    mean_wind_speed = np.mean(wind_speed)

    cla = 0
    while float(bounds[cla])<mean_wind_speed:
        cla = cla+1
        if cla == len(bounds)-1:
            break
    wind_class = int(cla)
    return cla
