#!/usr/bin/env python

"""
Bindu van Raak
PVGIS_Standard.py
This example requests the typical meteorological year data
of solar irradiance or wind at a specific longitude and latitude
To be used with the European Commission's PVGIS data API
This database is limited to Europe, Asia and Africa
(and a small area of Australia)
https://re.jrc.ec.europa.eu/pvg_static/web_service.html#TMY
"""

# Base URL - http://re.jrc.ec.europa.eu/pvgis5/tmy.php
# Example Minimum URL format - http://re.jrc.ec.europa.eu/pvgis5/seriescalc.php?lat=45&lon=8

import requests as req
import sys
import pandas as pd
import requests as req
from io import StringIO
import numpy as np
import re

def get_wind_standard_year(lat, lon, days):
    """Get wind and solar irradiance standard time for coordinates
    for certain time period.

    Parameters
    ----------
        lat: latitude
        lon: longitude
        days: number of standard days requested
    """

    base_url = "http://re.jrc.ec.europa.eu/api/tmy?lat={}&lon={}&usehorizon={}&outputformat={}"
    url = base_url.format(lat, lon, 1, "csv")
    r = req.get(url)

    string_data = r.text

    # Get wind time series'
    hrs = int(days * 24)
    df = pd.read_csv(StringIO(string_data), sep=',', skiprows=16)

    wind_speed = df['WS10m'].head(hrs)

    return wind_speed


def get_solar_standard_year(lat, lon, runtime):

    startyear = 2007
    endyear = 2016
    peakpower = 1
    loss = 14
    optimalangles = 1
    pvtechchoice = 'crystSi'
    database = 'PVGIS-SARAH'
    pvcalculation = 1

    base_url = "http://re.jrc.ec.europa.eu/api/seriescalc?lat={}&lon={}&peakpower={}&loss={}\
        &startyear={}&endyear={}&optimalangles={}&pvtechchoice={}&pvcalculation={}"

    # TODO: Iterate over all databases and change the years accordingly
    url = base_url.format(lat, lon,
        peakpower, loss,
        startyear, endyear, optimalangles,
        pvtechchoice, pvcalculation)

    # Request the data
    r = req.get(url)

    df = pd.read_csv(StringIO(r.text), sep=',', skiprows=10)
    hrs = int(runtime * 24)

    # forge first line because the database starts at 4 minutes to 1 rater than at 00:00. This also implies a 4 minute shift between timeseries.
    # It is in the opinion of the developer that this is affordable.
    firstline = pd.DataFrame({'Date':'20061231:2356',
                            'P':[0],
                            'W10': [df['WS10m'][0]]})

    df.drop(['G(i)', 'H_sun', 'T2m', 'Int'], axis = 1, inplace = True)
    df = df.head(87671)
    appended = firstline.append(df)
    appended.index = pd.DatetimeIndex(start = '1/1/2007', freq = 'H', periods = 87672)
    newdf = appended[~((appended.index.month ==2)&(appended.index.day ==29))]

    pvyield = newdf['P']
    pvaverage = pd.DataFrame({'pvaverage': np.arange (8760)-np.arange (8760)})
    pvaverage.index = pd.DatetimeIndex(start = '1/1/2010', freq = 'H', periods = 8760)

    for n in np.arange(8759):
        sigma = float(0)
        for k in np.arange(9)+1:
            ind = k*8760+float(n)
            ind = int(ind)
            sigma = sigma+float(pvyield[ind])
        pav = sigma/10
        pvaverage['pvaverage'][n] = pav
    pvaveragecut = pvaverage.head(hrs)

    return pvaveragecut

# TODO: Move this to OSELC app
def get_optimal_panel_config(lat, lon):

    try:
        base_url = "http://re.jrc.ec.europa.eu/api/PVcalc?lat={}&lon={}\
            &loss=14&peakpower=1&outputformatchoice=basic&optimalinclination=1\
            &optimalangles=1&inclined_optimum=1&vertical_optimum=1"

        url = base_url.format(lat, lon)
        r = req.get(url)

        slope = [int(k) for k in re.findall(r'\b\d+\b', r.text.splitlines()[5])][0]
        azimuth = [int(k) for k in re.findall(r'\b\d+\b', r.text.splitlines()[6])][0]

        return slope, azimuth
    except:
        return 0, 0