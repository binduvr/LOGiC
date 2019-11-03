enter = '\r\n'
import os
from logic.report_generator.functions.L_figuremaker import multicolfigure as figure

def contributors(reportdict):
	conts = '\\section*{Contributors}' + \
	enter + \
	'The Microgrid Assessment Tool has been developed by the LOGiC Team at the Off Grid Test Center. ' + enter +\
	'The tool is based on the Offgridders tool, initially developed by Martha Hoffmann at the Reinier Lemoin Instute in Berlin, Germany. ' + enter+\
	'Based on this work and with financial support by LOGiC the team was able to succesfully developt this implementation. ' +enter+\
	'Other contributers to the tool are: '+enter+\
	'\\begin{itemize}' +enter+\
	'\\item Alex and Stan Bankras at Stalex (web development)' +enter+\
	'\\item Ewout van der Beek at NEDU (data interpretation)' +enter+\
	'\\item Wind Energy Solutions BV (general support)' +enter+\
	'\\end{itemize}' +enter+\
	'\\vfill'+enter+\
    figure('logiclogo.png', None,'logiclogo')+enter+\
	'\\centering \\small{The OGTC MAT is powered by LOGiC}'
	return conts
