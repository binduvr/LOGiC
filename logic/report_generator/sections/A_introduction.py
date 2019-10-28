from unidecode import unidecode as udec
import os
enter = '\r\n'


def introduction(reportdict):
	res = str(reportdict['residential_demand'])
	intro = 'This document shortly reports the results of the use of the LOGiC ' + \
	'sizing tool. This introduction describes the input values used to perform the calculations.' + \
	'The system is assumed to be located at or close to ' + udec(reportdict['address']) + '.'
	return intro

def generalinfo(reportdict):
    comps = reportdict['active_components']
    if not comps['grid_connection']:
        griddescription = 'off-grid microgrid. This means that the microgrid '+\
        'has to generate all electrical energy consumed in the grid locally '+\
        'and that no extra energy can be bought from external parties. '+\
        'Shortages are fulfilled by using a back-up diesel generator. '
    else:
        griddescription = 'grid-connected microgrid. This means that a '+\
        'local energy shortage can be fulfilled by purchasing energy from the '+\
        'main grid. Shortages can, however also be fulfilled by means of '+\
        'a back-up diesel generator. '

    if comps['wind']:
        if comps['solar']:
            sources = 'wind power, solar power and a back-up generator'
        else:
            sources = 'wind power and a back-up generator'
    elif comps['solar']:
        sources = 'solar power and a back-up generator'
    else:
        sources = 'a diesel generator'
    if comps['storage']:
        storage = ' combined with a storage facility.'
    else:
        storage = '.'
    geninfo = '\\section*{Microgrids}' +enter+\
    'In order to make this report comprehendable to the user the '+\
    'general properties of a microgrid are shortly discussed.\\\ '+\
    'A microgrid is a local energy system that is capable of generating, '+\
    'storing and delivering energy locally. Microgrids can be both '+\
    'connected to the main grid (grid-connected microgrids) as well as '+\
    'being completely isolated (off-grid microgrids). The microgrid '+\
    'considered in this assessment is a ' + griddescription +\
    'There multpile possible reasons to apply a microgrid: '+\
    '\\begin{itemize}'+enter+' '+\
    '\\item No grid is available (remote location) ' + enter +\
    '\\item There is a grid availble, but is is not reliable (enough)  ' + enter +\
    '\\item The wish to generate the own energy locally as a stakeholder or a community ' + enter +\
    '\\end{itemize}' + enter +\
    'In all cases renewable sources are often considered as a possible source '+\
    'of energy for the microgrid, either from an economic or a sustainable driver. ' +\
    'In the case of this microgrid the following sources are considered: '+\
    sources +storage+\
    ''
    return geninfo
