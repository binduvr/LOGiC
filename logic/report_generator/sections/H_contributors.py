enter = '\r\n'
import os
from logic.report_generator.functions.L_figuremaker import multicolfigure as figure
from logic.report_generator.functions.L_figuremaker import rightsmallfigure as rightfigure
def contributors(reportdict):
	conts = '\\subsection*{Development}' + \
	enter + \
	'The Microgrid Assessment Tool has been developed by the LOGiC Team at the Off Grid Test Center. ' + enter +\
	'The tool is based on the Offgridders tool, initially developed by Martha Hoffmann at the Reinier Lemoin Instute in Berlin, Germany. ' + enter+\
	'Based on this work and with financial support by LOGiC the team was able to succesfully develop this implementation. ' +enter+\
	'Sources and tools utilised by the tool include: '+enter+\
	'\\begin{itemize}' +enter+\
	'\\item PVGIS weather database' +enter+\
	'\\item ENTSO-E (load profiles)' +enter+\
	'\\item NASA Surface Meteorology and Solar Energy' +enter+\
	'\\item World Bank (socio-ecenomic parameters)' +enter+\
	'\\end{itemize}' +enter+\
	'\\vfill'+enter+\
    rightfigure('logiclogo.png', None,'logiclogo')
	return conts
